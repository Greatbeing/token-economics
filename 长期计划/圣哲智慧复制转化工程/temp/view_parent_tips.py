#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查看给家长的提示部分内容"""

import re

def extract_section(content, section_title):
    """提取指定章节内容"""
    pattern = rf'^## {re.escape(section_title)}.*?(?=^## |^# |\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return match.group(0) if match else None

def main():
    file_path = "outputs/儿童哲学史/优化阶段/第六章优化稿.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取给家长的提示部分
    tips_section = extract_section(content, "给家长的提示：如何做孩子的心灵探险伙伴")
    
    if tips_section:
        print("=== 给家长的提示部分内容 ===")
        print(tips_section)
        
        # 统计字数
        pattern = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
        chinese_chars = pattern.findall(tips_section)
        print(f"\n该部分中文字数: {len(chinese_chars)}字")
    else:
        print("未找到给家长的提示部分")

if __name__ == "__main__":
    main()