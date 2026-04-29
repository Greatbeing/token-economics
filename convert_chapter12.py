#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第12章 Markdown to HTML 转换器
- 对话分行处理
- 小标题独立成行
- 场景描述、思维剧场等特殊元素处理
"""

import re
import os

def convert_dialog_line(text):
    """识别并转换对话格式 **人物**：（对话内容）"""
    # 对话格式：多个**人物**：（内容）或 **人物**：（内容）
    pattern = r'\*\*([^*]+?)\*\*[：:]([^\n*]+)'
    
    def replace_dialog(match):
        speaker = match.group(1).strip()
        content = match.group(2).strip()
        # 清理表情符号等
        content = re.sub(r'🌟', '', content)
        return f'<div class="dialog-line"><strong class="speaker">{speaker}：</strong>{content}</div>'
    
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # 检查是否是纯对话行（只有对话，没有其他内容）
        dialog_match = re.match(r'^(\*\*[^*]+?\*\*[：:].+)$', line.strip())
        if dialog_match:
            # 尝试解析对话
            inner = line.strip()
            match = re.match(r'\*\*([^*]+?)\*\*[：:](.*)', inner)
            if match:
                speaker = match.group(1).strip()
                content = match.group(2).strip()
                # 清理表情符号等
                content = re.sub(r'🌟', '', content)
                result.append(f'<div class="dialog-line"><strong class="speaker">{speaker}：</strong>{content}</div>')
                i += 1
                continue
        
        # 检查是否是混合行（对话+其他内容）
        hybrid_match = re.search(r'\*\*([^*]+?)\*\*[：:]([^\n]+)', line)
        if hybrid_match and not line.strip().startswith('**') and not line.strip().startswith('-') and not line.strip().startswith('#'):
            # 保持原样，因为这行包含其他内容
            pass
        
        result.append(line)
        i += 1
    
    return '\n'.join(result)

def convert_markdown_to_html(markdown_content):
    """将Markdown内容转换为HTML"""
    lines = markdown_content.split('\n')
    html_lines = []
    in_thought_theater = False
    in_stage_direction = False
    in_think_box = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # 跳过重复的章标题（保留第一个）
        if stripped.startswith('# 第十二章') and i > 0:
            i += 1
            continue
        
        # 处理思想剧场开始
        if '### 思想剧场' in stripped:
            html_lines.append('<div class="thought-theater">')
            in_thought_theater = True
            i += 1
            continue
        
        # 处理场景描述
        if stripped.startswith('**时间**：') or stripped.startswith('**地点**：') or stripped.startswith('**人物**：') or stripped.startswith('**场景**：'):
            html_lines.append(f'<div class="stage-direction">{stripped}</div>')
            i += 1
            continue
        
        # 处理场景闪回
        if '场景闪回' in stripped:
            html_lines.append(f'<div class="stage-direction">{stripped}</div>')
            i += 1
            continue
        
        # 处理h1标题
        if stripped.startswith('# ') and not stripped.startswith('## ') and not stripped.startswith('### '):
            title = stripped.lstrip('# ').strip()
            # 移除重复的章标题
            if '第十二章' in title and i > 5:
                i += 1
                continue
            html_lines.append(f'<h1>{title}</h1>')
            i += 1
            continue
        
        # 处理h2标题（课时/节）
        if stripped.startswith('## '):
            title = stripped.lstrip('# ').strip()
            html_lines.append(f'<h2>{title}</h2>')
            i += 1
            continue
        
        # 处理h3标题（小节/思想剧场标题等）
        if stripped.startswith('### '):
            title = stripped.lstrip('# ').strip()
            # 检查是否是"别再问了"这种样式
            if '别再问' in title:
                html_lines.append(f'<h3 class="question-header">{title}</h3>')
            else:
                html_lines.append(f'<h3>{title}</h3>')
            i += 1
            continue
        
        # 处理h4标题（古人这么做等）
        if stripped.startswith('#### '):
            title = stripped.lstrip('# ').strip()
            html_lines.append(f'<h4>{title}</h4>')
            i += 1
            continue
        
        # 处理分隔线
        if stripped.startswith('---'):
            # 检查是否需要关闭思想剧场
            if in_thought_theater:
                html_lines.append('</div>')  # 关闭 thought-theater
                in_thought_theater = False
            html_lines.append('<hr>')
            i += 1
            continue
        
        # 处理对话行 - **人物**：（对话内容）
        dialog_match = re.match(r'^(\*\*)([^*]+)(\*\*[：:])(.+)$', stripped)
        if dialog_match:
            speaker = dialog_match.group(2).strip()
            content = dialog_match.group(4).strip()
            # 清理表情符号
            content = re.sub(r'🌟', '', content)
            html_lines.append(f'<div class="dialog-line"><strong class="speaker">{speaker}：</strong>{content}</div>')
            i += 1
            continue
        
        # 处理列表项
        if stripped.startswith('- ') or stripped.startswith('* '):
            content = stripped[2:].strip()
            # 清理表情符号
            content = re.sub(r'🌟', '', content)
            html_lines.append(f'<li>{content}</li>')
            i += 1
            continue
        
        # 处理有序列表
        list_match = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if list_match:
            content = list_match.group(2).strip()
            # 清理表情符号
            content = re.sub(r'🌟', '', content)
            html_lines.append(f'<li>{content}</li>')
            i += 1
            continue
        
        # 处理表格
        if stripped.startswith('|'):
            # 收集整个表格
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            # 简单处理表格
            html_lines.append(convert_table(table_lines))
            continue
        
        # 处理引用/重点
        if stripped.startswith('>'):
            content = stripped.lstrip('> ').strip()
            html_lines.append(f'<blockquote>{content}</blockquote>')
            i += 1
            continue
        
        # 处理普通段落
        if stripped:
            # 清理表情符号
            content = re.sub(r'🌟', '', stripped)
            html_lines.append(f'<p>{content}</p>')
        
        i += 1
    
    # 确保关闭未关闭的标签
    if in_thought_theater:
        html_lines.append('</div>')
    
    return '\n'.join(html_lines)

def convert_table(table_lines):
    """将Markdown表格转换为HTML"""
    if not table_lines:
        return ''
    
    rows = []
    for line in table_lines:
        # 解析行
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        row_cells = []
        for cell in cells:
            # 清理表情符号
            cell = re.sub(r'🌟', '', cell)
            row_cells.append(f'<td>{cell}</td>')
        rows.append(f'<tr>{"".join(row_cells)}</tr>')
    
    return f'<table>{"".join(rows)}</table>'

def create_html_document(title, content, css_path='style_mobile.css'):
    """创建完整的HTML文档"""
    html = f'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN" xml:lang="zh-CN">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
    <title>{title}</title>
    <link rel="stylesheet" href="{css_path}">
    <style>
        body {{
            font-family: "宋体", "SimSun", serif;
            font-size: 12pt;
            line-height: 1.8;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            font-family: "黑体", "SimHei", sans-serif;
            font-size: 22pt;
            text-align: center;
            color: #2c3e50;
            margin: 1.5em 0;
            page-break-after: avoid;
        }}
        h2 {{
            font-family: "黑体", "SimHei", sans-serif;
            font-size: 16pt;
            color: #34495e;
            margin: 2em 0 0.8em 0;
            border-left: 4px solid #3498db;
            padding-left: 0.5em;
            page-break-after: avoid;
        }}
        h3 {{
            font-family: "黑体", "SimHei", sans-serif;
            font-size: 14pt;
            color: #2c3e50;
            margin: 1.5em 0 0.5em 0;
            page-break-after: avoid;
        }}
        h4 {{
            font-family: "黑体", "SimHei", sans-serif;
            font-size: 12pt;
            color: #34495e;
            margin: 1.2em 0 0.4em 0;
            page-break-after: avoid;
        }}
        p {{
            margin: 0.5em 0;
            text-indent: 2em;
        }}
        .dialog-line {{
            margin: 0.8em 0;
            padding: 0.5em 1em;
            border-left: 3px solid #e74c3c;
            background-color: #fef9f9;
            text-indent: 0;
            line-height: 1.8;
        }}
        .dialog-line .speaker {{
            color: #c0392b;
            font-weight: bold;
        }}
        .thought-theater {{
            background-color: #f0f7ff;
            border: 1px solid #3498db;
            border-radius: 8px;
            padding: 1.5em;
            margin: 1.5em 0;
            page-break-inside: avoid;
        }}
        .stage-direction {{
            font-style: italic;
            color: #7f8c8d;
            margin: 0.5em 0;
            text-indent: 0;
        }}
        .think-box {{
            background-color: #fff8e1;
            border: 1px solid #f39c12;
            border-radius: 8px;
            padding: 1em 1.5em;
            margin: 1.5em 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
            font-size: 11pt;
        }}
        table th {{
            background-color: #34495e;
            color: white;
            padding: 0.5em;
            text-align: left;
        }}
        table td {{
            border: 1px solid #bdc3c7;
            padding: 0.5em;
            vertical-align: top;
        }}
        li {{
            margin: 0.3em 0;
            margin-left: 1em;
        }}
        blockquote {{
            background-color: #f5f5f5;
            border-left: 4px solid #9b59b6;
            padding: 0.5em 1em;
            margin: 1em 0;
            font-style: italic;
        }}
        hr {{
            border: none;
            border-top: 1px dashed #bdc3c7;
            margin: 2em 0;
        }}
        .question-header {{
            background-color: #fff3e0;
            padding: 0.5em;
            border-radius: 4px;
            color: #e65100;
        }}
    </style>
</head>
<body>
    <div class="book-content">
        {content}
    </div>
</body>
</html>'''
    return html

if __name__ == '__main__':
    # 读取Markdown文件
    md_path = '长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/优化阶段/第十二章优化稿.md'
    
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 转换
    html_content = convert_markdown_to_html(md_content)
    
    # 创建完整HTML文档
    full_html = create_html_document(
        '第十二章：我们为什么要学哲学？',
        html_content
    )
    
    # 保存HTML
    output_dir = '长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/移动端适配/chapters_fixed'
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, '第12章_修复版.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f'HTML已生成: {output_path}')
