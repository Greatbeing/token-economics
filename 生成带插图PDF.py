#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将优化后的WebP图片嵌入清理后的HTML，生成带插图的完整PDF
改进排版：对话分行、小标题、引用块等
"""

import os
import re
import base64
from pathlib import Path

# 路径配置
BASE_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史")
IMAGES_DIR = BASE_DIR / "移动端适配/optimized_images"
CHAPTERS_DIR = BASE_DIR / "移动端适配/chapters_clean"
OUTPUT_DIR = BASE_DIR / "最终交付"
OUTPUT_HTML = CHAPTERS_DIR / "merged_with_images.html"
OUTPUT_PDF = OUTPUT_DIR / "和古人一起想问题_移动端优化版.pdf"

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

def get_chapter_images_html(chapter_num):
    """生成章节的图片HTML"""
    images = get_image_files_for_chapter(chapter_num)
    
    if not images:
        return ""
    
    images_html = '\n\n<!-- 章节插图 -->\n<div class="chapter-illustrations">\n'
    
    for i, img_path in enumerate(images, 1):
        b64 = load_image_as_base64(img_path)
        if b64:
            # 缩放图片到合适的移动端尺寸 (300px宽度)
            images_html += f'''<figure class="illustration">
    <img src="data:image/webp;base64,{b64}" 
         alt="第{chapter_num}章插图{i}" 
         style="width:280px;height:auto;display:block;margin:0 auto;" />
</figure>
'''
    
    images_html += '</div>\n'
    return images_html

def improve_dialogue_style(content):
    """改进对话样式，使人物对话独立成行"""
    # 匹配人物对话模式：小星：、小宇：、老子：等
    # 将对话从段落中提取出来，使用专门的样式
    
    # 处理对话框格式
    dialogue_pattern = r'<p>([（]?[^\n：]+[）]?：)([^<]+)</p>'
    
    def replace_dialogue(match):
        speaker = match.group(1)
        text = match.group(2)
        return f'''<p class="dialogue"><span class="speaker">{speaker}</span>{text}</p>'''
    
    improved = re.sub(dialogue_pattern, replace_dialogue, content)
    return improved

def clean_and_format_content(content):
    """清理并格式化内容"""
    # 移除多余的空白
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # 确保HTML实体正确
    content = content.replace('&', '&amp;')
    content = content.replace('<', '&lt;')
    content = content.replace('>', '&gt;')
    
    return content

def process_chapter(chapter_num):
    """处理单个章节"""
    chapter_file = CHAPTERS_DIR / f"ch{chapter_num}_clean.html"
    
    if not chapter_file.exists():
        print(f"  警告: 文件不存在 {chapter_file}")
        return None
    
    with open(chapter_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取body内容（移除html/head/body标签）
    body_match = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
    if body_match:
        body_content = body_match.group(1)
    else:
        body_content = content
    
    # 改进对话样式
    body_content = improve_dialogue_style(body_content)
    
    # 添加章节插图
    body_content += get_chapter_images_html(chapter_num)
    
    return body_content

def generate_complete_html():
    """生成完整的HTML文档"""
    print("=" * 60)
    print("生成带插图的儿童哲学史HTML")
    print("=" * 60)
    
    # HTML头部
    html_head = '''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN" xml:lang="zh-CN">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>和古人一起想问题 - 儿童版中国哲学史</title>
    <style>
@page {
    size: A5;
    margin: 12mm 10mm 12mm 12mm;
}

* {
    box-sizing: border-box;
}

body {
    width: 115mm;
    min-height: 170mm;
    margin: 0 auto;
    padding: 12mm;
    background-color: #fff;
    font-family: "宋体", "SimSun", "Source Han Serif SC", "Noto Serif SC", serif;
    font-size: 10pt;
    line-height: 1.75;
    color: #333;
    text-align: justify;
}

/* 标题样式 */
h1 {
    font-family: "黑体", "SimHei", "Noto Sans SC", sans-serif;
    font-size: 16pt;
    font-weight: bold;
    text-align: center;
    margin: 0.8em 0 0.6em 0;
    color: #1a1a1a;
    border-bottom: 2px solid #3498db;
    padding-bottom: 0.25em;
    page-break-before: always;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    font-family: "黑体", "SimHei", "Noto Sans SC", sans-serif;
    font-size: 13pt;
    font-weight: bold;
    margin: 1em 0 0.4em 0;
    color: #2c3e50;
    border-left: 3px solid #3498db;
    padding-left: 0.4em;
}

h3 {
    font-family: "黑体", "SimHei", "Noto Sans SC", sans-serif;
    font-size: 11pt;
    font-weight: bold;
    margin: 0.8em 0 0.3em 0;
    color: #34495e;
}

/* 段落样式 */
p {
    margin: 0.5em 0;
    text-indent: 2em;
    orphans: 2;
    widows: 2;
}

/* 对话样式 - 人物对话独立成行 */
.dialogue {
    margin: 0.4em 0;
    padding-left: 0.5em;
    text-indent: 0;
    border-left: 2px solid #e0e0e0;
}

.speaker {
    font-weight: bold;
    color: #2980b9;
    margin-right: 0.3em;
}

/* 舞台指示/旁白 */
.stage-direction {
    font-style: italic;
    color: #666;
    margin: 0.5em 0;
    text-indent: 0;
    padding-left: 1em;
}

/* 引用块 */
blockquote {
    margin: 0.8em 1.5em;
    padding: 0.6em 0.8em;
    background-color: #f8f9fa;
    border-left: 3px solid #3498db;
    font-style: normal;
    color: #555;
    text-indent: 0;
}

blockquote p {
    margin: 0.3em 0;
    text-indent: 0;
}

/* 表格样式 */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.8em 0;
    font-size: 9pt;
    page-break-inside: avoid;
}

td, th {
    border: 1px solid #ddd;
    padding: 0.4em;
    text-align: left;
}

th {
    background-color: #f0f4f8;
    font-weight: bold;
}

/* 列表样式 */
li {
    margin: 0.3em 0;
    margin-left: 1.2em;
    list-style-type: disc;
}

li p {
    margin: 0.2em 0;
}

/* 强调文字 */
strong {
    color: #c0392b;
    font-weight: bold;
}

em {
    font-style: italic;
    color: #555;
}

/* 分隔线 */
hr {
    border: none;
    border-top: 1px dashed #ccc;
    margin: 1.2em 0;
}

/* 章节插图区域 */
.chapter-illustrations {
    margin-top: 1.5em;
    padding-top: 1em;
    border-top: 1px solid #e8e8e8;
    text-align: center;
}

.illustration {
    margin: 0.6em 0;
    page-break-inside: avoid;
}

.illustration img {
    max-width: 100%;
    height: auto;
}

/* 打印样式 */
@media print {
    h1 {
        page-break-before: always;
    }
    h1:first-of-type {
        page-break-before: avoid;
    }
    .chapter-illustrations {
        page-break-inside: avoid;
    }
    p, li {
        orphans: 2;
        widows: 2;
    }
}

/* 屏幕阅读样式 */
@media screen {
    body {
        max-width: 750px;
        padding: 20px;
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

    # 生成所有章节内容
    full_content = html_head
    
    for chapter_num in range(1, 13):
        print(f"  处理第{chapter_num}章...")
        chapter_content = process_chapter(chapter_num)
        if chapter_content:
            full_content += f"\n<!-- 第{chapter_num}章 -->\n" + chapter_content + "\n"
    
    full_content += html_foot
    
    # 保存HTML文件
    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    file_size = os.path.getsize(OUTPUT_HTML) / 1024 / 1024
    print(f"\n✓ HTML已生成: {OUTPUT_HTML}")
    print(f"  文件大小: {file_size:.2f} MB")
    
    return str(OUTPUT_HTML)

def generate_pdf(html_path):
    """使用wkhtmltopdf生成PDF"""
    import subprocess
    
    print("\n" + "=" * 60)
    print("生成PDF文档")
    print("=" * 60)
    
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 检查wkhtmltopdf是否可用
    try:
        subprocess.run(['wkhtmltopdf', '--version'], capture_output=True, check=True)
    except:
        print("错误: wkhtmltopdf未安装或不可用")
        return False
    
    # 构建命令
    cmd = [
        'wkhtmltopdf',
        '--enable-local-file-access',
        '--page-size', 'A5',
        '--orientation', 'Portrait',
        '--margin-top', '12mm',
        '--margin-bottom', '12mm',
        '--margin-left', '12mm',
        '--margin-right', '10mm',
        '--print-media-type',
        '--enable-javascript',
        '--javascript-delay', '3000',
        '--image-quality', '85',
        '--no-stop-slow-scripts',
        html_path,
        str(OUTPUT_PDF)
    ]
    
    print("正在生成PDF，请稍候...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0 and OUTPUT_PDF.exists():
            file_size = os.path.getsize(OUTPUT_PDF) / 1024 / 1024
            print(f"\n✓ PDF已生成: {OUTPUT_PDF}")
            print(f"  文件大小: {file_size:.2f} MB")
            return True
        else:
            print(f"错误: PDF生成失败")
            if result.stderr:
                print(f"错误信息: {result.stderr[:500]}")
            return False
            
    except subprocess.TimeoutExpired:
        print("错误: PDF生成超时")
        return False
    except Exception as e:
        print(f"错误: {e}")
        return False

def main():
    print("=" * 60)
    print("儿童哲学史PDF生成器")
    print("=" * 60)
    
    # 1. 生成带图片的HTML
    html_path = generate_complete_html()
    
    # 2. 生成PDF
    if html_path:
        generate_pdf(html_path)
    
    print("\n" + "=" * 60)
    print("处理完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()
