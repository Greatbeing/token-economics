#!/usr/bin/env python3
"""
批量修复PDF - 生成完整的儿童哲学史PDF
修复乱码和图片比例问题
"""

import os
import re
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import shutil

def fix_html_for_pdf(html_file, css_file):
    """修复HTML文件的CSS引用"""
    
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换CSS引用为修复版
    if 'style.css' in content:
        content = content.replace('style.css', 'style_fixed.css')
    
    # 保存修复后的HTML
    fixed_html = html_file.replace('.html', '_pdf_fixed.html')
    with open(fixed_html, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return fixed_html


def generate_pdf(html_file, output_pdf):
    """使用wkhtmltopdf生成PDF"""
    
    html_path = os.path.abspath(html_file)
    output_path = os.path.abspath(output_pdf)
    
    cmd = [
        'wkhtmltopdf',
        '--enable-local-file-access',
        '--encoding', 'utf-8',
        '--page-size', 'A4',
        '--orientation', 'Portrait',
        '--no-stop-slow-scripts',
        '--javascript-delay', '3000',
        '--margin-top', '15mm',
        '--margin-bottom', '15mm',
        '--margin-left', '15mm',
        '--margin-right', '15mm',
        '--disable-smart-shrinking',
        html_path,
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            return True, os.path.getsize(output_path)
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)


def merge_pdfs(pdf_files, output_pdf):
    """合并多个PDF文件"""
    
    if len(pdf_files) == 1:
        shutil.copy(pdf_files[0], output_pdf)
        return True
    
    # 使用pdfunite合并
    cmd = ['pdfunite'] + pdf_files + [output_pdf]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        # 尝试使用Python合并
        try:
            from PyPDF2 import PdfMerger
            merger = PdfMerger()
            for pdf in pdf_files:
                merger.append(pdf)
            merger.write(output_pdf)
            merger.close()
            return True
        except:
            return False


def main():
    # 设置路径
    base_dir = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史")
    html_dir = base_dir / "排版阶段/章节HTML/修正版"
    output_dir = base_dir / "最终交付/章节PDF_修复版"
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 获取所有章节HTML文件
    chapters = []
    for i in range(1, 13):
        chapter_file = html_dir / f"第{i}章样张_fixed.html"
        if chapter_file.exists():
            chapters.append(chapter_file)
    
    print(f"找到 {len(chapters)} 个章节文件")
    print("=" * 50)
    
    # 修复并生成PDF
    chapter_pdfs = []
    
    for chapter_file in chapters:
        print(f"\n处理: {chapter_file.name}")
        
        # 修复HTML
        fixed_html = fix_html_for_pdf(str(chapter_file), "")
        
        # 生成PDF
        output_pdf = output_dir / f"{chapter_file.stem.replace('_fixed', '')}_修复版.pdf"
        success, result = generate_pdf(fixed_html, str(output_pdf))
        
        if success:
            size_mb = result / 1024 / 1024
            print(f"  ✅ 生成成功 ({size_mb:.2f} MB)")
            chapter_pdfs.append(str(output_pdf))
        else:
            print(f"  ❌ 生成失败: {result[:100]}")
    
    # 合并所有章节PDF
    print("\n" + "=" * 50)
    print("正在合并所有章节PDF...")
    
    final_pdf = base_dir / "最终交付" / "和古人一起想问题_完整版_修复版.pdf"
    success = merge_pdfs(chapter_pdfs, str(final_pdf))
    
    if success:
        final_size = os.path.getsize(final_pdf) / 1024 / 1024
        print(f"\n✅ 完整版PDF已生成!")
        print(f"   文件: {final_pdf}")
        print(f"   大小: {final_size:.2f} MB")
        print(f"   章节数: {len(chapter_pdfs)}")
    else:
        print("❌ 合并失败!")


if __name__ == "__main__":
    main()
