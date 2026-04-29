#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查看实践练习部分内容"""

import re

def extract_section(content, section_title):
    """提取指定章节内容"""
    # 构建正则表达式
    pattern = rf'^## {re.escape(section_title)}.*?(?=^## |^# |\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        return match.group(0)
    else:
        # 尝试另一种模式
        pattern = rf'^## .*{re.escape(section_title)}.*?(?=^## |^# |\Z)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        return match.group(0) if match else None

def main():
    file_path = "outputs/儿童哲学史/优化阶段/第六章优化稿.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取实践练习部分
    practice_section = extract_section(content, "实践练习：三周心灵训练计划（可操作版）")
    
    if practice_section:
        print("=== 实践练习部分内容 ===")
        print(practice_section[:1000])  # 显示前1000字符
        
        # 统计字数
        pattern = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
        chinese_chars = pattern.findall(practice_section)
        print(f"\n该部分中文字数: {len(chinese_chars)}字")
        
        # 分析结构
        lines = practice_section.split('\n')
        print(f"行数: {len(lines)}")
        
        # 显示标题结构
        print("\n=== 子标题结构 ===")
        for line in lines:
            if line.startswith('###'):
                print(line)
    else:
        print("未找到实践练习部分")

if __name__ == "__main__":
    main()