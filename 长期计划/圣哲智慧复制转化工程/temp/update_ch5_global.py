#!/usr/bin/env python3
import re

# 读取第五章文件
with open('outputs/儿童哲学史/优化阶段/第五章优化稿.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 定位全球望远镜部分
pattern = r'(## 全球望远镜（深度对比版）.*?)(?=---\n\n## 实践练习：三周规则实验室)'
match = re.search(pattern, content, re.DOTALL)
if not match:
    print("未找到全球望远镜部分")
    exit(1)

global_section = match.group(1)

# 对比一：墨子“兼爱”vs基督教“博爱”
# 在思考题后添加视觉建议，或者插入在思考题之前？按照第四章的样式，视觉建议放在思考题之前。
# 找到表格后的“对比点”区域
sub1_pattern = r'(### 对比一：墨子“兼爱”vs基督教“博爱”.*?\n\n)(.*?)(\n\n\*\*对比点\*\*：)'
sub1_match = re.search(sub1_pattern, global_section, re.DOTALL)
if sub1_match:
    before_table = sub1_match.group(1)
    table_content = sub1_match.group(2)
    after_table = sub1_match.group(3)  # “**对比点**：”行
    # 在表格后、对比点前插入视觉建议
    visual_suggestion1 = "\n\n【视觉建议】：简笔画爱心Wi-Fi信号覆盖地球，左边墨子手持信号发射器，右边耶稣张开双臂，中间有孩子连接两种爱心网络。"
    new_sub1 = before_table + table_content + visual_suggestion1 + after_table
    global_section = global_section.replace(sub1_match.group(0), new_sub1)
else:
    print("未找到对比一表格")

# 对比二：孟子“仁政”vs西方“福利国家”理念
# 将“简笔画地图构思”改为【视觉建议】
sub2_pattern = r'(### 对比二：孟子“仁政”vs西方“福利国家”理念.*?\n\n)(.*?)(\n\n\*\*简笔画地图构思\*\*：)(.*?)(\n\n\*\*对比点\*\*：)'
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
with open('outputs/儿童哲学史/优化阶段/第五章优化稿.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("第五章全球望远镜已更新")