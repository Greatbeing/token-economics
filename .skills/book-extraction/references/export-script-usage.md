# 导出工具使用说明（内部文档）

> 本文档描述的是智能体内部使用的导出工具。
> 当用户需要PDF或Word格式时，智能体会调用此工具生成相应文件。

## 工具位置

`scripts/export_report.py`

## 功能说明

智能体内部使用的导出工具，支持将Markdown报告转换为以下格式：
- **PDF**：正式文档，便于打印或分享
- **Word**：可编辑文档，便于进一步编辑或添加内容

智能体在用户需要时调用此工具，生成PDF或Word格式的文件。

## 工具使用方式（供智能体参考）

智能体在以下情况会调用此工具：

1. **生成报告后**：自动生成PDF和Word格式供用户下载
2. **用户请求下载时**：根据用户请求的格式生成相应文件

### 调用方式

```bash
python scripts/export_report.py <input_file> --format <format>
```

### 参数说明

- `<input_file>`：输入的Markdown报告文件路径
- `--format`：输出格式，可选值：`pdf` / `word`，多个格式用逗号分隔（如：`pdf,word`）
- `--output` / `-o`：输出文件路径（可选）
- `--output-dir`：输出目录（可选）
- `--base-name`：输出文件基础名（可选）

## 调用示例（供智能体参考）

### 示例1：生成PDF和Word
```bash
python scripts/export_report.py book-report.md --format pdf,word
```

### 示例2：只生成PDF
```bash
python scripts/export_report.py book-report.md --format pdf
```

### 示例3：只生成Word
```bash
python scripts/export_report.py book-report.md --format word
```

## 用户交互方式

智能体在用户请求PDF或Word格式时的标准回复：

> **正在生成PDF版本...** 📄
>
> PDF文件已生成：`{书名}-报告.pdf`
> 文件位置：`./{书名}-报告.pdf`

或：

> **正在生成Word版本...** 📝
>
> Word文件已生成：`{书名}-报告.docx`
> 文件位置：`./{书名}-报告.docx`

如用户同时请求两种格式：

> **正在生成PDF和Word版本...** 📄📝
>
> PDF文件已生成：`{书名}-报告.pdf`
> Word文件已生成：`{书名}-报告.docx`
> 文件位置：`./{书名}-报告.pdf` 和 `./{书名}-报告.docx`

## 依赖安装

脚本依赖以下Python库：
- `markdown`：Markdown解析
- `python-docx`：Word文档生成
- `weasyprint`：PDF生成

**Python依赖安装**：
```bash
pip install markdown python-docx weasyprint
```

**系统依赖（PDF导出需要）**：
- **Linux系统**：安装中文字体包
  ```bash
  sudo apt install fonts-noto-cjk fonts-wqy-zenhei fonts-wqy-microhei
  fc-cache -fv
  ```
- **Windows/macOS系统**：系统通常已包含所需字体，无需额外安装

**注意**：
- `weasyprint`在某些系统上可能需要额外安装系统依赖（如GTK+、字体库）
- 如果PDF导出失败，可以运行诊断脚本：`python scripts/diagnose_pdf.py`

## 常见问题

### Q1：导出PDF时出现字体错误或空白
**A**：这通常是因为系统缺少中文字体。解决方法：
- **Linux系统**：安装中文字体包
  ```bash
  sudo apt install fonts-noto-cjk fonts-wqy-zenhei fonts-wqy-microhei
  fc-cache -fv
  ```
- **Windows/macOS系统**：系统通常已包含中文字体，无需额外安装
- **验证方法**：运行诊断脚本 `python scripts/diagnose_pdf.py`
- **替代方案**：如果问题持续，先导出为Word格式，再用Word的"另存为PDF"功能

### Q2：Word导出后表格格式混乱
**A**：Word导出为简化版本，主要保留文本内容。建议在Word中手动调整表格格式，或导出为PDF格式。

### Q3：脚本提示缺少依赖库
**A**：按照"依赖安装"章节的命令安装所需的Python库。如果使用的是虚拟环境，请确保在正确的环境中安装。

### Q4：应该选择PDF还是Word格式？
**A**：根据使用场景选择：
- **PDF格式**：适合需要打印、直接分享、正式存档的场景
- **Word格式**：适合需要进一步编辑、添加内容、与他人协作的场景
- **同时导出**：可以使用`--format pdf,word`同时导出两种格式

## 技术限制

1. **PDF生成**：
   - 依赖weasyprint的CSS渲染能力，某些Markdown特性可能无法完美呈现
   - 需要系统安装中文字体才能正确显示中文内容
   - PDF文件大小取决于内容和复杂度，长报告生成可能较慢
2. **Word导出**：为简化版本，主要保留文本内容，表格、代码块等复杂格式需要手动调整
3. **文件大小**：对于包含大量案例和内容的长报告，PDF和Word生成可能较慢

## 诊断工具

提供PDF导出诊断脚本：`scripts/diagnose_pdf.py`

**使用方法**：
```bash
python scripts/diagnose_pdf.py
```

**诊断内容**：
- 检查依赖库是否完整安装
- 检查系统是否包含中文字体
- 测试PDF生成功能
- 提供问题诊断和解决方案建议

**何时使用**：
- PDF导出失败时
- PDF显示空白或乱码时
- 不确定PDF功能是否正常时

### 进阶使用

### 导出并重命名
```bash
python scripts/export_report.py book-report.md --format pdf --output "影响力-深度榨取报告.pdf"
```

### 自定义输出目录
```bash
python scripts/export_report.py book-report.md --format pdf,word --output-dir ./reports
```

### 批量导出（用户自主选择）
```bash
# 只导出PDF
python scripts/export_report.py book-report.md --format pdf

# 只导出Word
python scripts/export_report.py book-report.md --format word

# 同时导出PDF和Word
python scripts/export_report.py book-report.md --format pdf,word
```

## 更新日志

- **v2.0**：移除JSON和CSV格式，专注Markdown/PDF/Word导出，改进用户体验
- **v1.0**：初始版本，支持多种格式导出
