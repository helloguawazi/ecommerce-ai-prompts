# 关键词驱动内容发布流程

## 技术栈

- **终端**: Claude Code (DeepSeek 兼容接口)
- **生图API**: Grsai API (`gpt-image-2`)
- **关键词源**: Excel 文件（`合并结果_搜索量≥50.xlsx` / `AI海报.xls`）

## 完整发布流程

### 第1步：取关键词

运行取词脚本，随机从 Excel 取出一个关键词并自动删除：

```bash
python -X utf8 .claude/keywords/pick_keyword.py
```

输出示例：
```json
{"keyword": "ai修图", "site": "image2", "domain": "image2.anyachina.cn"}
```

### 第2步：判断站点归属

| 关键词特征 | 站点 | 域名 |
|-----------|------|------|
| 含"海报" | poster | poster.anyachina.cn |
| 其他（默认） | image2 | image2.anyachina.cn |

### 第3步：写文章

Claude 写约 600 字 SEO 文章，标题关键词前置 15-30 字有场景。

**外链规则**：在引言段落后、图片前，单独放一行带链接的推荐语。每篇文章措辞不同（emoji、句式、推荐角度都变化）。

| 文章站点 | 推荐链接 |
|---------|---------|
| image2 站 | 同时推荐 `aishop.anyachina.cn` 和 `poster.anyachina.cn`（两个链接） |
| poster 站 | 推荐 `aishop.anyachina.cn`（只放一个） |
| aishop 站 | 推荐 `poster.anyachina.cn`（只放一个） |

格式示例：
```
👉 推荐工具：[aishop.anyachina.cn](url) 一键生成商品图
⭐ 试试 [poster.anyachina.cn](url) 做促销海报，30秒出图
```

页面底部保留：
```
*在线工具：[未来图AI](https://www.weilaituai.cn/)*
```

### 第4步：生图

```bash
python .claude/scripts/generate_image.py --prompt "图片描述" --output "文件名.jpg" --aspect "1024x1024"
```

先读 `.claude/keywords/generated.json` 查重避免雷同。

**配图方向**：
- poster → 海报成品展示
- image2 → 前后对比 / 工具界面

### 第5步：写文件

文件名规则：`{关键词}.md`，直接放根目录。

图片存 `images/` 目录。

### 第6步：更新日志

追加记录到 `.claude/keywords/generated.json`：

```json
{
  "id": 47,
  "keyword": "关键词",
  "site": "image2",
  "title": "文章标题",
  "file": "关键词.md",
  "image": "images/xxx.jpg",
  "image_prompt": "AI生成用提示词",
  "date": "2026-07-16"
}
```

### 第7步：清理 Excel 已用关键词

```python
# 从 Excel 删除已用关键词
```

### 第8步：Git 提交

```bash
git add .
git commit -m "add N articles"
git push
```

## 批量跑5篇流程

1. 运行 `pick_keyword.py` 取5个关键词（每次取一个，取5次）
2. 逐个写文章（.md）
3. 批量生图（5张一起）
4. 更新 `generated.json`
5. 从 Excel 删除已用的关键词
6. `git add && git commit && git push`

## .gitignore 白名单规则

只同步 `.md` 和图片文件，其余全部忽略：

```
# 先忽略所有
*

# 允许进入子目录
!*/

# 允许 Markdown 文章
!*.md

# 允许图片文件
!*.jpg !*.jpeg !*.png !*.gif !*.webp !*.svg

# 排除临时缓存
tsk_*.png
wechat_*.png

# 本地配置
.claude/
```

## 已知问题 & 解决方案

### 安全分类器 "temporarily unavailable"

**现象**：执行 Bash/PowerShell 时报错 `DeepSeek-V4-Flash is temporarily unavailable, so auto mode cannot determine the safety of...`

**原因**：设置 `CLAUDE_CODE_ATTRIBUTION_HEADER: "0"` 会导致 DeepSeek 端拒绝分类器请求（HTTP 429）。

**解决**：删除 `settings.json` 中的 `CLAUDE_CODE_ATTRIBUTION_HEADER` 项（保留 `DISABLE_CLIENT_CONTEXT` 和 `DISABLE_NONCE` 不影响缓存）。

### git 误提交 py/tmp 文件

**解决**：已配置白名单 `.gitignore`，只有 `.md` 和图片文件会被跟踪。
