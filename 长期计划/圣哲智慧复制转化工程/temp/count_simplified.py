#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统计简化版本的字数"""

import re

def count_chinese_chars(text):
    """统计中文字符数"""
    pattern = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
    chinese_chars = pattern.findall(text)
    return len(chinese_chars)

# 读取简化版本
with open("temp/comic_script_simplified.md", "r", encoding="utf-8") as f:
    simplified_content = f.read()

simplified_count = count_chinese_chars(simplified_content)
print(f"简化版本中文字数: {simplified_count}字")

# 原始版本字数（根据之前统计）
original_comic_count = 1593
print(f"原始版本中文字数: {original_comic_count}字")
print(f"精简了: {original_comic_count - simplified_count}字")