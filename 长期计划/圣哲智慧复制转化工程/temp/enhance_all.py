#!/usr/bin/env python3
import os
import re
import sys

base_dir = "outputs/儿童哲学史/优化阶段"
backup_dir = os.path.join(base_dir, "backup_practice")
os.makedirs(backup_dir, exist_ok=True)

def enhance_practice_section(original, chapter_num):
    """增强实践练习部分"""
    # 检测是否已经包含独立版和合作版
    if "独立完成版" in original and "亲子合作版" in original:
        print(f"第{chapter_num}章已包含两种版本，跳过增强")
        return original
    
    # 提取现有各部分
    task_obj = re.search(r'### 任务目标\n(.*?)(?=\n###|\n---|\Z)', original, re.DOTALL)
    material = re.search(r'### 材料准备\n(.*?)(?=\n###|\n---|\Z)', original, re.DOTALL)
    steps = re.search(r'### 具体步骤\n(.*?)(?=\n###|\n---|\Z)', original, re.DOTALL)
    table = re.search(r'### 记录表格\n(.*?)(?=\n###|\n---|\Z)', original, re.DOTALL)
    sample = re.search(r'### 预期产出样例\n(.*?)(?=\n###|\n---|\Z)', original, re.DOTALL)
    parent_tip = re.search(r'### 给家长的提示.*?\n(.*?)(?=\n###|\n---|\Z)', original, re.DOTALL)
    
    # 构建增强版内容
    enhanced = f"## 实践练习：{chapter_num}章主题实践（可操作增强版）\n\n"
    
    # 任务目标和材料准备保持不变
    if task_obj:
        enhanced += f"### 任务目标\n{task_obj.group(1).strip()}\n\n"
    if material:
        enhanced += f"### 材料准备\n{material.group(1).strip()}\n\n"
    
    # 版本选择说明
    enhanced += "### 版本选择说明\n\n"
    enhanced += "本练习提供两种版本，适合不同年龄和家庭情况的孩子：\n\n"
    enhanced += "- **独立完成版**（适合11-12岁）：强调自主探索，培养独立思考能力。\n"
    enhanced += "- **亲子合作版**（适合8-10岁）：家长参与引导，在互动中理解哲学概念。\n\n"
    enhanced += "你可以根据实际情况选择一种版本完成，也可以先尝试独立版，再与家人合作完成合作版。\n\n"
    
    # 独立完成版
    enhanced += "### 独立完成版（适合11-12岁）\n\n"
    if table:
        enhanced += f"#### 记录表格\n{table.group(1).strip()}\n\n"
    if steps:
        enhanced += f"#### 具体步骤\n{steps.group(1).strip()}\n\n"
    
    # 亲子合作版
    enhanced += "### 亲子合作版（适合8-10岁）\n\n"
    if parent_tip:
        enhanced += f"#### 家长引导指南\n{parent_tip.group(1).strip()}\n\n"
    else:
        # 默认家长指南
        enhanced += "#### 家长引导指南\n\n"
        enhanced += "1. **共同选择观察对象**：和孩子一起讨论并选择本周观察对象（如植物、宠物、天气）。\n"
        enhanced += "2. **每日5分钟陪伴观察**：每天固定时间陪孩子观察，鼓励孩子描述看到的变化。\n"
        enhanced += "3. **周末分享会**：周六或周日举行家庭分享会，每人分享本周的观察发现和感受。\n"
        enhanced += "4. **延伸讨论**：根据孩子的观察，讨论“自然”“规律”“时机”等概念在生活中的体现。\n\n"
    
    # 完整完成样例（关键章节提供详细样例）
    enhanced += "### 完整完成样例\n\n"
    if chapter_num == 1:
        enhanced += "#### 独立完成版样例（学生小明，11岁）\n\n"
        enhanced += "**观察记录表（填写示例）**\n\n"
        enhanced += "| 观察日期 | 观察对象 | 它是如何“自己发生”的？ | 这让我联想到“道”的哪个特点？ | 我的感受 |\n"
        enhanced += "|----------|----------|------------------------|-------------------------------|----------|\n"
        enhanced += "| 6月10日 | 小区池塘荷花 | 荷叶刚从水面露出，卷着的 | 无（尚未显现） | 好奇：它会怎么打开？ |\n"
        enhanced += "| 6月12日 | 同一朵荷花 | 下雨后荷叶完全展开，有露珠 | 自然（不刻意） | 惊讶：雨水就是它的闹钟！ |\n"
        enhanced += "| 6月14日 | 同一朵荷花 | 荷花苞出现，粉红色尖尖 | 反者道之动（从合到开） | 期待：快要开了！ |\n"
        enhanced += "| 6月16日 | 同一朵荷花 | 荷花半开，蜜蜂绕飞 | 自然与生命互动 | 喜悦：生命在互相帮助！ |\n\n"
        enhanced += "**三周实践总结**\n\n"
        enhanced += "- **第一周**：观察荷花自然开放的过程，理解了“道”的自然性。\n"
        enhanced += "- **第二周**：观察蚂蚁搬运食物，发现群体协作的“无名”规律。\n"
        enhanced += "- **第三周**：观察自己帮助同学的自然反应，体会到“道”在人际关系中的体现。\n\n"
        enhanced += "**我的收获**：\n"
        enhanced += "“道”不是神秘的东西，而是生活中无处不在的规律。当我学会观察和顺应这些规律时，做事更顺畅，心情也更轻松。就像荷花知道在雨后开放，我也在学着找到自己的“自然节奏”。\n\n"
        enhanced += "#### 亲子合作版样例（家庭实践）\n\n"
        enhanced += "**家庭观察周记录**\n\n"
        enhanced += "- **孩子（8岁）观察**：多肉植物在阳光下叶子变红，阴天变绿。\n"
        enhanced += "- **爸爸观察**：每天傍晚小区鸟叫声最密集，像在开“鸟民大会”。\n"
        enhanced += "- **妈妈观察**：周末邻居家孩子笑声最多，工作日安静。\n\n"
        enhanced += "**家庭讨论要点**：\n"
        enhanced += "1. 这些现象有没有人为安排？（没有，都是自然发生）\n"
        enhanced += "2. 如果我们干预会怎样？（比如给多肉天天浇水→可能烂根）\n"
        enhanced += "3. 我们家的生活中有哪些“自然规律”？（如晚饭后全家放松时间）\n\n"
    else:
        enhanced += "#### 样例说明\n\n"
        enhanced += "请参考第一章的完整完成样例，按照相似格式填写你的实践记录。\n\n"
        enhanced += "**基本要求**：\n"
        enhanced += "1. 每周至少完成3次观察记录\n"
        enhanced += "2. 周末写一段总结反思（至少100字）\n"
        enhanced += "3. 尝试将哲学概念与生活经验联系起来\n\n"
    
    enhanced += "---\n"
    return enhanced

def process_chapter(chapter_num):
    """处理单个章节"""
    filename_map = {
        1: "第一章优化稿.md",
        2: "第二章优化稿.md",
        3: "第三章优化稿.md",
        4: "第四章优化稿.md",
        5: "第五章优化稿.md",
        6: "第六章优化稿.md",
        7: "第七章优化稿.md",
        8: "第八章优化稿.md",
        9: "第九章优化稿.md",
        10: "第十章优化稿.md",
        11: "第十一章优化稿.md",
        12: "第十二章优化稿.md"
    }
    
    filename = filename_map.get(chapter_num)
    if not filename:
        print(f"无效章节编号: {chapter_num}")
        return
    
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        print(f"文件不存在: {filepath}")
        return
    
    # 读取原文件
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 备份
    backup_path = os.path.join(backup_dir, filename)
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 查找实践练习部分
    # 使用正则匹配从## 实践练习开始到下一个##或---之前的内容
    pattern = r'(\n## 实践练习[:：].*?)(?=\n## |\n---\n|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not match:
        # 尝试查找"实践环节"
        pattern = r'(\n## 实践环节[:：].*?)(?=\n## |\n---\n|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not match:
        print(f"第{chapter_num}章未找到实践练习部分，跳过")
        return
    
    old_section = match.group(1)
    print(f"第{chapter_num}章找到实践练习部分，长度{len(old_section)}字符")
    
    # 增强实践练习部分
    new_section = enhance_practice_section(old_section, chapter_num)
    
    # 替换原内容
    new_content = content.replace(old_section, new_section)
    
    # 保存
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"第{chapter_num}章增强完成")

if __name__ == "__main__":
    # 处理所有章节
    for i in range(1, 13):
        process_chapter(i)
    print("全部章节处理完成")

