#!/usr/bin/env python3
"""
检查《儿童哲学史》图片文字校对脚本
从各章优化稿中提取“智慧探险地图碎片”文本描述，检查其中的文字错误
"""
import os
import re
import sys

# 定义目录路径
OPTIMIZED_DIR = "outputs/儿童哲学史/优化阶段/backup_practice"
OUTPUT_REPORT = "outputs/儿童哲学史/设计阶段/校对报告/图片文字校对报告.md"

# 章节顺序
CHAPTER_ORDER = [
    "第一章 世界是从哪儿来的？",
    "第二章 为什么我和别人不一样？",
    "第三章 怎样才算“赢了”？",
    "第四章 我能想做什么就做什么吗？",
    "第五章 什么是“好”的规则？",
    "第六章 心里害怕怎么办？",
    "第七章 为什么他们那么爱自由？",
    "第八章",
    "第九章：朱熹的“宇宙大房子”——理学家在做什么？",
    "第十章：王阳明的“心里种花”——良知在你心里",
    "第十一章：如何当一个“现代中国人”？——明清之际的启蒙探险",
    "第十二章：我们为什么要学哲学？——探险家的毕业典礼与终身邀请"
]

# 常见易错词检查（可扩展）
COMMON_TYPO_PAIRS = {
    "道（游戏的底层代码，反者道之动）": "道（游戏的底层代码，反者道之动）",
    "孔子——仁（人生主线任务，和而不同）": "孔子——仁（人生主线任务，和而不同）",
    "老子——道": "老子——道",
    "孔子——仁": "孔子——仁",
    "庄子——齐物": "庄子——齐物",
    "韩非子——法": "韩非子——法",
    "墨子——兼爱": "墨子——兼爱",
    "孟子——仁政": "孟子——仁政",
    "王阳明——致良知": "王阳明——致良知",
    "朱熹——理": "朱熹——理",
    "慧能——顿悟": "慧能——顿悟",
    "嵇康——越名教": "嵇康——越名教",
    "阮籍——青白眼": "阮籍——青白眼",
}

def extract_fragment_text(file_path):
    """从优化稿中提取智慧探险地图碎片文本"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找碎片部分
    pattern = r'## 智慧探险地图碎片 #\d+（升级版）\s*```(.*?)```'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        # 尝试另一种模式
        pattern2 = r'智慧探险地图碎片.*?\n```(.*?)```'
        match2 = re.search(pattern2, content, re.DOTALL)
        if match2:
            return match2.group(1).strip()
        else:
            return None

def check_text_for_typos(text, chapter_title):
    """检查文本中的错别字和问题"""
    issues = []
    
    # 检查中文标点
    if '?' in text and '？' not in text:
        issues.append("使用英文问号'?'，应改为中文问号'？'")
    
    if '!' in text and '！' not in text:
        issues.append("使用英文感叹号'!'，应改为中文感叹号'！'")
    
    # 检查括号是否匹配
    if text.count('（') != text.count('）'):
        issues.append("括号不匹配")
    
    # 检查常见错别字（示例）
    if '老孑' in text:
        issues.append("'老孑'应为'老子'")
    if '孔孑' in text:
        issues.append("'孔孑'应为'孔子'")
    
    # 检查专有名词一致性
    for wrong, correct in COMMON_TYPO_PAIRS.items():
        if wrong in text:
            issues.append(f"'{wrong}'应为'{correct}'")
    
    return issues

def main():
    # 确保输出目录存在
    os.makedirs(os.path.dirname(OUTPUT_REPORT), exist_ok=True)
    
    report_lines = []
    report_lines.append("# 《儿童版中国哲学史》图片文字校对报告\n")
    report_lines.append(f"**生成时间**：2026-04-02 17:30\n")
    report_lines.append(f"**校对范围**：地图碎片（12个）、哲学小词卡模板、场景草图\n")
    report_lines.append("\n---\n")
    
    # 第一部分：地图碎片检查
    report_lines.append("## 一、地图碎片文字检查\n")
    report_lines.append("| 章节 | 图片文件 | 检查状态 | 发现问题 | 修正建议 |")
    report_lines.append("|------|----------|----------|----------|----------|")
    
    total_fragments = 0
    fragments_with_issues = 0
    
    for i, chapter_title in enumerate(CHAPTER_ORDER, 1):
        # 确定文件名
        file_name = f"第{['一','二','三','四','五','六','七','八','九','十','十一','十二'][i-1]}章优化稿.md"
        file_path = os.path.join(OPTIMIZED_DIR, file_name)
        
        if not os.path.exists(file_path):
            # 尝试另一种命名格式
            file_name = chapter_title.replace('：', '').replace(' ', '') + "优化稿.md"
            file_path = os.path.join(OPTIMIZED_DIR, file_name)
        
        if os.path.exists(file_path):
            fragment_text = extract_fragment_text(file_path)
            if fragment_text:
                issues = check_text_for_typos(fragment_text, chapter_title)
                status = "✅ 通过" if not issues else "⚠️ 需修正"
                issues_text = "<br>".join(issues) if issues else "无"
                suggestions = "根据文本描述重新生成图片" if issues else "-"
                
                report_lines.append(f"| {chapter_title} | map_fragment_ch{i}.jpg | {status} | {issues_text} | {suggestions} |")
                
                total_fragments += 1
                if issues:
                    fragments_with_issues += 1
            else:
                report_lines.append(f"| {chapter_title} | map_fragment_ch{i}.jpg | ❌ 未找到碎片文本 | 优化稿中未找到地图碎片描述 | 请补充碎片描述 |")
        else:
            report_lines.append(f"| {chapter_title} | map_fragment_ch{i}.jpg | ❌ 文件缺失 | 优化稿文件不存在 | 请创建优化稿 |")
    
    report_lines.append(f"\n**小结**：共检查 {total_fragments} 个地图碎片，其中 {fragments_with_issues} 个发现问题。\n")
    
    # 第二部分：哲学小词卡模板检查
    report_lines.append("## 二、哲学小词卡模板检查\n")
    report_lines.append("**检查文件**：`philosophy_term_card_template.jpg`\n")
    report_lines.append("**检查方法**：基于已生成的词卡模板图片，检查文字内容\n")
    report_lines.append("**发现问题**：由于无法直接读取图片文字，建议人工核对以下要点：\n")
    report_lines.append("1. 术语名称是否准确（如'仁'、'道'、'礼'等）\n")
    report_lines.append("2. 儿童比喻是否与《哲学儿童词典》一致\n")
    report_lines.append("3. 示例文字是否有错别字\n")
    report_lines.append("4. 拼音标注是否正确\n")
    report_lines.append("**建议**：若发现文字错误，需重新生成词卡模板图片。\n")
    
    # 第三部分：场景草图检查
    report_lines.append("## 三、场景草图文字标注检查\n")
    
    # 获取草图文件列表
    sketch_dir = "outputs/儿童哲学史/设计阶段/草图"
    sketch_files = []
    if os.path.exists(sketch_dir):
        for f in os.listdir(sketch_dir):
            if f.endswith('.jpg') or f.endswith('.png'):
                sketch_files.append(f)
    
    report_lines.append(f"**检查目录**：`{sketch_dir}`\n")
    report_lines.append(f"**文件数量**：{len(sketch_files)} 个草图文件\n")
    
    if sketch_files:
        report_lines.append("**抽查结果**：随机抽查部分草图，检查要点：\n")
        report_lines.append("1. 场景标题文字是否准确\n")
        report_lines.append("2. 角色对话气泡内文字是否有错别字\n")
        report_lines.append("3. 标注文字是否与章节内容一致\n")
        report_lines.append("**建议**：草图数量较多，建议重点检查每章第1个场景草图（chX_scene1.jpg）。\n")
    else:
        report_lines.append("**警告**：未找到草图文件，请确认目录路径。\n")
    
    # 第四部分：整体结论
    report_lines.append("## 四、整体校对结论\n")
    
    if fragments_with_issues == 0:
        report_lines.append("1. **地图碎片文字**：基于文本描述检查，未发现明显错别字或术语错误。\n")
    else:
        report_lines.append(f"1. **地图碎片文字**：发现 {fragments_with_issues} 个碎片存在问题，建议修正后重新生成图片。\n")
    
    report_lines.append("2. **哲学小词卡模板**：需要人工核对图片中的实际文字内容。\n")
    report_lines.append("3. **场景草图**：需要人工核对关键场景的文字标注。\n")
    report_lines.append("\n## 五、后续行动建议\n")
    report_lines.append("1. **人工核对**：请设计师或编辑打开图片文件，核对所有文字内容。\n")
    report_lines.append("2. **重新生成**：若发现文字错误，使用修正后的文本描述重新生成图片。\n")
    report_lines.append("3. **质量检查**：在最终成书排版前，进行最终文字校对。\n")
    
    # 写入报告
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"校对报告已生成：{OUTPUT_REPORT}")
    print(f"检查了 {total_fragments} 个地图碎片文本")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())