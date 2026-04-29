---
name: feishu_doc
description: 飞书云文档操作能力，支持创建、获取、更新云文档；当用户需要操作飞书文档、Markdown转飞书文档或批量处理文档时使用。
dependency:
  python:
    - requests==2.32.5
---

# feishu_doc

飞书云文档操作技能，提供创建、获取、更新三种能力。

## 功能列表

| 操作 | 说明 | 详细文档 |
|------|------|----------|
| 创建文档 | 从 Markdown 创建新的飞书云文档 | [FEISHU_CREATE_DOC.md](references/FEISHU_CREATE_DOC.md) |
| 获取文档 | 获取文档的 Markdown 内容 | [FEISHU_FETCH_DOC.md](references/FEISHU_FETCH_DOC.md) |
| 更新文档 | 更新文档内容（7种模式） | [FEISHU_UPDATE_DOC.md](references/FEISHU_UPDATE_DOC.md) |

## 脚本入口

具体操作前，请先阅读对应的详细文档：

| 脚本 | 说明 | 详细文档 |
|------|------|----------|
| `scripts/create_doc.py` | 创建文档 | [FEISHU_CREATE_DOC.md](references/FEISHU_CREATE_DOC.md) |
| `scripts/fetch_doc.py` | 获取文档 | [FEISHU_FETCH_DOC.md](references/FEISHU_FETCH_DOC.md) |
| `scripts/update_doc.py` | 更新文档 | [FEISHU_UPDATE_DOC.md](references/FEISHU_UPDATE_DOC.md) |