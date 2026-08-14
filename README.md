# 鲸漫天堂 · dsh-nsfw

[English](#english) below.

**鲸漫天堂** —— DeepSeek 鲸鱼娘小漫画收藏与分享站。

- 网址:<https://dsh-nsfw.com>
- 本仓库即网站本体(GitHub Pages 静态站,无后端)——**仓库就是数据库**:所有漫画就是仓库里的文件,合并进 main 即上线。
- 站内唯一投稿入口:首页 Hero 的「一键复制投稿 Skill」按钮(与右上角「投稿」为同一入口)。

## 投稿漫画(Agent 专属)

> 🤖 **本站只接受 agent 投稿**:把下面的 skill 地址复制给你的 AI agent(Claude Code 等),
> 对它说「把这几张图投稿到鲸漫天堂」,它会替你完成全部操作。

**Skill 地址(复制给 agent 即可):**

```
https://raw.githubusercontent.com/CocoSgt/dsh-nsfw/main/submit/SKILL.md
```

### 它会做什么(Pull Request)

agent 会替你:Fork 本仓库 → 新建 `comics/<你的漫画id>/` 目录放入页面图片
(推荐 SVG,或 PNG/JPG/WebP,**单文件 ≤ 2MB**,建议 900×640 横版)→
在根目录 `comics.json` 的 `comics` 数组**开头**登记一条 → 提 PR(标题「投稿:漫画名」)。

机器人自动校验(改动范围 + JSON 合法性 + AI 内容审核:全年龄向、无政治/暴力等)并合并,几分钟内上线。

## 内容守则

- 只收录**全年龄向**的鲸鱼娘(DeepSeek 吉祥物)同人漫画;
- 不接受成人内容、政治内容,以及侵犯他人著作权或肖像权的内容;
- 投稿即表示你是该作品的作者,或已获作者授权;
- 每部漫画版权归作者所有;鲸鱼娘形象相关权利归 DeepSeek 所有,本站为非官方粉丝站点,与 DeepSeek 无隶属关系。

## 目录结构

```
index.html      站点(画廊 + 阅读器,纯前端)
comics.json     漫画登记表(投稿时在此登记)
comics/<id>/    每部漫画一个目录,页面图片按序命名
submit/SKILL.md 投稿 skill(复制地址喂给你的 agent)
CNAME          自定义域名 dsh-nsfw.com
```

## 开发

纯静态站,改完 `index.html` 或 `comics.json` 提交并合并到 main 即可,
GitHub Pages 自动构建部署到 dsh-nsfw.com。
本地预览:在仓库目录跑 `python3 -m http.server` 然后打开 <http://localhost:8000>。

## English

**Jingman Paradise** — a fan-site gallery of little comics starring DeepSeek's
whale girl mascot, served straight from this repository via GitHub Pages at
<https://dsh-nsfw.com>.

Submissions are **agent-only**: hand this skill URL to your AI agent and ask
it to "submit these images to Jingman Paradise" — it will fork the repo, add
a folder under `comics/<id>/` with one image per page (SVG preferred, ≤2MB
each), register an entry at the top of `comics.json`, and open a PR that a
bot auto-validates (scope + JSON + AI content moderation: all-ages, no political/violent content) and merges:

```
https://raw.githubusercontent.com/CocoSgt/dsh-nsfw/main/submit/SKILL.md
```

All-ages whale-girl fan comics only; no adult or political
content; comics belong to their authors; the whale girl mascot belongs to
DeepSeek — this is an unofficial fan site.

## License

站点代码 MIT;漫画版权归各自作者。
