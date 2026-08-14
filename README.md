# 鲸漫天堂 · dsh-nsfw

[English](#english) below.

**鲸漫天堂** —— DeepSeek 鲸鱼娘小漫画收藏与分享站。

- 网址:<https://dsh-nsfw.com>
- 本仓库即网站本体(GitHub Pages 静态站,无后端)——**仓库就是数据库**:所有漫画就是仓库里的文件,合并进 main 即上线。

## 投稿漫画(两种方式,任选)

### 方式一:Pull Request

1. Fork 本仓库;
2. 新建目录 `comics/<你的漫画id>/`(id 用小写字母、数字和连字符,如 `my-whale-story`);
3. 把漫画页面放进去,每页一张图(推荐 SVG,或 PNG/JPG/WebP,**单文件 ≤ 2MB**,建议 900×640 横版);
4. 在根目录 `comics.json` 的 `comics` 数组**开头**加一条:

   ```json
   {
     "id": "my-whale-story",
     "title": "我的漫画名",
     "author": "你的名字或 ID",
     "date": "2026-08-14",
     "tags": ["日常"],
     "cover": "comics/my-whale-story/p1.svg",
     "pages": ["comics/my-whale-story/p1.svg", "comics/my-whale-story/p2.svg"]
   }
   ```

5. 提 PR,标题写「投稿:漫画名」。合并后立即上线。

### 方式二:Issue 附件

不想动 Git 就开一个 [新 Issue](https://github.com/CocoSgt/dsh-nsfw/issues/new?labels=upload),
标题写漫画名,把图片按顺序拖进正文(可注明作者名与标签),维护者会替你整理上架。

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

To submit: open a PR adding a folder under `comics/<id>/` with one image per
page (SVG preferred, ≤2MB each) plus an entry at the top of `comics.json` —
or just open an issue with your images attached and a maintainer will shelve
it for you. All-ages whale-girl fan comics only; no adult or political
content; comics belong to their authors; the whale girl mascot belongs to
DeepSeek — this is an unofficial fan site.

## License

站点代码 MIT;漫画版权归各自作者。
