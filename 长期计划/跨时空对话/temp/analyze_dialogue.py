#!/usr/bin/env python3
import re

with open('temp/dialogue_for_podcast.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

dialogues = []
for line in lines:
    line = line.strip()
    if not line or '：' not in line:
        continue
    role, text = line.split('：', 1)
    dialogues.append((role, text))

# 按角色分组
role_texts = {}
for role, text in dialogues:
    if role not in role_texts:
        role_texts[role] = []
    role_texts[role].append(text)

# 统计
for role, texts in role_texts.items():
    total_chars = sum(len(t) for t in texts)
    num_lines = len(texts)
    print(f"{role}: {num_lines}条台词，总字符数{total_chars}")
    
    # 估算时长
    if role == '孔子':
        # 沉稳浑厚约120字/分钟
        estimated_minutes = total_chars / 120
    elif role == '庄子':
        # 悠远空灵约100字/分钟
        estimated_minutes = total_chars / 100
    else:  # 小张
        # 平均约130字/分钟（语速变化）
        estimated_minutes = total_chars / 130
    
    print(f"  预计时长: {estimated_minutes:.2f}分钟 ({estimated_minutes*60:.1f}秒)")

# 总统计
total_chars_all = sum(len(t) for _, t in dialogues)
print(f"\n总计: {len(dialogues)}条台词，总字符数{total_chars_all}")
print(f"平均语速120字/分钟: {total_chars_all/120:.2f}分钟 ({total_chars_all/120*60:.1f}秒)")
print(f"平均语速150字/分钟: {total_chars_all/150:.2f}分钟 ({total_chars_all/150*60:.1f}秒)")

# 提取每个角色的纯文本文件
for role, texts in role_texts.items():
    with open(f'temp/{role}_text.txt', 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(texts))
    print(f"已保存 {role}_text.txt")