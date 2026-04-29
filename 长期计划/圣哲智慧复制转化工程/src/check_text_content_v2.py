#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查文字内容完整性脚本（版本2）
统计12章优化稿的总字数，检查文件完整性
使用实际文件名
"""

import os
import sys
import re
import json

def count_chinese_characters(text):
    """统计中文字符数"""
    # 汉字
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 标点符号（中文标点）
    chinese_punctuation = len(re.findall(r'[，。！？；："'（）《》【】]', text))
    # 英文单词
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    # 数字
    numbers = len(re.findall(r'\d+', text))
    # 总非空白字符
    total_chars = len(re.sub(r'\s+', '', text))
    # 原始文本长度
    text_length = len(text)
    
    return {
        'chinese_chars': chinese_chars,
        'chinese_punctuation': chinese_punctuation,
        'english_words': english_words,
        'numbers': numbers,
        'total_chars': total_chars,
        'text_length': text_length
    }

def check_chapter_files():
    """检查所有章节文件"""
    base_dir = "outputs/儿童哲学史/优化阶段"
    
    # 实际章节文件（根据ls输出）
    chapter_files = [
        "第一章优化稿.md",
        "第二章优化稿.md", 
        "第三章优化稿.md",
        "第四章优化稿.md",
        "第五章优化稿.md",
        "第六章优化稿.md",
        "第七章优化稿.md",
        "第八章优化稿.md",
        "第九章优化稿.md",
        "第十章优化稿.md",
        "第十一章优化稿.md",
        "第十二章优化稿.md"
    ]
    
    print("=" * 70)
    print("《儿童版中国哲学史》文字内容完整性检查")
    print("=" * 70)
    
    chapter_stats = []
    total_stats = {
        'chinese_chars': 0,
        'chinese_punctuation': 0,
        'english_words': 0,
        'numbers': 0,
        'total_chars': 0,
        'text_length': 0,
        'file_count': 0,
        'total_file_size': 0
    }
    
    missing_files = []
    
    for chapter_file in chapter_files:
        file_path = os.path.join(base_dir, chapter_file)
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                stats = count_chinese_characters(content)
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
                total_stats['total_file_size'] += file_size
                
                # 显示检查结果
                print(f"✓ {chapter_file:20} | 大小: {file_size:6,}字节 | 汉字: {stats['chinese_chars']:5,} | 状态: 正常")
                
            except Exception as e:
                print(f"✗ {chapter_file:20} | 错误: {str(e):30} | 状态: 损坏")
                missing_files.append(chapter_file)
        else:
            print(f"✗ {chapter_file:20} | 文件不存在{'':26} | 状态: 缺失")
            missing_files.append(chapter_file)
    
    print("\n" + "=" * 70)
    print("统计汇总")
    print("=" * 70)
    
    # 估算总字数（中文字符 + 英文单词*0.5 + 标点*0.2）
    estimated_words = total_stats['chinese_chars'] + total_stats['english_words'] * 0.5
    
    print(f"文件数量: {total_stats['file_count']}/12")
    print(f"缺失文件: {len(missing_files)}个")
    if missing_files:
        print(f"缺失列表: {', '.join(missing_files)}")
    
    print(f"\n详细统计:")
    print(f"  中文字符数: {total_stats['chinese_chars']:,}")
    print(f"  中文标点数: {total_stats['chinese_punctuation']:,}")
    print(f"  英文单词数: {total_stats['english_words']:,}")
    print(f"  数字数量: {total_stats['numbers']:,}")
    print(f"  总字符数: {total_stats['total_chars']:,}")
    print(f"  文本长度: {total_stats['text_length']:,}")
    print(f"  总文件大小: {total_stats['total_file_size']:,}字节")
    
    print(f"\n估算总字数: {estimated_words:,.0f}字")
    print(f"  注: 估算公式 = 中文字符数 + 英文单词数 × 0.5")
    
    # 检查是否符合7万字预估
    if estimated_words >= 65000 and estimated_words <= 75000:
        print(f"  状态: ✓ 符合7万字左右预估")
    else:
        print(f"  状态: ⚠ 偏离7万字预估（偏差较大）")
    
    # 检查哲学儿童词典
    dict_file = os.path.join(base_dir, "哲学儿童词典.md")
    if os.path.exists(dict_file):
        with open(dict_file, 'r', encoding='utf-8') as f:
            dict_content = f.read()
        dict_stats = count_chinese_characters(dict_content)
        dict_size = os.path.getsize(dict_file)
        print(f"\n哲学儿童词典:")
        print(f"  文件大小: {dict_size:,}字节")
        print(f"  中文字符: {dict_stats['chinese_chars']:,}")
        print(f"  英文单词: {dict_stats['english_words']:,}")
    
    # 检查backup_practice目录
    backup_dir = os.path.join(base_dir, "backup_practice")
    if os.path.exists(backup_dir):
        backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.md')]
        print(f"\n备份文件: {len(backup_files)}个（在backup_practice目录中）")
        if backup_files:
            print(f"  备份列表: {', '.join(sorted(backup_files)[:5])}" + 
                  ("..." if len(backup_files) > 5 else ""))
    
    print("\n" + "=" * 70)
    
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
    
    # 输出JSON格式结果用于报告
    result_json = {
        'status': 'complete' if result['all_present'] else 'incomplete',
        'file_count': result['total_stats']['file_count'],
        'estimated_words': result['estimated_words'],
        'total_file_size': result['total_stats']['total_file_size']
    }
    
    print("\nJSON结果:")
    print(json.dumps(result_json, ensure_ascii=False, indent=2))
    
    # 退出码
    sys.exit(0 if result['all_present'] else 1)