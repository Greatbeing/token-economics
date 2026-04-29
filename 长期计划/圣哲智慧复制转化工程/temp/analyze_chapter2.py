import re
import sys

# 读取第二章优化稿
with open('outputs/儿童哲学史/优化阶段/第二章优化稿.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到所有小星和小宇的台词
lines = content.split('\n')
child_lines = []
for i, line in enumerate(lines):
    if re.search(r'^\s*\*\*小星\*\*', line) or re.search(r'^\s*\*\*小宇\*\*', line):
        child_lines.append((i+1, line))
    elif re.search(r'^\s*\*\*小星的.*?\*\*', line) or re.search(r'^\s*\*\*小宇的.*?\*\*', line):
        child_lines.append((i+1, line))

print("儿童角色台词统计:")
for idx, (line_num, line) in enumerate(child_lines):
    print(f"{idx+1}. 行{line_num}: {line.strip()}")

# 分类统计
questions = []
challenges = []
choices = []

for line_num, line in child_lines:
    # 提取台词内容（去除角色标签）
    match = re.search(r'^\s*\*\*(小星|小宇)(的)?(.*?)\*\*\s*[:：]\s*(.*)', line)
    if match:
        role = match.group(1)
        suffix = match.group(2)  # 的
        label = match.group(3)   # 即兴提问/辩论回合等
        text = match.group(4)
        
        # 判断是否为提问（包含问号）
        if '？' in text or '?' in text:
            questions.append((line_num, role, text))
        
        # 判断是否为质疑反驳（根据标签或关键词）
        if label and ('质疑' in label or '反驳' in label or '追问' in label or '辩论' in label):
            challenges.append((line_num, role, text))
        elif re.search(r'可是|但是|不过|然而|难道|怎么|为何|为什么|不对|错了|误解', text):
            challenges.append((line_num, role, text))
        
        # 立场选择暂时不自动判断，需要手动识别

print("\n=== 提问次数统计 ===")
for i, (ln, role, text) in enumerate(questions):
    print(f"{i+1}. 行{ln} {role}: {text}")
print(f"总提问次数: {len(questions)}")

print("\n=== 质疑反驳次数统计 ===")
for i, (ln, role, text) in enumerate(challenges):
    print(f"{i+1}. 行{ln} {role}: {text}")
print(f"总质疑反驳次数: {len(challenges)}")

# 输出总结
print("\n=== 当前统计结果 ===")
print(f"儿童提问次数: {len(questions)}")
print(f"质疑反驳次数: {len(challenges)}")
print("立场选择次数: 需要手动识别（目前可能为0）")