#!/usr/bin/env python3
"""
生成A4尺寸的《儿童版中国哲学史》完整PDF
包含：封面、目录页、12章内容，书签导航
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
TOC_HTML = OUTPUT_DIR / "目录页_corrected.html"
CHAPTERS_DIR = BASE_DIR / "outputs/儿童哲学史/排版阶段/章节HTML"
FINAL_PDF = OUTPUT_DIR / "儿童版中国哲学史_A4完整版.pdf"

# 正确章节标题（与HTML内容一致）
CHAPTER_TITLES = [
    "第一章 世界是从哪儿来的？",
    "第二章 为什么我和别人不一样？",
    "第三章 怎样才算“赢了”？",
    "第四章 我能想做什么就做什么吗？",
    "第五章 什么是“好”的规则？",
    "第六章 心里害怕怎么办？",
    "第七章 为什么他们那么爱自由？",
    "第八章 烦恼是怎么来的？",
    "第九章 朱熹的\"宇宙大房子\"",
    "第十章 王阳明的\"心里种花\"",
    "第十一章 如何当一个\"现代中国人\"？",
    "第十二章 我们为什么要学哲学？"
]

# 章节HTML文件名（按顺序）
CHAPTER_FILES = [
    "第1章样张.html",
    "第2章样张.html",
    "第3章样张.html",
    "第4章样张.html",
    "第5章样张.html",
    "第6章样张.html",
    "第7章样张.html",
    "第8章样张.html",
    "第9章样张.html",
    "第10章样张.html",
    "第11章样张.html",
    "第12章样张.html"
]

def check_dependencies():
    """检查必要工具"""
    tools = ['wkhtmltopdf', 'pdfinfo']
    for tool in tools:
        if subprocess.run(['which', tool], capture_output=True).returncode != 0:
            print(f"错误: 未找到 {tool}")
            sys.exit(1)
    print("✓ 依赖检查通过")

def check_files():
    """检查输入文件"""
    missing = []
    if not COVER_JPG.exists():
        missing.append(COVER_JPG)
    if not TOC_HTML.exists():
        missing.append(TOC_HTML)
    for f in CHAPTER_FILES:
        path = CHAPTERS_DIR / f
        if not path.exists():
            missing.append(path)
    if missing:
        print("错误: 以下文件不存在:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)
    print("✓ 所有输入文件存在")

def convert_cover_to_pdf(output_path):
    """将封面JPG转换为单页PDF"""
    try:
        img = Image.open(COVER_JPG)
        # 创建A4尺寸的画布
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.pdfgen import canvas
        
        c = canvas.Canvas(str(output_path), pagesize=A4)
        page_width, page_height = A4
        
        # 计算图片缩放以适合页面
        img_width, img_height = img.size
        scale = min(page_width / img_width, page_height / img_height) * 0.95
        new_width = img_width * scale
        new_height = img_height * scale
        x = (page_width - new_width) / 2
        y = (page_height - new_height) / 2
        
        c.drawImage(str(COVER_JPG), x, y, width=new_width, height=new_height)
        c.showPage()
        c.save()
        print(f"✓ 封面转换为PDF: {output_path}")
    except Exception as e:
        print(f"错误: 封面转换失败: {e}")
        sys.exit(1)

def convert_html_to_pdf(html_path, pdf_path, title):
    """使用wkhtmltopdf将HTML转换为PDF"""
    cmd = [
        'wkhtmltopdf',
        '--page-size', 'A4',
        '--margin-top', '15mm',
        '--margin-bottom', '15mm',
        '--margin-left', '15mm',
        '--margin-right', '15mm',
        '--encoding', 'UTF-8',
        '--no-stop-slow-scripts',
        '--enable-local-file-access',
        str(html_path),
        str(pdf_path)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"警告: wkhtmltopdf返回错误: {result.stderr}")
        else:
            print(f"✓ HTML转换完成: {title}")
    except subprocess.TimeoutExpired:
        print(f"警告: HTML转换超时: {title}")
    except Exception as e:
        print(f"警告: HTML转换异常: {e}")

def merge_pdfs_with_bookmarks(cover_pdf, toc_pdf, chapter_pdfs, output_path):
    """合并PDF并添加书签"""
    merger = PyPDF2.PdfMerger()
    
    # 添加封面
    merger.append(cover_pdf)
    
    # 添加目录
    merger.append(toc_pdf)
    
    # 添加章节并记录页码
    chapter_page_starts = []
    current_page = 0
    
    # 封面和目录的页数
    with open(cover_pdf, 'rb') as f:
        cover_reader = PyPDF2.PdfReader(f)
        current_page += len(cover_reader.pages)
    
    with open(toc_pdf, 'rb') as f:
        toc_reader = PyPDF2.PdfReader(f)
        current_page += len(toc_reader.pages)
    
    # 记录第一章起始页码（从0开始计数）
    first_chapter_start = current_page
    
    for i, chapter_pdf in enumerate(chapter_pdfs):
        with open(chapter_pdf, 'rb') as f:
            chapter_reader = PyPDF2.PdfReader(f)
            page_count = len(chapter_reader.pages)
            chapter_page_starts.append((i, current_page))
            current_page += page_count
    
    # 合并所有章节
    for chapter_pdf in chapter_pdfs:
        merger.append(chapter_pdf)
    
    # 添加书签
    for i, (chapter_idx, page_start) in enumerate(chapter_page_starts):
        title = CHAPTER_TITLES[chapter_idx]
        # 书签页码是相对于PDF起始的绝对页码
        merger.add_outline_item(title, page_start)
    
    # 保存最终PDF
    merger.write(str(output_path))
    merger.close()
    
    print(f"✓ PDF合并完成，共{current_page}页")
    
    # 返回各章节起始页码（从1开始计数，用于目录页）
    page_starts = [page_start + 1 for _, page_start in chapter_page_starts]
    return page_starts

def main():
    print("开始生成A4尺寸完整PDF...")
    
    # 检查依赖和文件
    check_dependencies()
    check_files()
    
    # 创建临时目录
    temp_dir = Path(tempfile.mkdtemp())
    print(f"临时目录: {temp_dir}")
    
    # 转换封面
    cover_pdf = temp_dir / "cover.pdf"
    convert_cover_to_pdf(cover_pdf)
    
    # 转换目录页
    toc_pdf = temp_dir / "toc.pdf"
    convert_html_to_pdf(TOC_HTML, toc_pdf, "目录页")
    
    # 转换各章节
    chapter_pdfs = []
    for i, (html_file, title) in enumerate(zip(CHAPTER_FILES, CHAPTER_TITLES)):
        html_path = CHAPTERS_DIR / html_file
        pdf_path = temp_dir / f"chapter_{i+1}.pdf"
        convert_html_to_pdf(html_path, pdf_path, title)
        chapter_pdfs.append(pdf_path)
    
    # 合并PDF并添加书签
    page_starts = merge_pdfs_with_bookmarks(cover_pdf, toc_pdf, chapter_pdfs, FINAL_PDF)
    
    # 输出页码信息
    print("\n章节起始页码:")
    for i, (title, page) in enumerate(zip(CHAPTER_TITLES, page_starts)):
        print(f"  {title} → 第 {page} 页")
    
    # 验证文件
    if FINAL_PDF.exists():
        size_mb = FINAL_PDF.stat().st_size / (1024 * 1024)
        print(f"\n✅ 完成！文件已生成: {FINAL_PDF}")
        print(f"   文件大小: {size_mb:.2f} MB")
        
        # 使用pdfinfo获取页数
        result = subprocess.run(['pdfinfo', str(FINAL_PDF)], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if line.startswith('Pages:'):
                print(f"   总页数: {line.split(':')[1].strip()}")
            if line.startswith('Page size:'):
                print(f"   页面尺寸: {line.split(':')[1].strip()}")
    else:
        print("错误: 最终PDF未生成")
        sys.exit(1)
    
    # 清理临时目录
    import shutil
    shutil.rmtree(temp_dir)
    
    print("\n任务完成！")

if __name__ == "__main__":
    main()