#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复儿童哲学史HTML和PDF生成脚本 v2
1. 清理表情符号和装饰性字符
2. 生成带base64嵌入图片的HTML
3. 使用wkhtmltopdf生成PDF
"""

import os
import re
import base64
import subprocess
from pathlib import Path

# 基础路径
BASE_DIR = Path("/app/data/所有对话/主对话/长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史")
IMAGES_DIR = BASE_DIR / "移动端适配/optimized_images"
OUTPUT_DIR = BASE_DIR / "移动端适配/chapters_final"
FINAL_PDF_DIR = BASE_DIR / "最终交付"

# 需要清理的字符模式
def clean_emojis_and_symbols(text):
    """清理表情符号和装饰性符号"""
    # 替换表情符号为空
    text = re.sub(r'🌟|✅|❌|💭|📚|📖|✨|💡|🔮|🎭|🏛️|🌊|☁️|🌙|⭐|🔍|💫|🎯|📝|⚡', '', text)
    text = re.sub(r'[\U0001F300-\U0001F9FF]', '', text)
    text = re.sub(r'[\U00002702-\U000027B0]', '', text)
    text = re.sub(r'[\U00002600-\U000026FF]', '', text)
    # 清理多余空格但保留换行
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

# 章节文件列表
CHAPTER_FILES = [
    "第一章优化稿.md", "第二章优化稿.md", "第三章优化稿.md",
    "第四章优化稿.md", "第五章优化稿.md", "第六章优化稿.md",
    "第七章优化稿.md", "第八章优化稿.md", "第九章优化稿.md",
    "第十章优化稿.md", "第十一章优化稿.md", "第十二章优化稿.md",
]

def get_image_path(chapter_num, scene_num):
    """获取图片路径"""
    return IMAGES_DIR / f"ch{chapter_num}_scene{scene_num}.webp"

def image_to_base64(image_path):
    """将图片转换为base64编码"""
    if image_path.exists():
        with open(image_path, "rb") as f:
            return f"data:image/webp;base64,{base64.b64encode(f.read()).decode()}"
    return ""

def md_to_html_content(md_text, chapter_num):
    """将Markdown内容转换为HTML"""
    lines = md_text.strip().split('\n')
    html_parts = []
    scene_num = 1
    
    i = 0
    while i < len(lines):
        raw_line = lines[i]
        line = raw_line.strip()
        
        # 跳过空行
        if not line:
            i += 1
            continue
            
        # 清理符号
        line = clean_emojis_and_symbols(line)
        
        # 章标题 h1 (# 标题)
        if line.startswith('# ') and not line.startswith('##'):
            # 检查是否是纯标题行（不含特殊符号）
            title = line[2:].strip()
            if title and not title.startswith('*'):
                html_parts.append(f'<h1>{title}</h1>\n')
            
        # 节标题 h2 (## 标题)
        elif line.startswith('## ') and not line.startswith('###'):
            title = line[3:].strip()
            # 在某些节标题后插入场景图片
            if any(kw in title for kw in ["第一站", "第二站", "第三站", "思想剧场"]):
                if scene_num > 1:
                    img_html = generate_image_html(chapter_num, scene_num)
                    html_parts.append(img_html)
                    scene_num += 1
            html_parts.append(f'<h2>{title}</h2>\n')
            
        # 小节标题 h3 (### 标题)
        elif line.startswith('### '):
            title = line[4:].strip()
            html_parts.append(f'<h3>{title}</h3>\n')
            
        # 引用/原文 (> 开头)
        elif line.startswith('>'):
            content = line[1:].strip()
            html_parts.append(f'<blockquote>{content}</blockquote>\n')
            
        # 分隔线
        elif line.startswith('---') or line.startswith('***') or line.startswith('___'):
            html_parts.append('<hr/>\n')
            
        # 列表项 (- 或 * 开头)
        elif line.startswith('- ') or line.startswith('* '):
            content = line[2:].strip()
            html_parts.append(f'<li>{content}</li>\n')
            
        # 表格行 (| 开头)
        elif line.startswith('|'):
            # 跳过分隔行如 |------|------|
            if re.match(r'\|[\s\-:]+\|', line):
                i += 1
                continue
            cells = [c.strip() for c in line.split('|')[1:-1]]
            html_parts.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>\n')
            
        # 代码块
        elif line.startswith('```'):
            html_parts.append('<pre><code>')
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                html_parts.append(lines[i] + '\n')
                i += 1
            html_parts.append('</code></pre>\n')
            
        # 强调文本 **text**
        elif '**' in line:
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            html_parts.append(f'<p>{line}</p>\n')
            
        # 普通段落
        else:
            html_parts.append(f'<p>{line}</p>\n')
        
        i += 1
    
    return ''.join(html_parts)

def generate_image_html(chapter_num, scene_num):
    """生成图片HTML"""
    img_src = image_to_base64(get_image_path(chapter_num, scene_num))
    if img_src:
        return f'''<div class="illustration-container">
    <img src="{img_src}" alt="第{chapter_num}章第{scene_num}个场景" class="chapter-illustration">
</div>
'''
    return ''

def generate_chapter_html(chapter_num, chapter_title, content_html):
    """生成完整的章节HTML"""
    
    html = f'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN" xml:lang="zh-CN">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{chapter_title} - 儿童版中国哲学史</title>
    <style>
@page {{
    size: A4;
    margin: 20mm 15mm 20mm 20mm;
}}

body {{
    width: 170mm;
    min-height: 257mm;
    margin: 0 auto;
    padding: 20mm;
    background-color: #fff;
    font-family: "宋体", "SimSun", "Source Han Serif SC", serif;
    font-size: 11pt;
    line-height: 1.8;
    color: #333;
}}

h1 {{
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 22pt;
    font-weight: bold;
    text-align: center;
    margin: 1em 0;
    color: #2c3e50;
}}

h2 {{
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 16pt;
    font-weight: bold;
    margin: 1.2em 0 0.5em 0;
    color: #34495e;
    border-left: 3px solid #3498db;
    padding-left: 0.5em;
}}

h3 {{
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 13pt;
    font-weight: bold;
    margin: 1em 0 0.5em 0;
    color: #2c3e50;
}}

p {{
    margin: 0.5em 0;
    text-indent: 2em;
}}

blockquote {{
    margin: 1em 2em;
    padding: 0.5em 1em;
    background-color: #f5f5f5;
    border-left: 3px solid #3498db;
    font-style: italic;
}}

.illustration-container {{
    text-align: center;
    margin: 1.5em 0;
}}

.chapter-illustration {{
    max-width: 100%;
    height: auto;
    border-radius: 8px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
}}

td, th {{
    border: 1px solid #ddd;
    padding: 0.5em;
    text-align: left;
}}

li {{
    margin: 0.3em 0;
    margin-left: 2em;
}}

strong {{
    color: #c0392b;
}}

hr {{
    border: none;
    border-top: 1px dashed #ccc;
    margin: 1.5em 0;
}}

pre {{
    background-color: #f5f5f5;
    padding: 1em;
    overflow-x: auto;
    border-radius: 4px;
}}
    </style>
</head>
<body>
    <div class="book-content">
        {content_html}
    </div>
</body>
</html>'''
    
    return html

def load_cover():
    """加载封面图片为base64"""
    cover_path = FINAL_PDF_DIR / "封面_A4竖版_最终.jpg"
    if cover_path.exists():
        with open(cover_path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return ""

def main():
    print("开始修复儿童哲学史HTML和PDF...")
    
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 加载封面
    cover_base64 = load_cover()
    print("封面加载完成")
    
    chapter_htmls = []
    
    # 中文数字转阿拉伯数字
    cn_to_arab = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10,'十一':11,'十二':12}
    
    # 处理每个章节
    for chapter_file in CHAPTER_FILES:
        md_path = BASE_DIR / "优化阶段" / chapter_file
        
        if not md_path.exists():
            print(f"文件不存在，跳过: {md_path}")
            continue
            
        # 提取章节号
        ch_match = re.search(r'第([一二三四五六七八九十]+)章', chapter_file)
        if ch_match:
            chapter_num = cn_to_arab.get(ch_match.group(1), 0)
        else:
            continue
        
        print(f"处理章节: {chapter_file}")
        
        # 读取MD内容
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 清理符号
        md_content = clean_emojis_and_symbols(md_content)
        
        # 转换为HTML
        content_html = md_to_html_content(md_content, chapter_num)
        
        # 在开头添加第一个场景图片
        img_html = generate_image_html(chapter_num, 1)
        content_html = img_html + content_html
        
        # 提取标题
        title_match = re.search(r'^# (.+)', md_content, re.MULTILINE)
        chapter_title = title_match.group(1) if title_match else f"第{chapter_num}章"
        
        # 生成完整HTML
        full_html = generate_chapter_html(chapter_num, chapter_title, content_html)
        
        # 保存章节HTML
        chapter_html_path = OUTPUT_DIR / f"ch{chapter_num}_final.html"
        with open(chapter_html_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"  HTML保存: {chapter_html_path}")
        
        chapter_htmls.append((chapter_num, chapter_title, full_html))
    
    # 生成合并PDF
    print("\n生成最终PDF...")
    final_pdf = FINAL_PDF_DIR / "和古人一起想问题_移动端优化版.pdf"
    
    # 创建合并HTML
    merged_html = f'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN" xml:lang="zh-CN">
<head>
    <meta charset="utf-8" />
    <title>和古人一起想问题 - 儿童版中国哲学史</title>
    <style>
@page {{
    size: A4;
    margin: 15mm;
}}

body {{
    font-family: "宋体", "SimSun", serif;
    font-size: 11pt;
    line-height: 1.8;
    color: #333;
    margin: 0;
    padding: 0;
}}

h1 {{
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 22pt;
    text-align: center;
    margin: 1em 0;
    color: #2c3e50;
}}

h2 {{
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 16pt;
    color: #34495e;
    border-left: 3px solid #3498db;
    padding-left: 0.5em;
    margin-top: 1em;
}}

h3 {{
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 13pt;
    color: #2c3e50;
}}

p {{
    margin: 0.5em 0;
    text-indent: 2em;
}}

blockquote {{
    margin: 1em 2em;
    padding: 0.5em 1em;
    background-color: #f5f5f5;
    border-left: 3px solid #3498db;
}}

.illustration-container {{
    text-align: center;
    margin: 1em 0;
    page-break-inside: avoid;
}}

.chapter-illustration {{
    max-width: 90%;
    height: auto;
    border-radius: 8px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

td, th {{
    border: 1px solid #ddd;
    padding: 0.5em;
}}

li {{
    margin: 0.3em 0;
    margin-left: 2em;
}}

strong {{
    color: #c0392b;
}}

hr {{
    border: none;
    border-top: 1px dashed #ccc;
    margin: 1em 0;
}}

.page-break {{
    page-break-after: always;
}}

.chapter-page {{
    page-break-after: always;
}}

.cover-page {{
    text-align: center;
    padding-top: 100mm;
}}
    </style>
</head>
<body>
    <div class="cover-page">
        <h1>和古人一起想问题</h1>
        <h2 style="text-align:center; border-left:none;">儿童版中国哲学史</h2>
        <div style="margin-top:3em;">
            <img src="{cover_base64}" alt="封面" style="max-width:50%; border-radius:8px;">
        </div>
    </div>
    <div class="page-break"></div>
'''
    
    for ch_num, ch_title, ch_html in sorted(chapter_htmls):
        # 提取body内容
        body_match = re.search(r'<div class="book-content">(.*?)</div>\s*</body>', ch_html, re.DOTALL)
        if body_match:
            content = body_match.group(1)
            merged_html += f'<div class="chapter-page">\n{content}\n</div>\n<div class="page-break"></div>\n'
    
    merged_html += '</body>\n</html>'
    
    # 保存合并HTML
    merged_html_path = OUTPUT_DIR / "merged_content.html"
    with open(merged_html_path, 'w', encoding='utf-8') as f:
        f.write(merged_html)
    print(f"合并HTML保存: {merged_html_path}")
    
    # 生成PDF
    cmd = [
        'wkhtmltopdf',
        '--enable-local-file-access',
        '--print-media-type',
        '--image-quality', '90',
        '--page-size', 'A4',
        '--margin-top', '15mm',
        '--margin-bottom', '15mm',
        '--margin-left', '15mm',
        '--margin-right', '15mm',
        str(merged_html_path),
        str(final_pdf)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            print(f"\nPDF生成成功: {final_pdf}")
            return True
        else:
            print(f"PDF生成失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("PDF生成超时")
        return False
    except FileNotFoundError:
        print("wkhtmltopdf未安装")
        return False

if __name__ == "__main__":
    main()
