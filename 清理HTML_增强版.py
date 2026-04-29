#!/usr/bin/env python3
"""
清理HTML中的Markdown符号 - 增强版
"""

import re
from pathlib import Path

WORK_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/最终合并")
input_file = WORK_DIR / "和古人一起想问题_合并版.html"

# 读取HTML
with open(input_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 删除所有##开头的行（Markdown标题）
lines = html.split('\n')
cleaned_lines = []
for line in lines:
    # 如果整行是###开头或##开头，清理掉
    stripped = line.strip()
    if stripped.startswith('###') or stripped.startswith('## '):
        # 如果在标签内可能有其他内容
        if '<' not in line:
            continue  # 跳过纯Markdown行
        # 如果在标签内，清理掉##符号
        line = re.sub(r'###\s*', '', line)
        line = re.sub(r'##\s*', '', line)
    # 否则保留
    cleaned_lines.append(line)

html = '\n'.join(cleaned_lines)

# 更激进的方法：删除所有###开头的纯文本行（在标签外的）
html = re.sub(r'\n\s*###\s*([^\n<]+)\s*\n', r'\n', html)
html = re.sub(r'\n\s*##\s*([^\n<]+)\s*\n', r'\n', html)

# 保存
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("清理完成！")
