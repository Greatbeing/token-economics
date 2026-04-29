#!/usr/bin/env python3
import re

# 读取文件
with open('outputs/儿童哲学史/优化阶段/第七章优化稿.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找所有包含儿童角色的行
lines = content.split('\n')
child_lines = []
for i, line in enumerate(lines):
    if re.search(r'小美|小强|小智|小慧', line):
        child_lines.append((i+1, line))

print(f"找到 {len(child_lines)} 行儿童台词")

# 统计
questions = []
challenges = []
choices = []

for lineno, line in child_lines:
    # 提取台词部分
    match = re.search(r'[：:] ?(.*)', line)
    if match:
        text = match.group(1)
    else:
        text = line
    
    # 判断提问（包含问号）
    if '？' in text or '?' in text:
        questions.append((lineno, text))
    
    # 判断质疑反驳（包含关键词）
    challenge_keywords = ['可是', '但是', '但', '不对', '质疑', '反驳', '如果.*呢', '难道']
    for keyword in challenge_keywords:
        if re.search(keyword, text):
            challenges.append((lineno, text))
            break
    
    # 判断立场选择（需要儿童做出选择的场景）
    # 这需要上下文判断，这里简单检测包含"选"、"选择"、"我觉得"等
    choice_keywords = ['选', '选择', '我觉得', '我选', '立场']
    for keyword in choice_keywords:
        if keyword in text:
            choices.append((lineno, text))
            break

print("\n=== 提问统计 ===")
for lineno, text in questions:
    print(f"{lineno}: {text}")

print(f"\n提问总数: {len(questions)}")

print("\n=== 质疑反驳统计 ===")
for lineno, text in challenges:
    print(f"{lineno}: {text}")

print(f"\n质疑反驳总数: {len(challenges)}")

print("\n=== 立场选择统计 ===")
for lineno, text in choices:
    print(f"{lineno}: {text}")

print(f"\n立场选择总数: {len(choices)}")

# 检查达标情况
print("\n=== 标准检查 ===")
print(f"提问次数≥8: {'✅' if len(questions) >= 8 else '❌'} ({len(questions)})")
print(f"质疑反驳次数≥4: {'✅' if len(challenges) >= 4 else '❌'} ({len(challenges)})")
print(f"立场选择次数≥2: {'✅' if len(choices) >= 2 else '❌'} ({len(choices)})")