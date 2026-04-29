#!/usr/bin/env python3
import re

def count_chinese(text):
    return len(re.findall(r'[\u4e00-\u9fff]', text))

with open('outputs/儿童哲学史/优化阶段/第十一章优化稿.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 按二级标题分割
sections = re.split(r'\n## ', content)
print(f"总章节数: {len(sections)}")
total = 0
for i, section in enumerate(sections):
    if i == 0:
        title = "开头"
    else:
        # 提取标题第一行
        lines = section.strip().split('\n')
        title = lines[0] if lines else f"章节{i}"
    chinese_count = count_chinese(section)
    total += chinese_count
    print(f"{i}. {title[:30]}... : {chinese_count} 汉字")

print(f"总计汉字: {total}")