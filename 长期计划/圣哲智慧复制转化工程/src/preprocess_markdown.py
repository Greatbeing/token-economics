#!/usr/bin/env python3
"""
预处理Markdown文件，优化对话格式
确保对话内容有正确的分行和段落分隔
"""

import os
import re
from pathlib import Path

# 路径配置
BASE_DIR = Path.cwd()
INPUT_DIR = BASE_DIR / "outputs/儿童哲学史/优化阶段/backup_practice"
OUTPUT_DIR = BASE_DIR / "outputs/儿童哲学史/排版阶段/优化后Markdown"
OUTPUT_DIR.mkdir(exist_ok=True)

def preprocess_markdown(input_path, output_path):
    """预处理Markdown文件，优化对话格式"""
    print(f"处理: {input_path.name}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 处理对话行：将 **角色**：（内容）格式包装成独立段落
    # 正则表达式匹配 **角色**：（内容）
    # 注意：内容可能包含括号、标点等
    
    # 首先，我们确保每个对话行都是独立的段落
    # 在Markdown中，独立段落之间有空行
    
    # 查找所有对话行
    lines = content.split('\n')
    processed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 检查是否是对话行：包含 ** 和 ：，并且可能是对话格式
        if re.match(r'^\*\*.*?\*\*：', line):
            # 这是一个对话行
            # 确保前面有空行（如果不是第一个元素）
            if i > 0 and processed_lines and processed_lines[-1].strip() != '':
                processed_lines.append('')
            
            # 添加对话行
            processed_lines.append(line)
            
            # 确保后面有空行
            if i < len(lines) - 1 and lines[i+1].strip() != '':
                processed_lines.append('')
        else:
            # 普通行，直接添加
            processed_lines.append(lines[i])
        
        i += 1
    
    # 重新组合内容
    content = '\n'.join(processed_lines)
    
    # 2. 为对话添加自定义HTML包装
    # 使用正则表达式匹配 **角色**：（内容）并替换为HTML
    def replace_dialog(match):
        role = match.group(1)
        # 提取内容：可能包含括号和表情
        full_text = match.group(0)
        
        # 从 **角色**：后面开始是内容
        content_start = full_text.find('：') + 1
        dialog_content = full_text[content_start:].strip()
        
        # 返回HTML格式的对话
        return f'<div class="dialog-line">\n<span class="dialog-role">{role}</span>：{dialog_content}\n</div>'
    
    # 应用替换（使用更复杂的正则表达式）
    # 匹配格式：**角色**：（可能的括号内容）实际对话
    pattern = re.compile(r'^\*\*([^*]+)\*\*：([^\n]+)', re.MULTILINE)
    content = pattern.sub(replace_dialog, content)
    
    # 3. 确保其他特殊元素也有正确的标记
    # 思想剧场部分
    if '思想剧场' in content:
        # 在思想剧场部分周围添加div
        # 这是一个简化的实现
        sections = content.split('## 思想剧场：')
        if len(sections) > 1:
            content = sections[0] + '<div class="thought-theater">\n## 思想剧场：' + sections[1]
            # 找到思想剧场的结束（下一个二级标题或文件结束）
            # 这里简化处理
    
    # 保存处理后的文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  已保存: {output_path.name}")

def main():
    """主函数：预处理所有章节Markdown文件"""
    print("开始预处理Markdown文件，优化对话格式...")
    
    # 获取所有章节Markdown文件
    chapter_files = sorted([f for f in INPUT_DIR.iterdir() if f.name.endswith('.md') and '第' in f.name and '章优化稿' in f.name])
    
    if not chapter_files:
        print("错误: 未找到章节Markdown文件")
        return
    
    print(f"找到 {len(chapter_files)} 个章节文件")
    
    # 预处理每个文件
    for input_file in chapter_files:
        output_file = OUTPUT_DIR / input_file.name
        preprocess_markdown(input_file, output_file)
    
    print(f"\n预处理完成！文件保存在: {OUTPUT_DIR}")
    print("下一步: 使用预处理后的Markdown重新生成HTML和PDF")

if __name__ == '__main__':
    main()