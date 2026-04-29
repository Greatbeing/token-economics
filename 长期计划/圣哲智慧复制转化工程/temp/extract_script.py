import re

with open('temp/视频脚本/庄子视频脚本.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找所有解说词块
pattern = r'解说词：\n> "(.+?)"'
matches = re.findall(pattern, content, re.DOTALL)

full_text = ""
for i, match in enumerate(matches, 1):
    # 清理多余的换行和空格
    clean_text = match.replace('\n', ' ').strip()
    full_text += clean_text + " "

print("提取的解说词总长度:", len(full_text))
print("\n完整解说文本:")
print(full_text)

# 保存到文件
with open('temp/视频素材/庄子/音频/解说文本.txt', 'w', encoding='utf-8') as f:
    f.write(full_text)