#!/usr/bin/env python3
"""批量修复HTML文件中的图片引用问题"""

import re
import os
from pathlib import Path

# 源目录和输出目录
SOURCE_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/修正版")
OUTPUT_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/移动端适配/chapters_optimized")
CSS_FILE = "style_mobile.css"
OPTIMIZED_IMAGES_DIR = "../optimized_images"

def fix_image_tags(content):
    """修复图片标签中的重复alt属性问题"""
    # 匹配形如: <img src="..." alt="场景X" style="..." /> alt="..." />
    # 修复为: <img src="..." alt="场景X" style="..." />
    fixed = re.sub(
        r'(<img\s+src="[^"]*"\s+alt="([^"]*)"[^>]*)\s*/>\s*alt="[^"]*"\s*/>',
        r'\1 />',
        content
    )
    # 另一种匹配: <img .../> alt="..."/>
    fixed = re.sub(
        r'(<img[^>]*>)\s*alt="[^"]*"\s*/?>',
        r'\1',
        fixed
    )
    return fixed

def process_chapter(input_file, output_file, chapter_num, chapter_title):
    """处理单个章节HTML"""
    print(f"处理: 第{chapter_num}章...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 修复图片标签问题
    content = fix_image_tags(content)
    
    # 2. 确保viewport元标签存在
    if 'viewport' not in content:
        content = content.replace(
            '<meta name="generator" content="pandoc" />',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=3.0, user-scalable=yes" />\n  <meta name="generator" content="pandoc" />'
        )
    else:
        # 更新viewport为更好的移动端设置
        content = re.sub(
            r'<meta\s+name="viewport"[^>]*/?>',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=3.0, user-scalable=yes" />',
            content
        )
    
    # 3. 更新标题
    content = re.sub(
        r'<title>[^<]*</title>',
        f'<title>和古人一起想问题——第一章：{chapter_title}</title>',
        content
    )
    
    # 4. 确保链接正确的CSS
    if f'link rel="stylesheet" href="{CSS_FILE}"' not in content:
        content = re.sub(
            r'<link\s+rel="stylesheet"\s+href="[^"]*">',
            f'<link rel="stylesheet" href="{CSS_FILE}">',
            content
        )
        # 如果没有CSS链接，添加它
        if CSS_FILE not in content:
            content = content.replace(
                '<link rel="stylesheet" href="style_fixed.css">',
                f'<link rel="stylesheet" href="style_fixed.css">\n  <link rel="stylesheet" href="{CSS_FILE}">'
            )
    
    # 5. 替换base64图片为WebP引用
    # 匹配base64图片
    base64_pattern = r'<img\s+src="data:image/[^"]+;base64,[^"]+"([^>]*)>'
    
    def replace_base64(match):
        attrs = match.group(1)
        # 提取或生成alt文本
        alt_match = re.search(r'alt="([^"]*)"', attrs)
        alt_text = alt_match.group(1) if alt_match else "场景插图"
        # 保持style属性
        style_match = re.search(r'style="([^"]*)"', attrs)
        style = style_match.group(1) if style_match else "max-width: 100%; height: auto;"
        # 清理alt中的base64名称
        alt_text = re.sub(r'\.jpg$|\.jpeg$|\.png$|\.webp$', '', alt_text)
        return f'<img src="{OPTIMIZED_IMAGES_DIR}/{chapter_num}_scene1.webp" alt="{alt_text}" style="{style}" />'
    
    content = re.sub(base64_pattern, replace_base64, content)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 计算大小
    original_size = os.path.getsize(input_file) / 1024
    new_size = os.path.getsize(output_file) / 1024
    print(f"  {original_size:.1f}KB → {new_size:.1f}KB")
    
    return new_size

def main():
    # 12章配置
    chapters = [
        (1, "世界是从哪儿来的？"),
        (2, "“道”是什么？"),
        (3, "人人都是“仁者”？"),
        (4, "我是谁？"),
        (5, "知识从哪儿来？"),
        (6, "幸福是什么？"),
        (7, "正义是什么？"),
        (8, "美是什么？"),
        (9, "什么是真正的自由？"),
        (10, "理想社会是什么样？"),
        (11, "怎样说话才算对？"),
        (12, "古人的智慧，今天怎么用？"),
    ]
    
    total_size = 0
    for num, title in chapters:
        input_file = SOURCE_DIR / f"第{num}章样张_fixed_pdf_fixed.html"
        output_file = OUTPUT_DIR / f"第{num}章_mobile.html"
        
        if input_file.exists():
            size = process_chapter(input_file, output_file, num, title)
            total_size += size
        else:
            print(f"⚠️  找不到: {input_file}")
    
    print(f"\n完成！总大小: {total_size:.1f}KB")

if __name__ == "__main__":
    main()
