#!/usr/bin/env python3
import re

# 读取第四章文件
with open('outputs/儿童哲学史/优化阶段/第四章优化稿.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 定位全球望远镜部分
pattern = r'(## 全球望远镜（深度对比版）.*?)(?=---\n\n## 实践练习：三周自由实验室)'
match = re.search(pattern, content, re.DOTALL)
if not match:
    print("未找到全球望远镜部分")
    exit(1)

global_section = match.group(1)

# 对比一：老子vs斯多葛学派
# 在表格和“思考题”之间插入对比点、差异说明、视觉建议
# 找到表格后的“思考题”位置
sub1_pattern = r'(### 对比一：老子vs斯多葛学派.*?\n\n)(.*?)(\n\n\*\*思考题\*\*：)'
sub1_match = re.search(sub1_pattern, global_section, re.DOTALL)
if sub1_match:
    before_table = sub1_match.group(1)  # 标题
    table_content = sub1_match.group(2)  # 表格
    after_table = sub1_match.group(3)   # “思考题”行
    # 构造新内容
    new_sub1 = before_table + table_content + "\n\n**对比点**：老子和斯多葛学派都强调“顺应”，但老子的“无为”是整体自然的不干预，斯多葛的“理性控制”是个体选择。\n\n**差异说明**：就像园丁对待花园——老子选择不按快进键，让万物自然生长；斯多葛学派则像区分“我的球”和“别人的球”，只控制自己能控制的。\n\n【视觉建议】：简笔画地图标出中国与古希腊罗马的地理位置，老子骑青牛在竹林旁，斯多葛哲人站在柱廊前，中间有孩子对比两种态度。\n" + after_table
    global_section = global_section.replace(sub1_match.group(0), new_sub1)
else:
    print("未找到对比一")

# 对比二：韩非子vs社会契约论
# 将“简笔画地图构思”改为【视觉建议】
sub2_pattern = r'(### 对比二：韩非子vs社会契约论.*?\n\n)(.*?)(\n\n\*\*简笔画地图构思\*\*：)(.*?)(\n\n\*\*对比点\*\*：)'
sub2_match = re.search(sub2_pattern, global_section, re.DOTALL)
if sub2_match:
    before_table2 = sub2_match.group(1)
    table_content2 = sub2_match.group(2)
    map_label = sub2_match.group(3)  # “简笔画地图构思：”
    map_content = sub2_match.group(4)
    after_map = sub2_match.group(5)  # “**对比点**：”
    # 替换为【视觉建议】
    new_map_label = "\n\n【视觉建议】："
    new_sub2 = before_table2 + table_content2 + new_map_label + map_content + after_map
    global_section = global_section.replace(sub2_match.group(0), new_sub2)
else:
    print("未找到对比二")

# 更新整个内容
new_content = content.replace(match.group(0), global_section)

# 写回文件
with open('outputs/儿童哲学史/优化阶段/第四章优化稿.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("第四章全球望远镜已更新")