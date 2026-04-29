import re

with open('outputs/儿童哲学史/优化阶段/第十二章优化稿.md', 'r', encoding='utf-8') as f:
    content = f.read()

child_names = ['小智', '小慧', '小美', '小强', '小启', '小蒙', '小变', '小星', '小宇']
lines = content.split('\n')
child_lines = []

for line in lines:
    line_stripped = line.strip()
    for name in child_names:
        if line_stripped.startswith(f'**{name}**') or line_stripped.startswith(f'{name}'):
            child_lines.append(line)
            break
        elif f'{name}：' in line:
            child_lines.append(line)
            break

questions = [l for l in child_lines if '？' in l or '?' in l]
doubts = [l for l in child_lines if any(keyword in l for keyword in ['可是', '但是', '不对', '质疑', '反驳'])]
stances = [l for l in child_lines if '立场选择' in l]

print(f"儿童台词总数: {len(child_lines)}")
print(f"提问次数: {len(questions)} (目标≥8)")
print(f"质疑反驳次数: {len(doubts)} (目标≥4)")
print(f"立场选择次数: {len(stances)} (目标≥2)")

# 检查生活共鸣点
life_experience_keywords = ['班级', '选举', '考试', '游戏时间', '嫉妒', '朋友', '成绩', '起床困难']
life_lines = []
for line in child_lines:
    if any(keyword in line for keyword in life_experience_keywords):
        life_lines.append(line)

print(f"\n生活共鸣点数量: {len(life_lines)}")
for line in life_lines[:5]:
    print(f"  - {line}")

if len(questions) >= 8 and len(doubts) >= 4 and len(stances) >= 2 and len(life_lines) >= 1:
    print("\n✅ 所有验收标准达标！")
else:
    print("\n❌ 部分标准未达标：")
    if len(questions) < 8:
        print(f"  提问次数不足: {len(questions)} < 8")
    if len(doubts) < 4:
        print(f"  质疑反驳次数不足: {len(doubts)} < 4")
    if len(stances) < 2:
        print(f"  立场选择次数不足: {len(stances)} < 2")
    if len(life_lines) < 1:
        print("  生活共鸣点不足")