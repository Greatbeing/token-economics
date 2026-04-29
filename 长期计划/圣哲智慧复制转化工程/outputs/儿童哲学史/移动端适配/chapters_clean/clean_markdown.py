#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面清理儿童哲学史Markdown - 清理所有残留符号和格式问题
"""

import os
import re
from pathlib import Path

# 路径配置
BASE_PATH = Path("/app/data/所有对话/主对话")
SOURCE_DIR = BASE_PATH / "长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/优化阶段"
OUTPUT_DIR = Path(__file__).parent

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHAPTER_FILES = [
    "第一章优化稿.md", "第二章优化稿.md", "第三章优化稿.md",
    "第四章优化稿.md", "第五章优化稿.md", "第六章优化稿.md",
    "第七章优化稿.md", "第八章优化稿.md", "第九章优化稿.md",
    "第十章优化稿.md", "第十一章优化稿.md", "第十二章优化稿.md",
]

# 表情符号模式
EMOJI_PATTERN = re.compile(
    r'[\U0001F300-\U0001F9FF]|[\U00002600-\U000026FF]|[\U00002700-\U000027BF]'
    r'|🌟|✅|❌|💭|📚|📖|✨|💡|🔮|🎭|🏛️|🌊|☁️|🌙|⭐|🔍|💫|🎯|📝|⚡'
    r'|💪|🎉|🎨|🎪|🎬|🎲|🏆|🥇|🏅|🎖️|📌|📍|🔑|🗝️|💎|🧭|🧩|🧪|🔬'
    r'|🌱|🌿|🌳|🌺|🌸|🌼|🌻|🌞|🌝|🌛|🌜|🌚|🌕|🌖|🌗|🌘|🌑|🌔|🌓'
    r'|🌈|⚡|🔥|💧|❄️|💨|🌀|🌪️|🌫️|⛅|🌥️|🌤️|☀️|🌧️|⛈️|🌩️|🌨️'
    r'|→|←|↑|↓|↔|↕|⇐|⇒|⇑|⇓|⇔|⟵|⟶|⟷|⟹|⟸|⟺|⤴|⤵|➔|➜|➝|➞|➟|➠|➡|➢|➣|➤'
    r'|✓|✗|✕|✖|✔|✘|✚|✝|✞|✟|✠|✡|★|☆|✪|✫|✬|✭|✮|✯|✰|✱|✲|✳|✴|✵|✶|✷|✸|✹|✺|✻|✼|✽|✾|✿|❀|❁|❂|❃|❄|❅|❆|❇|❈|❉|❊|❋|❌|❍|❎|❏|❐|❑|❒|❓|❔|❕|❖|❗|❘|❙|❚|❛|❜|❝|❞|❟|❠|❡|❢|❤|❥|❦|❧|♨|♩|♪|♫|♬|♭|♮|♯'
)

# 拼音声调字符范围（扩展版）
PINYIN_TONE_CHARS = 'àáǎâäåæèéěêëìíǐîïòóǒôöøùúǔûüǖǘǚǜāēěīōūǖǚÀÁǍÂÄÅÆÈÉĚÊËÌÍǏÎÏÒÓǑÔÖØÙÚǓÛÜǕǗǙǛĀĒĔĪŌŪ'

def is_pinyin_line(line):
    """判断是否是拼音行"""
    line = line.strip()
    if not line:
        return False
    
    # 如果包含中文，不是拼音行
    if re.search(r'[\u4e00-\u9fff]', line):
        return False
    
    # 检查是否包含带声调符号的拼音字符
    has_tone = any(c in PINYIN_TONE_CHARS for c in line)
    
    if has_tone:
        return True
    
    # 检查是否是纯拼音（无中文、无声调）
    # 允许的字符：字母、空格、标点符号
    # 移除标点后检查
    clean_for_check = re.sub(r'[,.\'\"\-—–\(\)\[\]\s]+', '', line)
    
    # 如果剩余部分全是英文字母
    if clean_for_check.isalpha() and clean_for_check.islower():
        # 检查是否像拼音（多个单词）
        words = line.split()
        if len(words) >= 2:
            # 检查每个词是否都是拼音字母
            pinyin_letters = set('abcdefghijklmnopqrstuvwxyz')
            if all(word.lower() and all(c in pinyin_letters for c in word.lower()) for word in words):
                return True
    
    return False

def clean_text(text):
    """清理文本中的残留符号"""
    # 1. 清理加粗 **text** -> 保留text
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    
    # 2. 清理斜体 *text* 或 _text_ -> 保留text
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    
    # 3. 清理行内代码 `code` -> 保留code
    text = re.sub(r'`(.+?)`', r'\1', text)
    
    # 4. 清理链接 [text](url) -> 保留text
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    
    # 5. 清理图片 ![alt](url)
    text = re.sub(r'!\[.*?\]\(.+?\)', '', text)
    
    # 6. 清理表情符号
    text = EMOJI_PATTERN.sub('', text)
    
    # 7. 清理多余的星号
    text = re.sub(r'\*{2,}', '', text)
    text = re.sub(r'(?<!\*)\*(?!\*)', '', text)
    
    # 8. 清理多余空格但保留换行
    text = re.sub(r'[ \t]+', ' ', text)
    
    return text.strip()

def process_chapter(chapter_file, chapter_num):
    """处理单个章节"""
    source_path = SOURCE_DIR / chapter_file
    if not source_path.exists():
        print(f"  [跳过] 文件不存在: {chapter_file}")
        return None
    
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.strip().split('\n')
    html_parts = []
    in_table = False
    
    for line in lines:
        # 跳过空行
        if not line.strip():
            html_parts.append('')
            continue
        
        # 检测拼音行并跳过
        if is_pinyin_line(line):
            continue
        
        # 清理文本内容
        cleaned_line = clean_text(line)
        
        # 再次检查清理后的行是否是纯拼音
        if is_pinyin_line(cleaned_line):
            continue
        
        # === 处理不同的Markdown语法 ===
        
        # 章标题 # text
        if cleaned_line.startswith('# ') and not cleaned_line.startswith('## '):
            title = cleaned_line[2:].strip()
            html_parts.append(f'<h1>{title}</h1>')
            
        # 节标题 ## text
        elif cleaned_line.startswith('## ') and not cleaned_line.startswith('### '):
            title = cleaned_line[3:].strip()
            html_parts.append(f'<h2>{title}</h2>')
            
        # 小节标题 ### text
        elif cleaned_line.startswith('### '):
            title = cleaned_line[4:].strip()
            html_parts.append(f'<h3>{title}</h3>')
            
        # 分隔线 --- 或 *** 或 ___
        elif re.match(r'^-{3,}$|^\*{3,}$|^_{3,}$', cleaned_line.strip()):
            html_parts.append('<hr/>')
            
        # 列表项 - text 或 * text 或 + text
        elif re.match(r'^[-*+]\s', cleaned_line):
            item = cleaned_line[2:].strip()
            html_parts.append(f'<li>{item}</li>')
            
        # 有序列表 1. text
        elif re.match(r'^\d+\.\s', cleaned_line):
            item = re.sub(r'^\d+\.\s', '', cleaned_line)
            html_parts.append(f'<li>{item}</li>')
            
        # 引用 > text
        elif cleaned_line.startswith('>'):
            quote = cleaned_line[1:].strip()
            # 检查引用内容是否是拼音
            if is_pinyin_line(quote):
                continue
            html_parts.append(f'<blockquote>{quote}</blockquote>')
            
        # 表格行 | col1 | col2 |
        elif cleaned_line.startswith('|'):
            # 表格分隔行，跳过
            if re.match(r'\|[\s\-:]*\|', cleaned_line):
                if in_table:
                    html_parts.append('</table>')
                    in_table = False
                elif not in_table:
                    html_parts.append('<table>')
                    in_table = True
                continue
            
            cells = [c.strip() for c in cleaned_line.split('|')[1:-1]]
            if cells:
                if not in_table:
                    html_parts.append('<table>')
                    in_table = True
                cells_html = ''.join(f'<td>{c}</td>' for c in cells)
                html_parts.append(f'<tr>{cells_html}</tr>')
                
        # 代码块 ``` ... ```
        elif cleaned_line.startswith('```'):
            if '<pre>' not in ''.join(html_parts[-5:]) if html_parts else False:
                html_parts.append('<pre><code>')
            else:
                html_parts.append('</code></pre>')
            continue
            
        # 普通段落
        else:
            if html_parts and html_parts[-1] == '<pre><code>':
                html_parts.append(cleaned_line)
            else:
                if not re.match(r'^[\|\s\-:*#]+$', cleaned_line):
                    html_parts.append(f'<p>{cleaned_line}</p>')
    
    # 关闭未关闭的表格
    if in_table:
        html_parts.append('</table>')
    
    return '\n'.join(html_parts)

def generate_html(content, title):
    """生成完整HTML"""
    return f'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN" xml:lang="zh-CN">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title} - 儿童版中国哲学史</title>
    <style>
@page {{
    size: A5;
    margin: 15mm 12mm 15mm 15mm;
}}

body {{
    width: 120mm;
    min-height: 180mm;
    margin: 0 auto;
    padding: 15mm;
    background-color: #fff;
    font-family: "宋体", "SimSun", "Source Han Serif SC", serif;
    font-size: 10pt;
    line-height: 1.8;
    color: #333;
}}

h1 {{
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 18pt;
    font-weight: bold;
    text-align: center;
    margin: 1em 0 0.8em 0;
    color: #2c3e50;
    border-bottom: 2px solid #3498db;
    padding-bottom: 0.3em;
}}

h2 {{
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 14pt;
    font-weight: bold;
    margin: 1.2em 0 0.5em 0;
    color: #34495e;
    border-left: 4px solid #3498db;
    padding-left: 0.5em;
}}

h3 {{
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 12pt;
    font-weight: bold;
    margin: 1em 0 0.5em 0;
    color: #2c3e50;
}}

p {{
    margin: 0.6em 0;
    text-indent: 2em;
}}

blockquote {{
    margin: 1em 2em;
    padding: 0.8em 1em;
    background-color: #f8f9fa;
    border-left: 4px solid #3498db;
    font-style: normal;
    color: #555;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 9pt;
}}

td, th {{
    border: 1px solid #ddd;
    padding: 0.5em;
    text-align: left;
}}

th {{
    background-color: #f5f5f5;
    font-weight: bold;
}}

li {{
    margin: 0.4em 0;
    margin-left: 1.5em;
    list-style-type: disc;
}}

strong {{
    color: #c0392b;
    font-weight: bold;
}}

hr {{
    border: none;
    border-top: 1px dashed #ccc;
    margin: 1.5em 0;
}}

pre {{
    background-color: #f5f5f5;
    padding: 1em;
    margin: 1em 0;
    overflow-x: auto;
    border-radius: 4px;
    font-size: 9pt;
    white-space: pre-wrap;
}}

@media print {{
    h1 {{
        page-break-before: always;
    }}
    h1:first-of-type {{
        page-break-before: avoid;
    }}
}}

@media screen {{
    body {{
        max-width: 800px;
    }}
}}
    </style>
</head>
<body>
    <div class="book-content">
{content}
    </div>
</body>
</html>'''

def main():
    print("=" * 60)
    print("开始全面清理Markdown文件")
    print("清理项目: 加粗、斜体、代码、标题、列表、引用、链接、")
    print("         分隔线、表格、表情符号、拼音注释等")
    print("=" * 60)
    
    all_contents = []
    
    for i, chapter_file in enumerate(CHAPTER_FILES, 1):
        print(f"\n处理: {chapter_file}")
        
        content = process_chapter(chapter_file, i)
        
        if content:
            # 提取章节标题
            title_match = re.search(r'<h1>(.+?)</h1>', content)
            title = title_match.group(1) if title_match else f"第{i}章"
            
            # 生成HTML
            html = generate_html(content, title)
            
            # 保存单个章节
            output_file = OUTPUT_DIR / f"ch{i}_clean.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"  ✓ 已保存: {output_file.name}")
            
            # 收集用于合并
            all_contents.append((title, content))
    
    # 生成合并的完整HTML
    print("\n" + "-" * 60)
    print("生成合并文件...")
    
    merged_content = '\n'.join(c for _, c in all_contents)
    merged_html = generate_html(merged_content, "和古人一起想问题")
    
    merged_file = OUTPUT_DIR / "merged_clean.html"
    with open(merged_file, 'w', encoding='utf-8') as f:
        f.write(merged_html)
    print(f"  ✓ 已保存: {merged_file.name}")
    
    print("\n" + "=" * 60)
    print(f"清理完成! 共处理 {len(all_contents)} 个章节")
    print(f"输出目录: {OUTPUT_DIR}")
    print("=" * 60)
    
    return OUTPUT_DIR / "merged_clean.html"

if __name__ == "__main__":
    merged_path = main()
