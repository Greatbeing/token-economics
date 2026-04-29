#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
儿童版中国哲学史 - 移动端HTML批量优化脚本
将base64内嵌图片替换为外部WebP图片引用
添加移动端viewport和CSS支持
"""

import os
import re
import json
from pathlib import Path

# 路径配置
BASE_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史")
SOURCE_DIR = BASE_DIR / "排版阶段/章节HTML/修正版"
OUTPUT_DIR = BASE_DIR / "移动端适配/chapters_optimized"
CSS_SOURCE = BASE_DIR / "移动端优化/style_mobile.css"
CSS_DEST = OUTPUT_DIR / "style_mobile.css"
IMAGES_DIR = BASE_DIR / "移动端适配/optimized_images"

# 章节列表
CHAPTERS = [
    ("第1章样张_fixed.html", "ch1", "第1章"),
    ("第2章样张_fixed.html", "ch2", "第2章"),
    ("第3章样张_fixed.html", "ch3", "第3章"),
    ("第4章样张_fixed.html", "ch4", "第4章"),
    ("第5章样张_fixed.html", "ch5", "第5章"),
    ("第6章样张_fixed.html", "ch6", "第6章"),
    ("第7章样张_fixed.html", "ch7", "第7章"),
    ("第8章样张_fixed.html", "ch8", "第8章"),
    ("第9章样张_fixed.html", "ch9", "第9章"),
    ("第10章样张_fixed.html", "ch10", "第10章"),
    ("第11章样张_fixed.html", "ch11", "第11章"),
    ("第12章样张_fixed.html", "ch12", "第12章"),
]

# 创建输出目录
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 复制CSS文件到输出目录
if CSS_SOURCE.exists():
    with open(CSS_SOURCE, 'r', encoding='utf-8') as f:
        css_content = f.read()
    with open(CSS_DEST, 'w', encoding='utf-8') as f:
        f.write(css_content)
    print(f"✅ 已复制移动端CSS到 {CSS_DEST}")
else:
    print(f"⚠️ 警告: 找不到CSS文件 {CSS_SOURCE}")

def convert_base64_to_webp(html_content, chapter_prefix):
    """
    将base64内嵌图片转换为外部WebP引用
    同时处理多种图片格式
    """
    # 统计替换
    replacements = {
        'total': 0,
        'scene1': 0,
        'scene2': 0,
        'scene3': 0,
        'scene4': 0,
        'other': 0
    }
    
    # 匹配base64图片的pattern
    # HTML中格式: <img src="data:image/jpeg;base64,...> 或者 <img src="data:image/jpeg;base64,... />
    # 修复: 移除末尾的 \s*/ 要求，因为HTML中没有 />
    base64_pattern = r'<img\s+src="data:image/[^"]+;base64,[^"]+"'
    
    # 按顺序查找所有base64图片
    matches = list(re.finditer(base64_pattern, html_content))
    replacements['total'] = len(matches)
    
    print(f"   📊 找到 {len(matches)} 张base64图片")
    
    # 反向遍历，以便正确替换
    for i, match in enumerate(reversed(matches)):
        original = match.group(0)
        
        # 确定是第几张图片 (1-4)
        img_index = (i % 4) + 1
        scene_key = f'scene{img_index}'
        
        # 生成WebP图片引用
        new_src = f'<img src="../optimized_images/{chapter_prefix}_scene{img_index}.webp" alt="场景{img_index}" style="max-width: 100%; height: auto; display: block; margin: 1em auto;" />'
        
        # 替换
        html_content = html_content.replace(original, new_src, 1)
        replacements[scene_key] += 1
        print(f"   🔄 替换场景{img_index}: {chapter_prefix}_scene{img_index}.webp")
    
    return html_content, replacements

def add_mobile_meta(html_content):
    """添加/更新移动端viewport meta标签"""
    # 移除旧的viewport
    html_content = re.sub(
        r'<meta\s+name="viewport"[^>]*>',
        '',
        html_content
    )
    
    # 添加新的viewport meta标签
    mobile_viewport = '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=3.0, user-scalable=yes" />'
    
    # 在<head>标签后插入
    html_content = re.sub(
        r'(<head[^>]*>)',
        r'\1\n  ' + mobile_viewport,
        html_content,
        count=1
    )
    
    return html_content

def add_mobile_css_link(html_content):
    """添加移动端CSS链接"""
    mobile_css_link = '<link rel="stylesheet" href="style_mobile.css">'
    
    # 检查是否已有该链接
    if 'style_mobile.css' not in html_content:
        # 在</head>前插入
        html_content = html_content.replace(
            '</head>',
            '  ' + mobile_css_link + '\n</head>'
        )
    
    return html_content

def process_chapter(source_file, chapter_prefix, chapter_name):
    """处理单个章节HTML文件"""
    print(f"\n📖 处理 {chapter_name}...")
    
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_len = len(content)
    
    # 1. 添加移动端viewport
    content = add_mobile_meta(content)
    print(f"   ✅ 添加移动端viewport")
    
    # 2. 添加移动端CSS链接
    content = add_mobile_css_link(content)
    print(f"   ✅ 添加移动端CSS链接")
    
    # 3. 转换base64图片为WebP引用
    content, stats = convert_base64_to_webp(content, chapter_prefix)
    print(f"   ✅ 替换图片: {stats['total']}张")
    
    # 保存处理后的文件
    output_file = OUTPUT_DIR / f"{chapter_name}_mobile.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    new_len = len(content)
    print(f"   💾 保存到: {output_file}")
    print(f"   📊 文件大小: {original_len/1024:.1f}KB → {new_len/1024:.1f}KB")
    
    return stats

def main():
    """主函数：批量处理所有章节"""
    print("=" * 60)
    print("🎯 儿童版中国哲学史 - 移动端HTML批量优化")
    print("=" * 60)
    
    total_stats = {
        'total': 0,
        'scene1': 0,
        'scene2': 0,
        'scene3': 0,
        'scene4': 0,
        'other': 0,
        'chapters': 0
    }
    
    for source_file, chapter_prefix, chapter_name in CHAPTERS:
        source_path = SOURCE_DIR / source_file
        
        if not source_path.exists():
            print(f"⚠️ 跳过: {source_file} (文件不存在)")
            continue
        
        stats = process_chapter(source_path, chapter_prefix, chapter_name)
        total_stats['total'] += stats['total']
        total_stats['scene1'] += stats['scene1']
        total_stats['scene2'] += stats['scene2']
        total_stats['scene3'] += stats['scene3']
        total_stats['scene4'] += stats['scene4']
        total_stats['chapters'] += 1
    
    print("\n" + "=" * 60)
    print("📈 批量处理完成!")
    print(f"   ✅ 处理章节: {total_stats['chapters']}/12")
    print(f"   🔄 替换图片: {total_stats['total']}张")
    print(f"   - 场景1: {total_stats['scene1']}张")
    print(f"   - 场景2: {total_stats['scene2']}张")
    print(f"   - 场景3: {total_stats['scene3']}张")
    print(f"   - 场景4: {total_stats['scene4']}张")
    print(f"   📂 输出目录: {OUTPUT_DIR}")
    print("=" * 60)
    
    return total_stats

if __name__ == '__main__':
    main()
