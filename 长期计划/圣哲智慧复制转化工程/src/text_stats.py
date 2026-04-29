#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计文字内容
"""

import os
import sys
import re

def count_text(text):
    """统计文本"""
    # 汉字
    chinese = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 英文单词
    english = len(re.findall(r'[a-zA-Z]+', text))
    # 总非空白字符
    total_chars = len(re.sub(r'\s+', '', text))
    # 原始长度
    raw_len = len(text)
    
    return {
        'chinese': chinese,
        'english': english,
        'total_chars': total_chars,
        'raw_len': raw_len
    }

def main():
    base = "outputs/儿童哲学史/优化阶段"
    files = [
        "第一章优化稿.md", "第二章优化稿.md", "第三章优化稿.md",
        "第四章优化稿.md", "第五章优化稿.md", "第六章优化稿.md",
        "第七章优化稿.md", "第八章优化稿.md", "第九章优化稿.md",
        "第十章优化稿.md", "第十一章优化稿.md", "第十二章优化稿.md"
    ]
    
    print("检查文字内容...")
    print("=" * 60)
    
    stats_list = []
    total_chinese = 0
    total_english = 0
    total_size = 0
    
    for fname in files:
        path = os.path.join(base, fname)
        if not os.path.exists(path):
            print(f"缺失: {fname}")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        size = os.path.getsize(path)
        stats = count_text(text)
        
        stats_list.append({
            'file': fname,
            'size': size,
            'stats': stats
        })
        
        total_chinese += stats['chinese']
        total_english += stats['english']
        total_size += size
        
        print(f"{fname:20} | 大小: {size:6,} | 汉字: {stats['chinese']:5,} | 英文词: {stats['english']:3,}")
    
    print("=" * 60)
    print(f"总文件数: {len(stats_list)}/12")
    print(f"总汉字数: {total_chinese:,}")
    print(f"总英文词数: {total_english:,}")
    print(f"总文件大小: {total_size:,}字节")
    
    # 估算总字数
    estimated = total_chinese + total_english * 0.5
    print(f"估算总字数: {estimated:,.0f}")
    
    # 检查完整性
    if len(stats_list) == 12:
        print("状态: ✓ 所有章节完整")
        sys.exit(0)
    else:
        print(f"状态: ✗ 缺失 {12 - len(stats_list)} 个章节")
        sys.exit(1)

if __name__ == "__main__":
    main()