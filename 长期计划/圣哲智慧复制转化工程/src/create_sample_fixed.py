#!/usr/bin/env python3
"""
创建修正版PDF示例（封面+第一章）
"""

import subprocess
from pathlib import Path
import PyPDF2

BASE_DIR = Path.cwd()

# 输入文件
COVER_HTML = BASE_DIR / "outputs/儿童哲学史/最终交付/cover_simple.html"
CHAPTER_HTML = BASE_DIR / "outputs/儿童哲学史/排版阶段/章节HTML/修正版/第1章样张_fixed.html"
TOC_HTML = BASE_DIR / "outputs/儿童哲学史/最终交付/目录页_完整版.html"

# 输出目录
OUTPUT_DIR = BASE_DIR / "outputs/儿童哲学史/最终交付/示例"
OUTPUT_DIR.mkdir(exist_ok=True)

def create_pdf_from_html(html_file, pdf_file, options=None):
    """从HTML创建PDF"""
    cmd = [
        'wkhtmltopdf',
        '--page-size', 'A4',
        '--margin-top', '20mm',
        '--margin-right', '20mm',
        '--margin-bottom', '20mm',
        '--margin-left', '20mm',
        '--disable-local-file-access',
        str(html_file),
        str(pdf_file)
    ]
    
    if options:
        cmd.extend(options)
    
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0

def main():
    print("创建修正版PDF示例...")
    
    # 1. 创建封面
    cover_pdf = OUTPUT_DIR / "cover.pdf"
    print("1. 生成封面...")
    if create_pdf_from_html(COVER_HTML, cover_pdf, ['--margin-top', '0', '--margin-right', '0', '--margin-bottom', '0', '--margin-left', '0']):
        print("  ✓ 封面生成成功")
    else:
        print("  ✗ 封面生成失败")
        return
    
    # 2. 创建目录页
    toc_pdf = OUTPUT_DIR / "toc.pdf"
    print("2. 生成目录页...")
    if create_pdf_from_html(TOC_HTML, toc_pdf):
        print("  ✓ 目录页生成成功")
    else:
        print("  ✗ 目录页生成失败")
        return
    
    # 3. 创建第一章
    chapter_pdf = OUTPUT_DIR / "chapter_1.pdf"
    print("3. 生成第一章...")
    if create_pdf_from_html(CHAPTER_HTML, chapter_pdf):
        print("  ✓ 第一章生成成功")
    else:
        print("  ✗ 第一章生成失败")
        return
    
    # 4. 合并PDF
    print("4. 合并PDF文件...")
    merger = PyPDF2.PdfMerger()
    
    for pdf_file in [cover_pdf, toc_pdf, chapter_pdf]:
        if pdf_file.exists():
            merger.append(str(pdf_file))
    
    final_pdf = OUTPUT_DIR / "儿童版中国哲学史_修正示例.pdf"
    merger.write(str(final_pdf))
    merger.close()
    
    print(f"\n✓ 示例PDF已生成: {final_pdf}")
    
    # 显示文件信息
    if final_pdf.exists():
        size = final_pdf.stat().st_size
        print(f"文件大小: {size:,} 字节")
        
        # 检查页面数
        cmd = ['pdfinfo', str(final_pdf)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Pages:'):
                    print(f"总页数: {line.split(':')[1].strip()}")
                    break
    
    print("\n修正内容总结:")
    print("1. 排版清晰度优化:")
    print("   - 对话内容独立成行，添加左侧边框和间距")
    print("   - 段落之间增加底部边距")
    print("   - 小标题增加上下边距")
    print("2. 封面设计修正:")
    print("   - 添加完整书名和副标题")
    print("   - 使用渐变背景确保可读性")
    print("3. 文件位置:")
    print(f"   - 封面: {cover_pdf}")
    print(f"   - 目录页: {toc_pdf}")
    print(f"   - 第一章: {chapter_pdf}")
    print(f"   - 合并版: {final_pdf}")

if __name__ == '__main__':
    main()