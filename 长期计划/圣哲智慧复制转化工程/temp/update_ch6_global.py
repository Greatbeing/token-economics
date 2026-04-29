#!/usr/bin/env python3
import re

# 读取第六章文件
with open('outputs/儿童哲学史/优化阶段/第六章优化稿.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 定位全球望远镜部分
pattern = r'(## 全球望远镜：中西心灵探险对话.*?)(?=---\n\n## 实践练习：三周心灵训练计划)'
match = re.search(pattern, content, re.DOTALL)
if not match:
    print("未找到全球望远镜部分")
    exit(1)

global_section = match.group(1)

# 对比组一：王阳明“致良知” vs 西方心理学“认知行为疗法（CBT）”
# 找到表格后的“思考题”
sub1_pattern = r'(### 对比组一：王阳明“致良知” vs 西方心理学“认知行为疗法（CBT）”.*?\n\n)(.*?)(\n\n\*\*思考题\*\*：)'
sub1_match = re.search(sub1_pattern, global_section, re.DOTALL)
if sub1_match:
    before_table = sub1_match.group(1)
    table_content = sub1_match.group(2)
    after_table = sub1_match.group(3)  # “**思考题**：”
    # 添加对比点、差异说明、视觉建议
    new_content = before_table + table_content + "\n\n**对比点**：王阳明“致良知”强调回归内在道德判断，西方CBT关注识别并改变负面思维模式，两者都通过行动验证，但起点不同（良知 vs 认知）。\n\n**差异说明**：就像照镜子——王阳明教孩子擦拭心里的明镜，看清是非；CBT教孩子识别镜子上的扭曲认知，纠正想法。\n\n【视觉建议】：简笔画对比图：左边王阳明手持镜子擦拭，右边心理学家拿着思维气泡图调整，中间孩子同时尝试两种方法。"
    global_section = global_section.replace(sub1_match.group(0), new_content + after_table)
else:
    print("未找到对比组一")

# 对比组二：禅宗“顿悟” vs 西方哲学“理性分析”
# 将“视觉描述”改为【视觉建议】
sub2_pattern = r'(### 对比组二：禅宗“顿悟” vs 西方哲学“理性分析”.*?\n\n)(.*?)(\n\n\*\*视觉描述\*\*：)(.*?)(\n\n\*\*思考题\*\*：)'
sub2_match = re.search(sub2_pattern, global_section, re.DOTALL)
if sub2_match:
    before_table2 = sub2_match.group(1)
    table_content2 = sub2_match.group(2)
    visual_label = sub2_match.group(3)  # “**视觉描述**：”
    visual_content = sub2_match.group(4)
    after_visual = sub2_match.group(5)  # “**思考题**：”
    # 替换为【视觉建议】
    new_visual_label = "\n\n【视觉建议】："
    new_sub2 = before_table2 + table_content2 + new_visual_label + visual_content + after_visual
    global_section = global_section.replace(sub2_match.group(0), new_sub2)
else:
    print("未找到对比组二")

# 更新整个内容
new_content = content.replace(match.group(0), global_section)

# 写回文件
with open('outputs/儿童哲学史/优化阶段/第六章优化稿.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("第六章全球望远镜已更新")