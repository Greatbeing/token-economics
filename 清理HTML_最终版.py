#!/usr/bin/env python3
"""
清理HTML中的Markdown符号 - 最终版
处理所有形式的## 和 ### 符号
"""

import re
from pathlib import Path

WORK_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/最终合并")
input_file = WORK_DIR / "和古人一起想问题_合并版.html"

# 读取HTML
with open(input_file, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"清理前: {len(html)} 字符")

# 1. 删除纯文本的### 标题（不在HTML标签内）
# 匹配独立的### xxx行（前后是换行）
html = re.sub(r'\n\s*###\s*([^\n<]+)\s*(?=\n)', r'\n', html)

# 2. 删除纯文本的## 标题（不在HTML标签内）
html = re.sub(r'\n\s*##\s*([^\n<]+)\s*(?=\n)', r'\n', html)

# 3. 处理HTML标签内的##符号
html = re.sub(r'<([^>]+)>\s*##+\s*', r'<\1>', html)

# 4. 再次清理残留的独立##行
lines = html.split('\n')
cleaned_lines = []
for line in lines:
    stripped = line.strip()
    # 如果整行只是##开头且不含HTML标签，则跳过
    if stripped.startswith('##') and '<' not in stripped:
        continue
    cleaned_lines.append(line)

html = '\n'.join(cleaned_lines)

# 5. 清理多余空行
html = re.sub(r'\n{3,}', '\n', html)

print(f"清理后: {len(html)} 字符")

# 保存
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("清理完成！")

# 验证
import subprocess
result = subprocess.run(
    ['grep', '-oE', '## [^<\\n]+'],
    input=html.encode('utf-8'),
    capture_output=True
)
remaining = result.stdout.decode('utf-8').strip()
if remaining:
    print(f"警告: 还有残留的##符号:\n{remaining}")
else:
    print("✓ 所有##符号已清理")
