#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将优化后的WebP图片嵌入清理后的HTML，生成带插图的完整PDF
"""

import os
import re
import base64
from pathlib import Path

# 路径配置
BASE_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史")
IMAGES_DIR = BASE_DIR / "移动端适配/optimized_images"
CHAPTERS_DIR = BASE_DIR / "移动端适配/chapters_clean"
ORIG_HTML_DIR = BASE_DIR / "排版阶段/章节HTML/修正版"
OUTPUT_HTML = CHAPTERS_DIR / "merged_with_images.html"
OUTPUT_PDF = BASE_DIR / "最终交付/和古人一起想问题_移动端优化版.pdf"

# 章节映射：clean文件名 -> 原始HTML文件名（用于获取图片位置）
CHAPTER_MAP = {
    "ch1_clean.html": "第1章样张_fixed.html",
    "ch2_clean.html": "第2章样张_fixed.html",
    "ch3_clean.html": "第3章样张_fixed.html",
    "ch4_clean.html": "第4章样张_fixed.html",
    "ch5_clean.html": "第5章样张_fixed.html",
    "ch6_clean.html": "第6章样张_fixed.html",
    "ch7_clean.html": "第7章样张_fixed.html",
    "ch8_clean.html": "第8章样张_fixed.html",
    "ch9_clean.html": "第9章样张_fixed.html",
    "ch10_clean.html": "第10章样张_fixed.html",
    "ch11_clean.html": "第11章样张_fixed.html",
    "ch12_clean.html": "第12章样张_fixed.html",
}

def load_image_as_base64(image_path):
    """加载WebP图片并转换为base64"""
    try:
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"  警告: 无法加载图片 {image_path}: {e}")
        return None

def get_image_files_for_chapter(chapter_num):
    """获取某章节的所有场景图片"""
    images = []
    for i in range(1, 5):  # 每章最多4张场景图
        img_path = IMAGES_DIR / f"ch{chapter_num}_scene{i}.webp"
        if img_path.exists():
            images.append(img_path)
    return images

def create_image_tag(base64_data, width=320, alt_text=""):
    """创建img标签，带base64图片"""
    if base64_data:
        return f'<img src="data:image/webp;base64,{base64_data}" alt="{alt_text}" style="width:{width}px;max-width:100%;display:block;margin:1em auto;" />'
    return ""

def extract_scenes_from_original(orig_html_path):
    """从原始HTML中提取场景信息，用于判断图片插入位置"""
    if not orig_html_path.exists():
        return []
    
    with open(orig_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取场景描述中的关键词（如"场景1"、"场景2"等）
    # 查找带有"场景"或序号的段落位置
    scenes = []
    
    # 查找原始HTML中的场景标记（通常是带有scene相关的div或h3）
    scene_patterns = [
        r'<div[^>]*class="[^"]*scene[^"]*"[^>]*>(.*?)</div>',
        r'<h3[^>]*>(.*?场景.*?)</h3>',
        r'（场景\d+）',
    ]
    
    for pattern in scene_patterns:
        matches = re.findall(pattern, content, re.DOTALL)
        scenes.extend(matches)
    
    return scenes[:4]  # 限制最多4个场景

def get_chapter_content_with_images(chapter_file, chapter_num):
    """获取章节内容并嵌入图片"""
    chapter_path = CHAPTERS_DIR / chapter_file
    if not chapter_path.exists():
        return None
    
    with open(chapter_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 获取该章节的图片
    images = get_image_files_for_chapter(chapter_num)
    
    if not images:
        print(f"  警告: 章节{chapter_num}没有找到图片")
        return content
    
    # 转换WebP为base64
    image_data_list = []
    for img_path in images:
        b64 = load_image_as_base64(img_path)
        if b64:
            image_data_list.append(b64)
    
    # 在章节末尾添加图片（每章4张场景图）
    if image_data_list:
        images_html = '\n\n<div class="chapter-images">\n'
        for i, b64 in enumerate(image_data_list, 1):
            img_tag = create_image_tag(b64, width=320, alt_text=f"第{chapter_num}章插图{i}")
            images_html += f'  <figure style="margin:1em 0;text-align:center;">\n    {img_tag}\n  </figure>\n'
        images_html += '</div>\n'
        content += images_html
    
    return content

def generate_merged_html():
    """生成包含所有章节和图片的完整HTML"""
    
    print("开始生成带图片的完整HTML...")
    
    # HTML头部和样式
    html_head = '''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN" xml:lang="zh-CN">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>和古人一起想问题 - 儿童版中国哲学史</title>
    <style>
@page {
    size: A5;
    margin: 15mm 12mm 15mm 15mm;
}

body {
    width: 120mm;
    min-height: 180mm;
    margin: 0 auto;
    padding: 15mm;
    background-color: #fff;
    font-family: "宋体", "SimSun", "Source Han Serif SC", serif;
    font-size: 10pt;
    line-height: 1.8;
    color: #333;
}

h1 {
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 18pt;
    font-weight: bold;
    text-align: center;
    margin: 1em 0 0.8em 0;
    color: #2c3e50;
    border-bottom: 2px solid #3498db;
    padding-bottom: 0.3em;
    page-break-before: always;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 14pt;
    font-weight: bold;
    margin: 1.2em 0 0.5em 0;
    color: #34495e;
    border-left: 4px solid #3498db;
    padding-left: 0.5em;
}

h3 {
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 12pt;
    font-weight: bold;
    margin: 1em 0 0.5em 0;
    color: #2c3e50;
}

p {
    margin: 0.6em 0;
    text-indent: 2em;
}

/* 对话样式 - 人物对话独立成行 */
.dialogue {
    margin: 0.5em 0;
    padding-left: 1em;
    text-indent: 0;
}

.speaker {
    font-weight: bold;
    color: #2980b9;
}

blockquote {
    margin: 1em 2em;
    padding: 0.8em 1em;
    background-color: #f8f9fa;
    border-left: 4px solid #3498db;
    font-style: normal;
    color: #555;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 9pt;
}

td, th {
    border: 1px solid #ddd;
    padding: 0.5em;
    text-align: left;
}

th {
    background-color: #f5f5f5;
    font-weight: bold;
}

li {
    margin: 0.4em 0;
    margin-left: 1.5em;
    list-style-type: disc;
}

strong {
    color: #c0392b;
    font-weight: bold;
}

hr {
    border: none;
    border-top: 1px dashed #ccc;
    margin: 1.5em 0;
}

.chapter-images {
    margin-top: 2em;
    padding-top: 1em;
    border-top: 1px solid #eee;
}

figure {
    margin: 0.8em 0;
}

figcaption {
    font-size: 9pt;
    color: #666;
    text-align: center;
    margin-top: 0.3em;
}

@media print {
    .chapter-images {
        page-break-inside: avoid;
    }
}

@media screen {
    body {
        max-width: 800px;
    }
}
    </style>
</head>
<body>
    <div class="book-content">
'''

    html_foot = '''
    </div>
</body>
</html>
'''

    # 生成HTML内容
    html_content = html_head
    
    # 按顺序处理所有章节
    for chapter_num in range(1, 13):
        chapter_file = f"ch{chapter_num}_clean.html"
        print(f"  处理第{chapter_num}章: {chapter_file}")
        
        chapter_html = get_chapter_content_with_images(chapter_file, chapter_num)
        if chapter_html:
            html_content += chapter_html + "\n\n"
    
    html_content += html_foot
    
    # 保存HTML
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nHTML已保存到: {OUTPUT_HTML}")
    print(f"HTML文件大小: {os.path.getsize(OUTPUT_HTML) / 1024 / 1024:.2f} MB")
    
    return str(OUTPUT_HTML)

def generate_pdf(html_path):
    """使用wkhtmltopdf生成PDF"""
    import subprocess
    
    print(f"\n开始生成PDF...")
    
    # 确保输出目录存在
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    
    # wkhtmltopdf命令
    cmd = [
        'wkhtmltopdf',
        '--enable-local-file-access',
        '--page-size', 'A5',
        '--margin-top', '15mm',
        '--margin-bottom', '15mm',
        '--margin-left', '15mm',
        '--margin-right', '12mm',
        '--print-media-type',
        '--enable-javascript',
        '--javascript-delay', '2000',
        '--image-quality', '90',
        html_path,
        str(OUTPUT_PDF)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"PDF已生成: {OUTPUT_PDF}")
            print(f"PDF文件大小: {os.path.getsize(OUTPUT_PDF) / 1024 / 1024:.2f} MB")
            return True
        else:
            print(f"PDF生成失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"生成PDF时出错: {e}")
        return False

def main():
    print("=" * 60)
    print("生成带插图的儿童哲学史PDF")
    print("=" * 60)
    
    # 1. 生成带图片的HTML
    html_path = generate_merged_html()
    
    # 2. 生成PDF
    if html_path:
        generate_pdf(html_path)
    
    print("\n完成!")

if __name__ == "__main__":
    main()
