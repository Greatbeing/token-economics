#!/usr/bin/env python3
"""
从HTML文件提取文本内容并转换为飞书Markdown格式 - 最终优化版
"""

import os
import re
from bs4 import BeautifulSoup, NavigableString, Tag

HTML_DIR = "./长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/优化版/"
OUTPUT_FILE = "./和古人一起想问题_完整版.md"

def clean_text(text):
    """清理文本"""
    if not text:
        return ""
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def extract_text_content(element):
    """递归提取纯文本"""
    if isinstance(element, NavigableString):
        return str(element)
    
    if element.name in ['script', 'style']:
        return ''
    
    if element.name == 'img':
        return ''
    
    texts = []
    for child in element.children:
        texts.append(extract_text_content(child))
    
    return ' '.join(texts)

def process_table(table):
    """处理表格"""
    rows = table.find_all('tr')
    if not rows:
        return ""
    
    table_data = []
    for row in rows:
        cells = row.find_all(['th', 'td'])
        row_data = [clean_text(cell.get_text()) for cell in cells]
        if row_data:
            table_data.append(row_data)
    
    if not table_data:
        return ""
    
    # 确定列数
    max_cols = max(len(row) for row in table_data)
    
    lines = []
    for i, row in enumerate(table_data):
        while len(row) < max_cols:
            row.append("")
        lines.append("| " + " | ".join(row) + " |")
        if i == 0:
            lines.append("| " + " | ".join(["---"] * max_cols) + " |")
    
    return "\n" + "\n".join(lines) + "\n"

def process_list(list_elem, ordered=False):
    """处理列表"""
    lines = []
    items = list_elem.find_all('li', recursive=False)
    for i, li in enumerate(items):
        text = clean_text(extract_text_content(li))
        if text:
            if ordered:
                lines.append(f"{i+1}. {text}")
            else:
                lines.append(f"- {text}")
    return "\n" + "\n".join(lines) + "\n" if lines else ""

def process_html(html_content):
    """处理HTML内容"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    for script in soup(["script", "style"]):
        script.decompose()
    
    body = soup.find('body')
    if not body:
        return ""
    
    result = []
    processed_elements = set()
    
    def get_text(elem):
        return clean_text(extract_text_content(elem))
    
    for element in body.descendants:
        if element in processed_elements:
            continue
        
        if not isinstance(element, Tag):
            continue
        
        # 跳过图片
        if element.name == 'img':
            alt = element.get('alt', '')
            if alt:
                result.append(f"\n> 🖼️ *{alt}*\n")
            processed_elements.add(element)
            continue
        
        # 标题
        if element.name == 'h2':
            text = get_text(element)
            if text and not text.startswith('第一章') and not text.startswith('第二章') and not text.startswith('第三章') and not text.startswith('第四章') and not text.startswith('第五章') and not text.startswith('第六章') and not text.startswith('第七章') and not text.startswith('第八章') and not text.startswith('第九章') and not text.startswith('第十章') and not text.startswith('第十一章') and not text.startswith('第十二章'):
                result.append(f"\n## {text}\n")
            processed_elements.add(element)
            continue
        
        if element.name == 'h3':
            text = get_text(element)
            if text:
                result.append(f"\n### {text}\n")
            processed_elements.add(element)
            continue
        
        if element.name == 'h4':
            text = get_text(element)
            if text:
                result.append(f"\n#### {text}\n")
            processed_elements.add(element)
            continue
        
        # 表格
        if element.name == 'table':
            table_md = process_table(element)
            if table_md:
                result.append(table_md)
            processed_elements.add(element)
            # 标记所有子元素
            for child in element.descendants:
                processed_elements.add(child)
            continue
        
        # 列表
        if element.name == 'ul':
            list_md = process_list(element, ordered=False)
            if list_md:
                result.append(list_md)
            processed_elements.add(element)
            for child in element.descendants:
                processed_elements.add(child)
            continue
        
        if element.name == 'ol':
            list_md = process_list(element, ordered=True)
            if list_md:
                result.append(list_md)
            processed_elements.add(element)
            for child in element.descendants:
                processed_elements.add(child)
            continue
        
        # 引用块
        if element.name == 'blockquote':
            text = get_text(element)
            if text:
                lines = [f"> {line}" for line in text.split('\n') if line.strip()]
                if lines:
                    result.append("\n" + "\n".join(lines) + "\n")
            processed_elements.add(element)
            for child in element.descendants:
                processed_elements.add(child)
            continue
        
        # 分割线
        if element.name == 'hr':
            result.append("\n---\n")
            processed_elements.add(element)
            continue
        
        # 段落 - 只处理顶层段落
        if element.name == 'p':
            # 检查是否有图片
            if element.find('img'):
                processed_elements.add(element)
                continue
            
            # 检查父级
            parent = element.parent
            if parent and parent.name in ['li', 'blockquote', 'td', 'th']:
                continue
            
            text = get_text(element)
            if text:
                result.append(f"\n{text}\n")
            processed_elements.add(element)
            continue
    
    # 合并并清理
    content = "".join(result)
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    return content

def process_all_chapters():
    """处理所有章节"""
    chapter_files = [
        ("第1章样张_优化.html", "第一章 万物之源：世界的本原是什么？"),
        ("第2章样张_优化.html", "第二章 知与不知：我们能认识世界吗？"),
        ("第3章样张_优化.html", "第三章 天人合一：人与自然的关系"),
        ("第4章样张_优化.html", "第四章 道法自然：顺应自然的智慧"),
        ("第5章样张_优化.html", "第五章 仁者爱人：儒家的人道精神"),
        ("第6章样张_优化.html", "第六章 兼爱非攻：墨家的和平理想"),
        ("第7章样张_优化.html", "第七章 无为而治：道家的政治哲学"),
        ("第8章样张_优化.html", "第八章 法不阿贵：法家的法治思想"),
        ("第9章样张_优化.html", "第九章 辩证思维：对立统一的智慧"),
        ("第10章样张_优化.html", "第十章 知行合一：认识与实践"),
        ("第11章样张_优化.html", "第十一章 理欲之辨：人性的思考"),
        ("第12章样张_优化.html", "第十二章 时代回响：传统与现代"),
    ]
    
    all_content = []
    
    for i, (filename, chapter_title) in enumerate(chapter_files, 1):
        filepath = os.path.join(HTML_DIR, filename)
        print(f"处理 {filename}...")
        
        if not os.path.exists(filepath):
            print(f"  警告：文件不存在")
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            markdown = process_html(html_content)
            
            # 添加章节标题和分隔
            all_content.append(f"\n---\n\n# {chapter_title}\n")
            all_content.append(markdown)
            
            print(f"  ✓ 完成 ({len(markdown)} 字符)")
            
        except Exception as e:
            print(f"  错误：{e}")
            import traceback
            traceback.print_exc()
    
    # 合并
    final_content = "".join(all_content)
    final_content = re.sub(r'\n{4,}', '\n\n\n', final_content)
    
    # 保存
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"\n✓ 已保存到 {OUTPUT_FILE}")
    print(f"  总字符数：{len(final_content)}")
    
    return OUTPUT_FILE

if __name__ == "__main__":
    process_all_chapters()
