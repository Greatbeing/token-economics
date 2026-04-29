#!/usr/bin/env python3
import re

with open('temp/dialogue_for_podcast.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

cleaned_lines = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    
    # 分割角色和台词
    if '：' in line:
        role, text = line.split('：', 1)
        # 清理台词：去除括号内的表演说明，但保留必要的停顿提示
        # 匹配中文括号和英文括号
        text = re.sub(r'（[^）]*）', '', text)  # 中文括号
        text = re.sub(r'\([^)]*\)', '', text)  # 英文括号
        text = re.sub(r'\[[^\]]*\]', '', text)  # 方括号
        # 去除多余的标点和空格
        text = re.sub(r'\s+', ' ', text).strip()
        # 保留必要的标点
        if text:
            cleaned_lines.append(f"{role}：{text}")
    else:
        cleaned_lines.append(line)

# 保存清理后的文本
with open('temp/cleaned_dialogue.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(cleaned_lines))

print(f"清理后对话行数: {len(cleaned_lines)}")

# 统计字符数
total_chars = sum(len(line.split('：', 1)[1]) if '：' in line else len(line) for line in cleaned_lines)
print(f"总字符数: {total_chars}")

# 创建用于播客的连续文本（不带角色名）
podcast_text = []
for line in cleaned_lines:
    if '：' in line:
        _, text = line.split('：', 1)
        podcast_text.append(text)
    else:
        podcast_text.append(line)

continuous_text = '。'.join(podcast_text)
continuous_text = re.sub(r'。+', '。', continuous_text)

print(f"播客文本字符数: {len(continuous_text)}")

with open('temp/cleaned_podcast_text.txt', 'w', encoding='utf-8') as f:
    f.write(continuous_text)