import re
import sys

# 读取文件
with open('outputs/儿童哲学史/优化阶段/第十一章优化稿.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取思想剧场部分（从 "## 思想剧场" 到下一个 "##" 或 "---" 分割）
# 用正则表达式找到思想剧场部分
thought_theater_pattern = r'## 思想剧场：时间裂缝里的对话.*?(?=\n##|\n---)'
thought_theater_match = re.search(thought_theater_pattern, content, re.DOTALL)

if not thought_theater_match:
    print("未找到思想剧场部分")
    sys.exit(1)

thought_theater = thought_theater_match.group(0)
print("思想剧场内容预览（前500字符）：")
print(thought_theater[:500])
print("\n" + "="*50)

# 统计儿童台词
child_names = ['小启', '小蒙', '小变']
child_lines = []

# 提取所有台词行（以孩子名字开头的行）
lines = thought_theater.split('\n')
for line in lines:
    line = line.strip()
    for name in child_names:
        if line.startswith(f'**{name}**') or line.startswith(f'{name}：'):
            child_lines.append(line)
            break

print(f"儿童台词共 {len(child_lines)} 句：")
for line in child_lines:
    print(f"  {line}")

# 统计提问次数（包含问号的台词）
questions = [line for line in child_lines if '？' in line or '?' in line]
print(f"\n提问次数：{len(questions)}")
for q in questions:
    print(f"  {q}")

# 统计质疑反驳次数（包含关键词）
keywords = ['质疑', '反驳', '不对', '可是', '但是', '但', '如果', '呢', '吗', '怎么', '为什么', '难道', '却']
# 注意：有些台词可能带有括号标注，如（质疑）、（困惑）等
doubt_lines = []
for line in child_lines:
    # 检查括号中的标注
    if '（质疑）' in line or '（反驳）' in line or '（困惑）' in line or '（提问）' in line:
        doubt_lines.append(line)
    else:
        # 检查关键词
        for kw in keywords:
            if kw in line:
                doubt_lines.append(line)
                break

# 去重（同一台词可能匹配多个关键词）
doubt_lines = list(set(doubt_lines))
print(f"\n质疑反驳次数：{len(doubt_lines)}")
for d in doubt_lines:
    print(f"  {d}")

# 统计立场选择次数（需要儿童做出选择的场景）
# 在思想剧场中，儿童明确做出选择的台词
# 如“我选...”、“我觉得...”、“我支持...”等
choice_keywords = ['选', '觉得', '支持', '同意', '赞成', '立场']
choice_lines = []
for line in child_lines:
    for kw in choice_keywords:
        if kw in line:
            choice_lines.append(line)
            break

print(f"\n立场选择次数：{len(choice_lines)}")
for c in choice_lines:
    print(f"  {c}")

# 输出统计结果
print("\n" + "="*50)
print("统计结果：")
print(f"儿童提问次数：{len(questions)}")
print(f"儿童质疑反驳次数：{len(doubt_lines)}")
print(f"儿童立场选择次数：{len(choice_lines)}")

# 检查是否达到目标
target_questions = 8
target_doubt = 4
target_choice = 2

print(f"\n目标：提问≥{target_questions}，质疑反驳≥{target_doubt}，立场选择≥{target_choice}")
print(f"提问达标：{'是' if len(questions) >= target_questions else '否'}")
print(f"质疑反驳达标：{'是' if len(doubt_lines) >= target_doubt else '否'}")
print(f"立场选择达标：{'是' if len(choice_lines) >= target_choice else '否'}")