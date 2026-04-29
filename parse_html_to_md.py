#!/usr/bin/env python3
"""
从HTML文件中提取《和古人一起想问题》的内容并转换为Markdown格式
"""

import os
import re
from html.parser import HTMLParser
from html import unescape
import html2text

# 配置html2text
h2t = html2text.HTML2Text()
h2t.ignore_links = False
h2t.ignore_images = False
h2t.ignore_emphasis = False
h2t.body_width = 0  # 不自动换行
h2t.unicode_snob = True
h2t.skip_internal_links = False

def clean_text(text):
    """清理文本中的多余空白"""
    # 移除多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    # 移除行首行尾空格
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    return text.strip()

def extract_chapter_number(filename):
    """从文件名提取章节号"""
    match = re.search(r'第(\d+)章', filename)
    if match:
        return int(match.group(1))
    return 0

def parse_html_file(filepath):
    """解析单个HTML文件并返回Markdown内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 提取章节标题 - 从第一个h2或h1标签
    chapter_title = ""
    title_match = re.search(r'<h[12][^>]*>(.*?)</h[12]>', html_content, re.DOTALL)
    if title_match:
        chapter_title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
    
    # 使用html2text转换
    markdown = h2t.handle(html_content)
    
    # 清理
    markdown = clean_text(markdown)
    
    return chapter_title, markdown

def extract_chapter_title_from_content(markdown):
    """从Markdown内容中提取章节标题"""
    lines = markdown.split('\n')
    for line in lines[:20]:  # 只看前20行
        line = line.strip()
        if line.startswith('## ') and '思想剧场' in line:
            # 找到"思想剧场"之前的章节标题
            return line.replace('## ', '').split('：')[0] if '：' in line else line.replace('## ', '')
        if line.startswith('## '):
            # 可能是章节标题
            title = line.replace('## ', '')
            if '章' in title or '第' in title:
                return title
    return ""

def process_all_chapters():
    """处理所有章节并合并"""
    html_dir = "./长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/优化版/"
    
    # 获取所有HTML文件并按章节号排序
    html_files = [f for f in os.listdir(html_dir) if f.endswith('.html')]
    html_files.sort(key=lambda x: extract_chapter_number(x))
    
    all_content = []
    chapter_titles = []
    
    for html_file in html_files:
        filepath = os.path.join(html_dir, html_file)
        print(f"处理: {html_file}")
        
        try:
            title, markdown = parse_html_file(filepath)
            
            # 提取章节标题（从内容中）
            chapter_title = extract_chapter_title_from_content(markdown)
            if not chapter_title:
                chapter_title = title
            
            chapter_titles.append(chapter_title)
            all_content.append(markdown)
            print(f"  -> 章节标题: {chapter_title}")
            print(f"  -> 内容长度: {len(markdown)} 字符")
            
        except Exception as e:
            print(f"  -> 错误: {e}")
    
    return all_content, chapter_titles

def save_markdown(content_list, titles, output_file):
    """保存为Markdown文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (title, content) in enumerate(zip(titles, content_list)):
            f.write(f"\n\n---\n\n")
            f.write(content)
    
    print(f"\n已保存到: {output_file}")
    print(f"总章节: {len(content_list)}")

if __name__ == "__main__":
    contents, titles = process_all_chapters()
    save_markdown(contents, titles, "./和古人一起想问题_完整版.md")
    
    # 打印章节概览
    print("\n章节概览:")
    for i, title in enumerate(titles, 1):
        print(f"  {i}. {title}")
