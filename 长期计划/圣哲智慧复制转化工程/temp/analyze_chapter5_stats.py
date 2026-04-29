import re
import sys

def count_participation(text):
    # 识别儿童角色台词（小星、小宇）
    child_pattern = re.compile(r'^\*\*小星\*\*.*|^\*\*小宇\*\*.*|^小星.*|^小宇.*', re.MULTILINE)
    
    child_lines = []
    for match in child_pattern.finditer(text):
        line = match.group(0)
        child_lines.append(line)
    
    # 统计提问（包含问号）
    questions = [line for line in child_lines if '？' in line or '?' in line]
    
    # 统计质疑反驳（包含关键词）
    challenge_keywords = ['质疑', '反驳', '不对', '可是', '但是', '追问', '挑战']
    challenges = []
    for line in child_lines:
        for keyword in challenge_keywords:
            if keyword in line:
                challenges.append(line)
                break
    
    # 统计立场选择（包含关键词）
    position_keywords = ['我觉得', '我选择', '我倾向', '我认为', '我支持']
    positions = []
    for line in child_lines:
        for keyword in position_keywords:
            if keyword in line:
                positions.append(line)
                break
    
    return {
        'total_child_lines': len(child_lines),
        'questions': questions,
        'question_count': len(questions),
        'challenges': challenges,
        'challenge_count': len(challenges),
        'positions': positions,
        'position_count': len(positions)
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_chapter5_stats.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到思想剧场部分（从## 思想剧场开始到下一个---）
    thought_theater_pattern = re.compile(r'##\s*思想剧场.*?(?=\n---|\Z)', re.DOTALL)
    thought_theater_match = thought_theater_pattern.search(content)
    
    if thought_theater_match:
        thought_theater_text = thought_theater_match.group(0)
        print("=== 思想剧场部分内容 ===")
        print(thought_theater_text[:500])
        print("...")
        print("\n=== 统计结果 ===")
        stats = count_participation(thought_theater_text)
    else:
        print("未找到思想剧场部分，统计全文")
        stats = count_participation(content)
    
    print(f"儿童台词总数: {stats['total_child_lines']}")
    print(f"提问次数: {stats['question_count']}")
    print("提问内容:")
    for q in stats['questions']:
        print(f"  - {q[:50]}...")
    
    print(f"\n质疑反驳次数: {stats['challenge_count']}")
    print("质疑反驳内容:")
    for c in stats['challenges']:
        print(f"  - {c[:50]}...")
    
    print(f"\n立场选择次数: {stats['position_count']}")
    print("立场选择内容:")
    for p in stats['positions']:
        print(f"  - {p[:50]}...")
    
    # 检查是否达到标准
    print("\n=== 标准检查 ===")
    print(f"提问次数≥8: {'✅' if stats['question_count'] >= 8 else '❌'} ({stats['question_count']})")
    print(f"质疑反驳次数≥4: {'✅' if stats['challenge_count'] >= 4 else '❌'} ({stats['challenge_count']})")
    print(f"立场选择次数≥2: {'✅' if stats['position_count'] >= 2 else '❌'} ({stats['position_count']})")

if __name__ == '__main__':
    main()