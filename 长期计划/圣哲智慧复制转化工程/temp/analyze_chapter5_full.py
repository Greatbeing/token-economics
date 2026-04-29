import re
import sys

def count_participation_full(text):
    # 识别儿童角色台词（小星、小宇），包括加粗和非加粗格式
    # 模式匹配：**小星**... 或 小星... (可能前面有空格)
    child_pattern = re.compile(r'^\s*\*\*小星\*\*[^\n]*|^\s*\*\*小宇\*\*[^\n]*|^\s*小星[^\n]*|^\s*小宇[^\n]*', re.MULTILINE)
    
    child_lines = []
    for match in child_pattern.finditer(text):
        line = match.group(0).strip()
        child_lines.append(line)
    
    # 统计提问（包含问号）
    questions = [line for line in child_lines if '？' in line or '?' in line]
    
    # 统计质疑反驳（包含关键词）
    challenge_keywords = ['质疑', '反驳', '不对', '可是', '但是', '追问', '挑战', '插话', '质疑', '问']
    challenges = []
    for line in child_lines:
        # 检查是否包含关键词
        for keyword in challenge_keywords:
            if keyword in line:
                challenges.append(line)
                break
    
    # 统计立场选择（包含关键词）
    position_keywords = ['我觉得', '我选择', '我倾向', '我认为', '我支持', '我的倾向', '我同意']
    positions = []
    for line in child_lines:
        for keyword in position_keywords:
            if keyword in line:
                positions.append(line)
                break
    
    # 提取所有儿童台词用于手动检查
    print("=== 所有儿童台词 ===")
    for i, line in enumerate(child_lines, 1):
        print(f"{i:2d}. {line}")
    
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
        print("Usage: python analyze_chapter5_full.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=== 统计整个文件的儿童参与度 ===")
    stats = count_participation_full(content)
    
    print(f"\n=== 统计结果 ===")
    print(f"儿童台词总数: {stats['total_child_lines']}")
    print(f"提问次数: {stats['question_count']}")
    print("提问内容:")
    for q in stats['questions']:
        print(f"  - {q[:80]}...")
    
    print(f"\n质疑反驳次数: {stats['challenge_count']}")
    print("质疑反驳内容:")
    for c in stats['challenges']:
        print(f"  - {c[:80]}...")
    
    print(f"\n立场选择次数: {stats['position_count']}")
    print("立场选择内容:")
    for p in stats['positions']:
        print(f"  - {p[:80]}...")
    
    # 检查是否达到标准
    print("\n=== 标准检查 ===")
    print(f"提问次数≥8: {'✅' if stats['question_count'] >= 8 else '❌'} ({stats['question_count']})")
    print(f"质疑反驳次数≥4: {'✅' if stats['challenge_count'] >= 4 else '❌'} ({stats['challenge_count']})")
    print(f"立场选择次数≥2: {'✅' if stats['position_count'] >= 2 else '❌'} ({stats['position_count']})")

if __name__ == '__main__':
    main()