import re
with open('outputs/儿童哲学史/优化阶段/第七章优化稿.md', 'r', encoding='utf-8') as f:
    text = f.read()
# 移除代码块
text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
# 移除行内代码
text = re.sub(r'`[^`]*`', '', text)
# 移除Markdown标记
text = re.sub(r'[#*\-_~`]', '', text)
# 统计汉字
hanzi = re.findall(r'[\u4e00-\u9fff]', text)
print(f'汉字数量: {len(hanzi)}')
# 粗略估算字数（汉字数 * 0.8，因为包含标点和空格）
approx = int(len(hanzi) * 0.8)
print(f'估算字数: {approx}')