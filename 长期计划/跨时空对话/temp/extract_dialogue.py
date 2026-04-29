#!/usr/bin/env python3
import re

# 读取剧本文件
with open('outputs/脚本/第三期短剧剧本_v2.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 使用正则表达式提取角色台词
# 匹配模式：**角色**：（可能有多行台词，直到下一个**角色**：或空行）
pattern = r'\*\*(.*?)\*\*：(.*?)(?=\n\s*\*\*|\n\n|\Z)'
matches = re.findall(pattern, content, re.DOTALL)

# 整理台词
dialogues = []
for role, text in matches:
    # 清理文本：去除首尾空白，合并内部空白
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    if text:
        dialogues.append((role, text))

# 输出统计
print(f"提取到 {len(dialogues)} 条台词")

# 保存为文本文件，每行格式：角色：台词
with open('temp/dialogue_text.txt', 'w', encoding='utf-8') as f:
    for role, text in dialogues:
        f.write(f"{role}：{text}\n\n")

print("对话文本已保存到 temp/dialogue_text.txt")

# 同时按场景分隔？剧本中有场景分隔线，但为了简单起见，我们先全部提取
# 也可以尝试按场景分割
scenes = content.split('---')
print(f"剧本有 {len(scenes)} 个场景分隔")
for i, scene in enumerate(scenes[:3], 1):
    print(f"\n=== 场景 {i} ===")
    # 提取该场景的台词
    scene_matches = re.findall(pattern, scene, re.DOTALL)
    for role, text in scene_matches:
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        if text:
            print(f"{role}：{text[:100]}...")