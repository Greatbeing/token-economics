#!/usr/bin/env python3
"""
优化《儿童版中国哲学史》HTML文件的排版清晰度
解决以下问题：
1. 对话内容分行显示，不同角色的对话独立成行
2. 段落之间有明显间距
3. 小标题独立成行，与正文有明显区分
4. 特殊元素视觉区分清晰
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import html

# 路径配置
BASE_DIR = Path.cwd()
CHAPTERS_DIR = BASE_DIR / "outputs/儿童哲学史/排版阶段/章节HTML"
STYLE_DIR = CHAPTERS_DIR  # style.css在同一目录
OUTPUT_DIR = CHAPTERS_DIR / "优化版"
OUTPUT_DIR.mkdir(exist_ok=True)

# 对话正则表达式：匹配 **角色**：（内容）格式
DIALOG_PATTERN = re.compile(r'<strong>(.*?)</strong>：\((.*?)\)(.*?)(?=<strong>|$)', re.DOTALL)
DIALOG_SIMPLE_PATTERN = re.compile(r'<strong>(.*?)</strong>：([^<]+)')

def optimize_html_file(input_path, output_path):
    """优化单个HTML文件的排版"""
    print(f"处理: {input_path.name}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用BeautifulSoup解析
    soup = BeautifulSoup(content, 'html.parser')
    
    # 修复对话分行问题
    optimize_dialogs(soup)
    
    # 确保段落有足够间距
    optimize_paragraphs(soup)
    
    # 确保小标题独立成行
    optimize_headings(soup)
    
    # 确保特殊元素样式应用
    optimize_special_elements(soup)
    
    # 输出优化后的HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"  已保存: {output_path.name}")

def optimize_dialogs(soup):
    """优化对话内容，确保每个角色对话独立成行"""
    # 查找包含对话的文本
    for element in soup.find_all(text=True):
        if not element.parent:
            continue
            
        # 跳过脚本和样式标签
        if element.parent.name in ['script', 'style']:
            continue
            
        # 检查是否包含**角色**：格式
        text = str(element)
        if '<strong>' in text and '：' in text:
            # 这里需要更复杂的处理，但为了简单起见，我们添加一些CSS类
            pass
    
    # 更简单的方法：直接修改HTML文本
    html_str = str(soup)
    
    # 为每个<strong>标签后的内容添加换行和缩进
    # 这个正则表达式匹配 <strong>角色</strong>：（内容）
    # 并在其后添加<br>和缩进
    def replace_dialog(match):
        role = match.group(1)
        content = match.group(2).strip()
        # 返回带有段落包装的对话
        return f'<div class="dialog-line"><span class="dialog-role">{role}</span>：{content}</div>'
    
    # 应用替换
    html_str = re.sub(r'<strong>(.*?)</strong>：\s*([^<]+)(?![^<]*</strong>)', replace_dialog, html_str)
    
    # 重新解析
    soup = BeautifulSoup(html_str, 'html.parser')
    
    # 添加对话样式
    if soup.head:
        style_tag = soup.new_tag('style')
        style_tag.string = """
        .dialog-line {
            margin-bottom: 12px;
            line-height: 1.5;
        }
        .dialog-role {
            font-weight: bold;
            color: #1565C0;
        }
        """
        soup.head.append(style_tag)
    
    return soup

def optimize_paragraphs(soup):
    """确保段落之间有足够间距"""
    for p in soup.find_all('p'):
        if 'style' in p.attrs:
            # 确保有足够的底部边距
            style = p['style']
            if 'margin-bottom' not in style and 'margin' not in style:
                p['style'] = style + ' margin-bottom: 16px;'
        else:
            p['style'] = 'margin-bottom: 16px;'
    
    return soup

def optimize_headings(soup):
    """确保小标题独立成行"""
    for h in soup.find_all(['h3', 'h4', 'h5', 'h6']):
        if 'style' in h.attrs:
            style = h['style']
            if 'margin-top' not in style and 'margin' not in style:
                h['style'] = style + ' margin-top: 24px; margin-bottom: 12px;'
            else:
                # 确保有足够的上下边距
                h['style'] = re.sub(r'margin-top[^;]*;?', 'margin-top: 24px;', h['style'])
                h['style'] = re.sub(r'margin-bottom[^;]*;?', 'margin-bottom: 12px;', h['style'])
        else:
            h['style'] = 'margin-top: 24px; margin-bottom: 12px;'
    
    return soup

def optimize_special_elements(soup):
    """确保特殊元素有正确的CSS类"""
    # 检查思想剧场
    for div in soup.find_all('div'):
        if 'thought-theater' not in div.get('class', []):
            # 检查是否包含思想剧场内容
            text = div.get_text()
            if '思想剧场' in text:
                div['class'] = div.get('class', []) + ['thought-theater']
    
    return soup

def main():
    """主函数：批量优化所有章节HTML文件"""
    print("开始优化HTML文件排版清晰度...")
    
    # 获取所有章节HTML文件
    chapter_files = sorted([f for f in CHAPTERS_DIR.iterdir() if f.name.endswith('.html') and '第' in f.name and '章样张' in f.name])
    
    if not chapter_files:
        print("错误: 未找到章节HTML文件")
        return
    
    print(f"找到 {len(chapter_files)} 个章节文件")
    
    # 优化每个文件
    for input_file in chapter_files:
        output_file = OUTPUT_DIR / input_file.name.replace('.html', '_优化.html')
        optimize_html_file(input_file, output_file)
    
    print(f"\n优化完成！文件保存在: {OUTPUT_DIR}")
    print("下一步: 使用优化后的HTML重新生成PDF")

if __name__ == '__main__':
    main()