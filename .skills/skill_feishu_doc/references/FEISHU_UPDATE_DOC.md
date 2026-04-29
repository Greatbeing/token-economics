# 更新飞书云文档

更新飞书云文档内容，支持 7 种更新模式。优先使用局部更新（replace_range/append/insert_before/insert_after），慎用 overwrite（会清空文档重写，可能丢失图片、评论等）。

## 调用方式

```bash
python3 scripts/update_doc.py --doc-id '文档ID' --mode '更新模式' --markdown 'Markdown内容' [--selection-with-ellipsis 'xxx'] [--selection-by-title 'xxx'] [--new-title '新标题'] [--task-id 'xxx']
```

## 参数

### --doc-id (必填)
文档 ID 或 URL。

### --mode (必填)
更新模式，支持以下值：

| 模式 | 说明 | 需要 markdown | 需要 selection |
|------|------|---------------|----------------|
| `overwrite` | 完全覆盖（慎用，会清空文档） | 是 | 否 |
| `append` | 追加到末尾 | 是 | 否 |
| `replace_range` | 定位替换（唯一匹配） | 是 | 是 |
| `replace_all` | 全文替换（多处匹配） | 是 | 否 |
| `insert_before` | 前插入 | 是 | 是 |
| `insert_after` | 后插入 | 是 | 是 |
| `delete_range` | 删除内容 | 否 | 是 |

### --markdown (必填，delete_range 除外)
新的 Markdown 内容。

### --selection-with-ellipsis (可选)
内容定位，支持两种格式：

1. **范围匹配**：`开头内容...结尾内容`
   - 匹配从开头到结尾的所有内容（包含中间内容）
   - 建议 10-20 字符确保唯一性

2. **精确匹配**：`完整内容`（不含 `...`）
   - 匹配完整的文本内容
   - 适合替换短文本、关键词等

**转义说明**：如果要匹配的内容本身包含 `...`，使用 `\.\.\.` 表示字面量的三个点。

示例：
- `你好...世界` → 匹配从"你好"到"世界"之间的任意内容
- `你好\.\.\.世界` → 匹配字面量 "你好...世界"

### --selection-by-title (可选)
标题定位，格式：`## 章节标题`（可带或不带 # 前缀）

自动定位整个章节（从该标题到下一个同级或更高级标题之前）。

示例：
- `## 功能说明` → 定位二级标题"功能说明"及其下所有内容
- `功能说明` → 定位任意级别的"功能说明"标题及其内容

### --new-title (可选)
更新文档标题。如果提供此参数，将在更新文档内容后同步更新文档标题。

特性：
- 仅支持纯文本，不支持富文本格式
- 长度限制：1-800 字符
- 可以与任何 mode 配合使用

### --task-id (可选)
异步任务 ID，用于查询任务状态。

## 返回值

### 成功
```json
{
  "status": "success",
  "result": {
    "success": true,
    "doc_id": "文档ID",
    "mode": "使用的模式",
    "message": "文档更新成功"
  }
}
```

### 异步模式
```json
{
  "status": "success",
  "result": {
    "task_id": "async_task_xxxx",
    "message": "文档更新已提交异步处理"
  }
}
```

---

## 使用示例

### append - 追加到末尾
```bash
python3 scripts/update_doc.py \
  --doc-id 'doxcnXXX' \
  --mode 'append' \
  --markdown '## 更新日志

2025-01-15: 新增功能 A'
```

### replace_range - 定位替换

**使用 selection-with-ellipsis**
```bash
python3 scripts/update_doc.py \
  --doc-id 'doxcnXXX' \
  --mode 'replace_range' \
  --selection-with-ellipsis '## 旧章节标题...旧章节结尾。' \
  --markdown '## 新章节标题

新的内容...'
```

**使用 selection-by-title（替换整个章节）**
```bash
python3 scripts/update_doc.py \
  --doc-id 'doxcnXXX' \
  --mode 'replace_range' \
  --selection-by-title '## 功能说明' \
  --markdown '## 功能说明

更新后的功能说明内容...'
```

### replace_all - 全文替换
```bash
python3 scripts/update_doc.py \
  --doc-id 'doxcnXXX' \
  --mode 'replace_all' \
  --selection-with-ellipsis '张三' \
  --markdown '李四'
```

### insert_before - 前插入
```bash
python3 scripts/update_doc.py \
  --doc-id 'doxcnXXX' \
  --mode 'insert_before' \
  --selection-with-ellipsis '## 危险操作...数据丢失风险。' \
  --markdown '> **警告**：以下操作需谨慎！'
```

### insert_after - 后插入
```bash
python3 scripts/update_doc.py \
  --doc-id 'doxcnXXX' \
  --mode 'insert_after' \
  --selection-with-ellipsis '```python...```' \
  --markdown '**输出示例**：
```
result = 42
```'
```

### delete_range - 删除内容
```bash
python3 scripts/update_doc.py \
  --doc-id 'doxcnXXX' \
  --mode 'delete_range' \
  --selection-with-ellipsis '## 废弃章节...不再需要的内容。'
```

### 同时更新标题和内容
```bash
python3 scripts/update_doc.py \
  --doc-id 'doxcnXXX' \
  --mode 'append' \
  --markdown '## 更新日志

2025-01-15: 新增功能...' \
  --new-title '项目文档（已更新）'
```

---

## 最佳实践

### 1. 小粒度精确替换
修改文档内容时，**定位范围越小越安全**。尤其是表格、分栏等嵌套块，应精确定位到需要修改的文本，避免影响其他内容。

### 2. 保护不可重建的内容
图片、画板、电子表格、多维表格、任务等内容以 token 形式存储，**无法读出后原样写入**。

保护策略：
- 替换时避开包含这些内容的区域
- 精确定位到纯文本部分进行修改

### 3. 分步更新优于整体覆盖
修改多处内容时：
- ✅ 多次小范围替换，逐步修改
- ⚠️ 谨慎使用 `overwrite` 重写整个文档

### 4. insert 模式扩大定位范围时注意插入位置
使用 `insert_before` 或 `insert_after` 时，如果目标内容重复出现，需要扩大 `selection_with_ellipsis` 范围来唯一定位。

关键：插入位置基于匹配范围的**边界**：
- `insert_after` → 插入在匹配范围的**结尾**之后
- `insert_before` → 插入在匹配范围的**开头**之前

---

## 注意事项

- `overwrite` 会清空文档后重写，可能丢失图片、评论等，仅在需要完全重建文档时使用
- `replace_range` 和 `replace_all` 的区别：前者要求匹配唯一，后者允许多处匹配
- `delete_range` 不需要 markdown 参数
- Markdown 语法需符合 Lark-flavored Markdown 规范
- 如果返回没有更新权限的错误，请让用户把文档链接发给你，将权限提高到编辑权限
