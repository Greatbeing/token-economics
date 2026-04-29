#!/usr/bin/env python3
import re

# 读取第十二章文件
with open('outputs/儿童哲学史/优化阶段/第十二章优化稿.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 定位全球望远镜部分
pattern = r'(\#\#\#\# 全球望远镜：1940s的东西方哲学共振\n\n.*?\n)(\|.*?\|\n.*?\|\n)(.*?)(\n\n\*\*小美\*\*：)'
match = re.search(pattern, content, re.DOTALL)
if not match:
    print("未找到全球望远镜部分")
    exit(1)

before = match.group(1)  # 标题和介绍
table = match.group(2)   # 表格头两行
table_content = match.group(3)  # 表格内容
after = match.group(4)   # 后面的内容

# 完善三要素
enhancement = """
**对比点**：东方哲学从“关系和谐”寻找意义，西方哲学从“个体自由”创造意义。

**差异说明（儿童比喻）**：
- 东方哲学像**编织毛衣**：每一针都连接着其他线，意义在于整体的温暖与和谐。
- 西方哲学像**搭积木**：每一块都是独立的选择，意义在于你创造出的独特建筑。

【视觉建议】简笔画地图：左边画中国地图，上面有“关系网”图案；右边画欧洲地图，上面有“个体小人”图案；中间用桥梁连接，桥梁上写着“对话”。
"""

# 合并新内容
new_section = before + table + table_content + enhancement + after

# 替换整个部分
new_content = content[:match.start()] + new_section + content[match.end():]

# 写回文件
with open('outputs/儿童哲学史/优化阶段/第十二章优化稿.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("第十二章全球望远镜部分已完善")