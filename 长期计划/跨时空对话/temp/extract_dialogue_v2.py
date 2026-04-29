#!/usr/bin/env python3
import re

with open('outputs/脚本/第三期短剧剧本_v2.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

dialogues = []
current_role = None
current_text = []

# 角色模式
role_pattern = re.compile(r'^\*\*(小张|孔子|庄子)\*\*：')

for line in lines:
    line = line.rstrip()
    
    # 检测角色行
    match = role_pattern.match(line)
    if match:
        # 保存前一个角色的台词
        if current_role and current_text:
            dialogues.append((current_role, ' '.join(current_text)))
            current_text = []
        current_role = match.group(1)
        # 如果该行还有台词内容（在冒号后）
        if '：“' in line:
            # 提取引号内容
            quote_match = re.search(r'：“(.*?)”', line)
            if quote_match:
                current_text.append(quote_match.group(1))
        continue
    
    # 如果是引号行（台词）
    if line.startswith('“') and current_role:
        # 提取引号内容，可能跨多行
        line_content = line.strip('“”')
        current_text.append(line_content)
        continue
    
    # 如果是空行，且当前有台词，结束当前台词段
    if not line.strip() and current_role and current_text:
        dialogues.append((current_role, ' '.join(current_text)))
        current_role = None
        current_text = []

# 添加最后一个
if current_role and current_text:
    dialogues.append((current_role, ' '.join(current_text)))

print(f"提取到 {len(dialogues)} 条台词")

# 保存为纯文本，用于播客生成
with open('temp/dialogue_for_podcast.txt', 'w', encoding='utf-8') as f:
    for role, text in dialogues:
        f.write(f"{role}：{text}\n\n")

print("对话文本已保存到 temp/dialogue_for_podcast.txt")

# 也按角色分开保存
roles = set([role for role, _ in dialogues])
for r in roles:
    with open(f'temp/dialogue_{r}.txt', 'w', encoding='utf-8') as f:
        for role, text in dialogues:
            if role == r:
                f.write(f"{text}\n\n")

print("按角色分开的文本已保存")