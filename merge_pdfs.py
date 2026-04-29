#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
儿童版中国哲学史 - PDF合并脚本
使用PyPDF2合并所有章节PDF
"""

import os
import subprocess
from pathlib import Path
from PyPDF2 import PdfMerger

# 路径配置
BASE_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史")
OUTPUT_DIR = BASE_DIR / "移动端适配"
CHAPTERS_DIR = OUTPUT_DIR / "chapters_optimized"

# 章节列表（按顺序）
CHAPTERS = [
    ("封面", OUTPUT_DIR / "封面_移动端.html"),
    ("第1章", CHAPTERS_DIR / "第1章_mobile.html"),
    ("第2章", CHAPTERS_DIR / "第2章_mobile.html"),
    ("第3章", CHAPTERS_DIR / "第3章_mobile.html"),
    ("第4章", CHAPTERS_DIR / "第4章_mobile.html"),
    ("第5章", CHAPTERS_DIR / "第5章_mobile.html"),
    ("第6章", CHAPTERS_DIR / "第6章_mobile.html"),
    ("第7章", CHAPTERS_DIR / "第7章_mobile.html"),
    ("第8章", CHAPTERS_DIR / "第8章_mobile.html"),
    ("第9章", CHAPTERS_DIR / "第9章_mobile.html"),
    ("第10章", CHAPTERS_DIR / "第10章_mobile.html"),
    ("第11章", CHAPTERS_DIR / "第11章_mobile.html"),
    ("第12章", CHAPTERS_DIR / "第12章_mobile.html"),
]

def html_to_pdf(html_path, pdf_path):
    """使用wkhtmltopdf将HTML转换为PDF"""
    cmd = [
        'wkhtmltopdf',
        '--enable-local-file-access',
        '--print-media-type',
        '--no-stop-slow-scripts',
        '--enable-javascript',
        '--javascript-delay', '1000',
        '--page-size', 'A4',
        '--orientation', 'Portrait',
        '--margin-top', '20mm',
        '--margin-bottom', '20mm',
        '--margin-left', '15mm',
        '--margin-right', '15mm',
        '--image-quality', '90',
        str(html_path),
        str(pdf_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return result.returncode == 0
    except:
        return False

def main():
    print("=" * 60)
    print("📄 儿童版中国哲学史 - PDF合并")
    print("=" * 60)
    
    temp_pdfs = []
    
    print(f"\n📑 重新生成PDF文件...\n")
    
    for i, (name, html_path) in enumerate(CHAPTERS, 1):
        pdf_path = OUTPUT_DIR / f"temp_{name}.pdf"
        temp_pdfs.append(pdf_path)
        
        if pdf_path.exists():
            size = os.path.getsize(pdf_path) / 1024
            print(f"[{i}/{len(CHAPTERS)}] {name} PDF 已存在 ✅ ({size:.1f}KB)")
            continue
            
        print(f"[{i}/{len(CHAPTERS)}] 生成 {name} PDF...", end=" ")
        if html_to_pdf(html_path, pdf_path):
            size = os.path.getsize(pdf_path) / 1024
            print(f"✅ ({size:.1f}KB)")
        else:
            print(f"❌")
    
    # 合并PDF
    print("\n🔗 合并PDF文件...")
    final_pdf = OUTPUT_DIR / "和古人一起想问题_完整版_移动端.pdf"
    
    try:
        merger = PdfMerger()
        for pdf_path in temp_pdfs:
            if pdf_path.exists():
                merger.append(str(pdf_path))
        
        with open(final_pdf, 'wb') as output:
            merger.write(output)
        merger.close()
        
        if final_pdf.exists():
            final_size = os.path.getsize(final_pdf) / (1024 * 1024)
            print(f"\n✅ 最终PDF已生成:")
            print(f"   📄 {final_pdf}")
            print(f"   📊 大小: {final_size:.2f}MB")
    except Exception as e:
        print(f"❌ PDF合并失败: {e}")
    
    # 清理临时文件
    print("\n🧹 清理临时文件...")
    for pdf in temp_pdfs:
        try:
            os.remove(pdf)
        except:
            pass
    
    print("\n" + "=" * 60)
    print("🎉 全部完成!")
    print("=" * 60)

if __name__ == '__main__':
    main()
