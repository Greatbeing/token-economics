#!/usr/bin/env python3
"""
创建章节-插图映射表
"""

import json
import os
from pathlib import Path

# 扫描草图源文件目录
IMAGE_DIR = Path("data/illustration_references/草图源文件")
OUTPUT_FILE = Path("data/illustration_references/chapter_illustration_mapping.json")

# 定义每章的标准位置（基于第一章结构）
# 位置标签对应章节中的特定标题
POSITION_MAPPING = {
    "after_thought_theater": "## 思想剧场",
    "after_first_station": "## 第一站",
    "after_second_station": "## 第二站", 
    "after_third_station": "## 第三站",
    "after_think_about": "## 想一想",
    "after_global_telescope": "## 全球望远镜",
    "after_practice": "## 实践练习"
}

# 每章的场景数量统计
chapter_scene_counts = {}
for i in range(1, 13):
    pattern = f"ch{i}_scene*.jpg"
    files = list(IMAGE_DIR.glob(pattern))
    chapter_scene_counts[i] = len(files)
    print(f"第{i}章: {len(files)}个场景")

# 生成映射表
mapping = {
    "chapters": [],
    "position_labels": POSITION_MAPPING,
    "total_scenes": sum(chapter_scene_counts.values())
}

# 为每章分配场景和位置
for chapter_num in range(1, 13):
    chapter_key = f"ch{chapter_num}"
    scene_files = []
    
    # 收集该章所有场景文件
    for scene_num in range(1, 5):  # 最多4个场景
        file_name = f"{chapter_key}_scene{scene_num}.jpg"
        file_path = IMAGE_DIR / file_name
        if file_path.exists():
            scene_files.append(file_name)
    
    if not scene_files:
        print(f"警告: 第{chapter_num}章没有场景文件")
        continue
    
    # 为每个场景分配位置（基于可用位置）
    positions = list(POSITION_MAPPING.keys())
    
    chapter_data = {
        "chapter_number": chapter_num,
        "chapter_key": chapter_key,
        "scenes": []
    }
    
    # 为每个场景分配位置（循环使用可用位置）
    for i, scene_file in enumerate(scene_files):
        # 如果位置不够用，重复使用最后一个位置
        position_idx = i if i < len(positions) else -1
        position_label = positions[position_idx]
        
        # 生成alt文本
        alt_text = f"第{chapter_num}章场景{i+1}"
        
        scene_data = {
            "file_name": scene_file,
            "position_label": position_label,
            "alt_text": alt_text,
            "description": f"第{chapter_num}章第{i+1}个场景插图"
        }
        
        chapter_data["scenes"].append(scene_data)
    
    mapping["chapters"].append(chapter_data)

# 保存为JSON文件
os.makedirs(OUTPUT_FILE.parent, exist_ok=True)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)

print(f"映射表已保存到: {OUTPUT_FILE}")
print(f"总计: {len(mapping['chapters'])}章, {mapping['total_scenes']}个场景")

# 打印摘要
for chapter in mapping["chapters"]:
    print(f"第{chapter['chapter_number']}章: {len(chapter['scenes'])}个场景")