#!/usr/bin/env python3
import re

def enhance_chapter8(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # 在慧能说完“天空会被云遮住”后插入新的儿童质疑
        if "天空会被云遮住，但天空本身没变。你的觉察力就是天空，烦恼只是暂时的天气。" in line:
            # 下一行是空行，再下一行是小敏的立场选择
            # 在空行后插入
            new_lines.append(lines[i+1])  # 空行
            # 插入新的儿童质疑
            new_lines.append("**小刚**：（疑惑）可是大师，如果天空一直不变，那为什么我们还会感觉到阴天呢？烦恼来了就是难受啊！\n")
            new_lines.append("**慧能**：问得好！阴天是感受，天空是觉察。你可以同时拥有“难受的感受”和“知道自己正在难受的觉察”。就像你可以一边牙疼，一边知道“哦，我在牙疼”。\n")
            new_lines.append("\n")
            i += 2  # 跳过空行和下一行（小敏的立场选择）
            continue
        
        # 在思想剧场延伸部分增加生活共鸣点
        # 在“小敏：我懂了！心里有灰尘（烦恼）要经常打扫。”之后插入
        if "**小敏**：我懂了！心里有灰尘（烦恼）要经常打扫。" in line:
            # 下一行是“慧能：（轻松舂米）...”，我们在这之前插入
            new_lines.append("**小雨**：（点头）我也有这种感觉！每次我练钢琴练不好时，心里就像蒙了一层灰，越着急越弹不好。\n")
            new_lines.append("**慧能**：正是！灰尘来了，你知道它是灰尘，就不会把它当成整个房间。\n")
            new_lines.append("\n")
        
        i += 1
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"已更新文件：{file_path}")

if __name__ == '__main__':
    enhance_chapter8('outputs/儿童哲学史/优化阶段/第八章优化稿.md')