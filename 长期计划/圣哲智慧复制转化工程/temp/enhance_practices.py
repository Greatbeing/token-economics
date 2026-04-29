#!/usr/bin/env python3
import os
import re
import sys

# 设置路径
base_dir = "outputs/儿童哲学史/优化阶段"
backup_dir = "outputs/儿童哲学史/优化阶段/backup"
os.makedirs(backup_dir, exist_ok=True)

# 定义增强函数
def enhance_practice(chapter_num, content):
    """增强实践练习部分"""
    # 查找实践练习部分
    pattern = r'(## 实践练习[:：].*?)(?=\n## |\n---|\n```|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        # 尝试查找"实践环节"
        pattern = r'(## 实践环节[:：].*?)(?=\n## |\n---|\n```|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not match:
        print(f"第{chapter_num}章未找到实践练习部分")
        return content
    
    practice_section = match.group(1)
    print(f"第{chapter_num}章找到实践练习部分，长度{len(practice_section)}字符")
    
    # 根据章节主题定制增强
    enhanced = enhance_practice_template(chapter_num, practice_section)
    
    # 替换原内容
    new_content = content.replace(practice_section, enhanced)
    return new_content

def enhance_practice_template(chapter_num, original):
    """根据章节生成增强版实践练习"""
    # 这里实现具体的增强逻辑
    # 暂时返回原内容，待完善
    return original

# 处理所有章节
for i in range(1, 13):
    chapter_map = {
        1: "第一章优化稿.md",
        2: "第二章优化稿.md",
        3: "第三章优化稿.md",
        4: "第四章优化稿.md",
        5: "第五章优化稿.md",
        6: "第六章优化稿.md",
        7: "第七章优化稿.md",
        8: "第八章优化稿.md",
        9: "第九章优化稿.md",
        10: "第十章优化稿.md",
        11: "第十一章优化稿.md",
        12: "第十二章优化稿.md"
    }
    
    filename = chapter_map[i]
    filepath = os.path.join(base_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"文件不存在: {filepath}")
        continue
    
    # 备份原文件
    backup_path = os.path.join(backup_dir, f"{filename}.backup")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 增强实践练习
    new_content = enhance_practice(i, content)
    
    # 保存新内容
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"第{i}章处理完成")

