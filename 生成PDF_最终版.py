#!/usr/bin/env python3
"""
为HTML添加封面并生成PDF
"""

import re
import base64
from pathlib import Path

# 路径
WORK_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/最终合并")
FINAL_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/最终交付")
COVER_IMG = FINAL_DIR / "封面_A4竖版_最终.jpg"
INPUT_HTML = WORK_DIR / "和古人一起想问题_合并版.html"
OUTPUT_HTML = FINAL_DIR / "和古人一起想问题_完整版_文字优化.html"
OUTPUT_PDF = FINAL_DIR / "和古人一起想问题_完整版_文字优化.pdf"

# 读取封面图片并转换为base64
with open(COVER_IMG, 'rb') as f:
    cover_data = f.read()
    cover_base64 = base64.b64encode(cover_data).decode('utf-8')

print(f"封面图片大小: {len(cover_base64)} 字符 (base64)")

# 读取HTML内容
with open(INPUT_HTML, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 读取CSS样式
css_file = WORK_DIR.parent / "修正版" / "style_fixed.css"
with open(css_file, 'r', encoding='utf-8') as f:
    css_content = f.read()

# 构建完整的HTML（添加封面）
full_html = f'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="Pandoc" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <title>和古人一起想问题 - 完整版</title>
  <style>
    {css_content}
    
    /* 封面样式 */
    .cover-page {{
        width: 100%;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        page-break-after: always;
        margin: 0;
        padding: 0;
    }}
    
    .cover-page img {{
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }}
    
    /* 章节样式 */
    body {{
        padding: 0;
        max-width: none;
        margin: 0;
    }}
    
    .chapter {{
        max-width: 100%;
        padding: 20mm;
        page-break-after: always;
    }}
    
    /* 删除Markdown残留 */
    p:empty {{
        display: none;
    }}
    
    /* 段落间距优化 */
    p {{
        margin-bottom: 16px;
        text-indent: 2em;
        line-height: 1.8;
    }}
    
    /* 表格响应式 */
    table {{
        font-size: 14px;
    }}
    
    /* 图片样式 */
    img {{
        max-width: 100%;
        height: auto;
    }}
    
    /* 引用块样式 */
    blockquote {{
        border-left: 3px solid #90CAF9;
        padding-left: 1em;
        margin-left: 0;
        color: #555;
        font-style: italic;
    }}
  </style>
</head>
<body>
  <!-- 封面 -->
  <div class="cover-page">
    <img src="data:image/jpeg;base64,{cover_base64}" alt="封面" />
  </div>
  
  <!-- 正文内容 -->
  {html_content}
</body>
</html>
'''

# 保存HTML
with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"HTML已保存: {OUTPUT_HTML}")
print(f"HTML大小: {len(full_html)} 字符")

# 生成PDF
import subprocess

print("\n正在生成PDF...")
pdf_cmd = [
    'wkhtmltopdf',
    '--enable-local-file-access',
    '--page-size', 'A4',
    '--orientation', 'Portrait',
    '--margin-top', '10mm',
    '--margin-bottom', '10mm',
    '--margin-left', '10mm',
    '--margin-right', '10mm',
    '--print-media-type',
    '--enable-javascript',
    '--javascript-delay', '1000',
    '--image-quality', '90',
    str(OUTPUT_HTML),
    str(OUTPUT_PDF)
]

result = subprocess.run(pdf_cmd, capture_output=True, text=True)

if result.returncode == 0:
    print(f"\n✓ PDF生成成功!")
    print(f"输出文件: {OUTPUT_PDF}")
    
    # 获取文件大小
    import os
    size = os.path.getsize(OUTPUT_PDF)
    print(f"文件大小: {size / (1024*1024):.2f} MB")
else:
    print(f"\n✗ PDF生成失败!")
    print(f"错误: {result.stderr}")
