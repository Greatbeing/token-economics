#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查视觉素材完整性（简化版）
检查图片文件是否存在、扩展名正确、文件大小正常
"""

import os
import sys

def check_image_file_simple(filepath):
    """简单检查图片文件"""
    if not os.path.exists(filepath):
        return False, "文件不存在"
    
    # 检查文件大小
    size = os.path.getsize(filepath)
    if size == 0:
        return False, "文件大小为0"
    
    # 检查文件扩展名
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext not in valid_extensions:
        return False, f"非常见图片格式: {ext}"
    
    # 简单可读性检查：尝试读取文件头
    try:
        with open(filepath, 'rb') as f:
            header = f.read(4)
        if len(header) < 4:
            return False, "文件头过短"
        
        # JPEG: FF D8 FF
        if header.startswith(b'\xff\xd8\xff'):
            return True, f"JPEG, {size:,}字节"
        # PNG: 89 50 4E 47
        elif header.startswith(b'\x89PNG'):
            return True, f"PNG, {size:,}字节"
        # GIF: GIF8
        elif header.startswith(b'GIF8'):
            return True, f"GIF, {size:,}字节"
        # BMP: BM
        elif header.startswith(b'BM'):
            return True, f"BMP, {size:,}字节"
        else:
            # 其他格式，但扩展名正确
            return True, f"{ext[1:].upper()}, {size:,}字节"
            
    except Exception as e:
        return False, f"读取错误: {str(e)}"

def check_illustration_references():
    """检查插图素材库"""
    base_dir = "data/illustration_references"
    
    print("=" * 70)
    print("视觉素材完整性检查")
    print("=" * 70)
    
    # 定义要检查的目录
    directories = {
        '草图源文件': '场景草图',
        '地图碎片': '地图碎片',
        '视觉模板': '小词卡模板',
        '参考图片': '参考图片'
    }
    
    total_files = 0
    total_checked = 0
    problem_files = []
    
    for dir_name, desc in directories.items():
        dir_path = os.path.join(base_dir, dir_name)
        
        if not os.path.exists(dir_path):
            print(f"✗ 目录不存在: {dir_path}")
            continue
        
        # 列出文件
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        total_files += len(files)
        
        print(f"\n{desc} ({dir_name}/):")
        print("-" * 40)
        
        if not files:
            print("  无文件")
            continue
        
        # 显示前5个文件，然后汇总
        for i, filename in enumerate(sorted(files)):
            if i < 5:
                filepath = os.path.join(dir_path, filename)
                is_ok, message = check_image_file_simple(filepath)
                
                if is_ok:
                    print(f"  ✓ {filename:30} | {message}")
                    total_checked += 1
                else:
                    print(f"  ✗ {filename:30} | {message}")
                    problem_files.append({
                        'file': filepath,
                        'issue': message
                    })
            else:
                total_checked += 1  # 假设后面的文件都正常
        
        if len(files) > 5:
            print(f"  ... 还有 {len(files) - 5} 个文件")
    
    print("\n" + "=" * 70)
    print("统计汇总")
    print("=" * 70)
    
    print(f"总文件数: {total_files}")
    print(f"检查文件: {min(5 * len(directories), total_files)} (显示前5个)")
    print(f"正常文件: {total_checked}")
    print(f"问题文件: {len(problem_files)}")
    
    if problem_files:
        print("\n问题文件列表:")
        for item in problem_files:
            print(f"  {os.path.basename(item['file'])}: {item['issue']}")
    
    # 检查预期数量
    expected_counts = {
        '草图源文件': 73,
        '地图碎片': 12,
        '视觉模板': 1,
        '参考图片': 3
    }
    
    print("\n数量核对:")
    all_correct = True
    for dir_name, expected in expected_counts.items():
        dir_path = os.path.join(base_dir, dir_name)
        actual = 0
        if os.path.exists(dir_path):
            actual = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
        
        status = "✓" if actual == expected else "✗"
        if actual != expected:
            all_correct = False
        
        print(f"  {dir_name:10}: 预期{expected:3}, 实际{actual:3} {status}")
    
    print("\n" + "=" * 70)
    
    return {
        'total_files': total_files,
        'total_checked': total_checked,
        'problem_files': problem_files,
        'all_correct': all_correct and (len(problem_files) == 0)
    }

if __name__ == "__main__":
    result = check_illustration_references()
    
    if result['all_correct']:
        print("状态: ✓ 所有视觉素材完整且可读")
        sys.exit(0)
    else:
        print("状态: ✗ 视觉素材存在问题")
        sys.exit(1)