#!/usr/bin/env python3
import re

# 读取第一章文件
with open('outputs/儿童哲学史/优化阶段/第一章优化稿.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到全球望远镜部分
start_idx = -1
for i, line in enumerate(lines):
    if line.strip() == '## 全球望远镜（深度对比版）':
        start_idx = i
        break

if start_idx == -1:
    print("未找到全球望远镜部分")
    exit(1)

# 找到下一个二级标题（##）作为结束
end_idx = -1
for i in range(start_idx + 1, len(lines)):
    if lines[i].startswith('## ') and i != start_idx:
        end_idx = i
        break
if end_idx == -1:
    end_idx = len(lines)

telescope_section = lines[start_idx:end_idx]
print(f"全球望远镜部分从第{start_idx+1}行到第{end_idx}行")

# 将部分合并为字符串
section_text = ''.join(telescope_section)
print("\n=== 当前全球望远镜内容 ===")
print(section_text)

# 分析对比数量
# 查找对比标题，如“### 对比一：”
comparisons = re.findall(r'### 对比[一二三四五六七八九十]+：', section_text)
print(f"\n找到 {len(comparisons)} 个对比")

# 检查每个对比是否有三要素
# 粗略检查
if '对比点' in section_text:
    print("已有对比点")
else:
    print("缺少对比点")

if '差异说明' in section_text:
    print("已有差异说明")
else:
    print("缺少差异说明")

if '思考题' in section_text:
    print("已有思考题")
else:
    print("缺少思考题")

# 检查视觉建议
if '【视觉建议】' in section_text or '简笔画' in section_text:
    print("已有视觉描述")
else:
    print("缺少视觉描述")