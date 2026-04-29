#!/usr/bin/env python3
"""
从HTML文件提取文本内容并转换为飞书Markdown格式
"""

import os
import re
from html.parser import HTMLParser
from bs4 import BeautifulSoup

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

def html_to_markdown(html_content, chapter_num):
    """将HTML转换为Markdown"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 移除script和style标签
    for script in soup(["script", "style"]):
        script.decompose()
    
    markdown_parts = []
    
    # 遍历body中的所有元素
    body = soup.find('body')
    if not body:
        return ""
    
    for element in body.children:
        if element.name is None:
            # 文本节点
            text = str(element).strip()
            if text:
                markdown_parts.append(text)
            continue
        
        if element.name == 'h2':
            # 二级标题
            text = element.get_text().strip()
            if text:
                markdown_parts.append(f"\n## {text}\n")
        
        elif element.name == 'h3':
            # 三级标题
            text = element.get_text().strip()
            if text:
                markdown_parts.append(f"\n### {text}\n")
        
        elif element.name == 'h4':
            # 四级标题
            text = element.get_text().strip()
            if text:
                markdown_parts.append(f"\n#### {text}\n")
        
        elif element.name == 'p':
            # 段落
            # 检查是否包含图片
            img = element.find('img')
            if img:
                # 跳过图片，添加文字描述
                alt = img.get('alt', '')
                if alt:
                    markdown_parts.append(f"\n> 📷 [{alt}]\n")
                continue
            
            text = element.get_text().strip()
            if text:
                # 检查是否有特殊的div class
                parent_div = element.find_parent('div', class_=True)
                if parent_div:
                    div_class = parent_div.get('class', [])
                    if 'thought-theater' in div_class:
                        # 思想剧场
                        markdown_parts.append(f"\n{text}\n")
                    elif 'ancient-wisdom' in div_class:
                        # 古人说
                        markdown_parts.append(f"\n> **古人的智慧：** {text}\n")
                    elif 'think-section' in div_class:
                        # 想一想
                        markdown_parts.append(f"\n🤔 **想一想：** {text}\n")
                    elif 'global-telescope' in div_class:
                        # 全球望远镜
                        markdown_parts.append(f"\n🌍 **全球望远镜：** {text}\n")
                    elif 'practice-section' in div_class:
                        # 实践练习
                        markdown_parts.append(f"\n✍️ **实践练习：** {text}\n")
                    else:
                        markdown_parts.append(f"\n{text}\n")
                else:
                    markdown_parts.append(f"\n{text}\n")
        
        elif element.name == 'ul':
            # 无序列表
            for li in element.find_all('li', recursive=False):
                text = li.get_text().strip()
                if text:
                    markdown_parts.append(f"- {text}")
            markdown_parts.append("")
        
        elif element.name == 'ol':
            # 有序列表
            for i, li in enumerate(element.find_all('li', recursive=False), 1):
                text = li.get_text().strip()
                if text:
                    markdown_parts.append(f"{i}. {text}")
            markdown_parts.append("")
        
        elif element.name == 'table':
            # 表格
            markdown_parts.append("")
            rows = element.find_all('tr')
            if rows:
                # 处理表头
                header_row = rows[0]
                headers = [th.get_text().strip() or td.get_text().strip() 
                          for th, td in zip(header_row.find_all('th'), header_row.find_all('td'))]
                if headers:
                    markdown_parts.append("| " + " | ".join(headers) + " |")
                    markdown_parts.append("| " + " | ".join(["---"] * len(headers)) + " |")
                
                # 处理数据行
                for row in rows[1:]:
                    cells = [td.get_text().strip() for td in row.find_all('td')]
                    if cells:
                        markdown_parts.append("| " + " | ".join(cells) + " |")
            markdown_parts.append("")
        
        elif element.name == 'blockquote':
            # 引用
            text = element.get_text().strip()
            if text:
                lines = text.split('\n')
                for line in lines:
                    if line.strip():
                        markdown_parts.append(f"> {line.strip()}")
                markdown_parts.append("")
        
        elif element.name == 'div':
            # 处理div容器
            div_class = element.get('class', [])
            
            if 'thought-theater' in div_class:
                # 思想剧场内容
                text = element.get_text().strip()
                # 移除图片标记
                text = re.sub(r'\[.*?\]', '', text)
                text = clean_text(text)
                if text:
                    markdown_parts.append(f"\n{text}\n")
            
            elif 'ancient-wisdom' in div_class:
                # 古人说
                text = element.get_text().strip()
                text = clean_text(text)
                if text:
                    markdown_parts.append(f"\n> 💬 **古人的智慧**\n>\n> {text}\n")
            
            elif 'think-section' in div_class:
                # 想一想
                text = element.get_text().strip()
                text = clean_text(text)
                if text:
                    markdown_parts.append(f"\n<callout emoji=\"🤔\" background-color=\"light-blue\">\n**想一想**\n\n{text}\n</callout>\n")
            
            elif 'global-telescope' in div_class:
                # 全球望远镜
                text = element.get_text().strip()
                text = clean_text(text)
                if text:
                    markdown_parts.append(f"\n<callout emoji=\"🌍\" background-color=\"light-green\">\n**全球望远镜**\n\n{text}\n</callout>\n")
            
            elif 'practice-section' in div_class:
                # 实践练习
                text = element.get_text().strip()
                text = clean_text(text)
                if text:
                    markdown_parts.append(f"\n<callout emoji=\"✍️\" background-color=\"light-yellow\">\n**实践练习**\n\n{text}\n</callout>\n")
            
            elif 'wisdom-map' in div_class:
                # 智慧探险地图
                text = element.get_text().strip()
                text = clean_text(text)
                if text:
                    markdown_parts.append(f"\n<callout emoji=\"🗺️\" background-color=\"light-blue\">\n**智慧探险地图**\n\n{text}\n</callout>\n")
            
            else:
                # 普通div，递归处理
                for child in element.children:
                    if child.name == 'p':
                        img = child.find('img')
                        if img:
                            alt = img.get('alt', '')
                            if alt:
                                markdown_parts.append(f"\n> 📷 [{alt}]\n")
                            continue
                        text = child.get_text().strip()
                        if text:
                            markdown_parts.append(f"\n{text}\n")
                    elif child.name == 'h2':
                        text = child.get_text().strip()
                        if text:
                            markdown_parts.append(f"\n## {text}\n")
                    elif child.name == 'h3':
                        text = child.get_text().strip()
                        if text:
                            markdown_parts.append(f"\n### {text}\n")
                    elif child.name == 'h4':
                        text = child.get_text().strip()
                        if text:
                            markdown_parts.append(f"\n#### {text}\n")
        
        elif element.name == 'img':
            # 图片标签，用文字描述替代
            alt = element.get('alt', '')
            if alt:
                markdown_parts.append(f"\n> 📷 [{alt}]\n")
        
        elif element.name == 'hr':
            # 分割线
            markdown_parts.append("\n---\n")
        
        elif element.name == 'br':
            # 换行
            markdown_parts.append("\n")
    
    return "\n".join(markdown_parts)


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
            continue
    
    # 合并所有内容
    final_content = "\n".join(all_content)
    
    # 清理多余空行
    final_content = re.sub(r'\n{4,}', '\n\n\n', final_content)
    
    # 保存到文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"\n✓ 所有章节已合并保存到 {OUTPUT_FILE}")
    print(f"  文件大小：{len(final_content)} 字符")
    
    return OUTPUT_FILE


if __name__ == "__main__":
    process_all_chapters()
