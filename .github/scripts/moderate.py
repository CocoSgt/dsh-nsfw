#!/usr/bin/env python3
"""投稿内容审核:用 OpenAI 视觉模型判断 PR 中的漫画是否符合全年龄向规范。
纯标准库实现,零 pip 依赖。

输入(环境变量):
  REVIEW_DIR      待审图片目录(svg 已在 workflow 中转为 png)
  COMICS_JSON     head 分支 comics.json 的本地路径(可选)
  OPENAI_API_KEY  OpenAI API 密钥(仓库 secret 注入)
  OPENAI_MODEL    可选,默认 gpt-4.1-mini
输出:
  /tmp/verdict.json  {"allowed": bool, "reasons": [str]}
退出码: 0 = 审核完成(结论看 verdict);非 0 = 审核流程本身失败。
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://api.openai.com/v1/chat/completions"
MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.6-luna")

POLICY = """你是「鲸漫天堂」(dsh-nsfw.com)的内容审核员。这是一个全年龄向的 \
DeepSeek 鲸鱼娘同人漫画站,所有投稿经你审核后自动上线,请严格把关。

以下任一命中即 allowed=false:
1. 色情、性暗示、软色情、擦边(全年龄向,按最严格标准判)
2. 现实政治:政治人物、政党、口号、旗帜、敏感历史或时事影射
3. 血腥、暴力、惊悚、自残
4. 仇恨言论、歧视、对特定群体的侮辱
5. 违法内容(毒品、赌博、武器制作教程等)
6. 广告、二维码、外部引流、诈骗信息
7. 真实个人的隐私信息(真人人脸照片、电话、住址等)
8. 与鲸鱼/鲸鱼娘主题完全无关的离题内容
9. 登记信息文本(标题、标签、作者名)含以上任何问题

边界说明:可爱、日常、职场吐槽、程序员梗都欢迎;梗图式夸张(如「插件都会炸」\
指程序报错)属正常创作,不算暴力。判断不确定时倾向拒绝(fail-closed),由人工复核。

下面依次给出:本次投稿的登记表 comics.json 全文,以及 PR 中新增/修改的每张图片\
(文件名在图片前标注)。reasons 用中文,逐条写明命中的标准和涉及的文件;全部通过\
时 reasons 为空数组。"""

MEDIA = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}

SCHEMA = {
    "type": "object",
    "properties": {
        "allowed": {"type": "boolean"},
        "reasons": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["allowed", "reasons"],
    "additionalProperties": False,
}

VERDICT_PATH = "/tmp/verdict.json"


def write_verdict(verdict: dict) -> None:
    with open(VERDICT_PATH, "w") as f:
        json.dump(verdict, f, ensure_ascii=False)
    print(json.dumps(verdict, ensure_ascii=False))


def main() -> None:
    review_dir = Path(os.environ["REVIEW_DIR"])
    comics_json = ""
    cj_path = os.environ.get("COMICS_JSON", "")
    if cj_path and Path(cj_path).exists():
        comics_json = Path(cj_path).read_text()

    images = sorted(p for p in review_dir.rglob("*") if p.suffix.lower() in MEDIA)
    if not images and not comics_json:
        write_verdict({"allowed": True, "reasons": []})
        return

    content = [
        {
            "type": "text",
            "text": f"{POLICY}\n\n<comics_json>\n{comics_json}\n</comics_json>",
        }
    ]
    for p in images:
        if p.stat().st_size > 4_500_000:
            write_verdict(
                {"allowed": False, "reasons": [f"{p.name} 超出审核大小上限,转人工复核"]}
            )
            return
        b64 = base64.standard_b64encode(p.read_bytes()).decode()
        content.append(
            {"type": "text", "text": f"图片文件: {p.relative_to(review_dir)}"}
        )
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:{MEDIA[p.suffix.lower()]};base64,{b64}"},
            }
        )

    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": content}],
        "max_completion_tokens": 8000,  # GPT-5 系列的推理 token 也计入此额度
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "verdict", "schema": SCHEMA, "strict": True},
        },
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:2000]
        print(f"OpenAI API HTTP {e.code}: {detail}", file=sys.stderr)
        if e.code == 401:
            print("提示: OPENAI_API_KEY 无效或已作废,请重设仓库 secret", file=sys.stderr)
        raise

    choice = data["choices"][0]
    if choice.get("finish_reason") == "content_filter":
        # 平台内容过滤器直接拦下 —— 内容本身高度可疑,fail-closed
        write_verdict(
            {"allowed": False, "reasons": ["平台内容过滤器拦截该投稿,转人工复核"]}
        )
        return

    write_verdict(json.loads(choice["message"]["content"]))


if __name__ == "__main__":
    main()
