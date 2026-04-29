#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统计第六章优化稿的字数（中文字符数）"""

import re

def count_chinese_chars(text):
    """统计中文字符数，中文标点也算"""
    # 匹配中文字符，包括中文标点
    pattern = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
    chinese_chars = pattern.findall(text)
    return len(chinese_chars)

def main():
    file_path = "outputs/儿童哲学史/优化阶段/第六章优化稿.md"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        total_chars = len(content)
        chinese_count = count_chinese_chars(content)
        
        print(f"文件总字符数: {total_chars}")
        print(f"中文字符数: {chinese_count}")
        
        # 检查是否超过7000字
        if chinese_count > 7000:
            print(f"⚠️ 章节篇幅超过7000字（当前{chinese_count}字），需要精简")
            print(f"需要精简的字数: {chinese_count - 7000}")
        else:
            print(f"✅ 章节篇幅在7000字以内（当前{chinese_count}字）")
            
        return chinese_count
        
    except Exception as e:
        print(f"读取文件出错: {e}")
        return None

if __name__ == "__main__":
    main()