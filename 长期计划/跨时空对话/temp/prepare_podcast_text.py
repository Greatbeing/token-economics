#!/usr/bin/env python3

# 读取对话文本
with open('temp/dialogue_for_podcast.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

podcast_lines = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    # 如果以角色名开头，去除角色名和冒号
    if '：' in line:
        # 分割角色和台词
        parts = line.split('：', 1)
        if len(parts) == 2:
            role, text = parts
            # 只保留台词
            podcast_lines.append(text)
        else:
            podcast_lines.append(line)
    else:
        podcast_lines.append(line)

# 合并为连续文本，用句号分隔
podcast_text = '。'.join(podcast_lines)
# 确保句号正确
podcast_text = podcast_text.replace('。。', '。')

print(f"播客文本长度：{len(podcast_text)} 字符")

# 保存
with open('temp/podcast_text.txt', 'w', encoding='utf-8') as f:
    f.write(podcast_text)

print("播客文本已保存到 temp/podcast_text.txt")

# 也创建一个带有角色提示的版本（用于调试）
with open('temp/podcast_with_roles.txt', 'w', encoding='utf-8') as f:
    for line in lines:
        f.write(line)

print("带有角色的版本已保存")