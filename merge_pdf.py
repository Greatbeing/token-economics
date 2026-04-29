#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并所有章节HTML为完整PDF
使用wkhtmltopdf
"""

import os
import subprocess
from pathlib import Path

# 路径配置
BASE_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史")
CHAPTERS_DIR = BASE_DIR / "移动端适配" / "chapters_fixed"
IMAGES_DIR = BASE_DIR / "移动端适配" / "optimized_images"
OUTPUT_DIR = BASE_DIR / "最终交付"
COVER_JPG = OUTPUT_DIR / "封面_A4竖版_最终.jpg"

# 确保输出目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 章节顺序
CHAPTER_FILES = [
    "第一章_修复版.html",
    "第二章_修复版.html",
    "第三章_修复版.html",
    "第四章_修复版.html",
    "第五章_修复版.html",
    "第六章_修复版.html",
    "第七章_修复版.html",
    "第八章_修复版.html",
    "第九章_修复版.html",
    "第十章_修复版.html",
    "第十一章_修复版.html",
    "第12章_修复版.html",
]

def create_cover_pdf():
    """将封面图片转换为PDF"""
    cover_pdf = OUTPUT_DIR / "cover_temp.pdf"
    
    # 使用PIL将图片转换为PDF
    try:
        from PIL import Image
        img = Image.open(COVER_JPG)
        # 转换为RGB如果需要
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(cover_pdf, "PDF", resolution=150)
        print(f"✅ 封面PDF已创建: {cover_pdf.name}")
        return cover_pdf
    except ImportError:
        print("PIL not available, trying alternative method...")
        # 备选方法：使用ImageMagick
        cmd = f'convert "{COVER_JPG}" -resize 2480x3508 -density 150 "{cover_pdf}"'
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ 封面PDF已创建: {cover_pdf.name}")
        return cover_pdf


def html_to_pdf(html_path, pdf_path):
    """将HTML转换为PDF"""
    html_abs = html_path.absolute()
    
    # 使用wkhtmltopdf
    cmd = [
        'wkhtmltopdf',
        '--enable-local-file-access',
        '--page-size', 'A4',
        '--orientation', 'Portrait',
        '--dpi', '150',
        '--image-quality', '85',
        '--no-stop-slow-scripts',
        '--javascript-delay', '1000',
        str(html_abs),
        str(pdf_path.absolute())
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"   ⚠️ wkhtmltopdf警告: {result.stderr[:200]}")
        # 仍然可能生成了文件
    
    return pdf_path.exists()


def merge_pdfs(pdf_list, output_path):
    """合并多个PDF文件"""
    if not pdf_list:
        print("❌ 没有PDF文件可合并")
        return False
    
    # 使用PyPDF2或pypdf合并
    try:
        from pypdf import PdfMerger
        merger = PdfMerger()
        
        for pdf in pdf_list:
            if pdf.exists():
                merger.append(str(pdf))
        
        merger.write(str(output_path))
        merger.close()
        print(f"✅ PDF合并完成: {output_path.name}")
        return True
    except ImportError:
        try:
            from PyPDF2 import PdfMerger
            merger = PdfMerger()
            
            for pdf in pdf_list:
                if pdf.exists():
                    merger.append(str(pdf))
            
            merger.write(str(output_path))
            merger.close()
            print(f"✅ PDF合并完成: {output_path.name}")
            return True
        except ImportError:
            print("❌ 需要安装PyPDF2或pypdf: pip install pypdf")
            return False


def main():
    print("="*60)
    print("开始生成完整PDF")
    print("="*60)
    
    # 1. 创建封面PDF
    print("\n📄 步骤1: 创建封面PDF...")
    cover_pdf = create_cover_pdf()
    
    # 2. 转换每个HTML章节为PDF
    print("\n📄 步骤2: 转换HTML章节为PDF...")
    chapter_pdfs = []
    
    for i, chapter_file in enumerate(CHAPTER_FILES, 1):
        html_path = CHAPTERS_DIR / chapter_file
        pdf_path = OUTPUT_DIR / f"chapter_{i:02d}.pdf"
        
        if not html_path.exists():
            print(f"   ⚠️ 跳过不存在的文件: {chapter_file}")
            continue
        
        print(f"   转换 {chapter_file}...")
        if html_to_pdf(html_path, pdf_path):
            chapter_pdfs.append(pdf_path)
            print(f"      ✅ {pdf_path.name}")
        else:
            print(f"      ❌ 转换失败")
    
    # 3. 合并所有PDF
    print("\n📄 步骤3: 合并所有PDF...")
    final_pdf = OUTPUT_DIR / "和古人一起想问题_移动端优化版.pdf"
    
    all_pdfs = [cover_pdf] + chapter_pdfs
    if merge_pdfs(all_pdfs, final_pdf):
        # 检查文件大小
        size_mb = final_pdf.stat().st_size / (1024 * 1024)
        print(f"\n📊 最终PDF大小: {size_mb:.2f} MB")
        
        if size_mb > 10:
            print("⚠️ 警告: 文件大小超过10MB")
        else:
            print("✅ 文件大小符合要求（<10MB）")
        
        # 清理临时文件
        print("\n🧹 清理临时文件...")
        for pdf in chapter_pdfs:
            try:
                pdf.unlink()
                print(f"   已删除: {pdf.name}")
            except:
                pass
        
        try:
            cover_pdf.unlink()
            print(f"   已删除: {cover_pdf.name}")
        except:
            pass
        
        print(f"\n🎉 完成！PDF保存在: {final_pdf}")
    else:
        print("❌ PDF合并失败")


if __name__ == "__main__":
    main()
