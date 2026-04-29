import re

def insert_content(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # 在小宇立场选择后的王阳明回应行之后插入
        if line.strip() == '**王阳明**：很好！你已经在擦了。镜子亮了一度。':
            # 下一行应该是空行
            next_line = lines[i+1] if i+1 < len(lines) else ''
            # 再下一行是#### 擦镜第二步
            # 在空行后插入新内容
            new_lines.append(next_line)  # 空行
            # 插入小星的立场选择
            new_lines.append('**小星**：（立场选择）那我选怕黑。最坏情况是…窗帘后面真的有人？但我知道检查过就没有，所以能承受。\n')
            new_lines.append('**小星**补充：其实我上周做噩梦，梦见被影子追，醒来后心跳好快。这算良知信号吗？\n')
            new_lines.append('**王阳明**：当然！那是良知在提醒“注意安全边界”。你可以用三问清单解码噩梦信号。\n')
            new_lines.append('\n')
            i += 1  # 跳过已处理的空行
        i += 1
    
    # 写入新文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("内容已插入")

if __name__ == '__main__':
    insert_content('outputs/儿童哲学史/优化阶段/第六章优化稿.md')