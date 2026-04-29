#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查文字内容完整性脚本
统计12章优化稿的总字数，检查文件完整性
"""

import os
import sys
import re

def count_chinese_characters(text):
    """统计中文字符数（粗略估算）"""
    # 汉字、标点、数字、英文字母都计入
    # 去除空白字符
    cleaned = re.sub(r'\s+', '', text)
    return len(cleaned)

def count_words_markdown(text):
    """更精确的统计：中文字符+英文单词"""
    # 中文字符
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 英文单词（按空格分割）
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    # 数字
    numbers = len(re.findall(r'\d+', text))
    # 总字符数（不含空白）
    total_chars = len(re.sub(r'\s+', '', text))
    
    return {
        'chinese_chars': chinese_chars,
        'english_words': english_words,
        'numbers': numbers,
        'total_chars': total_chars,
        'text_length': len(text)
    }

def check_chapter_files():
    """检查所有章节文件"""
    base_dir = "outputs/儿童哲学史/优化阶段"
    
    # 预期的章节文件
    expected_chapters = []
    for i in range(1, 13):
        chapter_num = i
        if i <= 10:
            filename = f"第{chapter_num}章优化稿.md"
        else:
            filename = f"第{chapter_num}章优化稿.md"
        expected_chapters.append(filename)
    
    print("=" * 60)
    print("文字内容完整性检查")
    print("=" * 60)
    
    # 检查每个文件
    chapter_stats = []
    total_stats = {
        'chinese_chars': 0,
        'english_words': 0,
        'numbers': 0,
        'total_chars': 0,
        'text_length': 0,
        'file_count': 0
    }
    
    missing_files = []
    
    for chapter_file in expected_chapters:
        file_path = os.path.join(base_dir, chapter_file)
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                stats = count_words_markdown(content)
                file_size = os.path.getsize(file_path)
                
                chapter_stats.append({
                    'file': chapter_file,
                    'path': file_path,
                    'stats': stats,
                    'file_size': file_size,
                    'status': '正常'
                })
                
                # 累加总统计
                for key in stats:
                    if key in total_stats:
                        total_stats[key] += stats[key]
                total_stats['file_count'] += 1
                
                print(f"✓ {chapter_file:20} | 中文字符: {stats['chinese_chars']:6} | 文件大小: {file_size:6}字节 | 状态: 正常")
                
            except Exception as e:
                print(f"✗ {chapter_file:20} | 错误: {str(e):30} | 状态: 损坏")
                missing_files.append(chapter_file)
        else:
            print(f"✗ {chapter_file:20} | 文件不存在{'':26} | 状态: 缺失")
            missing_files.append(chapter_file)
    
    print("\n" + "=" * 60)
    print("统计汇总")
    print("=" * 60)
    
    # 估算总字数（中文字符 + 英文单词*0.5）
    estimated_words = total_stats['chinese_chars'] + total_stats['english_words'] * 0.5
    
    print(f"文件数量: {total_stats['file_count']}/12")
    print(f"缺失文件: {len(missing_files)}个")
    if missing_files:
        print(f"缺失列表: {', '.join(missing_files)}")
    
    print(f"\n文字统计:")
    print(f"  中文字符数: {total_stats['chinese_chars']:,}")
    print(f"  英文单词数: {total_stats['english_words']:,}")
    print(f"  数字数量: {total_stats['numbers']:,}")
    print(f"  总字符数: {total_stats['total_chars']:,}")
    print(f"  文本长度: {total_stats['text_length']:,}")
    
    print(f"\n估算总字数: {estimated_words:,.0f}字")
    print(f"  注: 估算公式 = 中文字符数 + 英文单词数 × 0.5")
    
    # 检查哲学儿童词典
    dict_file = os.path.join(base_dir, "哲学儿童词典.md")
    if os.path.exists(dict_file):
        with open(dict_file, 'r', encoding='utf-8') as f:
            dict_content = f.read()
        dict_stats = count_words_markdown(dict_content)
        dict_size = os.path.getsize(dict_file)
        print(f"\n哲学儿童词典:")
        print(f"  文件大小: {dict_size:,}字节")
        print(f"  中文字符: {dict_stats['chinese_chars']:,}")
    
    # 检查backup_practice目录
    backup_dir = os.path.join(base_dir, "backup_practice")
    if os.path.exists(backup_dir):
        backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.md')]
        print(f"\n备份文件: {len(backup_files)}个（在backup_practice目录中）")
    
    print("\n" + "=" * 60)
    
    # 返回结果
    return {
        'chapter_stats': chapter_stats,
        'total_stats': total_stats,
        'missing_files': missing_files,
        'estimated_words': estimated_words,
        'all_present': len(missing_files) == 0
    }

if __name__ == "__main__":
    result = check_chapter_files()
    
    # 输出简要结果用于报告
    print("\n简要结果:")
    print(f"章节完整性: {'✓ 完整' if result['all_present'] else '✗ 不完整'}")
    print(f"估算总字数: {result['estimated_words']:,.0f}字")
    
    # 退出码
    sys.exit(0 if result['all_present'] else 1)