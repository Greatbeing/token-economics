#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查看哲学漫画脚本内容"""

import re

def extract_section(content, section_title):
    """提取指定章节内容"""
    # 构建正则表达式
    pattern = rf'^## {re.escape(section_title)}.*?(?=^## |^# |\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        return match.group(0)
    else:
        return None

def main():
    file_path = "outputs/儿童哲学史/优化阶段/第六章优化稿.md"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取哲学漫画脚本
        comic_section = extract_section(content, "哲学漫画脚本：怕的变形记")
        
        if comic_section:
            print("=== 哲学漫画脚本内容 ===")
            print(comic_section)
            
            # 统计字数
            import temp.analyze_ch6_structure as analyzer
            chinese_count = analyzer.count_chinese_chars(comic_section)
            print(f"\n该部分中文字数: {chinese_count}")
            
            # 查看具体结构
            lines = comic_section.split('\n')
            print(f"\n行数: {len(lines)}")
            
            # 显示前100行
            print("\n=== 前100行 ===")
            for i, line in enumerate(lines[:100]):
                if line.strip():
                    print(f"{i+1}: {line}")
        else:
            print("未找到哲学漫画脚本部分")
            
        # 提取实践练习部分
        practice_section = extract_section(content, "实践练习：三周心灵训练计划（可操作版）")
        
        if practice_section:
            print("\n\n=== 实践练习部分（前500字符）===")
            print(practice_section[:500])
            
            # 统计字数
            chinese_count = analyzer.count_chinese_chars(practice_section)
            print(f"\n该部分中文字数: {chinese_count}")
        
    except Exception as e:
        print(f"出错: {e}")

if __name__ == "__main__":
    main()