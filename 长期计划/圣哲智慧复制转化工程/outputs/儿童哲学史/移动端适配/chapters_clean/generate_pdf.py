#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成清理后的PDF文件
"""

import subprocess
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
FINAL_DIR = Path("/app/data/所有对话/主对话/长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/最终交付")

# 确保最终交付目录存在
FINAL_DIR.mkdir(parents=True, exist_ok=True)

merged_html = OUTPUT_DIR / "merged_clean.html"
output_pdf = FINAL_DIR / "和古人一起想问题_移动端优化版.pdf"

if not merged_html.exists():
    print(f"错误: 找不到HTML文件 {merged_html}")
    exit(1)

print("=" * 60)
print("开始生成PDF...")
print("=" * 60)

# wkhtmltopdf命令参数
cmd = [
    "wkhtmltopdf",
    "--enable-local-file-access",  # 允许访问本地文件
    "--page-size", "A5",  # 页面大小
    "--margin-top", "15mm",  # 上边距
    "--margin-bottom", "15mm",  # 下边距
    "--margin-left", "15mm",  # 左边距
    "--margin-right", "12mm",  # 右边距
    "--print-media-type",  # 使用打印样式
    "--no-stop-slow-scripts",  # 不停止慢脚本
    "--enable-javascript",  # 启用JavaScript
    "--javascript-delay", "1000",  # JavaScript延迟
    "--image-quality", "90",  # 图片质量
    str(merged_html),  # 输入HTML
    str(output_pdf)  # 输出PDF
]

print(f"输入: {merged_html}")
print(f"输出: {output_pdf}")
print()

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    
    if result.returncode == 0:
        print("✓ PDF生成成功!")
        print(f"文件路径: {output_pdf}")
        
        # 检查文件大小
        file_size = output_pdf.stat().st_size
        print(f"文件大小: {file_size / 1024 / 1024:.2f} MB")
    else:
        print("✗ PDF生成失败!")
        print(f"错误: {result.stderr}")
        
except subprocess.TimeoutExpired:
    print("✗ PDF生成超时!")
except Exception as e:
    print(f"✗ 发生错误: {e}")

print("=" * 60)
