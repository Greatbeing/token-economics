# 获取飞书云文档

获取飞书云文档的 Markdown 内容（Lark-flavored 格式）。

## 调用方式

```bash
python3 scripts/fetch_doc.py --doc-id '文档ID或URL' [--offset 0] [--limit 10000]
```

## 参数

### --doc-id (必填)
文档 ID 或 URL，支持多种格式：
- 直接传 URL：`https://xxx.feishu.cn/docx/Z1Fjxxx`
- 直接传 token：`Z1Fjxxx`
- 知识库 URL：`https://xxx.feishu.cn/wiki/Z1Fjxxx`

系统会自动解析并提取正确的文档 token。

### --offset (可选)
字符偏移量，用于大文档分页获取，默认 0。

### --limit (可选)
返回的最大字符数，仅在明确要求分页时使用。

## 返回值

### 成功
```json
{
  "status": "success",
  "result": {
    "title": "文档标题",
    "markdown": "文档的 Markdown 内容..."
  }
}
```

## 使用示例

### 示例1：通过 URL 获取文档
```bash
python3 scripts/fetch_doc.py --doc-id 'https://xxx.feishu.cn/docx/doxcnXXX'
```

### 示例2：通过 token 获取文档
```bash
python3 scripts/fetch_doc.py --doc-id 'doxcnXXX'
```

### 示例3：分页获取大文档
```bash
python3 scripts/fetch_doc.py --doc-id 'doxcnXXX' --offset 0 --limit 5000
```

---

## 重要：图片、文件、画板的处理

**文档中的图片、文件、画板以 HTML 标签形式返回，需要单独处理！**

### 识别格式

返回的 Markdown 中，媒体文件以 HTML 标签形式出现：

**图片**
```html
<image token="Z1FjxxxxxxxxxxxxxxxxxxxtnAc" width="1833" height="2491" align="center"/>
```

**文件**
```html
<view type="1">
  <file token="Z1FjxxxxxxxxxxxxxxxxxxxtnAc" name="skills.zip"/>
</view>
```

**画板**
```html
<whiteboard token="Z1FjxxxxxxxxxxxxxxxxxxxtnAc"/>
```

---

## 注意事项

1. 大文档建议使用 offset 和 limit 分页获取
2. 图片、文件、画板的 token 需要单独下载处理
3. 返回的 Markdown 符合 Lark-flavored Markdown 规范
4. 文档内容可能包含飞书特有的扩展标签
5. 如果返回没有阅读权限的错误，请让用户把文档链接发给你即可授权
