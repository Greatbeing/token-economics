#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析第六章的儿童参与感指标"""

import re

def count_participation(text):
    """统计儿童提问、质疑反驳、立场选择的次数"""
    
    # 儿童台词通常以 **小星**、**小宇**、**小慧**、**小智** 等开头
    # 假设格式为：**小星**：（台词内容）
    
    # 匹配儿童台词
    child_pattern = re.compile(r'\*\*小[星宇慧智强]\*\*：.*?（.*?）')
    # 改进：匹配所有可能的儿童角色
    child_lines = re.findall(r'\*\*小[^\*]{1,3}\*\*：.*?（.*?）', text)
    
    if not child_lines:
        # 尝试另一种格式：**小星**：（台词内容）不带括号
        child_lines = re.findall(r'\*\*小[^\*]{1,3}\*\*：[^（]*', text)
    
    print(f"找到 {len(child_lines)} 条儿童台词")
    
    # 统计提问（包含问号）
    questions = 0
    for line in child_lines:
        if '？' in line or '?' in line:
            questions += 1
    
    # 统计质疑反驳（包含关键词）
    keywords = ['质疑', '反驳', '不对', '可是', '但是', '不过', '然而', '怎么', '为什么', '真的吗']
    challenges = 0
    for line in child_lines:
        for keyword in keywords:
            if keyword in line:
                challenges += 1
                break
    
    # 统计立场选择（包含"选"、"我选"等）
    choices = 0
    choice_patterns = ['我选', '选', '选择', '立场选择']
    for line in child_lines:
        for pattern in choice_patterns:
            if pattern in line:
                choices += 1
                break
    
    # 输出结果
    print(f"儿童提问次数: {questions}")
    print(f"质疑反驳次数: {challenges}")
    print(f"立场选择次数: {choices}")
    
    # 检查是否达标
    target_questions = 8
    target_challenges = 4
    target_choices = 2
    
    print(f"\n目标：提问≥{target_questions}，质疑反驳≥{target_challenges}，立场选择≥{target_choices}")
    
    if questions >= target_questions and challenges >= target_challenges and choices >= target_choices:
        print("✅ 所有儿童参与感指标达标！")
    else:
        print("⚠️ 部分指标未达标：")
        if questions < target_questions:
            print(f"  - 提问次数不足：{questions}/{target_questions}")
        if challenges < target_challenges:
            print(f"  - 质疑反驳次数不足：{challenges}/{target_challenges}")
        if choices < target_choices:
            print(f"  - 立场选择次数不足：{choices}/{target_choices}")
    
    return questions, challenges, choices

def main():
    file_path = "outputs/儿童哲学史/优化阶段/第六章优化稿.md"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("=== 第六章儿童参与感指标分析 ===\n")
        questions, challenges, choices = count_participation(content)
        
        # 输出一些示例台词
        print("\n=== 示例儿童台词（前10条）===")
        child_lines = re.findall(r'\*\*小[^\*]{1,3}\*\*：.*', content)
        for i, line in enumerate(child_lines[:10]):
            print(f"{i+1}. {line}")
            
        return questions, challenges, choices
        
    except Exception as e:
        print(f"读取文件出错: {e}")
        return None, None, None

if __name__ == "__main__":
    main()