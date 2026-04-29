#!/usr/bin/env python3
import PyPDF2
import sys

pdf_path = sys.argv[1] if len(sys.argv) > 1 else 'outputs/儿童哲学史/最终交付/儿童版中国哲学史.pdf'

try:
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        if reader.outline:
            print("书签列表:")
            for item in reader.outline:
                if isinstance(item, PyPDF2.generic.Destination):
                    print(f"  标题: {item.title}, 页码: {item.page.page_number}")
                else:
                    print(f"  标题: {item}")
        else:
            print("PDF中没有书签")
except Exception as e:
    print(f"读取书签出错: {e}")
    sys.exit(1)