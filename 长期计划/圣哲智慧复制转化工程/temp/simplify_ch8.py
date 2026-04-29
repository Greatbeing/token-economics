#!/usr/bin/env python3
import re

def count_chinese_chars(text):
    """统计中文字符数"""
    return len(re.findall(r'[\u4e00-\u9fff]', text))

def simplify_content(content):
    """对第八章内容进行精简"""
    original_chinese = count_chinese_chars(content)
    print(f"原始中文字符数: {original_chinese}")
    
    # 1. 精简禅宗故事时间：慧能的传奇
    # 找到从 "## 禅宗故事时间：慧能的传奇" 到下一个 "##" 标题之间的内容
    pattern = r'(## 禅宗故事时间：慧能的传奇\n\n)(.*?)(\n\n## )'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        story_section = match.group(2)
        # 简化每个章节的描述
        # 第一章：砍柴少年
        story_section = re.sub(r'慧能小时候家里很穷，父亲早逝，他每天上山砍柴卖钱养家。', 
                               '慧能小时候家里穷，每天砍柴卖钱养家。', story_section)
        # 第二章：千里求法
        story_section = re.sub(r'24岁那年，慧能决定去湖北黄梅东山寺，拜五祖弘忍为师。走了整整一个月，终于到达。', 
                               '24岁那年，慧能去湖北黄梅东山寺，拜五祖弘忍为师。走了一个月才到达。', story_section)
        story_section = re.sub(r'弘忍看他是个不识字的樵夫，便说：“你这蛮子也想成佛？”', 
                               '弘忍看他是个不识字的樵夫，说：“你这蛮子也想成佛？”', story_section)
        # 第三章：舂米行者
        story_section = re.sub(r'弘忍让慧能在厨房舂米（用脚踩石杵捣米），一干就是八个月。', 
                               '弘忍让慧能在厨房舂米，一干就是八个月。', story_section)
        story_section = re.sub(r'慧能个子小，体重不够，就在腰上绑块大石头增加重量。', 
                               '慧能个子小，就在腰上绑块石头增加重量。', story_section)
        # 第四章：偈子比赛
        story_section = re.sub(r'弘忍要选接班人，让大家写偈子（佛教诗歌）。', 
                               '弘忍要选接班人，让大家写偈子（佛教诗歌）。', story_section)  # 保留
        # 第五章：夜传衣钵
        story_section = re.sub(r'半夜，弘忍叫慧能到房间，给他讲解《金刚经》，并把袈裟衣钵传给他，说：“你现在是第六祖，快走，有人会害你。”', 
                               '半夜，弘忍叫慧能到房间，传他衣钵，说：“你现在是第六祖，快走，有人会害你。”', story_section)
        # 第六章：开坛说法
        story_section = re.sub(r'后来慧能在广东曹溪开坛说法，创立“顿悟”禅法，强调“不立文字，教外别传，直指人心，见性成佛”。', 
                               '后来慧能在广东曹溪开坛说法，创立“顿悟”禅法。', story_section)
        story_section = re.sub(r'他的语录被弟子编成《六祖坛经》，是中国佛教唯一被称为“经”的著作。', 
                               '他的语录被编成《六祖坛经》。', story_section)
        
        # 替换回原内容
        new_story_section = match.group(1) + story_section + match.group(3)
        content = content[:match.start()] + new_story_section + content[match.end():]
    
    # 2. 精简全球望远镜部分：简化差异说明和思考题的文字
    # 找到全球望远镜部分（可能有两个表格）
    # 由于表格结构固定，我们可以简化每个单元格的文字
    # 但为了简单，我们删除一些冗余的描述性文字
    # 例如：“核心比喻”可以缩短
    # 由于表格是markdown格式，我们使用正则匹配每个表格的行
    # 但考虑到复杂性，我们暂时跳过
    
    # 3. 精简实践环节：三周计划表格中的描述文字
    # 找到“## 实践环节：三周“心灵扫除实验”计划”到下一个“##”标题
    pattern_practice = r'(## 实践环节：三周“心灵扫除实验”计划\n\n)(.*?)(\n\n## )'
    match_practice = re.search(pattern_practice, content, re.DOTALL)
    if match_practice:
        practice_section = match_practice.group(2)
        # 简化表格中的“记录要点”列的文字
        # 例如：“记录情绪类型（晴、阴、雨、雷）” -> “记录情绪类型”
        practice_section = re.sub(r'记录情绪类型（晴、阴、雨、雷）', '记录情绪类型', practice_section)
        practice_section = re.sub(r'写下原标签和改写后句子', '记录标签改写', practice_section)
        practice_section = re.sub(r'记录分心次数（正常！）', '记录分心次数', practice_section)
        practice_section = re.sub(r'识别主要烦恼类型', '识别烦恼类型', practice_section)
        practice_section = re.sub(r'积累成功体验', '积累成功体验', practice_section)  # 不变
        practice_section = re.sub(r'连接自然，静心', '连接自然', practice_section)
        # 第二周
        practice_section = re.sub(r'熟悉念头“家族”', '熟悉念头类型', practice_section)
        practice_section = re.sub(r'体验“第三人视角”', '体验第三人视角', practice_section)
        practice_section = re.sub(r'聚焦行动，减少焦虑', '聚焦行动', practice_section)
        practice_section = re.sub(r'体验“我不是我的念头”', '体验自我与念头分离', practice_section)
        practice_section = re.sub(r'创意表达，转化情绪', '创意表达情绪', practice_section)
        # 第三周
        practice_section = re.sub(r'建立觉察习惯', '建立觉察习惯', practice_section)
        practice_section = re.sub(r'主动应对策略', '主动应对策略', practice_section)
        practice_section = re.sub(r'培养积极视角', '培养积极视角', practice_section)
        practice_section = re.sub(r'深化理解', '深化理解', practice_section)
        practice_section = re.sub(r'看见成长轨迹', '看见成长', practice_section)
        practice_section = re.sub(r'肯定努力，持续练习', '肯定努力', practice_section)
        
        # 替换回原内容
        new_practice_section = match_practice.group(1) + practice_section + match_practice.group(3)
        content = content[:match_practice.start()] + new_practice_section + content[match_practice.end():]
    
    # 4. 精简家长指南部分：简化一些解释性文字
    # 找到“## 给家长的话：如何支持孩子的心灵扫除探险”到下一个“##”标题
    pattern_parent = r'(## 给家长的话：如何支持孩子的心灵扫除探险\n\n)(.*?)(\n\n## )'
    match_parent = re.search(pattern_parent, content, re.DOTALL)
    if match_parent:
        parent_section = match_parent.group(2)
        # 简化常见问题解答的文字
        # 例如：“Q：孩子说“这些练习没用，我还是烦”？”可以缩短回答
        # 但为了保持完整性，我们只删除一些冗余短语
        parent_section = re.sub(r'可以当着孩子面说：', '可以说：', parent_section)
        parent_section = re.sub(r'当孩子自己遇到压力（如工作 deadline）', '当自己遇到压力时', parent_section)
        parent_section = re.sub(r'（而不是“你怎么解决它？”）', '', parent_section)
        parent_section = re.sub(r'用“烦恼转化日志”共同记录，可视化进步。', '用日志共同记录进步。', parent_section)
        
        # 替换回原内容
        new_parent_section = match_parent.group(1) + parent_section + match_parent.group(3)
        content = content[:match_parent.start()] + new_parent_section + content[match_parent.end():]
    
    # 5. 精简禅宗小知识部分：缩短每个小知识的描述
    pattern_knowledge = r'(## 禅宗小知识：影响中国文化的一千三百年\n\n)(.*?)(\n\n---)'
    match_knowledge = re.search(pattern_knowledge, content, re.DOTALL)
    if match_knowledge:
        knowledge_section = match_knowledge.group(2)
        # 简化每个小知识的解读文字
        knowledge_section = re.sub(r'就像你烦恼时，好朋友不说大道理，而是递给你一杯热可可——有时候陪伴比答案更重要。', 
                                   '就像烦恼时，好朋友递给你一杯热可可——陪伴比答案更重要。', knowledge_section)
        knowledge_section = re.sub(r'画一张“烦恼枯山水”——用简单线条画烦恼，旁边留白。看到烦恼只是整体中的一小部分。', 
                                   '画“烦恼枯山水”——看到烦恼只是整体的一小部分。', knowledge_section)
        knowledge_section = re.sub(r'和家人一起练五分钟“慢动作武术”（如太极拳），感受身体动、心静的状态。', 
                                   '和家人练五分钟“慢动作武术”，感受身体动、心静的状态。', knowledge_section)
        knowledge_section = re.sub(r'每天晚饭前，全家静坐一分钟，只听呼吸声。', 
                                   '每天晚饭前，全家静坐一分钟听呼吸。', knowledge_section)
        
        # 替换回原内容
        new_knowledge_section = match_knowledge.group(1) + knowledge_section + match_knowledge.group(3)
        content = content[:match_knowledge.start()] + new_knowledge_section + content[match_knowledge.end():]
    
    new_chinese = count_chinese_chars(content)
    print(f"精简后中文字符数: {new_chinese}")
    print(f"精简字数: {original_chinese - new_chinese}")
    
    return content

if __name__ == '__main__':
    with open('outputs/儿童哲学史/优化阶段/第八章优化稿.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = simplify_content(content)
    
    with open('outputs/儿童哲学史/优化阶段/第八章优化稿.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("文件已更新。")