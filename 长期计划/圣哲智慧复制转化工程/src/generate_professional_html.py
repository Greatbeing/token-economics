#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成专业排版HTML样张
基于第一章优化文稿，应用专业图书排版规范
"""

import os
import base64
import json
import re
from pathlib import Path

# 路径配置
BASE_DIR = Path("/app/data/files")
CHAPTER_MD_PATH = BASE_DIR / "outputs/儿童哲学史/优化阶段/第一章优化稿.md"
ILLUSTRATION_MAPPING_PATH = BASE_DIR / "data/illustration_references/chapter_illustration_mapping.json"
OUTPUT_HTML_PATH = BASE_DIR / "outputs/儿童哲学史/优化排版/第一章_专业排版.html"
OUTPUT_CSS_PATH = BASE_DIR / "outputs/儿童哲学史/优化排版/style_optimized.css"
ILLUSTRATION_SOURCE_DIR = BASE_DIR / "data/illustration_references/草图源文件"

def load_illustration_mapping():
    """加载插图映射配置"""
    with open(ILLUSTRATION_MAPPING_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def image_to_data_uri(image_path):
    """将图片转换为Data URI格式"""
    if not os.path.exists(str(image_path)):
        print(f"警告: 图片不存在 {image_path}")
        return ""
    
    # 根据文件扩展名确定MIME类型
    ext = str(image_path).lower().split('.')[-1]
    mime_map = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'svg': 'image/svg+xml'
    }
    mime_type = mime_map.get(ext, 'image/jpeg')
    
    try:
        with open(str(image_path), 'rb') as img_file:
            encoded = base64.b64encode(img_file.read()).decode('utf-8')
        return f"data:{mime_type};base64,{encoded}"
    except Exception as e:
        print(f"转换图片失败 {image_path}: {e}")
        return ""

def get_chapter_illustrations(chapter_num=1):
    """获取指定章节的插图Data URI"""
    mapping = load_illustration_mapping()
    illustrations = []
    
    for chapter in mapping['chapters']:
        if chapter['chapter_number'] == chapter_num:
            for scene in chapter['scenes']:
                img_path = ILLUSTRATION_SOURCE_DIR / scene['file_name']
                data_uri = image_to_data_uri(img_path)
                if data_uri:
                    illustrations.append({
                        'data_uri': data_uri,
                        'alt_text': scene['alt_text'],
                        'description': scene['description'],
                        'position_label': scene['position_label']
                    })
            break
    
    return illustrations

def markdown_to_html_with_images(markdown_content, illustrations):
    """将Markdown转换为HTML，并嵌入插图"""
    # 首先将Markdown转换为HTML（简单处理，实际应该使用markdown库）
    # 这里使用正则处理基本格式，更复杂的处理可以使用python-markdown库
    
    # 处理标题
    html = markdown_content
    
    # 添加插图占位符，稍后替换
    # 先找到各个位置标签对应的位置
    position_mapping = {
        'after_thought_theater': '## 思想剧场：星空下的辩论会',
        'after_first_station': '## 第一站：神话的创世想象',
        'after_second_station': '## 第二站：老子的"道"——世界的底层代码',
        'after_third_station': '## 第三站：孔子的"天命"——人生游戏的主线任务'
    }
    
    # 为每个插图创建HTML标签
    illustration_html = {}
    for i, illus in enumerate(illustrations):
        img_html = f'''<div class="illustration-container">
    <div class="illustration-title">{illus['description']}</div>
    <img src="{illus['data_uri']}" alt="{illus['alt_text']}" class="chapter-illustration">
    <div class="illustration-caption">{illus['alt_text']}</div>
</div>'''
        illustration_html[illus['position_label']] = img_html
    
    # 在适当位置插入插图
    # 这里简化处理，直接替换特定的标记
    # 实际应该根据位置标签插入到对应标题之后
    
    return html

def generate_css_content():
    """生成CSS样式内容"""
    css = """/* 儿童版中国哲学史 - 专业图书排版样式 */
/* 基于中文图书排版规范（CY/T 120-2015）和童书排版标准 */

/* 页面基本设置 */
@page {
    size: A4;
    margin: 25mm 15mm 20mm 25mm; /* 上 右 下 左 (天头 切口 地脚 订口) */
}

body {
    /* A4尺寸设置 */
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto;
    padding: 0;
    background-color: #fff;
    
    /* 字体设置 */
    font-family: "宋体", "SimSun", "Source Han Serif SC", serif;
    font-size: 12pt; /* 小四号 */
    line-height: 1.5; /* 1.5倍行距 */
    color: #333;
    
    /* 文本对齐 */
    text-align: justify;
    text-justify: inter-ideograph;
}

/* 标题层级系统 */
/* 章标题 (一级标题) */
h1 {
    font-family: "黑体", "SimHei", "Source Han Sans SC", sans-serif;
    font-size: 24pt; /* 二号字 */
    font-weight: bold;
    text-align: center;
    margin: 2em 0 1em 0;
    color: #2c3e50;
    page-break-after: avoid;
}

/* 节标题 (二级标题) */
h2 {
    font-family: "黑体", "SimHei", "Source Han Sans SC", sans-serif;
    font-size: 18pt; /* 三号字 */
    font-weight: bold;
    text-align: left;
    margin: 1.5em 0 0.5em 0;
    color: #34495e;
    border-left: 4px solid #3498db;
    padding-left: 0.5em;
    page-break-after: avoid;
}

/* 小节标题 (三级标题) */
h3 {
    font-family: "黑体", "SimHei", "Source Han Sans SC", sans-serif;
    font-size: 14pt; /* 四号字 */
    font-weight: bold;
    text-align: left;
    margin: 1em 0 0.5em 0;
    color: #2c3e50;
    page-break-after: avoid;
}

/* 段落格式 */
p {
    margin: 0 0 1em 0;
    text-indent: 2em; /* 首行缩进2字符 */
    word-spacing: 0.05em;
    letter-spacing: 0.02em;
}

/* 特殊段落 - 无缩进 */
p.no-indent {
    text-indent: 0;
}

/* 对话行 */
.dialog-line {
    margin: 0.5em 0;
    padding: 0.2em 0 0.2em 1em;
    border-left: 2px solid #e74c3c;
    background-color: #f9f9f9;
    text-indent: 0;
}

.dialog-line strong {
    color: #c0392b;
}

/* 特殊元素容器 */
/* 思想剧场 */
.thought-theater {
    background-color: #f0f7ff;
    border: 1px solid #3498db;
    border-radius: 8px;
    padding: 1em 1.5em;
    margin: 1.5em 0;
    page-break-inside: avoid;
}

.thought-theater .meta {
    font-size: 11pt;
    color: #7f8c8d;
    margin-bottom: 0.5em;
}

/* 想一想 */
.think-about {
    background-color: #fff8e1;
    border: 1px solid #f39c12;
    border-radius: 8px;
    padding: 1em 1.5em;
    margin: 1.5em 0;
    page-break-inside: avoid;
}

.think-about h3 {
    color: #d35400;
    margin-top: 0;
}

/* 古人说 */
.ancient-saying {
    background-color: #e8f5e9;
    border: 1px solid #27ae60;
    border-radius: 8px;
    padding: 1em 1.5em;
    margin: 1.5em 0;
    page-break-inside: avoid;
}

.ancient-saying .original {
    font-family: "楷体", "KaiTi", "STKaiti", cursive;
    font-size: 13pt;
    color: #2ecc71;
    margin-bottom: 0.5em;
}

.ancient-saying .translation {
    font-style: italic;
    color: #27ae60;
}

/* 全球望远镜 */
.global-telescope {
    background-color: #e3f2fd;
    border: 1px solid #2980b9;
    border-radius: 8px;
    padding: 1em 1.5em;
    margin: 1.5em 0;
    page-break-inside: avoid;
}

.global-telescope .comparison-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
}

.global-telescope .comparison-table th {
    background-color: #3498db;
    color: white;
    padding: 0.5em;
    text-align: center;
}

.global-telescope .comparison-table td {
    border: 1px solid #bdc3c7;
    padding: 0.5em;
    vertical-align: top;
}

/* 智慧探险地图 */
.wisdom-map {
    background-color: #f5f5f5;
    border: 2px dashed #9b59b6;
    border-radius: 10px;
    padding: 1.5em;
    margin: 2em 0;
    font-family: "等宽字体", "Courier New", monospace;
    page-break-inside: avoid;
}

.wisdom-map .map-title {
    font-family: "黑体", sans-serif;
    font-size: 16pt;
    color: #8e44ad;
    margin-bottom: 0.5em;
}

/* 哲学生词卡 */
.philosophy-vocab {
    background-color: #fffde7;
    border: 1px solid #f1c40f;
    border-radius: 8px;
    padding: 1em;
    margin: 1.5em 0;
    page-break-inside: avoid;
}

.philosophy-vocab table {
    width: 100%;
    border-collapse: collapse;
}

.philosophy-vocab th {
    background-color: #f39c12;
    color: white;
    padding: 0.5em;
    text-align: left;
}

.philosophy-vocab td {
    border: 1px solid #f1c40f;
    padding: 0.5em;
    vertical-align: top;
}

/* 插图容器 */
.illustration-container {
    text-align: center;
    margin: 1.5em 0;
    page-break-inside: avoid;
}

.illustration-title {
    font-family: "黑体", sans-serif;
    font-size: 13pt;
    color: #2c3e50;
    margin-bottom: 0.5em;
    font-weight: bold;
}

.chapter-illustration {
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.illustration-caption {
    font-size: 11pt;
    color: #7f8c8d;
    font-style: italic;
    margin-top: 0.5em;
}

/* 表格样式 */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    page-break-inside: avoid;
}

table th {
    background-color: #34495e;
    color: white;
    padding: 0.5em;
    text-align: left;
    font-weight: bold;
}

table td {
    border: 1px solid #bdc3c7;
    padding: 0.5em;
    vertical-align: top;
}

table tr:nth-child(even) {
    background-color: #f9f9f9;
}

/* 代码块 */
pre, code {
    font-family: "Courier New", "Monaco", "Consolas", monospace;
    font-size: 11pt;
}

pre {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 1em;
    overflow: auto;
    page-break-inside: avoid;
}

/* 列表样式 */
ul, ol {
    margin: 1em 0 1em 2em;
    padding: 0;
}

li {
    margin: 0.5em 0;
}

/* 打印优化 */
@media print {
    body {
        width: auto;
        min-height: auto;
        margin: 0;
    }
    
    /* 避免孤行寡行 */
    h1, h2, h3, h4, h5, h6 {
        page-break-after: avoid;
    }
    
    p, li, blockquote {
        page-break-inside: avoid;
    }
    
    /* 确保表格不跨页断开 */
    table {
        page-break-inside: avoid;
    }
    
    /* 插图和特殊容器不跨页 */
    .thought-theater,
    .think-about,
    .ancient-saying,
    .global-telescope,
    .wisdom-map,
    .philosophy-vocab,
    .illustration-container {
        page-break-inside: avoid;
    }
}

/* 儿童友好颜色辅助类 */
.highlight-yellow {
    background-color: #fffacd;
    padding: 0.1em 0.3em;
    border-radius: 3px;
}

.highlight-blue {
    background-color: #e3f2fd;
    padding: 0.1em 0.3em;
    border-radius: 3px;
}

.highlight-green {
    background-color: #e8f5e9;
    padding: 0.1em 0.3em;
    border-radius: 3px;
}

/* 特殊符号 */
.star-symbol {
    color: #f39c12;
    font-weight: bold;
}

/* 页眉页脚 */
.header, .footer {
    display: none; /* 打印时可添加 */
}

/* 章节分隔 */
.chapter-break {
    page-break-before: always;
}

/* 防止最后一页只有标题 */
.avoid-orphan {
    page-break-inside: avoid;
}
"""
    return css

def generate_html_content(markdown_content, illustrations):
    """生成完整的HTML内容"""
    # 读取插图映射
    mapping = load_illustration_mapping()
    
    # 构建插图位置映射
    illustration_by_position = {}
    for illus in illustrations:
        illustration_by_position[illus['position_label']] = illus
    
    # 处理Markdown内容，插入插图
    lines = markdown_content.split('\n')
    html_lines = []
    
    # 转换Markdown为HTML（简化版）
    for line in lines:
        # 处理一级标题
        if line.startswith('# '):
            # 确保标题格式正确
            html_lines.append(f'<h1>{line[2:]}</h1>')
        
        # 处理二级标题
        elif line.startswith('## '):
            title_content = line[3:]
            html_lines.append(f'<h2>{title_content}</h2>')
            
            # 检查是否需要在此标题后插入插图
            # 根据位置标签查找
            for position_label, title_pattern in mapping['position_labels'].items():
                if title_content.startswith(title_pattern[3:]):  # 去掉前面的"## "
                    if position_label in illustration_by_position:
                        illus = illustration_by_position[position_label]
                        img_html = f'''<div class="illustration-container">
    <div class="illustration-title">{illus['description']}</div>
    <img src="{illus['data_uri']}" alt="{illus['alt_text']}" class="chapter-illustration">
    <div class="illustration-caption">{illus['alt_text']}</div>
</div>'''
                        html_lines.append(img_html)
        
        # 处理三级标题
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        
        # 处理粗体
        elif '**' in line:
            # 简单替换
            processed = line.replace('**', '<strong>', 1)
            processed = processed.replace('**', '</strong>', 1)
            html_lines.append(f'<p>{processed}</p>')
        
        # 处理表格行（简化）
        elif line.startswith('|'):
            # 暂时按段落处理
            html_lines.append(f'<p>{line}</p>')
        
        # 空行
        elif line.strip() == '':
            html_lines.append('')
        
        # 普通段落
        else:
            html_lines.append(f'<p>{line}</p>')
    
    # 构建完整的HTML文档
    html_content = f'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN" xml:lang="zh-CN">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
    <title>第一章：世界是从哪儿来的？（老子、孔子、神话） - 儿童版中国哲学史</title>
    <link rel="stylesheet" href="style_optimized.css">
    <style>
        /* 内联关键CSS确保立即渲染 */
        body {{
            font-family: "宋体", "SimSun", serif;
            font-size: 12pt;
            line-height: 1.5;
            color: #333;
        }}
        h1 {{ font-family: "黑体", "SimHei", sans-serif; font-size: 24pt; }}
        h2 {{ font-family: "黑体", "SimHei", sans-serif; font-size: 18pt; }}
        h3 {{ font-family: "黑体", "SimHei", sans-serif; font-size: 14pt; }}
    </style>
</head>
<body>
    <div class="book-content">
        <h1>第一章：世界是从哪儿来的？（老子、孔子、神话）</h1>
        
        <!-- 内容开始 -->
        {chr(10).join(html_lines)}
        <!-- 内容结束 -->
        
        <div class="chapter-end">
            <p>（第一章完）</p>
        </div>
    </div>
</body>
</html>'''
    
    return html_content

def main():
    """主函数"""
    print("开始生成专业排版HTML样张...")
    
    # 1. 确保输出目录存在
    os.makedirs(os.path.dirname(OUTPUT_HTML_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_CSS_PATH), exist_ok=True)
    
    # 2. 加载Markdown内容
    print("加载第一章优化稿...")
    with open(CHAPTER_MD_PATH, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # 3. 获取插图Data URI
    print("获取插图Data URI...")
    illustrations = get_chapter_illustrations(1)
    print(f"找到 {len(illustrations)} 张插图")
    
    # 4. 生成CSS文件
    print("生成CSS样式文件...")
    css_content = generate_css_content()
    with open(OUTPUT_CSS_PATH, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    # 5. 生成HTML文件
    print("生成HTML文件...")
    html_content = generate_html_content(markdown_content, illustrations)
    with open(OUTPUT_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"完成！")
    print(f"HTML文件: {OUTPUT_HTML_PATH}")
    print(f"CSS文件: {OUTPUT_CSS_PATH}")

if __name__ == "__main__":
    main()