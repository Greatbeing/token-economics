#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown转HTML转换器 - 儿童哲学史
批量将Markdown文件转换为HTML，并插入对应章节图片
"""

import re
import os
from pathlib import Path

# 章节配置
CHAPTERS = [
    ("第一章优化稿.md", "第一章 世界是从哪儿来的？", "ch1", 4),
    ("第二章优化稿.md", "第二章 什么是对？什么是错？", "ch2", 4),
    ("第三章优化稿.md", "第三章 人应该追求什么？", "ch3", 4),
    ("第四章优化稿.md", "第四章 什么是真正的自由？", "ch4", 4),
    ("第五章优化稿.md", "第五章 人与自然应该如何相处？", "ch5", 4),
    ("第六章优化稿.md", "第六章 人应该如何看待自己？", "ch6", 4),
    ("第七章优化稿.md", "第七章 什么是真正的勇敢？", "ch7", 4),
    ("第八章优化稿.md", "第八章 人应该如何面对困境？", "ch8", 4),
    ("第九章优化稿.md", "第九章 什么是真正的美德？", "ch9", 4),
    ("第十章优化稿.md", "第十章 什么是好的社会？", "ch10", 4),
    ("第十一章优化稿.md", "第十一章 什么是中国智慧？", "ch11", 4),
]

# CSS样式
CSS_STYLE = """
        body {
            font-family: "宋体", "SimSun", serif;
            font-size: 12pt;
            line-height: 1.8;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            font-family: "黑体", "SimHei", sans-serif;
            font-size: 22pt;
            text-align: center;
            color: #2c3e50;
            margin: 1.5em 0;
            page-break-after: avoid;
        }
        h2 {
            font-family: "黑体", "SimHei", sans-serif;
            font-size: 16pt;
            color: #34495e;
            margin: 2em 0 0.8em 0;
            border-left: 4px solid #3498db;
            padding-left: 0.5em;
            page-break-after: avoid;
        }
        h3 {
            font-family: "黑体", "SimHei", sans-serif;
            font-size: 14pt;
            color: #2c3e50;
            margin: 1.5em 0 0.5em 0;
            page-break-after: avoid;
        }
        h4 {
            font-family: "黑体", "SimHei", sans-serif;
            font-size: 12pt;
            color: #34495e;
            margin: 1.2em 0 0.4em 0;
            page-break-after: avoid;
        }
        p {
            margin: 0.5em 0;
            text-indent: 2em;
        }
        .dialog-line {
            margin: 0.8em 0;
            padding: 0.5em 1em;
            border-left: 3px solid #e74c3c;
            background-color: #fef9f9;
            text-indent: 0;
            line-height: 1.8;
        }
        .dialog-line .speaker {
            color: #c0392b;
            font-weight: bold;
        }
        .thought-theater {
            background-color: #f0f7ff;
            border: 1px solid #3498db;
            border-radius: 8px;
            padding: 1.5em;
            margin: 1.5em 0;
            page-break-inside: avoid;
        }
        .stage-direction {
            font-style: italic;
            color: #7f8c8d;
            margin: 0.5em 0;
            text-indent: 0;
        }
        .think-box {
            background-color: #fff8e1;
            border: 1px solid #f39c12;
            border-radius: 8px;
            padding: 1em 1.5em;
            margin: 1.5em 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
            font-size: 11pt;
        }
        table th {
            background-color: #34495e;
            color: white;
            padding: 0.5em;
            text-align: left;
        }
        table td {
            border: 1px solid #bdc3c7;
            padding: 0.5em;
            vertical-align: top;
        }
        li {
            margin: 0.3em 0;
            margin-left: 1em;
        }
        blockquote {
            background-color: #f5f5f5;
            border-left: 4px solid #9b59b6;
            padding: 0.5em 1em;
            margin: 1em 0;
            font-style: italic;
        }
        hr {
            border: none;
            border-top: 1px dashed #bdc3c7;
            margin: 2em 0;
        }
        .question-header {
            background-color: #fff3e0;
            padding: 0.5em;
            border-radius: 4px;
            color: #e65100;
        }
        .chapter-image {
            text-align: center;
            margin: 1.5em 0;
            page-break-inside: avoid;
        }
        .chapter-image img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .chapter-image .caption {
            font-size: 10pt;
            color: #666;
            margin-top: 0.5em;
            text-align: center;
        }
"""


def make_html_header(title):
    """生成HTML头部"""
    return f'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN" xml:lang="zh-CN">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
    <title>{title}</title>
    <link rel="stylesheet" href="style_mobile.css">
    <style>
{CSS_STYLE}
    </style>
</head>
<body>
    <div class="book-content">
        <h1>{title}</h1>
'''


HTML_FOOTER = '''
    </div>
</body>
</html>
'''


def convert_markdown_to_html(markdown_content, chapter_prefix, num_images):
    """将Markdown内容转换为HTML"""
    
    # 生成图片HTML
    images_html = ""
    for i in range(1, num_images + 1):
        img_path = f"{chapter_prefix}_scene{i}.webp"
        images_html += f'''
        <div class="chapter-image">
            <img src="{img_path}" alt="场景{i}" />
        </div>
'''
    
    # 在开头插入图片
    html_content = images_html + "\n"
    
    lines = markdown_content.split('\n')
    in_thought_theater = False
    in_think_box = False
    in_table = False
    in_list = False
    
    for i, line in enumerate(lines):
        original_line = line
        
        # 跳过文件头部的标题行（# 标题）
        if i == 0 and line.startswith('# '):
            continue
        
        # 处理思想剧场开始
        if '## 思想剧场' in line or '##思想剧场' in line:
            in_thought_theater = True
            html_content += '<div class="thought-theater">\n'
            continue
        
        # 处理思想剧场结束（在下一个## 之前）
        if in_thought_theater and line.startswith('## ') and '思想剧场' not in line:
            in_thought_theater = False
            html_content += '</div>\n'
        
        # 处理想一想开始
        if '## 想一想' in line or '##想一想' in line:
            in_think_box = True
            html_content += '<div class="think-box">\n'
            continue
        
        # 处理想一想结束
        if in_think_box and line.startswith('## ') and '想一想' not in line:
            in_think_box = False
            html_content += '</div>\n'
        
        # 处理分隔线
        if line.strip() == '---':
            html_content += '<hr>\n'
            continue
        
        # 处理场景描述（括号开头）
        if line.strip().startswith('（') and line.strip().endswith('）'):
            html_content += f'<div class="stage-direction">{line.strip()[1:-1]}</div>\n'
            continue
        
        # 处理场景描述（**时间** 等）
        if line.strip().startswith('**时间**：') or line.strip().startswith('**地点**：') or line.strip().startswith('**人物**：') or line.strip().startswith('**场景**：'):
            # 检查是否是场景标题
            if i > 0 and lines[i-1].strip() and lines[i-1].strip().startswith('**场景**'):
                continue
            content = re.sub(r'\*\*', '', line.strip())
            html_content += f'<div class="stage-direction">{content}</div>\n'
            continue
        
        # 处理对话格式 **人物**：内容
        dialog_match = re.match(r'\*\*([^*：]+)：\*\*', line)
        if dialog_match:
            speaker = dialog_match.group(1)
            content = re.sub(r'\*\*', '', line)
            html_content += f'<div class="dialog-line"><strong class="speaker">{speaker}：</strong>{content.split("：", 1)[1]}</div>\n'
            continue
        
        # 处理标题
        if line.startswith('### '):
            title = re.sub(r'\*\*', '', line[4:])
            html_content += f'<h4>{title}</h4>\n'
            continue
        
        if line.startswith('## '):
            # 排除思想剧场和想一想标题
            if '思想剧场' in line or '想一想' in line:
                continue
            title = re.sub(r'\*\*', '', line[3:])
            html_content += f'<h2>{title}</h2>\n'
            continue
        
        # 处理表格
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                html_content += '<table>\n'
            
            # 解析表格行
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if all(c.replace('-', '').replace(':', '') == '' for c in cells):
                html_content += '</table>\n'
                in_table = False
                continue
            
            if in_table and i > 0 and '|' in lines[i-1] and lines[i-1].strip().startswith('|'):
                # 不是表头行
                html_content += '<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>\n'
            else:
                # 表头行
                html_content += '<tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr>\n'
            continue
        else:
            if in_table:
                html_content += '</table>\n'
                in_table = False
        
        # 处理列表项
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line.strip()[2:])
            html_content += f'<li>{content}</li>\n'
            in_list = True
            continue
        else:
            if in_list:
                in_list = False
        
        # 处理引用块
        if line.strip().startswith('>'):
            content = re.sub(r'^>\s?', '', line.strip())
            html_content += f'<blockquote>{content}</blockquote>\n'
            continue
        
        # 处理普通段落 - 移除**但保留内容
        if line.strip():
            # 保留**强调**但转换格式
            content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
            # 移除段首的缩进空格
            content = content.strip()
            if content:
                html_content += f'<p>{content}</p>\n'
    
    # 关闭未关闭的标签
    if in_thought_theater:
        html_content += '</div>\n'
    if in_think_box:
        html_content += '</div>\n'
    if in_table:
        html_content += '</table>\n'
    
    return html_content


def process_chapters():
    """处理所有章节"""
    base_path = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史")
    source_dir = base_path / "优化阶段"
    output_dir = base_path / "移动端适配" / "chapters_fixed"
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    for md_file, title, prefix, num_images in CHAPTERS:
        md_path = source_dir / md_file
        
        if not md_path.exists():
            print(f"❌ 文件不存在: {md_path}")
            results.append((md_file, False, "文件不存在"))
            continue
        
        print(f"📖 处理: {md_file}")
        
        try:
            # 读取Markdown文件
            with open(md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # 转换为HTML
            html_content = convert_markdown_to_html(md_content, prefix, num_images)
            
            # 组合完整HTML
            full_html = make_html_header(title) + html_content + HTML_FOOTER
            
            # 输出文件名
            chapter_num = md_file.replace('优化稿.md', '').replace('第', '')
            output_file = output_dir / f"第{chapter_num}_修复版.html"
            
            # 保存HTML
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            print(f"   ✅ 已保存: {output_file.name}")
            results.append((md_file, True, str(output_file)))
            
        except Exception as e:
            import traceback
            print(f"   ❌ 错误: {e}")
            traceback.print_exc()
            results.append((md_file, False, str(e)))
    
    # 打印总结
    print("\n" + "="*50)
    print("处理完成！")
    print("="*50)
    success = sum(1 for _, ok, _ in results if ok)
    print(f"成功: {success}/{len(results)}")
    
    return results


if __name__ == "__main__":
    process_chapters()
