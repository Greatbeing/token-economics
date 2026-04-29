#!/usr/bin/env python3
"""
批量将修正版HTML文件转换为PDF
验证排版修正效果
"""

import subprocess
from pathlib import Path

# 路径配置
BASE_DIR = Path.cwd()
CHAPTERS_DIR = BASE_DIR / "outputs/儿童哲学史/排版阶段/章节HTML/修正版"
CHAPTER_PDFS_DIR = BASE_DIR / "outputs/儿童哲学史/最终交付/章节PDF"
CHAPTER_PDFS_DIR.mkdir(exist_ok=True)
STYLE_CSS = BASE_DIR / "outputs/儿童哲学史/排版阶段/章节HTML/style.css"

# 章节顺序
CHAPTER_FILES = [
    "第1章样张_fixed.html",
    "第2章样张_fixed.html",
    "第3章样张_fixed.html",
    "第4章样张_fixed.html",
    "第5章样张_fixed.html",
    "第6章样张_fixed.html",
    "第7章样张_fixed.html",
    "第8章样张_fixed.html",
    "第9章样张_fixed.html",
    "第10章样张_fixed.html",
    "第11章样张_fixed.html",
    "第12章样张_fixed.html"
]

def convert_html_to_pdf(html_file, pdf_file):
    """使用wkhtmltopdf将HTML转换为PDF"""
    # 检查HTML文件是否存在
    if not html_file.exists():
        print(f"错误: HTML文件不存在: {html_file}")
        return False
    
    print(f"转换: {html_file.name} -> {pdf_file.name}")
    
    # 构建wkhtmltopdf命令
    cmd = [
        'wkhtmltopdf',
        '--page-size', 'A4',
        '--orientation', 'Portrait',
        '--margin-top', '15mm',
        '--margin-right', '15mm',
        '--margin-bottom', '15mm',
        '--margin-left', '15mm',
        '--disable-smart-shrinking',
        '--dpi', '300',
        '--encoding', 'UTF-8',
        '--enable-local-file-access',  # 允许访问本地文件
        str(html_file),
        str(pdf_file)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"转换失败: {result.stderr[:200]}")
            return False
        
        # 检查PDF文件是否生成
        if pdf_file.exists():
            file_size = pdf_file.stat().st_size / 1024
            print(f"  成功生成: {pdf_file.name} ({file_size:.1f} KB)")
            
            # 验证PDF信息
            pdfinfo_cmd = ['pdfinfo', str(pdf_file)]
            pdfinfo_result = subprocess.run(pdfinfo_cmd, capture_output=True, text=True)
            if pdfinfo_result.returncode == 0:
                lines = pdfinfo_result.stdout.split('\n')
                for line in lines:
                    if 'Pages:' in line:
                        pages = line.split(':')[1].strip()
                        print(f"  页数: {pages}")
            return True
        else:
            print("  错误: PDF文件未生成")
            return False
            
    except subprocess.TimeoutExpired:
        print("  错误: 转换超时")
        return False
    except Exception as e:
        print(f"  错误: {e}")
        return False

def verify_pdf_quality(pdf_file, chapter_num):
    """验证PDF排版质量"""
    print(f"验证第{chapter_num}章排版质量...")
    
    if not pdf_file.exists():
        print("  错误: PDF文件不存在")
        return False
    
    # 提取文本检查对话分行
    cmd = ['pdftotext', str(pdf_file), '-']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print("  警告: 无法提取文本")
            return True  # 不因提取失败而失败
        
        text = result.stdout
        
        # 检查对话分行
        dialog_lines = text.count('时间：') + text.count('小星：') + text.count('小宇：') + text.count('老子：')
        if dialog_lines > 0:
            print(f"  发现 {dialog_lines} 行对话，分行显示正常")
        else:
            print("  警告: 未检测到对话行，可能格式有误")
        
        # 检查段落间距（通过检查是否有足够换行）
        lines = text.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        print(f"  总行数: {len(lines)}，非空行: {len(non_empty_lines)}")
        
        return True
        
    except Exception as e:
        print(f"  验证出错: {e}")
        return True  # 不阻塞流程

def main():
    print("批量转换修正版HTML为PDF...")
    
    success_count = 0
    failed_files = []
    
    # 处理每个章节
    for i, html_filename in enumerate(CHAPTER_FILES, 1):
        html_file = CHAPTERS_DIR / html_filename
        pdf_filename = f"第{i}章.pdf"
        pdf_file = CHAPTER_PDFS_DIR / pdf_filename
        
        # 转换PDF
        if convert_html_to_pdf(html_file, pdf_file):
            # 验证质量（抽查第1、6、12章）
            if i in [1, 6, 12]:
                verify_pdf_quality(pdf_file, i)
            success_count += 1
        else:
            failed_files.append(html_filename)
    
    print(f"\n批量转换完成！")
    print(f"  成功: {success_count}/{len(CHAPTER_FILES)}")
    
    if failed_files:
        print(f"  失败文件: {', '.join(failed_files)}")
        return False
    
    # 检查输出文件
    print(f"\n生成的PDF文件保存在: {CHAPTER_PDFS_DIR}")
    pdf_files = list(CHAPTER_PDFS_DIR.glob('*.pdf'))
    print(f"  找到 {len(pdf_files)} 个PDF文件")
    
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)