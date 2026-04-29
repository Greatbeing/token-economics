#!/usr/bin/env python3
import re
import sys

def analyze_chapter8(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有儿童角色的台词行
    # 格式如：**小敏**：（举手）...
    pattern = r'\*\*([小敏刚雨]+)\*\*：(.+)'
    matches = re.findall(pattern, content)
    
    child_lines = []
    for name, line in matches:
        child_lines.append((name, line.strip()))
    
    print(f"找到 {len(child_lines)} 条儿童台词")
    
    # 分类统计
    questions = []
    challenges = []
    choices = []
    
    for name, line in child_lines:
        # 判断是否为提问（包含问号）
        if '？' in line or '?' in line:
            questions.append((name, line))
        
        # 判断是否为质疑反驳（包含关键词）
        challenge_keywords = ['质疑', '反驳', '不对', '可是', '但是', '不过', '如果', '但我觉得', '可是', '但']
        # 检查台词中是否包含这些关键词，或者有（质疑）标注
        # 实际上标注可能在台词前，如（质疑），但我们已经去掉了**部分
        # 这里简单检查
        if any(keyword in line for keyword in challenge_keywords):
            challenges.append((name, line))
        
        # 判断是否为立场选择（包含关键词）
        choice_keywords = ['我选', '第二个', '选', '选择', '立场']
        if any(keyword in line for keyword in choice_keywords):
            choices.append((name, line))
    
    print("\n=== 提问次数统计 ===")
    for name, line in questions:
        print(f"{name}: {line[:50]}...")
    print(f"总提问次数: {len(questions)}")
    
    print("\n=== 质疑反驳统计 ===")
    for name, line in challenges:
        print(f"{name}: {line[:50]}...")
    print(f"总质疑反驳次数: {len(challenges)}")
    
    print("\n=== 立场选择统计 ===")
    for name, line in choices:
        print(f"{name}: {line[:50]}...")
    print(f"总立场选择次数: {len(choices)}")
    
    return {
        'questions': len(questions),
        'challenges': len(challenges),
        'choices': len(choices),
        'child_lines': child_lines
    }

if __name__ == '__main__':
    file_path = sys.argv[1] if len(sys.argv) > 1 else 'outputs/儿童哲学史/优化阶段/第八章优化稿.md'
    analyze_chapter8(file_path)