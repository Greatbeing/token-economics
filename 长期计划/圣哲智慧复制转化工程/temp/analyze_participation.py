import re
import sys

def count_participation(text):
    # 统计儿童提问：包含“？”且由儿童角色（小星、小宇等）发出的台词
    child_lines = re.findall(r'(\*\*小星\*\*|\*\*小宇\*\*)[：:]?(.*?)\n', text)
    
    questions = 0
    challenges = 0
    choices = 0
    
    for role, line in child_lines:
        line = line.strip()
        # 提问：包含问号
        if '？' in line or '?' in line:
            questions += 1
        # 质疑反驳：包含“质疑”、“反驳”、“不对”、“可是”、“但是”等关键词
        if any(keyword in line for keyword in ['质疑', '反驳', '不对', '可是', '但是', '等等', '怎么证明', '瞎猜', '打断']):
            challenges += 1
    
    # 统计立场选择：在“想一想”部分中的选项选择
    # 查找“问题一”、“问题二”等部分中的选项
    think_sections = re.findall(r'### 问题[一二三四五六七八九十].*?(?=\n###|\n---|\n##)', text, re.DOTALL)
    for section in think_sections:
        # 计算选项数量（如“□”或“- [ ]”）
        choices += section.count('□') + section.count('[ ]')
    
    return questions, challenges, choices

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_participation.py <chapter_file>")
        return
    
    filename = sys.argv[1]
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    
    questions, challenges, choices = count_participation(text)
    
    print(f"儿童提问次数: {questions}")
    print(f"质疑反驳次数: {challenges}")
    print(f"立场选择次数: {choices}")
    
    # 检查是否达标
    if questions >= 8:
        print("✓ 儿童提问达标 (≥8)")
    else:
        print(f"✗ 儿童提问未达标 (需要{8-questions}次)")
    
    if challenges >= 4:
        print("✓ 质疑反驳达标 (≥4)")
    else:
        print(f"✗ 质疑反驳未达标 (需要{4-challenges}次)")
    
    if choices >= 2:
        print("✓ 立场选择达标 (≥2)")
    else:
        print(f"✗ 立场选择未达标 (需要{2-choices}次)")

if __name__ == '__main__':
    main()