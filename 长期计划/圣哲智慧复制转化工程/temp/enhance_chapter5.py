import re

def enhance_content(content):
    lines = content.split('\n')
    enhanced_lines = []
    
    # 状态变量
    in_mozi_section = False
    in_mengzi_section = False
    in_hanfeizi_section = False
    
    # 计数器
    added_questions = 0
    added_challenges = 0
    added_positions = 0
    added_life_points = 0
    
    for i, line in enumerate(lines):
        enhanced_lines.append(line)
        
        # 检测进入各节
        if '## 第一站：墨子的"兼爱"' in line or '## 第一站：墨子的"兼爱"' in line:
            in_mozi_section = True
            in_mengzi_section = False
            in_hanfeizi_section = False
        elif '## 第二站：孟子的"仁政"' in line:
            in_mozi_section = False
            in_mengzi_section = True
            in_hanfeizi_section = False
        elif '## 第三站：法家的"法治"' in line:
            in_mozi_section = False
            in_mengzi_section = False
            in_hanfeizi_section = True
        
        # 在思想剧场部分增加儿童提问
        if '## 思想剧场：班级宪法制定大会' in line:
            # 在班主任讲话后增加儿童提问
            pass
        
        # 在墨子部分的小星辩论回合后增加追问
        if in_mozi_section and '**小星**：那资源分配呢？我只有一个苹果，给亲妹妹还是给陌生同学？' in line:
            # 增加一个生活共鸣点：学校午餐分配
            enhanced_lines.append('')
            enhanced_lines.append('**小宇**：就像我们学校午餐的水果分配！有时候苹果不够，老师会把一个苹果切成两半给两个同学，这也是一种公平吗？')
            added_questions += 1
            added_life_points += 1
            
            # 增加小星的追问
            enhanced_lines.append('')
            enhanced_lines.append('**小星**追问：如果切苹果的方法大家都同意，那就算公平。但要是有人不喜欢吃苹果，想换香蕉呢？规则能考虑到每个人的不同喜好吗？')
            added_questions += 1
            added_challenges += 1
        
        # 在孟子部分增加立场选择
        if in_mengzi_section and '**小星**质疑：这不还是惩罚吗？和韩非子的"法治"有什么区别？' in line:
            # 在孟子回答后增加小宇的立场选择
            # 找到孟子回答的结束位置（下一个空行或下一段）
            pass
        
        # 在韩非子部分增加生活共鸣点
        if in_hanfeizi_section and '**小宇**追问：那规则太多怎么办？我们会不会被各种"不许"束缚？' in line:
            # 增加生活共鸣点：班级手机管理
            enhanced_lines.append('')
            enhanced_lines.append('**小星**：就像我们班的手机管理！一开始只有"上课不许玩手机"，结果有人偷偷看时间被批评，后来改成"上课手机放书包，紧急情况举手"，大家反而更愿意遵守了。')
            added_life_points += 1
    
    return '\n'.join(enhanced_lines)

def main():
    with open('outputs/儿童哲学史/优化阶段/第五章优化稿.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    enhanced = enhance_content(content)
    
    with open('outputs/儿童哲学史/优化阶段/第五章优化稿_enhanced.md', 'w', encoding='utf-8') as f:
        f.write(enhanced)
    
    print("增强版已保存为第五章优化稿_enhanced.md")

if __name__ == '__main__':
    main()