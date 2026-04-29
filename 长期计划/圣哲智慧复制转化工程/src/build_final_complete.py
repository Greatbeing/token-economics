#!/usr/bin/env python3
"""
生成最终完整版《儿童版中国哲学史》PDF
包含：封面、完整目录页（含原始完整标题）、12章内容，书签导航
A4尺寸，优化排版
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
TOC_HTML_FULL = OUTPUT_DIR / "目录页_完整版.html"  # 完整标题目录页
TOC_HTML_SIMPLE = OUTPUT_DIR / "目录页_corrected.html"  # 简化标题目录页（备用）
CHAPTERS_DIR = BASE_DIR / "outputs/儿童哲学史/排版阶段/章节HTML"
FINAL_PDF = OUTPUT_DIR / "儿童版中国哲学史_最终完整版.pdf"

# 完整原始标题（用于书签）
FULL_TITLES = [
    "第一章：世界是从哪儿来的？（老子、孔子、神话）",
    "第二章：为什么我和别人不一样？（孟子、告子、荀子）",
    "第三章：怎样才算“赢了”？（庄子、惠施、孙子）",
    "第四章：我能想做什么就做什么吗？（老子、韩非子、杨朱）",
    "第五章：什么是“好”的规则？（墨子、孟子、法家）",
    "第六章：心里害怕怎么办？（王阳明、禅宗、庄子）",
    "第七章：为什么他们那么爱自由？（嵇康、阮籍、王弼）",
    "第八章：烦恼是怎么来的？（慧能、神秀、禅宗）",
    "第九章：朱熹的\"宇宙大房子\"——理学家在做什么？",
    "第十章：王阳明的\"心里种花\"——良知在你心里",
    "第十一章：如何当一个\"现代中国人\"？（顾炎武、黄宗羲、龚自珍）",
    "第十二章：我们为什么要学哲学？（总结与展望）"
]

# 简化标题（用于内部参考，保持与HTML内容一致）
SIMPLE_TITLES = [
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

# 章节起始页码（基于A4 PDF的实际页码）
CHAPTER_PAGE_STARTS = [4, 9, 14, 18, 23, 29, 35, 45, 51, 57, 63, 69]

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
    if not TOC_HTML_FULL.exists():
        print(f"警告: 完整目录页不存在，将使用简化目录页")
        if not TOC_HTML_SIMPLE.exists():
            missing.append(TOC_HTML_SIMPLE)
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
    """使用wkhtmltopdf将HTML转换为PDF，优化参数"""
    # 检查CSS文件是否存在
    css_dir = html_path.parent
    css_file = css_dir / "style.css"
    css_option = ""
    if css_file.exists():
        css_option = f"--user-style-sheet {css_file}"
    
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
        '--javascript-delay', '5000',  # 等待JS执行
        '--load-error-handling', 'ignore',
        '--load-media-error-handling', 'ignore',
    ]
    
    if css_option:
        cmd.extend(css_option.split())
    
    cmd.extend([
        str(html_path),
        str(pdf_path)
    ])
    
    try:
        print(f"正在转换: {title}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"警告: wkhtmltopdf返回错误: {result.stderr[:500]}")
        else:
            print(f"✓ HTML转换完成: {title}")
    except subprocess.TimeoutExpired:
        print(f"警告: HTML转换超时: {title}")
    except Exception as e:
        print(f"警告: HTML转换异常: {e}")

def merge_pdfs_with_bookmarks(cover_pdf, toc_pdf, chapter_pdfs, output_path):
    """合并PDF并添加完整标题书签"""
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
    
    # 章节页起始页码（基于实际测量）
    for i, chapter_pdf in enumerate(chapter_pdfs):
        with open(chapter_pdf, 'rb') as f:
            chapter_reader = PyPDF2.PdfReader(f)
            chapter_page_starts.append(current_page)
            merger.append(chapter_pdf)
            current_page += len(chapter_reader.pages)
    
    # 添加书签（使用完整标题）
    for i, title in enumerate(FULL_TITLES):
        page_num = CHAPTER_PAGE_STARTS[i] - 1  # 转换为0-based
        merger.add_outline_item(title, page_num)
        print(f"✓ 添加书签: {title} → 第 {CHAPTER_PAGE_STARTS[i]} 页")
    
    # 保存最终PDF
    merger.write(output_path)
    merger.close()
    print(f"✓ 最终PDF已生成: {output_path}")

def verify_pdf(pdf_path):
    """验证PDF质量"""
    print("\n验证PDF质量:")
    
    # 使用pdfinfo检查基本信息
    cmd = ['pdfinfo', str(pdf_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        info = result.stdout
        # 检查页面尺寸
        if "595.276 x 841.89" in info or "A4" in info.upper():
            print("✓ 页面尺寸: A4 (210×297mm)")
        else:
            print("✗ 页面尺寸: 非A4")
        
        # 检查页数
        pages_line = [line for line in info.split('\n') if 'Pages:' in line]
        if pages_line:
            pages = pages_line[0].split(':')[1].strip()
            print(f"✓ 总页数: {pages} 页")
            if int(pages) >= 70:
                print("✓ 页数满足要求 (≥70页)")
            else:
                print("✗ 页数不足70页")
    
    # 检查文件大小
    size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    print(f"✓ 文件大小: {size_mb:.2f} MB")
    
    # 检查是否包含完整标题
    with open(pdf_path, 'rb') as f:
        pdf_content = f.read()
        full_title_sample = FULL_TITLES[0].encode('utf-8')
        if full_title_sample in pdf_content:
            print("✓ PDF中包含完整标题")
        else:
            print("✗ PDF中未检测到完整标题")

def main():
    print("=" * 60)
    print("生成《儿童版中国哲学史》最终完整版PDF")
    print("=" * 60)
    
    # 检查依赖和文件
    check_dependencies()
    check_files()
    
    # 创建临时目录
    temp_dir = Path(tempfile.mkdtemp(prefix="philosophy_book_"))
    print(f"临时目录: {temp_dir}")
    
    # 1. 转换封面为PDF
    cover_pdf = temp_dir / "cover.pdf"
    convert_cover_to_pdf(cover_pdf)
    
    # 2. 转换目录页为PDF（优先使用完整版）
    toc_pdf = temp_dir / "toc.pdf"
    toc_html = TOC_HTML_FULL if TOC_HTML_FULL.exists() else TOC_HTML_SIMPLE
    convert_html_to_pdf(toc_html, toc_pdf, "目录页")
    
    # 3. 转换各章节为PDF
    chapter_pdfs = []
    for i, chapter_file in enumerate(CHAPTER_FILES):
        chapter_path = CHAPTERS_DIR / chapter_file
        chapter_pdf = temp_dir / f"chapter_{i+1}.pdf"
        convert_html_to_pdf(chapter_path, chapter_pdf, SIMPLE_TITLES[i])
        chapter_pdfs.append(chapter_pdf)
    
    # 4. 合并PDF并添加书签
    merge_pdfs_with_bookmarks(cover_pdf, toc_pdf, chapter_pdfs, FINAL_PDF)
    
    # 5. 验证PDF质量
    verify_pdf(FINAL_PDF)
    
    # 6. 清理临时文件（可选）
    # import shutil
    # shutil.rmtree(temp_dir)
    # print(f"临时目录已清理")
    
    print("\n" + "=" * 60)
    print("生成完成!")
    print(f"最终PDF: {FINAL_PDF}")
    print(f"文件大小: {os.path.getsize(FINAL_PDF) / (1024 * 1024):.2f} MB")
    print("=" * 60)

if __name__ == "__main__":
    main()