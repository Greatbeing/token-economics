#!/usr/bin/env python3
"""
修复HTML文字排版问题 - 完整版
1. 将###转换为<h3>标签
2. 将##转换为<h2>标签
3. 删除Markdown符号
4. 优化段落间距
5. 合并12章HTML
"""

import re
import os
from pathlib import Path

# 工作目录
WORK_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/修正版")
OUTPUT_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/最终合并")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def convert_markdown_headers(html):
    """将Markdown标题转换为HTML标签"""
    
    # 1. 处理### xxx -> <h3>xxx</h3>
    # 匹配行首的### 标题
    def replace_h3(match):
        title = match.group(1).strip()
        # 生成id
        safe_id = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]+', '-', title)
        safe_id = safe_id.strip('-')
        return f'<h3 id="{safe_id}">{title}</h3>'
    
    html = re.sub(r'^###\s+(.+)$', replace_h3, html, flags=re.MULTILINE)
    
    # 2. 处理## xxx -> <h2>xxx</h2>
    def replace_h2(match):
        title = match.group(1).strip()
        safe_id = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]+', '-', title)
        safe_id = safe_id.strip('-')
        return f'<h2 id="{safe_id}">{title}</h2>'
    
    html = re.sub(r'^##\s+(.+)$', replace_h2, html, flags=re.MULTILINE)
    
    # 3. 清理残留的#符号（在标签内）
    html = re.sub(r'<([^>]+)>\s*#+\s*', r'<\1>', html)
    
    return html


def clean_html_content(html):
    """清理HTML中的残留符号和优化格式"""
    
    # 1. 删除残留的 ** 符号
    html = re.sub(r'\*\*([^*]+)\*\*', r'\1', html)
    
    # 2. 删除 emoji
    emojis = (
        "🧠💭✨🌟⭐💡🔮🎭🏛️🌊☁️🌙📚📖📝⚡🎯🎪🎨🎬❌✅❓💬📌🔥💫🌈☀️🌧️❄️🌸🌺🌻"
        "🏃🚶💪👶👧🧒👦👨👩👴👵💪👋✋👌🤌🤏👈👉👆👇☝️👍👎✊👊🤛🤜💔❣️💕"
        "💞💓💗💖💘💝💟🧡💛💚💙💜🖤🤍🤎❤️❓💬📢🔔⚡🎈🎉🎊🎋🎍🎎🎏🎐🎑🧧"
    )
    emoji_pattern = re.compile("[" + emojis + "\U0001F300-\U0001F9FF" + "]", flags=re.UNICODE)
    html = emoji_pattern.sub('', html)
    
    # 3. 删除拼音注释
    html = re.sub(r'拼音：[A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜüêēḕḗḙīᾑīḯōóǫ́ṓṑūúmǔǔǖǘǚǜ\s,]+', ' ', html)
    
    # 4. 清理多余空行
    html = re.sub(r'\n{3,}', '\n', html)
    
    # 5. 清理多余的空白字符
    html = re.sub(r'[ \t]+\n', '\n', html)
    
    return html


def merge_chapters():
    """合并所有章节"""
    
    chapters = [
        "第1章样张_fixed.html",
        "第2章样张_fixed.html",
        "第3章样张_fixed.html",
        "第4章样张_fixed.html",
        "第5章样张_fixed.html",
        "第6章样张_fixed.html",
        "第7章样张_fixed.html",
        "第8章样张_fixed.html",
        "第9章样张_fixed.html",
        "第10章样张_fixed.html",
        "第11章样张_fixed.html",
        "第12章样张_fixed.html",
    ]
    
    # 读取CSS样式
    css_file = WORK_DIR / "style_fixed.css"
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # 构建合并后的HTML
    merged_html = f'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="Pandoc" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <title>和古人一起想问题 - 完整版</title>
  <style>
    {css_content}
    
    /* 对话段落优化 */
    body {{
        padding: 0;
        max-width: none;
    }}
    
    .chapter {{
        max-width: 100%;
        page-break-after: always;
    }}
    
    /* 删除Markdown残留 */
    p:empty {{
        display: none;
    }}
    
    /* 段落间距优化 */
    p {{
        margin-bottom: 16px;
        text-indent: 2em;
        line-height: 1.8;
    }}
    
    /* 表格响应式 */
    table {{
        font-size: 14px;
    }}
    
    /* 图片样式 */
    img {{
        max-width: 100%;
        height: auto;
    }}
    
    /* 引用块样式 */
    blockquote {{
        border-left: 3px solid #90CAF9;
        padding-left: 1em;
        margin-left: 0;
        color: #555;
        font-style: italic;
    }}
  </style>
</head>
<body>
'''
    
    for chapter_file in chapters:
        filepath = WORK_DIR / chapter_file
        if filepath.exists():
            print(f"处理: {chapter_file}")
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 转换Markdown标题
            content = convert_markdown_headers(content)
            
            # 清理内容
            cleaned = clean_html_content(content)
            
            # 提取body内容
            body_match = re.search(r'<body>(.*?)</body>', cleaned, re.DOTALL)
            if body_match:
                body_content = body_match.group(1)
                chapter_num = chapter_file.replace("样张_fixed.html", "").replace("第", "第")
                merged_html += f'\n<!-- {chapter_num} -->\n<div class="chapter">\n{body_content}\n</div>\n'
            else:
                print(f"  警告: 未找到body标签 {chapter_file}")
        else:
            print(f"警告: 文件不存在 {chapter_file}")
    
    merged_html += '''
</body>
</html>
'''
    
    return merged_html


def main():
    """主函数"""
    
    print("=" * 60)
    print("开始处理HTML文件...")
    print("=" * 60)
    
    # 合并所有章节
    print("\n1. 合并12章HTML文件并清理Markdown符号...")
    merged_html = merge_chapters()
    
    # 保存合并后的HTML
    output_html = OUTPUT_DIR / "和古人一起想问题_合并版.html"
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(merged_html)
    print(f"\n✓ 合并完成: {output_html}")
    
    # 验证
    import subprocess
    result = subprocess.run(
        ['grep', '-oE', '## [^<\\n]+'],
        input=merged_html.encode('utf-8'),
        capture_output=True
    )
    remaining = result.stdout.decode('utf-8').strip()
    if remaining:
        print(f"\n警告: 还有残留的##符号")
        for line in remaining.split('\n')[:5]:
            print(f"  - {line}")
    else:
        print("✓ 所有##符号已清理或转换")
    
    result = subprocess.run(
        ['grep', '-oE', '### [^<\\n]+'],
        input=merged_html.encode('utf-8'),
        capture_output=True
    )
    remaining = result.stdout.decode('utf-8').strip()
    if remaining:
        print(f"\n警告: 还有残留的###符号")
    else:
        print("✓ 所有###符号已转换")
    
    print("\n" + "=" * 60)
    print("HTML处理完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
