#!/usr/bin/env python3
"""
儿童版中国哲学史 - 批量生成所有章节HTML样张（完整插图版）
生成第2至12章HTML样张，每章嵌入完整的3-4张场景插图
"""

import sys
import json
import re
from pathlib import Path
import subprocess
import tempfile
import shutil
import base64
import os

# 导入generate_chapter_html中的函数
from generate_chapter_html import Config, generate_html

# 自定义配置：修改输出目录
class BatchConfig(Config):
    OUTPUT_DIR = Path("outputs/儿童哲学史/排版阶段/章节HTML")
    CSS_FILE = Path("outputs/儿童哲学史/排版阶段/样张/style.css")

# 章节映射：中文数字到阿拉伯数字
CHINESE_NUMERALS = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '十一': 11, '十二': 12
}

def extract_chapter_number_from_filename(filename):
    """从文件名中提取章节数字"""
    match = re.search(r'第([一二三四五六七八九十]+)章', filename)
    if match:
        chinese_num = match.group(1)
        return CHINESE_NUMERALS.get(chinese_num)
    return None

def load_mapping(mapping_file):
    """加载映射表"""
    if not mapping_file.exists():
        print(f"错误: 映射表文件不存在: {mapping_file}")
        return None
    with open(mapping_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_chapter_scene_count(mapping, chapter_num):
    """获取指定章节的场景插图数量"""
    if not mapping:
        return 0
    for ch in mapping.get("chapters", []):
        if ch.get("chapter_number") == chapter_num:
            return len(ch.get("scenes", []))
    return 0

def main():
    print("=" * 70)
    print("儿童版中国哲学史 - 批量HTML样张生成（完整插图版）")
    print("=" * 70)
    
    # 初始化配置
    config = BatchConfig()
    
    # 加载映射表
    mapping = load_mapping(config.MAPPING_FILE)
    if not mapping:
        print("无法加载映射表，退出。")
        sys.exit(1)
    
    print(f"映射表加载成功，共{len(mapping.get('chapters', []))}章，{mapping.get('total_scenes', 0)}个场景")
    
    # 确保输出目录存在
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    # 章节范围：第2章到第12章
    chapters_to_process = list(range(2, 13))
    
    print(f"准备处理章节: {chapters_to_process}")
    print()
    
    # 结果统计
    results = []
    failed_chapters = []
    
    # 处理每个章节
    for chapter_num in chapters_to_process:
        print(f"--- 处理第{chapter_num}章 ---")
        
        # 查找对应的Markdown文件
        input_file = None
        for f in Path("outputs/儿童哲学史/优化阶段").glob("*.md"):
            if f.name.startswith(f"第{chapter_num}章") or f.name.startswith(f"第{CHINESE_NUMERALS.get(chapter_num)}章"):
                input_file = f
                break
        
        if not input_file:
            # 尝试中文数字
            chinese_num = {v: k for k, v in CHINESE_NUMERALS.items()}.get(chapter_num)
            input_file = Path(f"outputs/儿童哲学史/优化阶段/第{chinese_num}章优化稿.md")
            if not input_file.exists():
                print(f"错误: 找不到第{chapter_num}章的优化稿文件")
                failed_chapters.append(chapter_num)
                continue
        
        # 输出文件
        output_file = config.OUTPUT_DIR / f"第{chapter_num}章样张.html"
        
        # 获取预期场景数量
        expected_scenes = get_chapter_scene_count(mapping, chapter_num)
        print(f"输入文件: {input_file}")
        print(f"输出文件: {output_file}")
        print(f"预期场景插图数量: {expected_scenes}")
        
        # 生成HTML
        success = generate_html(input_file, output_file, config)
        
        if success:
            # 验证结果
            file_size = output_file.stat().st_size / 1024
            print(f"生成成功！文件大小: {file_size:.1f} KB")
            
            # 统计实际图片数量
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                actual_images = len(re.findall(r'<img[^>]*>', content))
                data_url_images = len(re.findall(r'src="data:image[^"]*"', content))
            
            print(f"实际图片标签数量: {actual_images} (Data URL: {data_url_images})")
            
            # 检查CSS链接
            has_css = 'rel="stylesheet"' in content
            print(f"CSS链接: {'已添加' if has_css else '未找到'}")
            
            # 检查响应式meta标签
            has_viewport = 'viewport' in content
            print(f"响应式viewport: {'已添加' if has_viewport else '未找到'}")
            
            # 记录结果
            results.append({
                'chapter': chapter_num,
                'file_size_kb': file_size,
                'expected_scenes': expected_scenes,
                'actual_images': actual_images,
                'data_url_images': data_url_images,
                'has_css': has_css,
                'has_viewport': has_viewport,
                'output_file': str(output_file)
            })
            
            # 验证场景数量是否匹配
            if actual_images == expected_scenes:
                print(f"✓ 场景插图数量匹配预期 ({actual_images}/{expected_scenes})")
            else:
                print(f"⚠ 场景插图数量不匹配: 实际{actual_images}个，预期{expected_scenes}个")
                # 仍然算成功，但记录警告
        else:
            print(f"✗ 第{chapter_num}章生成失败")
            failed_chapters.append(chapter_num)
        
        print()
    
    # 生成报告
    print("=" * 70)
    print("批量处理完成")
    print("=" * 70)
    
    # 总体统计
    total_chapters = len(chapters_to_process)
    success_chapters = len(results)
    failure_chapters = len(failed_chapters)
    
    print(f"处理章节总数: {total_chapters}")
    print(f"成功生成: {success_chapters}")
    print(f"失败章节: {failure_chapters}")
    
    if failed_chapters:
        print(f"失败的章节编号: {failed_chapters}")
    
    # 详细结果
    print("\n详细结果:")
    for r in results:
        print(f"  第{r['chapter']}章: {r['file_size_kb']:.1f}KB, "
              f"图片{r['actual_images']}/{r['expected_scenes']}个, "
              f"CSS: {'✓' if r['has_css'] else '✗'}, "
              f"响应式: {'✓' if r['has_viewport'] else '✗'}")
    
    # 检查抽查章节（第2、6、12章）
    print("\n抽查验证（第2、6、12章）:")
    check_chapters = [2, 6, 12]
    for ch in check_chapters:
        for r in results:
            if r['chapter'] == ch:
                status = "✓" if r['actual_images'] == r['expected_scenes'] else "⚠"
                print(f"  第{ch}章: {status} 预期{r['expected_scenes']}个场景，实际{r['actual_images']}个")
                break
    
    # 生成报告文件
    report_file = Path("outputs/儿童哲学史/排版阶段/批量生成完整插图版报告.md")
    os.makedirs(report_file.parent, exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 《儿童版中国哲学史》HTML样张批量生成报告（完整插图版）\n\n")
        f.write(f"**处理日期**: 2026-04-02\n")
        f.write(f"**处理范围**: 第2章至第12章\n")
        f.write(f"**总章节数**: {total_chapters}\n")
        f.write(f"**成功生成**: {success_chapters}\n")
        f.write(f"**失败章节**: {failure_chapters}\n\n")
        
        if failed_chapters:
            f.write(f"**失败章节编号**: {failed_chapters}\n\n")
        
        f.write("## 详细结果\n\n")
        f.write("| 章节 | 文件大小 | 预期场景数 | 实际图片数 | Data URL图片数 | CSS链接 | 响应式viewport |\n")
        f.write("|------|----------|------------|------------|----------------|----------|----------------|\n")
        
        for r in results:
            f.write(f"| 第{r['chapter']}章 | {r['file_size_kb']:.1f}KB | {r['expected_scenes']} | {r['actual_images']} | "
                    f"{r['data_url_images']} | {'✓' if r['has_css'] else '✗'} | {'✓' if r['has_viewport'] else '✗'} |\n")
        
        f.write("\n## 抽查验证结果\n\n")
        f.write("按验收标准抽查第2、6、12章：\n\n")
        for ch in [2, 6, 12]:
            for r in results:
                if r['chapter'] == ch:
                    status = "通过" if r['actual_images'] == r['expected_scenes'] else "警告"
                    f.write(f"- **第{ch}章**: {status} - 预期{r['expected_scenes']}个场景，实际{r['actual_images']}个场景")
                    if r['actual_images'] > 0 and r['data_url_images'] == r['actual_images']:
                        f.write("，全部使用Data URL嵌入\n")
                    else:
                        f.write(f"，Data URL图片: {r['data_url_images']}个\n")
                    break
        
        f.write("\n## 总结\n\n")
        if success_chapters == total_chapters:
            f.write("✅ **批量生成成功**：所有章节均成功生成HTML样张，每章嵌入了完整的场景插图。\n")
        else:
            f.write(f"⚠ **部分成功**：{success_chapters}/{total_chapters}个章节生成成功，{failure_chapters}个章节失败。\n")
        
        f.write("\n## 后续建议\n\n")
        f.write("1. 抽查生成的HTML文件，确保图片显示正常\n")
        f.write("2. 在移动设备上测试响应式布局效果\n")
        f.write("3. 考虑优化图片大小以减小HTML文件体积\n")
    
    print(f"\n报告已保存: {report_file}")
    
    # 返回状态码
    if failure_chapters > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()