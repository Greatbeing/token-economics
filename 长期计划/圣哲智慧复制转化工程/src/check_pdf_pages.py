#!/usr/bin/env python3
import PyPDF2
import sys

pdf_path = sys.argv[1] if len(sys.argv) > 1 else "outputs/儿童哲学史/最终交付/儿童版中国哲学史_A4完整版.pdf"

reader = PyPDF2.PdfReader(pdf_path)
total_pages = len(reader.pages)

# 检查几个关键页码的内容
check_pages = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 17, 18, 22, 23, 28, 29, 34, 35, 44, 45, 50, 51, 56, 57, 62, 63, 68, 69]

for page_num in check_pages:
    if page_num < total_pages:
        page = reader.pages[page_num]
        text = page.extract_text()
        preview = text[:200].replace('\n', ' ').strip()
        print(f"第 {page_num+1} 页: {preview}")
        if page_num in [3, 8, 13, 17, 22, 28, 34, 44, 50, 56, 62, 68]:
            print(f"--- 检查章节开始页 {page_num+1} ---")