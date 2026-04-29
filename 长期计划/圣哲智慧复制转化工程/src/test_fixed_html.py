#!/usr/bin/env python3
"""
测试修正后的HTML文件
"""

import subprocess
from pathlib import Path

# 测试第一章
html_file = Path("outputs/儿童哲学史/排版阶段/章节HTML/修正版/第1章样张_fixed.html")
pdf_file = Path("outputs/儿童哲学史/最终交付/test_chapter1.pdf")

if html_file.exists():
    print(f"测试文件: {html_file}")
    
    # 使用wkhtmltopdf转换，尝试禁用安全限制
    cmd = [
        'wkhtmltopdf',
        '--page-size', 'A4',
        '--margin-top', '20mm',
        '--margin-right', '20mm',
        '--margin-bottom', '20mm',
        '--margin-left', '20mm',
        '--disable-local-file-access',  # 允许访问本地文件
        str(html_file),
        str(pdf_file)
    ]
    
    print("运行命令:", " ".join(cmd))
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print("返回码:", result.returncode)
    print("标准输出:", result.stdout[:500] if result.stdout else "无")
    print("标准错误:", result.stderr[:500] if result.stderr else "无")
    
    if pdf_file.exists():
        print(f"PDF生成成功: {pdf_file}")
        
        # 检查PDF信息
        cmd = ['pdfinfo', str(pdf_file)]
        info_result = subprocess.run(cmd, capture_output=True, text=True)
        
        if info_result.returncode == 0:
            print("PDF信息:")
            print(info_result.stdout)
    else:
        print("PDF生成失败")
else:
    print("HTML文件不存在")