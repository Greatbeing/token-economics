import re

def extract_narration(script_path):
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有解说词块：以“解说词：”开头，然后是引用块
    pattern = r'解说词：\s*\n>\s*"([^"]+)"'
    matches = re.findall(pattern, content)
    
    # 如果没有找到，尝试另一种模式
    if not matches:
        pattern = r'解说词：\s*\n>\s*([^"]+)'
        matches = re.findall(pattern, content)
    
    # 如果还没有，尝试更通用的模式
    if not matches:
        # 查找所有>开头的行
        lines = content.split('\n')
        in_narration = False
        narration_lines = []
        for line in lines:
            if '解说词：' in line:
                in_narration = True
                continue
            if in_narration and line.strip().startswith('>'):
                narration_lines.append(line.strip()[1:].strip())
            elif in_narration and line.strip() == '':
                in_narration = False
    
        if narration_lines:
            # 合并连续的行
            combined = []
            current = ''
            for line in narration_lines:
                if line.endswith('。') or line.endswith('？') or line.endswith('！'):
                    current += line
                    combined.append(current)
                    current = ''
                else:
                    current += line + ' '
            if current:
                combined.append(current)
            matches = combined
    
    return matches

if __name__ == '__main__':
    script_path = 'temp/视频脚本/庄子视频脚本_竖屏.md'
    narrations = extract_narration(script_path)
    
    print(f"找到 {len(narrations)} 段解说词")
    for i, narration in enumerate(narrations, 1):
        print(f"\n场景{i}:")
        print(narration)
    
    # 保存为纯文本文件
    output_path = 'temp/视频素材/庄子/音频_竖屏/解说文本.txt'
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for narration in narrations:
            f.write(narration + '\n\n')
    
    print(f"\n解说词已保存到: {output_path}")