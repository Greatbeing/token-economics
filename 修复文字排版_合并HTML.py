#!/usr/bin/env python3
"""
修复HTML文字排版问题：
1. 删除 ## Markdown符号
2. 删除 emoji 和拼音注释
3. 优化段落间距
4. 合并12章HTML
"""

import re
import os
from pathlib import Path

# 工作目录
WORK_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/修正版")
OUTPUT_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/最终合并")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def clean_text_content(text):
    """清理文本内容中的残留符号"""
    
    # 1. 删除 ## Markdown符号
    text = re.sub(r'^##\s+', '', text, flags=re.MULTILINE)
    
    # 2. 删除残留的 ** 符号
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    
    # 3. 删除 emoji 符号
    emojis = (
        "🧠💭✨🌟⭐💡🔮🎭🏛️🌊☁️🌙📚📖📝⚡🎯🎪🎨🎬❌✅❓💬📌🔥💫🌈☀️🌧️❄️🌸🌺🌻"
        "🏃🚶💪👶👧🧒👦👨👩👴👵💪👋✋👌🤌🤏👈👉👆👇☝️👍👎✊👊🤛🤜"
    )
    emoji_pattern = re.compile("[" + emojis + "\U0001F300-\U0001F9FF" + "]", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    
    # 4. 删除拼音注释 (格式：拼音：xxx)
    text = re.sub(r'拼音：[A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜüêēḕḗḙīᾑīḯōóǫ́ṓṑūúmǔǔǖǘǚǜ\s,]+', '', text)
    
    # 5. 清理多余空格
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r' +', ' ', text)
    
    return text


def clean_html_content(html):
    """清理HTML中的残留符号和优化格式"""
    
    # 1. 处理h2/h3标题中的##符号（包括各种变体）
    # 匹配 h2 id="xxx"> ## 标题 或 h3 id="xxx"> ## 标题
    html = re.sub(r'<h([23])([^>]*)>\s*##+\s*', r'<h\1\2>', html)
    
    # 2. 处理段落和div中的##符号
    html = re.sub(r'>\s*##+\s*([^<\n]+)', r'>\1', html)
    
    # 3. 删除残留的 ** 符号
    html = re.sub(r'\*\*([^*]+)\*\*', r'\1', html)
    
    # 5. 删除 emoji
    emojis = (
        "🧠💭✨🌟⭐💡🔮🎭🏛️🌊☁️🌙📚📖📝⚡🎯🎪🎨🎬❌✅❓💬📌🔥💫🌈☀️🌧️❄️🌸🌺🌻"
        "🏃🚶💪👶👧🧒👦👨👩👴👵💪👋✋👌🤌🤏👈👉👆👇☝️👍👎✊👊🤛🤜💔❣️💕"
        "💞💓💗💖💘💝💟🧡💛💚💙💜🖤🤍🤎❤️❓💬📢🔔⚡"
    )
    emoji_pattern = re.compile("[" + emojis + "\U0001F300-\U0001F9FF" + "]", flags=re.UNICODE)
    html = emoji_pattern.sub('', html)
    
    # 6. 删除拼音注释
    html = re.sub(r'拼音：[A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜüêēḕḗḙīᾑīḯōóǫ́ṓṑūúmǔǔǖǘǚǜ\s,]+', ' ', html)
    
    # 7. 清理多余空行
    html = re.sub(r'\n{3,}', '\n', html)
    
    # 8. 修复段落格式 - 给对话添加样式
    # 为人物对话添加class
    speaker_pattern = r'(小星|小宇|老子|孔子|孟子|告子|荀子|庄子|韩非子|墨子|杨朱|慧能|神秀|嵇康|阮籍|王弼|顾炎武|黄宗羲|龚自珍|王阳明|朱熹|程颢|程颐|张载|梁启超|冯友兰|鲁迅|蔡元培)'
    
    return html


def process_single_chapter(html_content, chapter_name):
    """处理单个章节"""
    
    # 清理内容
    cleaned = clean_html_content(html_content)
    
    return cleaned


def merge_chapters():
    """合并所有章节"""
    
    # 定义章节顺序
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
    
    /* 对话样式 - 人物名字加粗 */
    p:has(span.speaker) {{
        margin-bottom: 12px;
    }}
    
    /* 修复标题格式 */
    h2:first-child,
    h1:first-child {{
        margin-top: 0;
    }}
    
    /* 删除Markdown残留 */
    p:empty,
    h2:empty,
    h3:empty {{
        display: none;
    }}
    
    /* 段落间距优化 */
    p {{
        margin-bottom: 16px;
        text-indent: 2em;
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
            
            # 清理内容
            cleaned = clean_html_content(content)
            
            # 提取body内容
            body_match = re.search(r'<body>(.*?)</body>', cleaned, re.DOTALL)
            if body_match:
                body_content = body_match.group(1)
                # 添加章节分隔注释
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
    print("\n1. 合并12章HTML文件...")
    merged_html = merge_chapters()
    
    # 保存合并后的HTML
    output_html = OUTPUT_DIR / "和古人一起想问题_合并版.html"
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(merged_html)
    print(f"\n✓ 合并完成: {output_html}")
    
    print("\n" + "=" * 60)
    print("HTML处理完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
