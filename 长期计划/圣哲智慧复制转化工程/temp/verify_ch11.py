import re

with open('outputs/儿童哲学史/优化阶段/第十一章优化稿.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 思想剧场部分：从 "## 思想剧场" 到 "---" 后接 "## 第一课时"
pattern = r'## 思想剧场：时间裂缝里的对话.*?(?=\n## 第一课时|\Z)'
match = re.search(pattern, content, re.DOTALL)
if not match:
    print("未找到思想剧场部分")
    exit()

thought_theater = match.group(0)
print("思想剧场长度:", len(thought_theater))

# 匹配儿童台词行：以 **小启**、**小蒙**、**小变** 开头，或者 小启：、小蒙：、小变：
child_pattern = r'(?:\*\*小[启蒙变]\*\*|小[启蒙变]：)[^\\n]*'
child_lines = re.findall(child_pattern, thought_theater)

print(f"找到 {len(child_lines)} 句儿童台词:")
for i, line in enumerate(child_lines, 1):
    print(f"{i:2}. {line}")

# 统计提问
questions = [line for line in child_lines if '？' in line or '?' in line]
print(f"\n提问次数: {len(questions)}")

# 统计质疑反驳：包含关键词
doubt_keywords = ['质疑', '反驳', '不对', '可是', '但是', '但', '如果', '呢', '吗', '怎么', '为什么', '难道', '却', '可是']
doubt_lines = []
for line in child_lines:
    if any(kw in line for kw in doubt_keywords):
        doubt_lines.append(line)
    # 额外检查括号标注
    if '（质疑）' in line or '（反驳）' in line or '（困惑）' in line:
        doubt_lines.append(line)

# 去重
doubt_lines = list(set(doubt_lines))
print(f"质疑反驳次数: {len(doubt_lines)}")
for d in doubt_lines:
    print(f"  {d}")

# 统计立场选择：包含选择关键词
choice_keywords = ['选', '觉得', '支持', '同意', '赞成', '立场', '该选', '更认同']
choice_lines = []
for line in child_lines:
    if any(kw in line for kw in choice_keywords):
        choice_lines.append(line)

choice_lines = list(set(choice_lines))
print(f"立场选择次数: {len(choice_lines)}")
for c in choice_lines:
    print(f"  {c}")

print("\n=== 达标情况 ===")
print(f"提问≥8: {'✅' if len(questions) >= 8 else '❌'} ({len(questions)}次)")
print(f"质疑反驳≥4: {'✅' if len(doubt_lines) >= 4 else '❌'} ({len(doubt_lines)}次)")
print(f"立场选择≥2: {'✅' if len(choice_lines) >= 2 else '❌'} ({len(choice_lines)}次)")

# 检查生活共鸣点（简单搜索）
life_keywords = ['班级', '学校', '同学', '班长', '选举', '作业', '考试', '游戏', '沙堡', '乐高']
life_found = []
for line in child_lines:
    if any(kw in line for kw in life_keywords):
        life_found.append(line)

print(f"\n生活共鸣点: {len(life_found)}处")
for l in life_found[:3]:  # 显示前三个
    print(f"  {l}")