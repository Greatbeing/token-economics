#!/usr/bin/env python3
"""
创建完整版《儿童版中国哲学史》PDF，包含封面和目录
使用PIL处理封面图片
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
import PyPDF2
from PIL import Image

# 路径配置
BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "outputs/儿童哲学史/最终交付"
COVER_JPG = OUTPUT_DIR / "封面设计.jpg"
TOC_HTML = OUTPUT_DIR / "目录页.html"
ORIGINAL_PDF = OUTPUT_DIR / "儿童版中国哲学史.pdf"
FINAL_PDF = OUTPUT_DIR / "儿童版中国哲学史_完整版.pdf"

# 检查文件是否存在
if not COVER_JPG.exists():
    print(f"错误: 封面图片不存在 {COVER_JPG}")
    sys.exit(1)
if not TOC_HTML.exists():
    print(f"错误: 目录页不存在 {TOC_HTML}")
    sys.exit(1)
if not ORIGINAL_PDF.exists():
    print(f"错误: 原始PDF不存在 {ORIGINAL_PDF}")
    sys.exit(1)

print("开始创建完整版PDF...")

# 步骤1: 将封面图片转换为PDF（使用PIL）
print("1. 转换封面图片为PDF...")
cover_pdf = OUTPUT_DIR / "cover_temp.pdf"
try:
    # 打开图片
    image = Image.open(COVER_JPG)
    # 转换为RGB（确保兼容性）
    if image.mode in ('RGBA', 'P'):
        image = image.convert('RGB')
    # 保存为PDF，使用A4尺寸（210x297mm）
    image.save(cover_pdf, "PDF", resolution=100.0)
    print(f"  封面PDF已生成: {cover_pdf}")
except Exception as e:
    print(f"封面转换失败: {e}")
    sys.exit(1)

# 步骤2: 将目录HTML转换为PDF
print("2. 转换目录页为PDF...")
toc_pdf = OUTPUT_DIR / "toc_temp.pdf"
# 使用wkhtmltopdf，但需要确保CSS能加载
# 复制样式文件到同一目录（已在generate_toc_html.py中完成）
cmd = ['wkhtmltopdf', '--page-width', '210mm', '--page-height', '297mm', '--disable-smart-shrinking',
       '--quiet',
       str(TOC_HTML.absolute()), str(toc_pdf.absolute())]
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f"目录转换失败: {result.stderr}")
    # 尝试不带disable-smart-shrinking
    cmd = ['wkhtmltopdf', '--page-width', '210mm', '--page-height', '297mm',
           str(TOC_HTML.absolute()), str(toc_pdf.absolute())]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"目录转换再次失败: {result.stderr}")
        sys.exit(1)
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

# 书签数据: 章节标题和原始起始页码（从原始PDF书签提取）
# 注意：原始页码是从原始PDF的第1页开始（即内容开始）
# 在合并后的PDF中，封面(1页)+目录(1页)=2页偏移
chapter_bookmarks = [
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

# 添加书签
for title, orig_page in chapter_bookmarks:
    # 计算新页码：原始页码 + 偏移量（封面1页 + 目录1页）
    new_page = orig_page + 1 + 1  # 封面和目录各占1页
    # 注意：PyPDF2页面索引从0开始
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
for title, orig_page in chapter_bookmarks:
    new_page = orig_page + 2
    print(f"  {title} → 第 {new_page} 页")

print("\n✅ 完整版PDF创建成功!")
print(f"文件位置: {FINAL_PDF.relative_to(BASE_DIR)}")
print(f"包含: 封面 + 目录 + 12章内容 (共{page_count}页)")