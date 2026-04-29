#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理HTML章节文件，清理Markdown符号，提取图片，生成完整PDF
"""

import os
import re
import base64
from pathlib import Path

# 路径设置
SOURCE_DIR = "长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/修正版"
OUTPUT_DIR = "长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/最终交付"
IMAGE_DIR = "images"

def extract_base64_images(html_content, output_path, chapter_num):
    """提取HTML中的base64图片并保存"""
    img_pattern = r'<img[^>]+src="data:image/([^"]+);base64,([^"]+)"[^>]*>'
    matches = re.findall(img_pattern, html_content)
    
    img_map = {}
    for i, (img_type, b64_data) in enumerate(matches):
        img_filename = f"chapter{chapter_num}_img{i+1}.{img_type if img_type else 'jpg'}"
        img_full_path = os.path.join(output_path, IMAGE_DIR, img_filename)
        
        try:
            img_data = base64.b64decode(b64_data)
            with open(img_full_path, 'wb') as f:
                f.write(img_data)
            img_map[f"data:image/{img_type};base64,{b64_data}"] = f"./{IMAGE_DIR}/{img_filename}"
            print(f"  保存图片: {img_filename}")
        except Exception as e:
            print(f"  图片保存失败 {img_filename}: {e}")
    
    return img_map

def replace_images_in_html(html_content, img_map):
    """替换HTML中的base64图片为本地文件路径"""
    for old_src, new_src in img_map.items():
        html_content = html_content.replace(f'src="{old_src}"', f'src="{new_src}"')
    return html_content

def clean_markdown(text):
    """清理Markdown符号和其他不需要的内容"""
    # 移除Markdown加粗符号
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    # 移除单个*符号（Markdown斜体）
    text = re.sub(r'\*(?!\*)(.+?)(?<!\*)\*', r'\1', text)
    # 移除下划线加粗
    text = re.sub(r'__(.+?)__', r'\1', text)
    # 移除Markdown标题符号（但不移除HTML标签）
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # 移除删除线
    text = re.sub(r'~~(.+?)~~', r'\1', text)
    # 移除HTML注释
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    # 移除各种emoji表情
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F700-\U0001F77F"  # alchemical symbols
        u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251"  # enclosed characters
        u"\U0001F004-\U0001F0CF"  # Mahjong Tiles
        u"\U0001F170-\U0001F251"  # Enclosed Alphanumeric Supplement
        u"\u2600-\u2B55"          # misc symbols
        u"\u231A-\u231B"          # watch/hourglass
        u"\u23E9-\u23F3"          # transport symbols
        u"\u23F8-\u23FA"          # stopwatch/scoreboard
        u"\u25AA-\u25AB"          # squares
        u"\u25B6"                 # play button
        u"\u25C0"                 # reverse button
        u"\u25FB-\u25FE"          # squares
        u"\u2611-\u2612"          # ballot box
        u"\u2614-\u2615"          # umbrella/coffee
        u"\u261A-\u261D"          # pointing hand
        u"\u2620-\u2623"          # skull/fleur-de-lis
        u"\u2626-\u2627"          # skull/peace
        u"\u262A"                 # star and crescent
        u"\u262E-\u262F"          # ankh/peace
        u"\u2638-\u263A"          # wheel/spa/sun
        u"\u2648-\u2653"          # zodiac
        u"\u265F-\u2660"          # chess pawn/white
        u"\u2661-\u2665"          # heart/diamond
        u"\u2666-\u2667"          # card symbols
        u"\u2668"                 # hotsprings
        u"\u2669-\u266B"          # music notes
        u"\u266D-\u266F"          # flat/natural/sharp
        u"\u2702-\u2705"          # scissors/checkmark
        u"\u2708-\u270D"          # plane/pen/hand
        u"\u270E-\u270F"          # pencil/lower right
        u"\u2712-\u2714"          # pencil/checkmark
        u"\u2716-\u271D"          # multiplication/checked/hand
        u"\u2720-\u2721"          # cross/star
        u"\u2728"                 # sparkles
        u"\u2733-\u2734"          # stars
        u"\u2744-\u2745"          # snowflake/eight
        u"\u2747-\u2748"          # sparkle/hot
        u"\u274C-\u274D"          # x mark/collision
        u"\u274E-\u274F"          # x marks
        u"\u2753-\u2757"          # question marks
        u"\u2763-\u2764"          # hearts
        u"\u2795-\u2797"          # plus/minus/divide
        u"\u2934-\u2935"          # arrows
        u"\u3030"                 # wavy dash
        u"\u3297-\u3298"          # ideographs
        u"\U00010000-\U0010ffff"  # supplementary characters
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    # 移除常见的Unicode符号
    text = re.sub(r'[\u2605\u2606\u2665\u2666\u2713\u2714\u2717\u2718\u2721\u2726-\u2729\u2744\u2747\u2750\u2751\u2752\u2764\u2794\u2795\u2796\u27A4\u27B3\u27C0-\u27C3\u27C4\u27C5\u27C6\u27E6-\u27F5\u27F8\u27F9\u27FA\u27FC\u27FF\u2800-\u28FF\u2900-\u297F\u2980-\u299F\u29BF\u29C0\u29C1\u29C2\u29C3\u29C4\u29C5\u29C6\u29C7\u29C8\u29C9\u29CA\u29CB\u29CC\u29CD\u29CE\u29CF\u29D0\u29D1\u29D2\u29D3\u29D4\u29D5\u29DC\u29DD\u29DE\u29DF\u29E0\u29E1\u29E2\u29E3\u29E4\u29E5\u29E6\u29E7\u29E8\u29E9\u29EA\u29EB\u29EC\u29ED\u29EE\u29EF\u29F0\u29F1\u29F2\u29F3\u29F4\u29F5\u29F6\u29F7\u29F8\u29F9\u29FA\u29FB\u29FC\u29FD\u29FE\u29FF\u2A00-\u2AFF\u2100-\u214F\u2190-\u21FF\u2200-\u22FF\u2300-\u23FF\u2400-\u243F\u2440-\u245F\u2460-\u24FF\u2500-\u257F\u2580-\u259F\u25A0-\u25FF\u2600-\u26FF\u2700-\u27BF\u3000-\u303F\u3200-\u32FF\u3300-\u33FF\uF000-\uFFFF]+', '', text)
    # 移除HTML注释
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    # 移除多余的空格
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text

def process_html_file(filepath, img_output_path, chapter_num):
    """处理单个HTML文件"""
    print(f"处理: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取图片
    print(f"  提取图片...")
    img_map = extract_base64_images(content, img_output_path, chapter_num)
    
    # 替换图片引用
    content = replace_images_in_html(content, img_map)
    
    # 清理Markdown符号
    print(f"  清理格式...")
    content = clean_markdown(content)
    
    return content

def create_combined_html(chapters_html, output_path):
    """创建合并的HTML文件"""
    
    # 创建简单的CSS样式
    css = """
    <style>
        body {
            font-family: 'Source Han Serif SC', 'SimSun', 'Songti SC', 'Noto Serif CJK SC', serif;
            font-size: 16px;
            line-height: 1.8;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            text-align: justify;
        }
        h1 {
            font-family: 'FZXiaoBiaoSong-B05S', 'FangSong', 'STFangsong', serif;
            font-size: 28px;
            color: #8B4513;
            text-align: center;
            margin: 40px 0 30px 0;
            border-bottom: 2px solid #D2691E;
            padding-bottom: 15px;
        }
        h2 {
            font-family: 'FZXiaoBiaoSong-B05S', 'FangSong', 'STFangsong', serif;
            font-size: 22px;
            color: #1565C0;
            margin: 35px 0 20px 0;
            border-bottom: 1px solid #81D4FA;
            padding-bottom: 8px;
        }
        h3 {
            font-size: 18px;
            font-weight: bold;
            color: #5D4037;
            margin: 25px 0 15px 0;
        }
        p {
            margin-bottom: 16px;
            text-indent: 2em;
        }
        .thought-theater {
            background-color: #FFF8E7;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .dialog-line {
            margin: 15px 0;
            padding: 10px;
            background-color: #F5F5F5;
            border-left: 3px solid #1565C0;
        }
        .practice-exercise {
            background-color: #E8F5E9;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #BDBDBD;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #F5F5F5;
        }
        .chapter-break {
            page-break-after: always;
            height: 100px;
        }
    </style>
    """
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>和古人一起想问题——儿童哲学史</title>
    {css}
</head>
<body>
"""
    
    # 添加封面
    html_content += """
    <div style="text-align: center; padding: 100px 20px; page-break-after: always;">
        <h1 style="font-size: 36px; color: #8B4513; border: none; margin-top: 200px;">
            和古人一起想问题
        </h1>
        <h2 style="font-size: 24px; color: #666; border: none; margin-top: 50px;">
            儿童版中国哲学史
        </h2>
        <p style="text-align: center; margin-top: 100px; color: #999;">
            —— 让哲学滋养童年 ——
        </p>
        <img src="./封面_A4竖版_最终.jpg" alt="封面" style="max-width: 400px; margin-top: 80px;">
    </div>
    """
    
    # 添加章节
    for i, chapter_content in enumerate(chapters_html):
        chapter_num = i + 1
        html_content += f'\n<div class="chapter-break"></div>\n'
        html_content += chapter_content
        html_content += '\n'
    
    html_content += """
</body>
</html>
"""
    
    # 保存HTML文件
    html_path = os.path.join(output_path, "combined_content.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nHTML文件已保存: {html_path}")
    return html_path

def main():
    """主函数"""
    print("=" * 60)
    print("开始处理儿童哲学史HTML文件")
    print("=" * 60)
    
    # 获取所有章节文件
    chapter_files = []
    for i in range(1, 13):
        filepath = os.path.join(SOURCE_DIR, f"第{i}章样张_fixed.html")
        if os.path.exists(filepath):
            chapter_files.append((filepath, i))
        else:
            print(f"警告: 文件不存在 - {filepath}")
    
    print(f"\n找到 {len(chapter_files)} 个章节文件\n")
    
    # 处理每个章节
    chapters_html = []
    for filepath, chapter_num in chapter_files:
        content = process_html_file(filepath, OUTPUT_DIR, chapter_num)
        chapters_html.append(content)
        print(f"  ✓ 第{chapter_num}章处理完成\n")
    
    # 创建合并的HTML
    print("\n创建合并HTML文档...")
    html_path = create_combined_html(chapters_html, OUTPUT_DIR)
    
    print("\n" + "=" * 60)
    print("HTML处理完成!")
    print("=" * 60)
    print(f"\n下一步: 使用wkhtmltopdf将HTML转换为PDF")
    print(f"命令: wkhtmltopdf --enable-local-file-access --page-size A4 {html_path} output.pdf")

if __name__ == "__main__":
    main()
