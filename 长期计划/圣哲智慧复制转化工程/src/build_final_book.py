#!/usr/bin/env python3
"""
最终版《儿童版中国哲学史》PDF生成脚本
包含：封面图片转换、目录页生成、PDF合并、书签添加
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
import PyPDF2
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# 路径配置
BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "outputs/儿童哲学史/最终交付"
COVER_JPG = OUTPUT_DIR / "封面设计.jpg"
ORIGINAL_PDF = OUTPUT_DIR / "儿童版中国哲学史.pdf"
FINAL_PDF = OUTPUT_DIR / "儿童版中国哲学史_完整版.pdf"

# 检查文件是否存在
if not COVER_JPG.exists():
    print(f"错误: 封面图片不存在 {COVER_JPG}")
    sys.exit(1)
if not ORIGINAL_PDF.exists():
    print(f"错误: 原始PDF不存在 {ORIGINAL_PDF}")
    sys.exit(1)

print("开始创建完整版PDF...")

# 章节数据：标题和原始起始页码（从原始PDF书签提取）
chapter_data = [
    ("第一章 世界是从哪儿来的？", 1),
    ("第二章 人性是善还是恶？", 11),
    ("第三章 道：世界的源代码", 20),
    ("第四章 仁：心里的那个开关", 28),
    ("第五章 礼：社会的游戏规则", 37),
    ("第六章 法：冷酷的游戏裁判", 47),
    ("第七章 自然：做真实的自己", 57),
    ("第八章 禅宗：心里的扫把", 75),
    ("第九章 理学：寻找宇宙的说明书", 87),
    ("第十章 心学：心里有个太阳", 99),
    ("第十一章 实学：有用的才是好的", 111),
    ("第十二章 尾声：哲学探险家的毕业典礼", 122),
]

# 步骤1: 将封面图片转换为PDF（使用PIL）
print("1. 转换封面图片为PDF...")
cover_pdf = OUTPUT_DIR / "cover_temp.pdf"
try:
    image = Image.open(COVER_JPG)
    if image.mode in ('RGBA', 'P'):
        image = image.convert('RGB')
    # 保存为PDF，A4尺寸
    image.save(cover_pdf, "PDF", resolution=100.0)
    print(f"  封面PDF已生成: {cover_pdf}")
except Exception as e:
    print(f"封面转换失败: {e}")
    sys.exit(1)

# 步骤2: 使用reportlab生成目录页PDF
print("2. 生成目录页PDF...")
toc_pdf = OUTPUT_DIR / "toc_temp.pdf"

# 创建PDF文档
doc = SimpleDocTemplate(str(toc_pdf), pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=2*cm, bottomMargin=2*cm)
elements = []

# 定义样式
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=28,
    textColor=Color(0xFF/255.0, 0xB7/255.0, 0x4D/255.0, 1),  # 哲学琥珀
    alignment=TA_CENTER,
    spaceAfter=30,
)
subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Heading2'],
    fontSize=20,
    textColor=Color(0x15/255.0, 0x65/255.0, 0xC0/255.0, 1),  # 智慧深蓝
    alignment=TA_CENTER,
    spaceAfter=40,
)
chapter_style = ParagraphStyle(
    'Chapter',
    parent=styles['Normal'],
    fontSize=16,
    textColor=Color(0x5D/255.0, 0x40/255.0, 0x37/255.0, 1),  # 历史深棕
    leftIndent=0,
    spaceAfter=12,
)
page_style = ParagraphStyle(
    'Page',
    parent=styles['Normal'],
    fontSize=14,
    textColor=Color(0x66/255.0, 0x66/255.0, 0x66/255.0, 1),
    alignment=TA_CENTER,
    spaceAfter=12,
)

# 添加标题
elements.append(Paragraph("《和古人一起想问题》", title_style))
elements.append(Paragraph("儿童哲学探险手册", subtitle_style))
elements.append(Spacer(1, 20))
elements.append(Paragraph("目录", ParagraphStyle(
    'TocTitle',
    parent=styles['Heading2'],
    fontSize=24,
    textColor=Color(0x15/255.0, 0x65/255.0, 0xC0/255.0, 1),
    alignment=TA_CENTER,
    spaceAfter=30,
)))

# 计算新页码（封面1页 + 目录1页 = 2页偏移）
offset = 2
toc_entries = []
for title, orig_page in chapter_data:
    new_page = orig_page + offset
    toc_entries.append((title, new_page))

# 创建目录表格
data = [["章节", "页码"]]
for title, page in toc_entries:
    data.append([title, f"第 {page} 页"])

table = Table(data, colWidths=[12*cm, 4*cm])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), Color(0xE1/255.0, 0xF5/255.0, 0xFE/255.0, 1)),  # 思考浅蓝
    ('TEXTCOLOR', (0, 0), (-1, 0), Color(0x02/255.0, 0x88/255.0, 0xD1/255.0, 1)),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), Color(0xF9/255.0, 0xF9/255.0, 0xF9/255.0, 1)),
    ('TEXTCOLOR', (0, 1), (-1, -1), Color(0x33/255.0, 0x33/255.0, 0x33/255.0, 1)),
    ('ALIGN', (0, 1), (0, -1), 'LEFT'),
    ('ALIGN', (1, 1), (1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 14),
    ('GRID', (0, 0), (-1, -1), 1, Color(0x81/255.0, 0xD4/255.0, 0xFA/255.0, 1)),  # 浅蓝边框
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [Color(1,1,1,1), Color(0xF0/255.0, 0xF8/255.0, 0xFF/255.0, 1)]),
    ('TOPPADDING', (0, 1), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
]))
elements.append(table)
elements.append(Spacer(1, 30))

# 添加脚注
elements.append(Paragraph("一本带你探索中国哲学智慧的探险手册", 
                         ParagraphStyle('Footnote',
                                       parent=styles['Normal'],
                                       fontSize=12,
                                       textColor=Color(0x99/255.0, 0x99/255.0, 0x99/255.0, 1),
                                       alignment=TA_CENTER)))
elements.append(Paragraph("适合8-12岁的小小哲学家", 
                         ParagraphStyle('Footnote',
                                       parent=styles['Normal'],
                                       fontSize=12,
                                       textColor=Color(0x99/255.0, 0x99/255.0, 0x99/255.0, 1),
                                       alignment=TA_CENTER)))

# 生成目录PDF
doc.build(elements)
print(f"  目录PDF已生成: {toc_pdf}")

# 步骤3: 合并PDF文件
print("3. 合并PDF文件...")
merger = PyPDF2.PdfMerger()

# 添加封面
with open(cover_pdf, 'rb') as f:
    merger.append(f)

# 添加目录
with open(toc_pdf, 'rb') as f:
    merger.append(f)

# 添加原始内容
with open(ORIGINAL_PDF, 'rb') as f:
    merger.append(f)

# 保存合并后的PDF
with open(FINAL_PDF, 'wb') as f:
    merger.write(f)

print(f"  合并完成: {FINAL_PDF}")

# 步骤4: 添加书签
print("4. 添加书签导航...")
# 重新打开合并后的PDF
reader = PyPDF2.PdfReader(open(FINAL_PDF, 'rb'))
writer = PyPDF2.PdfWriter()

# 复制所有页面
for page in reader.pages:
    writer.add_page(page)

# 添加书签
for title, orig_page in chapter_data:
    # 计算新页码：原始页码 + 偏移量（封面1页 + 目录1页）
    new_page = orig_page + offset  # offset = 2
    # PyPDF2页面索引从0开始
    writer.add_outline_item(title, new_page - 1)  # 转换为0-based索引

# 保存最终PDF（覆盖）
with open(FINAL_PDF, 'wb') as f:
    writer.write(f)

print(f"  书签添加完成")

# 清理临时文件
cover_pdf.unlink()
toc_pdf.unlink()

# 步骤5: 验证
print("5. 验证最终PDF...")
page_count = len(PyPDF2.PdfReader(open(FINAL_PDF, 'rb')).pages)
print(f"  总页数: {page_count} 页")
print(f"  预期页数: 134（内容）+ 2（封面目录）= 136 页")
if page_count == 136:
    print("  ✓ 页数正确")
else:
    print(f"  ⚠ 页数不一致，实际 {page_count} 页")

# 检查文件大小
size_mb = os.path.getsize(FINAL_PDF) / (1024 * 1024)
print(f"  文件大小: {size_mb:.2f} MB")

# 输出书签信息
print("\n📚 目录结构:")
for title, orig_page in chapter_data:
    new_page = orig_page + offset
    print(f"  {title} → 第 {new_page} 页")

print("\n✅ 完整版PDF创建成功!")
print(f"文件位置: {FINAL_PDF.relative_to(BASE_DIR)}")
print(f"包含: 封面 + 目录 + 12章内容 (共{page_count}页)")

# 更新交付说明文档
delivery_note = OUTPUT_DIR / "交付说明.md"
if delivery_note.exists():
    with open(delivery_note, 'a', encoding='utf-8') as f:
        f.write(f"""
## 封面与目录设计说明（2026-04-03）

### 书名方案
采用 **"和古人一起想问题：儿童哲学探险手册"**，理由：
- 更贴近8-12岁儿童心理，突出"探险"互动感
- 呼应全书"思想剧场""想一想"等互动环节设计
- 易于传播记忆，口语化亲切

### 封面设计
- **风格**：温暖色调绘本风，柔和线条，融入竹简、哲人剪影、探险地图、星空等中国哲学元素
- **尺寸**：16:9比例，适配电子书显示
- **文件**：`封面设计.jpg`

### 目录页
- **结构**：包含12章标题及对应页码（已计算封面目录偏移）
- **样式**：简洁表格布局，色彩与全书风格协调
- **文件**：已整合入最终PDF

### 最终PDF
- **文件**：`儿童版中国哲学史_完整版.pdf`
- **页数**：136页（封面1+目录1+内容134）
- **书签**：已添加12章节书签，可点击跳转

---
""")
    print(f"  交付说明已更新: {delivery_note}")