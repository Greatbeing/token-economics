#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析第五章优化稿中的儿童参与感指标
"""

import re
import sys

def read_file_content(filepath):
    """读取文件内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def analyze_child_participation(content):
    """分析儿童参与度"""
    lines = content.split('\n')
    
    # 初始化统计
    child_questions = 0  # 包含问号的儿童台词
    child_doubts = 0     # 包含质疑、反驳等关键词的台词
    child_choices = 0    # 立场选择场景
    
    # 儿童角色标识
    child_patterns = [r'^\*\*小星\*\*', r'^\*\*小宇\*\*', r'^\*\*小星\*\*：', r'^\*\*小宇\*\*：', 
                     r'^\*\*小星的即兴提问\*\*', r'^\*\*小宇的笔记\*\*', r'^\*\*小星的辩论回合\*\*',
                     r'^\*\*小宇的追问回合\*\*', r'^\*\*小星的质疑回合\*\*']
    
    # 质疑反驳关键词
    doubt_keywords = ['质疑', '反驳', '不对', '可是', '但', '但是', '如果', '呢', '怎么', '为什么',
                     '追问', '质疑', '挑战', '反对', '不同意', '不一定', '不见得']
    
    # 立场选择关键词
    choice_keywords = ['选择', '倾向', '偏好', '投票', '支持', '赞成', '反对', '认同', '不认同']
    
    # 当前角色
    current_speaker = None
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # 检查是否为儿童角色台词
        is_child = False
        child_name = None
        
        for pattern in child_patterns:
            if re.search(pattern, line_stripped):
                is_child = True
                if '小星' in pattern:
                    child_name = '小星'
                elif '小宇' in pattern:
                    child_name = '小宇'
                break
        
        # 如果是儿童角色的行
        if is_child:
            # 检查是否包含问号
            if '？' in line_stripped or '?' in line_stripped:
                child_questions += 1
                print(f"提问 {child_questions}: {line_stripped[:80]}...")
            
            # 检查是否包含质疑关键词
            for keyword in doubt_keywords:
                if keyword in line_stripped:
                    child_doubts += 1
                    print(f"质疑 {child_doubts}: {line_stripped[:80]}...")
                    break
        
        # 检查立场选择场景（可能跨越多行）
        if any(keyword in line_stripped for keyword in choice_keywords):
            # 检查是否为儿童相关的选择
            if '你的倾向' in line_stripped or '你的选择' in line_stripped or '□墨 □孟 □韩' in line_stripped:
                child_choices += 1
                print(f"立场选择 {child_choices}: {line_stripped[:80]}...")
    
    # 手动补充检查（因为可能格式不匹配）
    # 搜索所有包含儿童名字的台词
    child_lines = []
    for i, line in enumerate(lines):
        if re.search(r'小星|小宇', line) and '：' in line:
            child_lines.append(line)
    
    # 重新统计（更精确）
    child_questions = 0
    child_doubts = 0
    
    for line in child_lines:
        # 提问统计
        if '？' in line or '?' in line:
            child_questions += 1
        
        # 质疑统计（需要更精确）
        doubt_patterns = [r'可是', r'但', r'但是', r'不对', r'质疑', r'反驳', r'追问', r'挑战', r'反对']
        for pattern in doubt_patterns:
            if re.search(pattern, line):
                child_doubts += 1
                break
    
    # 立场选择场景（在"想一想"部分）
    choice_scenes = 0
    in_think_section = False
    for i, line in enumerate(lines):
        if '## 想一想' in line:
            in_think_section = True
        elif in_think_section and any(keyword in line for keyword in ['你的倾向', '你的选择', '□墨 □孟 □韩']):
            choice_scenes += 1
    
    return {
        'child_questions': child_questions,
        'child_doubts': child_doubts,
        'child_choices': choice_scenes,
        'total_child_lines': len(child_lines)
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python analyze_chapter5.py <文件路径>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    content = read_file_content(filepath)
    
    stats = analyze_child_participation(content)
    
    print("\n=== 第五章儿童参与度统计 ===")
    print(f"儿童提问次数: {stats['child_questions']} (目标: ≥8)")
    print(f"质疑反驳次数: {stats['child_doubts']} (目标: ≥4)")
    print(f"立场选择次数: {stats['child_choices']} (目标: ≥2)")
    print(f"儿童台词总行数: {stats['total_child_lines']}")
    
    # 检查目标达成情况
    questions_ok = stats['child_questions'] >= 8
    doubts_ok = stats['child_doubts'] >= 4
    choices_ok = stats['child_choices'] >= 2
    
    print(f"\n目标达成情况:")
    print(f"  提问次数 {'✓' if questions_ok else '✗'} ({stats['child_questions']}/8)")
    print(f"  质疑次数 {'✓' if doubts_ok else '✗'} ({stats['child_doubts']}/4)")
    print(f"  选择次数 {'✓' if choices_ok else '✗'} ({stats['child_choices']}/2)")
    
    return stats

if __name__ == '__main__':
    main()