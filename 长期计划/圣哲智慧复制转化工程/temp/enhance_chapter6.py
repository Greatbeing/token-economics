import re

def enhance_content(content):
    lines = content.split('\n')
    enhanced_lines = []
    
    # 状态变量
    in_first_camp = False
    in_second_camp = False
    in_third_camp = False
    
    # 计数器
    added_positions = 0
    added_life_points = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        enhanced_lines.append(line)
        
        # 检测营区
        if '## 第一营区：良知信号站（王阳明）' in line:
            in_first_camp = True
            in_second_camp = False
            in_third_camp = False
        elif '## 第二营区：不二法门屋（禅宗）' in line:
            in_first_camp = False
            in_second_camp = True
            in_third_camp = False
        elif '## 第三营区：木鸡修炼场（庄子）' in line:
            in_first_camp = False
            in_second_camp = False
            in_third_camp = True
        
        # 在第一营区增加立场选择（小星选择怕黑）
        if in_first_camp and '**小宇**：（立场选择）我选考试怕失误。最坏情况是考不及格…嗯，我能承受，因为可以补考。' in line:
            # 在小宇的立场选择后，增加小星的立场选择
            enhanced_lines.append('')
            enhanced_lines.append('**小星**：那我选怕黑。最坏情况是…窗帘后面真的有人？但我知道检查过就没有，所以能承受。')
            added_positions += 1
            # 同时增加生活共鸣点：分享噩梦经历
            enhanced_lines.append('')
            enhanced_lines.append('**小星**补充：其实我上周做噩梦，梦见被影子追，醒来后心跳好快。这算良知信号吗？')
            enhanced_lines.append('**王阳明**：当然！那是良知在提醒“注意安全边界”。你可以用三问清单解码噩梦信号。')
            added_life_points += 1
        
        # 在第二营区增加生活共鸣点（情绪云朵与学校经历）
        if in_second_camp and '**小宇**：哇，“它只是…”这样一想，好像没那么可怕了。' in line:
            # 在小宇感叹后，增加小星的生活共鸣点
            enhanced_lines.append('')
            enhanced_lines.append('**小星**：就像我上次数学考差了，本来觉得“我完了”，但用“它只是…”一想——它只是一次成绩，提醒我要多练习。')
            added_life_points += 1
        
        # 在第三营区增加立场选择（选择修炼方法）
        if in_third_camp and '**小星**：这能让我不怕吗？' in line:
            # 在庄子回答后插入（需要找到庄子回答的结束）
            # 这里我们稍后处理，先简单添加
            pass
        
        i += 1
    
    # 如果没有增加足够的立场选择，在第三营区添加
    if added_positions < 1:
        # 找到第三营区中庄子回答后的位置
        for j in range(len(enhanced_lines)):
            if '**庄子**：' in enhanced_lines[j] and '**小星**：这能让我不怕吗？' in enhanced_lines[j-2]:
                # 在庄子回答后插入空行和新的立场选择
                # 假设庄子回答后是空行
                k = j + 1
                while k < len(enhanced_lines) and enhanced_lines[k].strip() == '':
                    k += 1
                # 在k位置插入
                enhanced_lines.insert(k, '')
                enhanced_lines.insert(k+1, '**小宇**：那我选择先试试“身体扫描”。最近我紧张时手心出汗，想看看“怕”住在哪里。')
                enhanced_lines.insert(k+2, '**庄子**：好选择！记得扫描时像庖丁看牛一样，顺着身体纹理，不强迫放松。')
                added_positions += 1
                break
    
    print(f"增强完成: 增加立场选择{added_positions}个, 生活共鸣点{added_life_points}个")
    return '\n'.join(enhanced_lines)

def main():
    with open('outputs/儿童哲学史/优化阶段/第六章优化稿.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    enhanced = enhance_content(content)
    
    # 保存增强版
    with open('outputs/儿童哲学史/优化阶段/第六章优化稿_enhanced.md', 'w', encoding='utf-8') as f:
        f.write(enhanced)
    
    print("增强版已保存为第六章优化稿_enhanced.md")
    
    # 验证统计
    import temp.analyze_chapter6 as analyzer
    child_lines, q_count, c_count, p_count = analyzer.analyze_content(enhanced)
    print(f"增强后统计: 提问{q_count}, 质疑反驳{c_count}, 立场选择{p_count}")

if __name__ == '__main__':
    main()