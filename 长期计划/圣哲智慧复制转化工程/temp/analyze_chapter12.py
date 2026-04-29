import re

# 读取文件
with open('outputs/儿童哲学史/优化阶段/第十二章优化稿.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义儿童角色名字
child_names = ['小智', '小慧', '小美', '小强', '小启', '小蒙', '小变', '小星', '小宇']

# 找到所有儿童台词行
lines = content.split('\n')
child_lines = []

for line in lines:
    line_stripped = line.strip()
    # 检查是否以儿童名字开头（可能带**加粗**或直接名字）
    for name in child_names:
        # 匹配格式：**小智**：（带加粗）
        if line_stripped.startswith(f'**{name}**'):
            child_lines.append(line)
            break
        # 匹配格式：小智：（无加粗）
        elif line_stripped.startswith(f'{name}'):
            child_lines.append(line)
            break
        # 匹配格式：包含"小智："（可能前面有空格）
        elif f'{name}：' in line:
            child_lines.append(line)
            break

print(f"找到 {len(child_lines)} 句儿童台词:")
for i, line in enumerate(child_lines[:30], 1):
    print(f"{i}: {line}")

# 统计提问次数（包含问号）
questions = [l for l in child_lines if '？' in l or '?' in l]
print(f"\n=== 提问次数: {len(questions)} ===")
for q in questions:
    print(f"  - {q}")

# 统计质疑反驳次数（包含关键词）
keywords = ['质疑', '反驳', '不对', '可是', '但是', '但', '如果.*呢', '可是.*', '但是.*']
doubt_lines = []
for line in child_lines:
    line_lower = line.lower()
    # 简单关键词匹配
    if any(keyword in line for keyword in ['可是', '但是', '不对', '质疑', '反驳']):
        doubt_lines.append(line)
    # 正则匹配更复杂的模式
    elif re.search(r'如果.*[呢吗]', line):
        doubt_lines.append(line)
    elif '但我觉得' in line:
        doubt_lines.append(line)

print(f"\n=== 质疑反驳次数: {len(doubt_lines)} ===")
for d in doubt_lines:
    print(f"  - {d}")

# 统计立场选择次数
# 查找包含"立场选择"标记的台词
stance_lines = []
for line in child_lines:
    if '立场选择' in line:
        stance_lines.append(line)

print(f"\n=== 立场选择次数: {len(stance_lines)} ===")
for s in stance_lines:
    print(f"  - {s}")

# 如果没有找到，可能需要查找儿童做出选择的场景
# 例如包含"选择"、"应该"、"更倾向"等词
if len(stance_lines) < 2:
    print("\n=== 搜索更多立场选择场景 ===")
    for line in child_lines:
        if any(word in line for word in ['选择', '应该', '更倾向', '我会', '我要']):
            print(f"  可能: {line}")

# 输出统计结果
print("\n=== 统计结果 ===")
print(f"儿童提问次数: {len(questions)} (目标≥8)")
print(f"儿童质疑反驳次数: {len(doubt_lines)} (目标≥4)")
print(f"儿童立场选择次数: {len(stance_lines)} (目标≥2)")