#!/usr/bin/env python3
"""
从HTML文件提取文本内容并转换为飞书Markdown格式 - 优化版
"""

import os
import re
from bs4 import BeautifulSoup, NavigableString

# HTML文件目录
HTML_DIR = "./长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/优化版/"

# 输出文件
OUTPUT_FILE = "./和古人一起想问题_完整版.md"

def clean_text(text):
    """清理文本中的多余空白"""
    if not text:
        return ""
    # 移除多余的空白字符
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()

def process_element(element, in_div=None):
    """递归处理HTML元素"""
    result = []
    
    if isinstance(element, NavigableString):
        text = str(element).strip()
        if text and text not in ['\n', '\r\n']:
            return [text]
        return []
    
    if element.name == 'img':
        # 图片用文字描述替代
        alt = element.get('alt', '')
        if alt:
            return [f"\n> 🖼️ **场景图：{alt}**\n"]
        return []
    
    if element.name == 'h2':
        text = element.get_text().strip()
        if text:
            return [f"\n## {text}\n"]
    
    if element.name == 'h3':
        text = element.get_text().strip()
        if text:
            return [f"\n### {text}\n"]
    
    if element.name == 'h4':
        text = element.get_text().strip()
        if text:
            return [f"\n#### {text}\n"]
    
    if element.name == 'p':
        # 跳过包含图片的段落
        if element.find('img'):
            return []
        text = element.get_text().strip()
        if text:
            # 检查父级div的class
            parent_div = element.find_parent('div', class_=True)
            if parent_div:
                div_class = ' '.join(parent_div.get('class', []))
                if 'ancient-wisdom' in div_class:
                    return [f"\n> 💬 **古人的智慧**\n>\n> {text}\n"]
                elif 'think-section' in div_class:
                    return [f"\n<callout emoji=\"🤔\" background-color=\"light-blue\">\n**想一想**\n\n{text}\n</callout>\n"]
                elif 'global-telescope' in div_class:
                    return [f"\n<callout emoji=\"🌍\" background-color=\"light-green\">\n**全球望远镜**\n\n{text}\n</callout>\n"]
                elif 'practice-section' in div_class:
                    return [f"\n<callout emoji=\"✍️\" background-color=\"light-yellow\">\n**实践练习**\n\n{text}\n</callout>\n"]
            return [f"\n{text}\n"]
        return []
    
    if element.name == 'ul':
        items = []
        for li in element.find_all('li', recursive=False):
            text = li.get_text().strip()
            if text:
                items.append(f"- {text}")
        if items:
            return ["\n"] + items + [""]
        return []
    
    if element.name == 'ol':
        items = []
        for i, li in enumerate(element.find_all('li', recursive=False), 1):
            text = li.get_text().strip()
            if text:
                items.append(f"{i}. {text}")
        if items:
            return ["\n"] + items + [""]
        return []
    
    if element.name == 'table':
        table_md = ["\n"]
        rows = element.find_all('tr')
        if rows:
            # 处理所有行
            all_rows = []
            for row in rows:
                cells = []
                # 处理th和td
                for cell in row.find_all(['th', 'td']):
                    text = cell.get_text().strip()
                    cells.append(text)
                if cells:
                    all_rows.append(cells)
            
            if all_rows:
                # 确定列数
                max_cols = max(len(row) for row in all_rows)
                
                # 输出所有行
                for i, row in enumerate(all_rows):
                    # 补齐列数
                    while len(row) < max_cols:
                        row.append("")
                    table_md.append("| " + " | ".join(row) + " |")
                    if i == 0:
                        table_md.append("| " + " | ".join(["---"] * max_cols) + " |")
        table_md.append("")
        return table_md
    
    if element.name == 'blockquote':
        text = element.get_text().strip()
        if text:
            lines = text.split('\n')
            quote_lines = [f"> {line.strip()}" for line in lines if line.strip()]
            return ["\n"] + quote_lines + [""]
        return []
    
    if element.name == 'hr':
        return ["\n---\n"]
    
    if element.name == 'br':
        return []
    
    # 处理div
    if element.name == 'div':
        div_class = ' '.join(element.get('class', []))
        
        # 特殊div的处理
        if 'thought-theater' in div_class:
            result.append("\n**🎭 思想剧场**\n")
        elif 'ancient-wisdom' in div_class:
            result.append("\n**💬 古人说**\n")
        elif 'think-section' in div_class:
            result.append("\n**🤔 想一想**\n")
        elif 'global-telescope' in div_class:
            result.append("\n**🌍 全球望远镜**\n")
        elif 'practice-section' in div_class:
            result.append("\n**✍️ 实践练习**\n")
        elif 'wisdom-map' in div_class:
            result.append("\n**🗺️ 智慧探险地图**\n")
        
        # 递归处理子元素
        for child in element.children:
            result.extend(process_element(child, div_class))
        
        return result
    
    # 其他元素，递归处理子元素
    for child in element.children:
        result.extend(process_element(child, in_div))
    
    return result


def html_to_markdown(html_content, chapter_num):
    """将HTML转换为Markdown"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 移除script和style标签
    for script in soup(["script", "style"]):
        script.decompose()
    
    # 获取body
    body = soup.find('body')
    if not body:
        return ""
    
    # 处理所有元素
    result = process_element(body)
    
    # 合并结果
    markdown = "".join(result)
    
    # 清理多余空行
    markdown = re.sub(r'\n{4,}', '\n\n\n', markdown)
    
    return markdown


def process_all_chapters():
    """处理所有章节"""
    all_content = []
    
    # 章节文件名
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
    
    for i, (filename, chapter_title) in enumerate(chapter_files, 1):
        filepath = os.path.join(HTML_DIR, filename)
        print(f"处理 {filename}...")
        
        if not os.path.exists(filepath):
            print(f"  警告：文件不存在 {filepath}")
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 转换为Markdown
            markdown = html_to_markdown(html_content, i)
            
            # 添加章节分隔
            all_content.append(f"\n---\n\n# {chapter_title}\n")
            all_content.append(markdown)
            
            print(f"  ✓ 完成")
            
        except Exception as e:
            print(f"  错误：{e}")
            import traceback
            traceback.print_exc()
            continue
    
    # 合并所有内容
    final_content = "".join(all_content)
    
    # 清理格式
    final_content = re.sub(r'\n{4,}', '\n\n\n', final_content)
    final_content = re.sub(r'---\n\n---', '---', final_content)
    
    # 保存到文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"\n✓ 所有章节已合并保存到 {OUTPUT_FILE}")
    print(f"  文件大小：{len(final_content)} 字符")
    
    return OUTPUT_FILE


if __name__ == "__main__":
    process_all_chapters()
