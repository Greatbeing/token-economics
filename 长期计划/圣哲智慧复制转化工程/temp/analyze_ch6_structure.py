#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析第六章章节结构，统计各部分字数"""

import re

def analyze_structure(content):
    """分析章节结构"""
    
    # 定义章节标题模式
    section_patterns = [
        (r'^# .*', '章标题'),
        (r'^## .*', '节标题'),
        (r'^### .*', '小节标题'),
        (r'^#### .*', '小小节标题'),
    ]
    
    lines = content.split('\n')
    sections = []
    current_section = {'title': '开头', 'content': '', 'level': 0}
    
    for line in lines:
        # 检查是否为标题
        is_title = False
        for pattern, level_name in section_patterns:
            if re.match(pattern, line):
                is_title = True
                # 保存当前section
                if current_section['content']:
                    sections.append(current_section.copy())
                
                # 开始新section
                current_section = {
                    'title': line.strip(),
                    'content': line + '\n',
                    'level': pattern.count('#')
                }
                break
        
        if not is_title:
            current_section['content'] += line + '\n'
    
    # 添加最后一个section
    if current_section['content']:
        sections.append(current_section.copy())
    
    return sections

def count_chinese_chars(text):
    """统计中文字符数"""
    pattern = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
    chinese_chars = pattern.findall(text)
    return len(chinese_chars)

def main():
    file_path = "outputs/儿童哲学史/优化阶段/第六章优化稿.md"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sections = analyze_structure(content)
        
        print("=== 第六章章节结构分析 ===\n")
        print(f"总段落数: {len(sections)}")
        
        total_chinese = count_chinese_chars(content)
        print(f"总中文字数: {total_chinese}")
        print()
        
        # 显示主要部分
        major_sections = []
        for i, section in enumerate(sections):
            chinese_count = count_chinese_chars(section['content'])
            if section['level'] <= 2:  # 只显示章和节标题
                major_sections.append((section['title'], chinese_count, section['level']))
        
        print("=== 主要章节结构 ===")
        for title, count, level in major_sections:
            indent = "  " * (level - 1) if level > 0 else ""
            print(f"{indent}{title} - {count}字")
        
        # 统计各部分字数
        print("\n=== 详细字数统计 ===")
        
        # 手动定义我们关心的大节
        major_parts = [
            ("思想剧场", r'^## 思想剧场'),
            ("第一营区：良知信号站", r'^## 第一营区'),
            ("第二营区：不二法门屋", r'^## 第二营区'),
            ("第三营区：木鸡修炼场", r'^## 第三营区'),
            ("全球望远镜", r'^## 全球望远镜'),
            ("实践练习", r'^## 实践练习'),
            ("智慧探险地图碎片", r'^## 智慧探险地图碎片'),
            ("本章哲学生词卡", r'^## 本章哲学生词卡'),
            ("给家长的提示", r'^## 给家长的提示'),
            ("与西方智慧对话", r'^## 与西方智慧对话'),
            ("知识迷宫闯关", r'^## 知识迷宫闯关'),
            ("哲学漫画脚本", r'^## 哲学漫画脚本'),
            ("本章小结", r'^## 本章小结'),
            ("下一章预告", r'^## 下一章预告'),
            ("附录", r'^## 附录'),
            ("心灵探险家日记片段", r'^## 心灵探险家日记片段'),
        ]
        
        part_stats = []
        for part_name, pattern in major_parts:
            # 找到该部分开始位置
            match = re.search(pattern, content, re.MULTILINE)
            if match:
                start = match.start()
                # 找到下一个部分开始位置
                next_match = None
                for next_part_name, next_pattern in major_parts:
                    if next_pattern == pattern:
                        continue
                    next_match = re.search(next_pattern, content[start+1:], re.MULTILINE)
                    if next_match:
                        next_start = start + 1 + next_match.start()
                        break
                
                if next_match:
                    part_content = content[start:next_start]
                else:
                    part_content = content[start:]
                
                chinese_count = count_chinese_chars(part_content)
                part_stats.append((part_name, chinese_count))
        
        # 排序并显示
        part_stats.sort(key=lambda x: x[1], reverse=True)
        
        for part_name, count in part_stats:
            percentage = (count / total_chinese) * 100
            print(f"{part_name:20s} {count:5d}字 ({percentage:.1f}%)")
        
        # 计算前几大板块
        print(f"\n总字数: {total_chinese}字")
        print(f"目标字数: ≤7000字")
        print(f"需要精简: {total_chinese - 7000}字")
        
        # 建议精简部分
        print("\n=== 精简建议 ===")
        print("1. '知识迷宫闯关'和'哲学漫画脚本'内容较长，可考虑精简或合并")
        print("2. '给家长的提示'可以稍微压缩")
        print("3. '与西方智慧对话'与'全球望远镜'可能有重复，可精简")
        print("4. '实践练习'部分确保简洁但保持可操作性")
        print("5. '附录'可以简化，保留核心工具")
        
    except Exception as e:
        print(f"出错: {e}")

if __name__ == "__main__":
    main()