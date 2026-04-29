#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查找哲学漫画脚本部分的精确内容"""

import re

def extract_comic_section(content):
    """提取哲学漫画脚本部分"""
    # 查找从"## 哲学漫画脚本：怕的变形记"到下一个"## "或文件结束的内容
    pattern = r'(## 哲学漫画脚本：怕的变形记.*?)(?=^## |\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        return match.group(1)
    return None

def main():
    file_path = "outputs/儿童哲学史/优化阶段/第六章优化稿.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    comic_section = extract_comic_section(content)
    
    if comic_section:
        print("=== 找到哲学漫画脚本部分 ===")
        print(f"部分长度: {len(comic_section)}字符")
        print(f"部分内容前500字符:\n{comic_section[:500]}")
        
        # 保存到文件以便查看
        with open("temp/comic_original_exact.txt", "w", encoding="utf-8") as f:
            f.write(comic_section)
        print("\n已保存到 temp/comic_original_exact.txt")
        
        # 统计字数
        pattern = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
        chinese_chars = pattern.findall(comic_section)
        print(f"中文字数: {len(chinese_chars)}字")
        
        return comic_section
    else:
        print("未找到哲学漫画脚本部分")
        return None

if __name__ == "__main__":
    main()