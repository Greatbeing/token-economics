#!/usr/bin/env python3
import re

def count_chinese_chars(text):
    """统计中文字符数"""
    return len(re.findall(r'[\u4e00-\u9fff]', text))

def simplify_content(content):
    """对第八章内容进行进一步精简"""
    original_chinese = count_chinese_chars(content)
    print(f"原始中文字符数: {original_chinese}")
    
    # 1. 进一步精简禅宗故事时间：合并章节，缩短描述
    pattern = r'(## 禅宗故事时间：慧能的传奇\n\n)(.*?)(\n\n## )'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        # 替换为更简洁的版本
        new_story = """## 禅宗故事时间：慧能的传奇

慧能（638年—713年），禅宗第六祖，他的故事像一部冒险电影。

**早年生活**：慧能小时候家里穷，每天砍柴卖钱养家。有一天在集市听到《金刚经》“应无所住而生其心”，心里一亮。

**求法经历**：24岁时去湖北黄梅拜五祖弘忍为师。弘忍看他是个不识字的樵夫，问他来求什么，慧能答：“只求成佛。”弘忍问：“你这蛮子也想成佛？”慧能反问：“人有南北，佛性也有南北吗？”弘忍知道此人根器不凡。

**寺院修行**：弘忍让慧能在厨房舂米八个月，他每天边舂米边思考“佛性是什么”，明白佛性就在每个人心里。

**继承衣钵**：弘忍要选接班人，让大家写偈子。神秀写：“身是菩提树，心如明镜台，时时勤拂拭，勿使惹尘埃。”慧能不识字，请人代写：“菩提本无树，明镜亦非台，本来无一物，何处惹尘埃。”弘忍知道慧能已悟到“空”的境界，半夜传他衣钵，让他南逃隐居十五年。

**开坛说法**：后来慧能在广东曹溪开坛说法，创立“顿悟”禅法，强调“不立文字，直指人心”。他的语录被编成《六祖坛经》。

**给探险家的问题**：
> 1. 慧能从砍柴少年到禅宗祖师，你觉得他最重要的品质是什么？
> 2. 如果让你用一句话向朋友介绍慧能，你会怎么说？

---
"""
        # 计算原故事结束位置
        end_pos = match.end()
        # 找到下一个标题的开始位置
        next_title_match = re.search(r'\n## ', content[end_pos:])
        if next_title_match:
            next_title_start = end_pos + next_title_match.start()
            # 替换从 match.start() 到 next_title_start 的内容
            content = content[:match.start()] + new_story + content[next_title_start:]
        else:
            # 如果没有下一个标题，替换到末尾
            content = content[:match.start()] + new_story
    
    # 2. 精简禅宗小知识部分：减少一个小知识，缩短描述
    pattern_knowledge = r'(## 禅宗小知识：影响中国文化的一千三百年\n\n)(.*?)(\n\n---)'
    match_knowledge = re.search(pattern_knowledge, content, re.DOTALL)
    if match_knowledge:
        # 替换为更简洁的版本，保留四个小知识
        new_knowledge = """## 禅宗小知识：影响中国文化的一千三百年

禅宗深深影响了中国的文学、艺术、茶道和日常生活。

### 1. 禅诗：王维的“空山不见人”
唐代诗人王维的诗充满禅意：
> 空山不见人，但闻人语响。  
> 返景入深林，复照青苔上。

**解读**：山“空”不是没人，而是不执着于“有人/无人”。就像烦恼来时，你知道它只是声音。

### 2. 茶道：赵州和尚的“吃茶去”
赵州禅师每次有人来访，不管问什么，都说：“吃茶去。”弟子问为什么，禅师答：“你也吃茶去。”

**儿童理解**：就像烦恼时，好朋友递给你一杯热可可——陪伴比答案更重要。

### 3. 园林：枯山水
日本禅宗园林“枯山水”用砂石表现水流。没有真水，却让你“看见”水。

**关联练习**：画“烦恼枯山水”——看到烦恼只是整体中的一小部分。

### 4. 现代应用：正念练习
现在流行的“正念”源头之一就是禅宗。练习专注呼吸、观察念头。

**家庭尝试**：每天晚饭前，全家静坐一分钟听呼吸。

---
"""
        content = re.sub(pattern_knowledge, new_knowledge, content, flags=re.DOTALL)
    
    # 3. 精简儿童创作角：减少一个示例
    # 查找作品展示区
    if "### 作品展示区" in content:
        # 简单方法：替换小刚的偈子为空
        content = content.replace("**小刚的偈子**（队友矛盾）\n> 队长偏心不给球，\n> 我心里头真难受。\n> 换个角度想一想，\n> 我练技术更自由。\n\n", "")
    
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