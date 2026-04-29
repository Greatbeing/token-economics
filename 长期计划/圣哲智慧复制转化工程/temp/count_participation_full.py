#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统计整个文件中的儿童参与感指标"""

import re

def count_participation(text):
    """统计儿童提问、质疑反驳、立场选择的次数"""
    
    # 查找所有儿童台词
    # 格式：**小X**：（内容）
    child_pattern = re.compile(r'\*\*小[^\*]{1,3}\*\*：.*?\n')
    child_matches = child_pattern.findall(text)
    
    print(f"找到 {len(child_matches)} 条儿童台词")
    
    # 显示所有儿童台词
    for i, line in enumerate(child_matches[:20]):
        print(f"{i+1}. {line.strip()}")
    
    # 统计提问（包含问号或"提问"关键词）
    questions = 0
    question_lines = []
    
    # 统计质疑反驳
    challenges = 0
    challenge_lines = []
    
    # 统计立场选择
    choices = 0
    choice_lines = []
    
    for line in child_matches:
        line_text = line.strip()
        
        # 检查提问
        if '？' in line_text or '?' in line_text or '提问' in line_text:
            questions += 1
            question_lines.append(line_text)
        
        # 检查质疑反驳
        challenge_keywords = ['质疑', '反驳', '不对', '可是', '但是', '不过', '然而', '怎么', '为什么', '真的吗', '难受']
        for keyword in challenge_keywords:
            if keyword in line_text:
                challenges += 1
                challenge_lines.append(line_text)
                break
        
        # 检查立场选择
        choice_keywords = ['我选', '选', '选择', '立场选择']
        for keyword in choice_keywords:
            if keyword in line_text:
                choices += 1
                choice_lines.append(line_text)
                break
    
    print(f"\n=== 统计结果 ===")
    print(f"儿童提问次数: {questions}")
    print(f"质疑反驳次数: {challenges}")
    print(f"立场选择次数: {choices}")
    
    # 检查达标情况
    target_questions = 8
    target_challenges = 4
    target_choices = 2
    
    print(f"\n目标：提问≥{target_questions}，质疑反驳≥{target_challenges}，立场选择≥{target_choices}")
    
    if questions >= target_questions and challenges >= target_challenges and choices >= target_choices:
        print("✅ 所有儿童参与感指标达标！")
    else:
        print("⚠️ 指标未达标：")
        if questions < target_questions:
            print(f"  - 提问次数不足：{questions}/{target_questions} (需增加{target_questions - questions}次)")
        if challenges < target_challenges:
            print(f"  - 质疑反驳次数不足：{challenges}/{target_challenges} (需增加{target_challenges - challenges}次)")
        if choices < target_choices:
            print(f"  - 立场选择次数不足：{choices}/{target_choices} (需增加{target_choices - choices}次)")
    
    return questions, challenges, choices

def main():
    file_path = "outputs/儿童哲学史/优化阶段/第六章优化稿.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=== 第六章儿童参与感指标全面分析 ===\n")
    questions, challenges, choices = count_participation(content)
    
    return questions, challenges, choices

if __name__ == "__main__":
    main()