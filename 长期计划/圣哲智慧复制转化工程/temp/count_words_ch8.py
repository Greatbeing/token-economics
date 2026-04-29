#!/usr/bin/env python3
import re

def count_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 统计汉字数量（中文字符）
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
    chinese_count = len(chinese_chars)
    
    # 估算总字数（汉字数 + 标点等）
    # 简单估算：汉字数 * 1.2
    estimated_words = int(chinese_count * 1.2)
    
    print(f"汉字数量: {chinese_count}")
    print(f"估算字数: {estimated_words}")
    return estimated_words

if __name__ == '__main__':
    count_words('outputs/儿童哲学史/优化阶段/第八章优化稿.md')