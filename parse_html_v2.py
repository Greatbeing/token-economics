#!/usr/bin/env python3
"""
从HTML文件中提取《和古人一起想问题》的内容并转换为Markdown格式
优化版：移除base64图片，正确提取章节标题
"""

import os
import re
from bs4 import BeautifulSoup

def remove_base64_images(html_content):
    """移除base64图片数据，保留alt文本"""
    # 移除data:image类型的src
    html_content = re.sub(r'src="data:image/[^"]*', 'src=""', html_content)
    # 移除base64图片标签但保留alt文本
    pattern = r'<img[^>]*alt="([^"]*)"[^>]*src=""[^>]*>'
    html_content = re.sub(pattern, r'[图片: \1]', html_content)
    return html_content

def extract_section_content(soup, section_id):
    """提取特定section的内容"""
    section = soup.find(id=section_id)
    if not section:
        return ""
    
    # 找到section的父div或下一个兄弟元素直到下一个section
    content_parts = []
    current = section.find_next(['h2', 'h3', 'p', 'ul', 'ol', 'table', 'div'])
    
    while current:
        # 检查是否到达下一个主section
        if current.name in ['h2', 'h3']:
            # 检查是否是新的主section
            if current.get('id') and current.get('id') != section_id:
                break
            # 或者检查文本内容是否是新的section标题
            text = current.get_text().strip()
            if any(keyword in text for keyword in ['思想剧场', '古人说', '想一想', '全球望远镜', '实践练习', '智慧探险地图']):
                break
        
        content_parts.append(str(current))
        current = current.find_next(['h2', 'h3', 'p', 'ul', 'ol', 'table', 'div'])
    
    return '\n'.join(content_parts)

def html_to_markdown(element):
    """将HTML元素转换为Markdown"""
    if not element:
        return ""
    
    text = str(element)
    soup = BeautifulSoup(text, 'html.parser')
    
    result = []
    
    for child in soup.children:
        if child.name is None:
            # 文本节点
            text_content = str(child).strip()
            if text_content:
                result.append(text_content)
        elif child.name == 'h2':
            text = child.get_text().strip()
            result.append(f"\n## {text}\n")
        elif child.name == 'h3':
            text = child.get_text().strip()
            result.append(f"\n### {text}\n")
        elif child.name == 'h4':
            text = child.get_text().strip()
            result.append(f"\n#### {text}\n")
        elif child.name == 'p':
            text = child.get_text().strip()
            if text:
                result.append(f"\n{text}\n")
        elif child.name == 'ul':
            for li in child.find_all('li', recursive=False):
                text = li.get_text().strip()
                if text:
                    result.append(f"- {text}")
        elif child.name == 'ol':
            for i, li in enumerate(child.find_all('li', recursive=False), 1):
                text = li.get_text().strip()
                if text:
                    result.append(f"{i}. {text}")
        elif child.name == 'table':
            # 转换表格
            rows = child.find_all('tr')
            if rows:
                md_table = []
                for i, row in enumerate(rows):
                    cells = row.find_all(['th', 'td'])
                    cell_texts = [cell.get_text().strip() for cell in cells]
                    md_table.append('| ' + ' | '.join(cell_texts) + ' |')
                    if i == 0:
                        md_table.append('| ' + ' | '.join(['---'] * len(cells)) + ' |')
                result.append('\n' + '\n'.join(md_table) + '\n')
        elif child.name == 'blockquote':
            text = child.get_text().strip()
            lines = text.split('\n')
            quoted = '\n'.join([f"> {line.strip()}" for line in lines if line.strip()])
            result.append(f"\n{quoted}\n")
        elif child.name == 'img':
            alt = child.get('alt', '')
            if alt:
                result.append(f"\n[图片: {alt}]\n")
        elif child.name == 'strong' or child.name == 'b':
            text = child.get_text().strip()
            if text:
                result.append(f"**{text}**")
        elif child.name == 'em' or child.name == 'i':
            text = child.get_text().strip()
            if text:
                result.append(f"*{text}*")
        else:
            # 递归处理其他标签
            result.append(html_to_markdown(child))
    
    return ''.join(result)

def parse_html_file(filepath):
    """解析单个HTML文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 移除base64图片
    html_content = remove_base64_images(html_content)
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 提取章节标题
    chapter_title = ""
    first_h2 = soup.find('h2')
    if first_h2:
        chapter_title = first_h2.get_text().strip()
        # 尝试提取"第一章 xxx"格式
        title_text = chapter_title
        if '：' in title_text:
            parts = title_text.split('：')
            if '章' in parts[0]:
                chapter_title = parts[0]
    
    # 提取正文内容
    body = soup.find('body')
    if not body:
        return chapter_title, ""
    
    # 获取所有主要内容元素
    content = []
    for element in body.children:
        if element.name in ['h2', 'h3', 'h4', 'p', 'ul', 'ol', 'table', 'blockquote', 'div']:
            # 跳过style标签
            if element.name == 'style':
                continue
            
            md = html_to_markdown(element)
            if md.strip():
                content.append(md)
    
    markdown = '\n'.join(content)
    
    # 清理多余空行
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    markdown = markdown.strip()
    
    return chapter_title, markdown

def find_chapter_title(markdown, chapter_num):
    """从Markdown内容中找到章节标题"""
    lines = markdown.split('\n')
    for line in lines[:50]:  # 查找前50行
        line = line.strip()
        if line.startswith('## '):
            # 检查是否包含章节信息
            text = line.replace('## ', '')
            if f'第{chapter_num}章' in text or f'第{chapter_num}节' in text:
                # 提取章节标题
                if '：' in text:
                    return text.split('：')[0] + '：' + text.split('：')[1].split('思想剧场')[0].strip()
                return text
        if '思想剧场' in line and '：' in line:
            # 尝试从"思想剧场：xxx"之前找标题
            parts = line.split('思想剧场')
            if len(parts) > 1:
                before = parts[0].replace('## ', '').strip()
                if before and '第' in before:
                    return before
    
    return f"第{chapter_num}章"

def process_all_chapters():
    """处理所有章节"""
    html_dir = "./长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/优化版/"
    
    html_files = sorted([f for f in os.listdir(html_dir) if f.endswith('.html')],
                       key=lambda x: int(re.search(r'第(\d+)章', x).group(1)) if re.search(r'第(\d+)章', x) else 0)
    
    all_content = []
    titles = []
    
    for i, html_file in enumerate(html_files, 1):
        filepath = os.path.join(html_dir, html_file)
        print(f"处理: {html_file}")
        
        try:
            title, markdown = parse_html_file(filepath)
            
            # 更准确地提取章节标题
            actual_title = find_chapter_title(markdown, i)
            if actual_title:
                title = actual_title
            
            titles.append(title)
            all_content.append(markdown)
            
            print(f"  -> 标题: {title}")
            print(f"  -> 长度: {len(markdown)} 字符")
            
        except Exception as e:
            print(f"  -> 错误: {e}")
            import traceback
            traceback.print_exc()
    
    return all_content, titles

def save_final_markdown(contents, titles, output_file):
    """保存最终的Markdown文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (title, content) in enumerate(zip(titles, contents), 1):
            f.write(f"\n\n{'='*60}\n\n")
            f.write(f"## {title}\n\n")
            f.write(content)
    
    print(f"\n已保存: {output_file}")

if __name__ == "__main__":
    contents, titles = process_all_chapters()
    save_final_markdown(contents, titles, "./和古人一起想问题.md")
    
    total_chars = sum(len(c) for c in contents)
    print(f"\n总计: {len(contents)} 章, {total_chars} 字符")
    
    print("\n章节列表:")
    for i, title in enumerate(titles, 1):
        print(f"  {i}. {title}")
