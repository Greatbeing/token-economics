import re

with open('outputs/儿童哲学史/优化阶段/第二章优化稿.md', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# 统计儿童台词
child_lines = []
for i, line in enumerate(lines):
    if re.search(r'^\s*\*\*小星\*\*', line) or re.search(r'^\s*\*\*小宇\*\*', line):
        child_lines.append((i+1, line))
    elif re.search(r'^\s*\*\*小星的.*?\*\*', line) or re.search(r'^\s*\*\*小宇的.*?\*\*', line):
        child_lines.append((i+1, line))

print("儿童角色台词（共{}处）:".format(len(child_lines)))
for idx, (line_num, line) in enumerate(child_lines):
    print(f"{idx+1}. 行{line_num}: {line.strip()}")

# 分类统计
questions = []
challenges = []
choices = []

for line_num, line in child_lines:
    # 提取台词内容
    match = re.search(r'^\s*\*\*(小星|小宇)(的)?(.*?)\*\*\s*[:：]\s*(.*)', line)
    if match:
        role = match.group(1)
        label = match.group(3)   # 即兴提问/辩论回合等
        text = match.group(4)
        
        # 提问（包含问号）
        if '？' in text or '?' in text:
            questions.append((line_num, role, text))
        
        # 质疑反驳（根据标签或关键词）
        if label and ('质疑' in label or '反驳' in label or '追问' in label or '辩论' in label or '即兴提问' in label):
            challenges.append((line_num, role, text))
        elif re.search(r'可是|但是|不过|然而|难道|怎么|为何|为什么|不对|错了|误解|难过|犹豫', text):
            challenges.append((line_num, role, text))
        
        # 立场选择（根据标签）
        if label and ('立场选择' in label):
            choices.append((line_num, role, text))

print("\n=== 提问次数统计（问号） ===")
for i, (ln, role, text) in enumerate(questions):
    print(f"{i+1}. 行{ln} {role}: {text}")
print(f"总提问次数: {len(questions)}")

print("\n=== 质疑反驳次数统计 ===")
for i, (ln, role, text) in enumerate(challenges):
    print(f"{i+1}. 行{ln} {role}: {text}")
print(f"总质疑反驳次数: {len(challenges)}")

print("\n=== 立场选择次数统计 ===")
for i, (ln, role, text) in enumerate(choices):
    print(f"{i+1}. 行{ln} {role}: {text}")
print(f"总立场选择次数: {len(choices)}")

# 检查生活共鸣点
life_pattern = r'儿童生活共鸣点|生活共鸣点'
life_matches = re.findall(life_pattern, content)
print(f"\n生活共鸣点数量: {len(life_matches)}")

# 总结
print("\n=== 验收标准检查 ===")
print(f"1. 文件非空: {'✓' if content.strip() else '✗'}")
print(f"2. 儿童提问≥8: {'✓' if len(questions) >= 8 else '✗'} ({len(questions)})")
print(f"3. 质疑反驳≥4: {'✓' if len(challenges) >= 4 else '✗'} ({len(challenges)})")
print(f"4. 立场选择≥2: {'✓' if len(choices) >= 2 else '✗'} ({len(choices)})")
print(f"5. 生活共鸣点≥1: {'✓' if len(life_matches) >= 1 else '✗'} ({len(life_matches)})")