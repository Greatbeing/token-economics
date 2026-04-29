import re

def analyze_content(content):
    lines = content.split('\n')
    
    child_lines = []
    question_count = 0
    challenge_count = 0
    position_count = 0
    life_point_count = 0
    
    # 正则匹配儿童台词
    child_pattern = re.compile(r'^\*\*(小星|小宇)\*\*.*')
    # 识别提问（包含问号）
    question_pattern = re.compile(r'.*\？.*|.*\?.*')
    # 识别质疑反驳（包含关键词）
    challenge_keywords = ['质疑', '反驳', '可是', '但是', '不对', '如果.*呢', '难道', '怎么.*呢', '为什么']
    challenge_pattern = re.compile('|'.join(challenge_keywords))
    # 识别立场选择
    position_keywords = ['选', '选择', '我选', '我觉得', '我认为', '我支持']
    position_pattern = re.compile('|'.join(position_keywords))
    
    for i, line in enumerate(lines):
        if child_pattern.match(line):
            child_lines.append((i+1, line))
            # 检查是否为提问
            if question_pattern.search(line):
                question_count += 1
                print(f"提问: {line}")
            # 检查是否为质疑反驳
            if challenge_pattern.search(line):
                challenge_count += 1
                print(f"质疑反驳: {line}")
            # 检查是否为立场选择
            if position_pattern.search(line):
                position_count += 1
                print(f"立场选择: {line}")
    
    print(f"\n统计结果:")
    print(f"儿童台词总数: {len(child_lines)}")
    print(f"提问次数: {question_count}")
    print(f"质疑反驳次数: {challenge_count}")
    print(f"立场选择次数: {position_count}")
    
    return child_lines, question_count, challenge_count, position_count

def main():
    with open('outputs/儿童哲学史/优化阶段/第六章优化稿.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    child_lines, q_count, c_count, p_count = analyze_content(content)
    
    print(f"\n目标: 提问≥8, 质疑反驳≥4, 立场选择≥2")
    print(f"需要增加: 提问{max(0, 8-q_count)}, 质疑反驳{max(0, 4-c_count)}, 立场选择{max(0, 2-p_count)}")

if __name__ == '__main__':
    main()