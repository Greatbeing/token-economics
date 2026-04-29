#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《儿童版中国哲学史》插图设计指引文档
"""

import os
import re
from pathlib import Path

def list_scene_files():
    """列出所有场景草图文件"""
    sketch_dir = Path("outputs/儿童哲学史/设计阶段/草图")
    scenes_by_chapter = {}
    
    if not sketch_dir.exists():
        return scenes_by_chapter
    
    for file in sketch_dir.glob("ch*.jpg"):
        filename = file.name
        # 匹配 ch{数字}_scene{数字}.jpg
        match = re.match(r'ch(\d+)_scene(\d+)\.jpg', filename)
        if match:
            chapter = int(match.group(1))
            scene = int(match.group(2))
            if chapter not in scenes_by_chapter:
                scenes_by_chapter[chapter] = []
            scenes_by_chapter[chapter].append((scene, filename))
    
    # 按章节和场景排序
    for chapter in scenes_by_chapter:
        scenes_by_chapter[chapter].sort(key=lambda x: x[0])
    
    return scenes_by_chapter

def list_map_fragments():
    """列出所有地图碎片文件"""
    map_dir = Path("outputs/儿童哲学史/设计阶段/视觉元素/地图碎片")
    fragments = []
    
    if map_dir.exists():
        for file in map_dir.glob("map_fragment_*.jpg"):
            fragments.append(file.name)
    
    fragments.sort()
    return fragments

def get_chapter_titles():
    """获取章节标题"""
    # 从优化稿目录读取
    titles = {}
    opt_dir = Path("outputs/儿童哲学史/优化阶段")
    
    # 章节编号到标题的映射（部分已知）
    chapter_map = {
        1: "世界是从哪儿来的？",
        2: "为什么我和别人不一样？",
        3: "怎样才算“赢了”？",
        4: "我能想做什么就做什么吗？",
        5: "什么是“好”的规则？",
        6: "心里害怕怎么办？",
        7: "为什么他们那么爱自由？",
        8: "魏晋风度：竹林里的“叛逆”少年",
        9: "朱熹的“宇宙大房子”——理学家在做什么？",
        10: "王阳明的“心里种花”——良知在你心里",
        11: "如何当一个“现代中国人”？——明清之际的启蒙探险",
        12: "我们为什么要学哲学？——探险家的毕业典礼与终身邀请"
    }
    
    # 验证文件是否存在
    for chapter, title in chapter_map.items():
        file_path = opt_dir / f"第{chapter_to_chinese(chapter)}章优化稿.md"
        if file_path.exists():
            titles[chapter] = title
    
    return titles

def chapter_to_chinese(num):
    """数字转中文"""
    chinese_map = {
        1: "一", 2: "二", 3: "三", 4: "四", 5: "五",
        6: "六", 7: "七", 8: "八", 9: "九", 10: "十",
        11: "十一", 12: "十二"
    }
    return chinese_map.get(num, str(num))

def generate_guide():
    """生成指引文档内容"""
    scenes_by_chapter = list_scene_files()
    fragments = list_map_fragments()
    chapter_titles = get_chapter_titles()
    
    lines = []
    lines.append("# 《儿童版中国哲学史》插图设计指引")
    lines.append("")
    lines.append("## 文档说明")
    lines.append("")
    lines.append("本文档为《儿童版中国哲学史》的插图设计提供详细指引，涵盖全书视觉风格、章节场景设计、地图碎片规范、小词卡模板使用等内容。旨在确保所有插图风格统一、符合儿童审美，并能准确传达哲学概念。")
    lines.append("")
    lines.append("**版本**：v1.0")
    lines.append("**生成日期**：2026-04-02")
    lines.append("**适用对象**：插图设计师、排版设计师、项目审核人员")
    lines.append("")
    
    lines.append("## 1. 全书视觉风格总览")
    lines.append("")
    lines.append("### 1.1 核心风格定位")
    lines.append("- **整体调性**：温暖智趣的哲学探险之旅")
    lines.append("- **视觉关键词**：温暖亲切、智趣好奇、通透灵动、简约深邃")
    lines.append("")
    lines.append("### 1.2 设计系统概要")
    lines.append("#### 配色方案")
    lines.append("- **主色调**：哲学琥珀 (#FFB74D)、思考浅蓝 (#81D4FA)、书卷米白 (#FFF8E1)")
    lines.append("- **辅助色**：道家青绿 (#A5D6A7)、儒家暖橙 (#FFCC80)、佛家浅紫 (#E1BEE7)、墨家深灰 (#BDBDBD)")
    lines.append("- **强调色**：智慧深蓝 (#1565C0)、历史深棕 (#5D4037)、互动亮黄 (#FFF176)")
    lines.append("")
    lines.append("#### 字体系统")
    lines.append("- **中文字体**：方正少儿简体（标题）、思源宋体 Regular（正文）、汉仪娃娃篆（趣味元素）")
    lines.append("- **英文字体**：Arial Rounded MT Bold（标题）、Arial（正文）")
    lines.append("")
    lines.append("#### 版面布局")
    lines.append("- **页面尺寸**：210mm × 285mm（A4竖向）")
    lines.append("- **网格系统**：12列网格")
    lines.append("- **图文搭配**：嵌入式、跨页式、侧栏式、独立页面")
    lines.append("")
    lines.append("### 1.3 已生成视觉资产统计")
    lines.append(f"- **场景草图**：共 {sum(len(scenes) for scenes in scenes_by_chapter.values())} 个（涵盖{len(scenes_by_chapter)}章）")
    lines.append(f"- **地图碎片**：共 {len(fragments)} 个（第1-12章）")
    lines.append("- **视觉模板**：哲学小词卡模板 1 个")
    lines.append("- **参考图片**：风格参考图片 3 张")
    lines.append("")
    
    lines.append("## 2. 章节场景设计指引")
    lines.append("")
    lines.append("### 2.1 通用设计原则")
    lines.append("1. **儿童视角**：画面需从8-12岁儿童的视角出发，强调亲切感与代入感")
    lines.append("2. **情感表达**：角色表情生动，肢体语言适度夸张，传递哲学思考的情绪变化")
    lines.append("3. **叙事性**：每个场景应具有清晰的叙事焦点，展现哲学对话或思想实验")
    lines.append("4. **视觉隐喻**：运用符号、色彩、构图等手法隐喻哲学概念")
    lines.append("5. **风格统一**：确保线条、色彩、造型与全书风格保持一致")
    lines.append("")
    
    # 各章节具体指引
    for chapter in sorted(scenes_by_chapter.keys()):
        title = chapter_titles.get(chapter, f"第{chapter_to_chinese(chapter)}章")
        scenes = scenes_by_chapter[chapter]
        
        lines.append(f"### 2.{chapter} 第{chapter_to_chinese(chapter)}章：{title}")
        lines.append("")
        lines.append("#### 核心哲学主题")
        # 根据章节内容简要描述
        theme_descriptions = {
            1: "宇宙起源、道的概念、无中生有",
            2: "个体差异、仁爱之心、推己及人",
            3: "胜负观念、辩证法、阴阳转化",
            4: "自由与约束、无为而治、自然之道",
            5: "规则正义、法治思想、社会秩序",
            6: "恐惧应对、心性修炼、勇气智慧",
            7: "自由精神、个性解放、魏晋风度",
            8: "竹林七贤、叛逆与真诚、艺术与哲学",
            9: "理学体系、格物致知、宇宙秩序",
            10: "心学思想、致良知、知行合一",
            11: "启蒙思想、中西交流、现代性探索",
            12: "哲学意义、终身学习、思想成长"
        }
        theme = theme_descriptions.get(chapter, "详见章节内容")
        lines.append(f"- **核心主题**：{theme}")
        lines.append(f"- **代表人物**：见各章智慧探险地图")
        lines.append("")
        
        lines.append("#### 场景设计要点")
        lines.append(f"本章共设计 {len(scenes)} 个关键场景，文件列表：")
        for scene_num, filename in scenes:
            lines.append(f"- **场景{scene_num}**：`{filename}`")
        lines.append("")
        
        # 通用场景描述模板（可根据实际内容调整）
        scene_descriptions = {
            1: "星空下的辩论会：小星和小宇在楼顶天台仰望星空，老子骑青牛出现",
            2: "校园冲突场景：儿童在日常矛盾中体验'仁'的概念",
            3: "游戏竞赛情境：通过胜负体验辩证思维",
            4: "自然观察场景：在山水间感悟自由与约束"
        }
        
        # 为每个场景提供简要描述
        for scene_num, filename in scenes:
            desc_key = scene_num if scene_num in scene_descriptions else 1
            desc = scene_descriptions.get(desc_key, "哲学对话场景")
            lines.append(f"**场景{scene_num}设计指引**：")
            lines.append(f"- **场景内容**：{desc}")
            lines.append(f"- **构图建议**：突出人物互动，背景简洁，营造对话氛围")
            lines.append(f"- **色彩建议**：使用本章主题色系，保持温暖明亮")
            lines.append(f"- **文件位置**：`outputs/儿童哲学史/设计阶段/草图/{filename}`")
            lines.append("")
        
        lines.append("---")
    
    lines.append("## 3. 智慧探险地图设计规范")
    lines.append("")
    lines.append("### 3.1 设计理念")
    lines.append("智慧探险地图是每章开篇的视觉索引，采用'可拼接藏宝图'风格，将哲学思想探索比喻为寻宝探险。")
    lines.append("")
    lines.append("### 3.2 视觉要素")
    lines.append("1. **地图碎片形状**：不规则撕裂边缘，模拟古老藏宝图碎片")
    lines.append("2. **核心问题图标**：醒目图标+文字，置于碎片中心位置")
    lines.append("3. **代表人物剪影**：Q版哲学家造型，分布在碎片不同区域")
    lines.append("4. **思想工具符号**：简化图形符号，代表本章核心思想工具")
    lines.append("5. **时间轴指示**：简约线条与时间标记，标明思想历史位置")
    lines.append("")
    lines.append("### 3.3 已生成地图碎片清单")
    for fragment in fragments:
        lines.append(f"- `{fragment}`")
    lines.append("")
    lines.append("### 3.4 拼接逻辑")
    lines.append("12个地图碎片可拼接为完整的中国哲学思想地图，拼接顺序按章节顺序排列。")
    lines.append("- **横向维度**：时间脉络（从古至今）")
    lines.append("- **纵向维度**：思想流派（儒、道、法、墨等）")
    lines.append("- **中心区域**：核心哲学问题集群")
    lines.append("")
    
    lines.append("## 4. 哲学小词卡模板使用说明")
    lines.append("")
    lines.append("### 4.1 模板文件")
    lines.append("- **文件名**：`philosophy_term_card_template.jpg`")
    lines.append("- **位置**：`outputs/儿童哲学史/设计阶段/视觉元素/`")
    lines.append("- **备份位置**：`data/illustration_references/视觉模板/`")
    lines.append("")
    lines.append("### 4.2 设计规格")
    lines.append("- **尺寸**：A6卡片大小（105mm × 148mm）")
    lines.append("- **布局**：上图为概念视觉化呈现，中为术语名称，下为儿童化定义")
    lines.append("- **色彩**：根据术语所属学派使用对应色系")
    lines.append("")
    lines.append("### 4.3 使用流程")
    lines.append("1. 确定术语所属学派，选择对应配色")
    lines.append("2. 根据术语内涵设计视觉隐喻图形")
    lines.append("3. 填写术语名称与儿童化定义")
    lines.append("4. 导出为高清图片，用于书籍附录")
    lines.append("")
    
    lines.append("## 5. 文件命名与路径规范")
    lines.append("")
    lines.append("### 5.1 目录结构")
    lines.append("```")
    lines.append("outputs/儿童哲学史/设计阶段/")
    lines.append("├── 草图/                    # 章节场景草图")
    lines.append("│   ├── ch1_scene1.jpg")
    lines.append("│   ├── ch1_scene2.jpg")
    lines.append("│   └── ...")
    lines.append("├── 视觉元素/")
    lines.append("│   ├── philosophy_term_card_template.jpg")
    lines.append("│   └── 地图碎片/")
    lines.append("│       ├── map_fragment_ch1.jpg")
    lines.append("│       └── ...")
    lines.append("├── 校对报告/")
    lines.append("│   └── 图片文字校对报告.md")
    lines.append("└── 视觉风格指南.md")
    lines.append("```")
    lines.append("")
    lines.append("### 5.2 素材库结构")
    lines.append("```")
    lines.append("data/illustration_references/")
    lines.append("├── 草图源文件/              # 场景草图备份")
    lines.append("├── 地图碎片/                # 地图碎片备份")
    lines.append("├── 视觉模板/                # 设计模板备份")
    lines.append("└── 参考图片/                # 风格参考图片")
    lines.append("```")
    lines.append("")
    lines.append("### 5.3 命名规则")
    lines.append("- **场景草图**：`ch{章节编号}_scene{场景编号}.jpg`")
    lines.append("- **地图碎片**：`map_fragment_ch{章节编号}.jpg`")
    lines.append("- **小词卡**：`term_card_{术语拼音}.jpg`（后续生成）")
    lines.append("- **文档文件**：使用中文描述性名称，如`视觉风格指南.md`")
    lines.append("")
    
    lines.append("## 6. 素材索引说明")
    lines.append("")
    lines.append("### 6.1 插图素材库索引")
    lines.append("| 分类 | 文件数量 | 主要用途 | 存放路径 |")
    lines.append("|------|----------|----------|----------|")
    lines.append("| 草图源文件 | 73 | 章节场景设计参考 | `data/illustration_references/草图源文件/` |")
    lines.append("| 地图碎片 | 12 | 章节开篇视觉索引 | `data/illustration_references/地图碎片/` |")
    lines.append("| 视觉模板 | 1 | 哲学小词卡设计 | `data/illustration_references/视觉模板/` |")
    lines.append("| 参考图片 | 3 | 风格借鉴与灵感 | `data/illustration_references/参考图片/` |")
    lines.append("")
    lines.append("### 6.2 关键文件清单")
    lines.append("#### 设计指南文档")
    lines.append("- `outputs/儿童哲学史/设计阶段/视觉风格指南.md` - 视觉风格定义与设计系统")
    lines.append("- `outputs/儿童哲学史/设计阶段/插图设计指引.md` - 本文件，具体设计指引")
    lines.append("")
    lines.append("#### 核心视觉资产")
    lines.append("- `outputs/儿童哲学史/设计阶段/视觉元素/philosophy_term_card_template.jpg` - 小词卡模板")
    lines.append("- `outputs/儿童哲学史/设计阶段/视觉元素/地图碎片/map_fragment_ch1.jpg`等 - 12个地图碎片")
    lines.append("")
    
    lines.append("## 7. 后续工作建议")
    lines.append("")
    lines.append("### 7.1 插图细化")
    lines.append("1. **基于草图深化**：在现有草图基础上进行精细化绘制")
    lines.append("2. **色彩统一调整**：确保所有插图符合配色规范")
    lines.append("3. **细节补充**：增加哲学符号、背景元素等细节")
    lines.append("")
    lines.append("### 7.2 排版整合准备")
    lines.append("1. **文件格式转换**：准备适用于排版的高分辨率图片")
    lines.append("2. **图文对应表**：建立插图与文字位置的对应关系")
    lines.append("3. **视觉层次规划**：设计全书图文搭配的视觉节奏")
    lines.append("")
    lines.append("### 7.3 质量检查清单")
    lines.append("- [ ] 所有插图风格一致性检查")
    lines.append("- [ ] 色彩准确性验证（印刷/屏幕）")
    lines.append("- [ ] 图像分辨率检查（≥300dpi）")
    lines.append("- [ ] 文件命名与路径规范性确认")
    lines.append("")
    
    lines.append("---")
    lines.append("**附录：章节优化稿位置**")
    lines.append("")
    for chapter in range(1, 13):
        title = chapter_titles.get(chapter, f"第{chapter_to_chinese(chapter)}章")
        lines.append(f"- 第{chapter_to_chinese(chapter)}章：`outputs/儿童哲学史/优化阶段/第{chapter_to_chinese(chapter)}章优化稿.md`")
    lines.append("")
    
    return "\n".join(lines)

def main():
    """主函数"""
    guide_content = generate_guide()
    
    # 保存文件
    output_path = Path("outputs/儿童哲学史/设计阶段/插图设计指引.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"插图设计指引已生成：{output_path}")
    
    # 统计信息
    scenes_by_chapter = list_scene_files()
    fragments = list_map_fragments()
    
    print(f"包含 {len(scenes_by_chapter)} 章的 {sum(len(scenes) for scenes in scenes_by_chapter.values())} 个场景指引")
    print(f"包含 {len(fragments)} 个地图碎片规范")
    print("素材库已建立于 data/illustration_references/")

if __name__ == "__main__":
    main()