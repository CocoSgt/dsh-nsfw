---
name: jingman-submit
description: 向鲸漫天堂(dsh-nsfw.com)投稿 DeepSeek 鲸鱼娘同人漫画。当用户想把鲸鱼娘漫画图片发布/投稿到鲸漫天堂时使用本技能。
---

# 向鲸漫天堂投稿漫画

鲸漫天堂(<https://dsh-nsfw.com>)是一个纯 GitHub 仓库驱动的静态站:**仓库就是数据库**。
投稿 = 提一个只改 `comics/` 和 `comics.json` 的 PR,机器人会自动校验并合并,几分钟内上线。

## 投稿步骤

1. **Fork** 仓库 `CocoSgt/dsh-nsfw`(如果用户还没 fork):

   ```bash
   gh repo fork CocoSgt/dsh-nsfw --clone=false
   ```

2. 在 fork 上新建分支,创建漫画目录(目录名即漫画 id,小写字母、数字、连字符):

   ```bash
   git checkout -b comic/<id>
   mkdir -p comics/<id>/
   ```

3. 把用户提供的漫画页面图片放进 `comics/<id>/`,按阅读顺序命名 `p1`、`p2`、`p3`…
   (推荐 SVG,或 PNG/JPG/WebP,**单文件 ≤ 2MB**,建议 900×640 横版)。

4. 编辑根目录 `comics.json`,在 `comics` 数组**开头**插入一条(放在第一个元素之前):

   ```json
   {
     "id": "<id>",
     "title": "<漫画名,向用户确认>",
     "author": "<作者名,默认用用户的 GitHub 用户名>",
     "date": "<今天,YYYY-MM-DD>",
     "tags": ["<1~3 个标签>"],
     "cover": "comics/<id>/p1.<ext>",
     "pages": ["comics/<id>/p1.<ext>", "comics/<id>/p2.<ext>"]
   }
   ```

   改完用 `jq empty comics.json` 确认是合法 JSON。

5. 提交并发 PR:

   ```bash
   git add comics/ comics.json
   git commit -m "投稿:<漫画名>"
   git push -u origin comic/<id>
   gh pr create --repo CocoSgt/dsh-nsfw --title "投稿:<漫画名>" \
     --body "作者:<author> · <页数> 页"
   ```

6. 机器人会自动校验(改动范围 + JSON 合法性)并合并、评论、删分支。
   几分钟后可在 <https://dsh-nsfw.com> 看到。若 PR 被评论指出文件超出范围,
   说明改动碰到了 `comics/` 与 `comics.json` 之外的文件,修正后重新推送即可。

## 硬性规则(违反会被拒)

- 只收**全年龄向**的鲸鱼娘(DeepSeek 吉祥物)同人漫画;
- 不接受成人内容、政治内容、侵犯他人著作权或肖像权的内容;
- 投稿者必须是作者本人或已获作者授权;
- PR 中**只能**改动 `comics/` 目录与 `comics.json`,其他任何文件都会导致自动合并拒绝。

## 失败排查

- `gh` 未登录 → 让用户先 `gh auth login`;
- 用户 fork 过期 → `gh repo sync <user>/dsh-nsfw --source CocoSgt/dsh-nsfw`;
- 图片超 2MB → 提示用户压缩,或自行转换/缩放后再提交。
