#!/usr/bin/env python3
"""
修复PDF乱码和图片比例问题
使用方法: python3 修复PDF生成.py
"""

import os
import sys
import re
import subprocess
from pathlib import Path

def fix_html_for_pdf(html_file, css_file, output_pdf):
    """修复HTML并生成PDF"""
    
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否有base64图片（可能会导致问题）
    base64_count = content.count('data:image')
    print(f"检测到 {base64_count} 个内嵌图片")
    
    # 替换CSS引用为新的修复版CSS
    if 'style.css' in content:
        content = content.replace('style.css', 'style_fixed.css')
        print("已替换CSS引用")
    
    # 确保UTF-8编码
    if 'charset' not in content.lower():
        content = content.replace('<head>', '<head>\n<meta charset="UTF-8">', 1)
    
    # 保存修复后的HTML
    fixed_html = html_file.replace('.html', '_pdf_fixed.html')
    with open(fixed_html, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已保存修复后的HTML: {fixed_html}")
    
    return fixed_html


def generate_pdf_with_wkhtmltopdf(html_file, output_pdf):
    """使用wkhtmltopdf生成PDF"""
    
    # 确保路径正确
    html_path = os.path.abspath(html_file)
    
    # wkhtmltopdf命令参数
    cmd = [
        'wkhtmltopdf',
        '--enable-local-file-access',  # 允许访问本地文件
        '--encoding', 'utf-8',          # UTF-8编码
        '--page-size', 'A4',            # A4页面
        '--orientation', 'Portrait',    # 纵向
        '--no-stop-slow-scripts',       # 不要停止慢脚本
        '--javascript-delay', '3000',   # 等待JS执行
        '--margin-top', '15mm',
        '--margin-bottom', '15mm',
        '--margin-left', '15mm',
        '--margin-right', '15mm',
        '--disable-smart-shrinking',    # 禁用智能缩放
        '--user-style-sheet', '',       # 用户样式表
        html_path,                       # 输入文件
        os.path.abspath(output_pdf)      # 输出文件
    ]
    
    print(f"\n开始生成PDF...")
    print(f"输入: {html_path}")
    print(f"输出: {os.path.abspath(output_pdf)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ PDF生成成功!")
            print(f"文件大小: {os.path.getsize(output_pdf) / 1024 / 1024:.2f} MB")
            return True
        else:
            print(f"❌ PDF生成失败!")
            print(f"错误: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ PDF生成超时!")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return False


def main():
    # 设置路径
    base_dir = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史")
    html_dir = base_dir / "排版阶段/章节HTML/修正版"
    output_dir = base_dir / "最终交付"
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 测试文件
    chapter_file = html_dir / "第1章样张_fixed.html"
    css_file = html_dir / "style_fixed.css"
    test_pdf = output_dir / "测试_第一章_修复版.pdf"
    
    print("=" * 50)
    print("PDF乱码和图片比例问题修复工具")
    print("=" * 50)
    
    if not chapter_file.exists():
        print(f"❌ HTML文件不存在: {chapter_file}")
        return
    
    if not css_file.exists():
        print(f"❌ CSS文件不存在: {css_file}")
        return
    
    # 修复HTML并生成PDF
    fixed_html = fix_html_for_pdf(str(chapter_file), str(css_file), str(test_pdf))
    
    # 生成PDF
    success = generate_pdf_with_wkhtmltopdf(fixed_html, str(test_pdf))
    
    if success:
        print("\n" + "=" * 50)
        print("修复完成! PDF文件已生成:")
        print(f"  {test_pdf}")
        print("=" * 50)
    else:
        print("\n❌ 修复失败!")


if __name__ == "__main__":
    main()
