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
                if hasattr(item, 'title'):
                    title = item.title
                    # 获取页码
                    page_ref = item.page
                    # 找到页码索引
                    page_num = None
                    for i, page in enumerate(reader.pages):
                        if page.indirect_reference == page_ref:
                            page_num = i + 1  # 1-based
                            break
                    print(f"  标题: {title}, 页码: {page_num}")
                else:
                    print(f"  标题: {item}")
        else:
            print("PDF中没有书签")
except Exception as e:
    import traceback
    print(f"读取书签出错: {e}")
    traceback.print_exc()