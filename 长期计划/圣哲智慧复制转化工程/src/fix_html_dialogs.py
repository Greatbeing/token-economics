#!/usr/bin/env python3
"""
修复HTML文件中的对话分行问题
"""

import os
import re
from pathlib import Path

# 路径配置
BASE_DIR = Path.cwd()
INPUT_DIR = BASE_DIR / "outputs/儿童哲学史/排版阶段/章节HTML"
OUTPUT_DIR = INPUT_DIR / "修正版"
OUTPUT_DIR.mkdir(exist_ok=True)

def fix_dialog_lines(html_content):
    """修复对话行，确保每个角色对话独立成行并有足够间距"""
    
    # 正则表达式匹配 <strong>角色</strong>：（内容）
    # 内容可能包含括号、标点等，直到下一个<strong>或行结束
    pattern = re.compile(r'(<strong>.*?</strong>：[^<]+)(?=<strong>|$)', re.DOTALL)
    
    def replace_dialog(match):
        dialog_line = match.group(1).strip()
        # 如果对话行已经包含HTML标签，保留它们
        # 否则，添加段落标签和间距
        return f'<div class="dialog-line">{dialog_line}</div>\n'
    
    # 应用替换
    result = pattern.sub(replace_dialog, html_content)
    
    # 确保对话行之间有间距
    result = result.replace('</div>\n<strong>', '</div>\n\n<strong>')
    result = result.replace('</div><strong>', '</div>\n\n<strong>')
    
    return result

def add_dialog_css(html_content):
    """添加对话CSS到HTML头部"""
    
    # 检查是否已有style标签
    if '<style>' in html_content:
        # 在现有style标签前添加对话CSS
        dialog_css = """
        /* 对话样式 */
        .dialog-line {
            margin-bottom: 16px;
            padding-left: 20px;
            border-left: 3px solid #81D4FA;
            line-height: 1.6;
        }
        
        .dialog-line strong {
            color: #1565C0;
            font-weight: bold;
        }
        
        .thought-theater .dialog-line {
            border-left-color: #FFCC80;
        }
        
        .thought-theater .dialog-line strong {
            color: #FF9800;
        }
        """
        
        # 找到第一个style标签，在它前面插入
        lines = html_content.split('\n')
        for i, line in enumerate(lines):
            if '<style>' in line:
                # 插入对话CSS
                lines.insert(i, dialog_css)
                break
        
        return '\n'.join(lines)
    
    return html_content

def process_html_file(input_file, output_file):
    """处理单个HTML文件"""
    print(f"处理: {input_file.name}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复对话行
    content = fix_dialog_lines(content)
    
    # 添加对话CSS
    content = add_dialog_css(content)
    
    # 保存文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  已保存: {output_file.name}")

def main():
    """主函数：批量处理所有章节HTML文件"""
    print("开始修复HTML文件对话分行问题...")
    
    # 获取所有章节HTML文件
    chapter_files = sorted([f for f in INPUT_DIR.iterdir() if f.name.endswith('.html') and '第' in f.name and '章样张' in f.name])
    
    if not chapter_files:
        print("错误: 未找到章节HTML文件")
        return
    
    print(f"找到 {len(chapter_files)} 个章节文件")
    
    # 处理每个文件
    for input_file in chapter_files:
        output_file = OUTPUT_DIR / input_file.name.replace('.html', '_fixed.html')
        process_html_file(input_file, output_file)
    
    print(f"\n修复完成！文件保存在: {OUTPUT_DIR}")
    print("下一步: 使用修正后的HTML重新生成PDF")

if __name__ == '__main__':
    main()