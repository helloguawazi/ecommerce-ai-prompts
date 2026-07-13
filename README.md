# 电商 AI 生图内容站群 · 流量词驱动发布系统

> **一句话**：输入关键词 → Claude 写文 + Grsai 生图 → 写入文件停住审核 → 你点头再发布

本站群以 AI 电商生图流量词为核心，通过 Claude Code Workflow 实现**关键词驱动的内容生产**，覆盖 3 个垂直子站。

---

## 站点矩阵

| 站点 | 域名 | 定位 |
|---|---|---|
| **AI 海报站** | [poster.anyachina.cn](https://poster.anyachina.cn) | AI 海报生成工具 |
| **AI 电商图站** | [aishop.anyachina.cn](https://aishop.anyachina.cn) | AI 商品图/详情页生成 |
| **Image2 流量站** | [image2.anyachina.cn](https://image2.anyachina.cn) | Image2/AI修图工具教程 |

---

## 工作流程

```
你说关键词
  → Claude 判断该发哪个站
  → Claude 写 SEO 文章（800-1500字）
  → Grsai API 生图（gpt-image-2）
  → 写入 prompts/ + git add
  → 停住，等你审核
  → 你满意 → 我 commit + push
```

## 生图 API

| 项目 | 内容 |
|---|---|
| 服务 | Grsai API |
| 模型 | gpt-image-2 / gpt-image-2-vip |
| 地址 | `https://grsaiapi.com/v1/api/generate` |
| 认证 | Bearer Token（设置环境变量 `GRSAI_API_KEY`） |

## 外链规则

- aishop 文章 → 植入 poster.anyachina.cn
- poster 文章 → 植入 aishop.anyachina.cn
- image2 文章 → 同时植入 aishop + poster

---

## 已发布文章

### Image2 流量站
- [AI修图怎么用？2026年最新AI修图工具在线使用教程](prompts/003-ai修图-使用教程.md)
- [bananapro官网怎么进？官网入口与使用教程](prompts/004-bananapro官网-入口教程.md)
- [电商AI作图怎么做？2026年电商图片AI生成教程](prompts/005-电商ai作图-教程.md)
- [P图用哪个AI？2026年最实用的4款AI P图工具推荐](prompts/006-p图用哪个ai-推荐.md)

### AI 电商图站
- （待更新）

### AI 海报站
- （待更新）

---

## 关键词数据资产

| 文件 | 内容 | 用途 |
|---|---|---|
| `合并结果_搜索量≥50.xlsx` | 260 个 AI 流量词（含搜索量） | image2 站选题 |
| `AI海报.xls` | 782 个海报相关词（含搜索量/竞争度） | poster 站选题 |

---

## 文件结构

```
.claude/
  skills/content-publish.md      Skill 定义
  workflows/content-publish.js   Workflow 编排
  keywords/keyword-mapping.yaml  站点映射参考
prompts/                         已生成的文章
images/                          配图
```

---

## 注意事项

1. **GRSAI_API_KEY**：使用前设置环境变量
2. **审核机制**：Workflow 只做 `git add` 不做 commit，你审核后再发
3. **内容差异化**：GitHub 内容与独立站保持角度差异
4. **页尾**：每篇保留 `https://www.weilaituai.cn/` 链接
