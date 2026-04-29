#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成素材清单
列出所有文字章节和图片文件的路径、大小、格式等信息
"""

import os
import sys
import datetime
from pathlib import Path

def get_file_info(filepath):
    """获取文件详细信息"""
    path = Path(filepath)
    
    if not path.exists():
        return None
    
    stat = path.stat()
    
    # 获取文件扩展名
    ext = path.suffix.lower()
    
    # 判断文件类型
    if ext in ['.md', '.txt']:
        file_type = '文本文件'
    elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']:
        file_type = '图像文件'
    else:
        file_type = '其他文件'
    
    # 获取修改时间
    mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
    
    return {
        'path': str(path),
        'name': path.name,
        'size': stat.st_size,
        'size_human': human_readable_size(stat.st_size),
        'type': file_type,
        'extension': ext[1:] if ext else '',
        'modified': mtime.strftime('%Y-%m-%d %H:%M:%S')
    }

def human_readable_size(size):
    """将字节数转换为可读格式"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0 or unit == 'GB':
            break
        size /= 1024.0
    return f"{size:.1f} {unit}"

def scan_directory(directory, recursive=True):
    """扫描目录中的文件"""
    base_path = Path(directory)
    if not base_path.exists():
        return []
    
    files = []
    if recursive:
        for file_path in base_path.rglob('*'):
            if file_path.is_file():
                files.append(str(file_path))
    else:
        for file_path in base_path.iterdir():
            if file_path.is_file():
                files.append(str(file_path))
    
    return sorted(files)

def generate_material_list():
    """生成素材清单"""
    print("正在生成素材清单...")
    
    # 定义要扫描的目录
    scan_dirs = {
        '文字内容': [
            'outputs/儿童哲学史/优化阶段/',
        ],
        '插图素材': [
            'data/illustration_references/草图源文件/',
            'data/illustration_references/地图碎片/',
            'data/illustration_references/视觉模板/',
            'data/illustration_references/参考图片/'
        ],
        '设计文档': [
            'outputs/儿童哲学史/设计阶段/',
            'outputs/儿童哲学史/排版阶段/'
        ]
    }
    
    all_files_info = []
    
    # 扫描所有目录
    for category, dir_list in scan_dirs.items():
        for directory in dir_list:
            if os.path.exists(directory):
                files = scan_directory(directory, recursive=False)
                for file_path in files:
                    info = get_file_info(file_path)
                    if info:
                        info['category'] = category
                        all_files_info.append(info)
    
    # 按类别和文件名排序
    all_files_info.sort(key=lambda x: (x['category'], x['name']))
    
    # 生成Markdown内容
    md_content = []
    md_content.append("# 《儿童版中国哲学史》素材清单")
    md_content.append("")
    md_content.append("## 文档说明")
    md_content.append("本文档列出了《儿童版中国哲学史》排版所需的所有素材文件，包括文字内容、插图素材和设计文档。")
    md_content.append("")
    md_content.append("**版本**：v1.0  ")
    md_content.append("**生成日期**：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    md_content.append("**文件总数**：" + str(len(all_files_info)))
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # 按类别输出
    current_category = None
    category_file_count = 0
    total_size = 0
    
    for file_info in all_files_info:
        if file_info['category'] != current_category:
            if current_category is not None:
                md_content.append(f"**本类别小计**：{category_file_count}个文件，总大小 {human_readable_size(category_size)}")
                md_content.append("")
                md_content.append("---")
                md_content.append("")
            
            current_category = file_info['category']
            category_file_count = 0
            category_size = 0
            
            md_content.append(f"## {current_category}")
            md_content.append("")
            md_content.append("| 文件名 | 类型 | 大小 | 修改时间 | 路径 |")
            md_content.append("|--------|------|------|----------|------|")
        
        category_file_count += 1
        category_size += file_info['size']
        total_size += file_info['size']
        
        # 简略路径（相对于当前目录）
        rel_path = file_info['path']
        if rel_path.startswith('./'):
            rel_path = rel_path[2:]
        
        md_content.append(f"| {file_info['name']} | {file_info['type']} | {file_info['size_human']} | {file_info['modified']} | `{rel_path}` |")
    
    # 最后一个小计
    if current_category is not None:
        md_content.append(f"**本类别小计**：{category_file_count}个文件，总大小 {human_readable_size(category_size)}")
        md_content.append("")
    
    md_content.append("---")
    md_content.append("")
    md_content.append("## 统计汇总")
    md_content.append("")
    
    # 分类统计
    category_stats = {}
    for file_info in all_files_info:
        cat = file_info['category']
        if cat not in category_stats:
            category_stats[cat] = {'count': 0, 'size': 0}
        category_stats[cat]['count'] += 1
        category_stats[cat]['size'] += file_info['size']
    
    md_content.append("| 类别 | 文件数量 | 总大小 |")
    md_content.append("|------|----------|--------|")
    for cat, stats in sorted(category_stats.items()):
        md_content.append(f"| {cat} | {stats['count']} | {human_readable_size(stats['size'])} |")
    
    md_content.append(f"| **总计** | **{len(all_files_info)}** | **{human_readable_size(total_size)}** |")
    md_content.append("")
    
    # 文字内容详细统计
    md_content.append("### 文字内容详细统计")
    md_content.append("")
    
    text_files = [f for f in all_files_info if f['category'] == '文字内容' and f['name'].endswith('.md')]
    chapter_files = [f for f in text_files if '优化稿' in f['name']]
    
    md_content.append("**章节优化稿**：" + str(len(chapter_files)) + "个文件")
    md_content.append("")
    
    if chapter_files:
        md_content.append("| 章节 | 文件大小 |")
        md_content.append("|------|----------|")
        for f in sorted(chapter_files, key=lambda x: x['name']):
            md_content.append(f"| {f['name'].replace('.md', '')} | {f['size_human']} |")
        md_content.append("")
    
    # 插图素材详细统计
    md_content.append("### 插图素材详细统计")
    md_content.append("")
    
    image_files = [f for f in all_files_info if f['category'] == '插图素材']
    
    for subdir in ['草图源文件', '地图碎片', '视觉模板', '参考图片']:
        subdir_files = [f for f in image_files if f['path'].find(f'/{subdir}/') != -1]
        if subdir_files:
            md_content.append(f"**{subdir}**：" + str(len(subdir_files)) + "个文件")
            md_content.append("")
            for f in sorted(subdir_files, key=lambda x: x['name'])[:5]:  # 只显示前5个
                md_content.append(f"- `{f['name']}` - {f['size_human']}")
            if len(subdir_files) > 5:
                md_content.append(f"- ... 还有 {len(subdir_files) - 5} 个文件")
            md_content.append("")
    
    md_content.append("---")
    md_content.append("")
    md_content.append("## 使用说明")
    md_content.append("")
    md_content.append("1. **文字内容**：12章优化稿已全部完成，位于 `outputs/儿童哲学史/优化阶段/` 目录")
    md_content.append("2. **插图素材**：共89个图像文件，已按照类型分类存储")
    md_content.append("3. **设计文档**：包含视觉风格指南、插图设计指引、排版规划方案等")
    md_content.append("4. **排版准备**：建议先阅读字体使用说明和色彩规范，确保一致性")
    md_content.append("")
    md_content.append("**注意**：排版前请确认所有字体文件已获得合法授权。")
    
    return "\n".join(md_content)

if __name__ == "__main__":
    # 生成清单内容
    list_content = generate_material_list()
    
    # 保存到文件
    output_path = "outputs/儿童哲学史/排版阶段/素材清单.md"
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(list_content)
        
        print(f"素材清单已生成：{output_path}")
        
        # 显示简要信息
        lines = list_content.split('\n')
        for line in lines[:20]:
            print(line)
        print("...")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"生成清单时出错：{str(e)}")
        sys.exit(1)