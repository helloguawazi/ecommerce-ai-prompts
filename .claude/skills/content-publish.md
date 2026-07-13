# Content Publish - 关键词驱动内容发布

流程：取词 -> 写文 -> 生图 -> 写入 -> 记录日志 -> git add 停住
所有操作通过脚本执行，防止安全拦截。

## 执行步骤

### Step 1: 取关键词
方式A（自动）：运行 `python -X utf8 .claude/scripts/pick_keyword.py`
方式B（手动）：用户直接说了关键词就用用户说的。

### Step 2: 判断站点归属
（同上）

### Step 3: 写文章
Claude 写约 600 字 SEO 文章，标题关键词前置 15-30 字有场景。
外链规则：aishop->poster / poster->aishop / image2->aishop+poster
页尾保留 weilaituai.cn

### Step 4: 生图
先读 `.claude/keywords/generated.json` 查重，避免雷同。
然后运行：`python .claude/scripts/generate_image.py --prompt "图片描述" --output "文件名.jpg"`
配图方向：poster->海报成品 / aishop->商品图 / image2->前后对比

### Step 5: 写入文件
prompts/{编号}-{关键词}.md（含配图+外链）
同时更新 README.md 目录

### Step 6: 记录日志
手动更新 `.claude/keywords/generated.json` 追加记录（id/site/keyword/title/file/image/image_prompt/date）

### Step 7: git add 停住
运行：`python .claude/scripts/git_ops.py add`
不要 commit 不要 push

## 提交发布（用户确认后）
`python .claude/scripts/git_ops.py commit "消息"`
`python .claude/scripts/git_ops.py push`

**When to use**: 用户说"出内容/发一篇/写文章/生成内容/跑一篇/做内容/来一篇/继续/下一个"时
**TRIGGER**: 出内容, 发一篇, 写文章, 生成内容, 跑一篇, 做内容, 来一篇, 继续, 下一个, 海报, 详情页, 主图, 白底图, image2, ai修图, ai生图, ai制图, ai图片, ai海报, ai, 教程, 怎么用, 推荐, 评测, 对比
