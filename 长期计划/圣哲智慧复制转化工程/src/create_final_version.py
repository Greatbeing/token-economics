#!/usr/bin/env python3
"""
创建最终修正版的《儿童版中国哲学史》PDF
包含排版优化和封面修复
"""

import os
import subprocess
from pathlib import Path
import PyPDF2

# 路径配置
BASE_DIR = Path.cwd()

# 输入文件
FIXED_CHAPTERS_DIR = BASE_DIR / "outputs/儿童哲学史/排版阶段/章节HTML/修正版"
COVER_HTML = BASE_DIR / "outputs/儿童哲学史/最终交付/cover_fixed.html"
TOC_HTML = BASE_DIR / "outputs/儿童哲学史/最终交付/目录页_完整版.html"
STYLE_CSS = BASE_DIR / "outputs/儿童哲学史/排版阶段/章节HTML/style.css"

# 输出目录
OUTPUT_DIR = BASE_DIR / "outputs/儿童哲学史/最终交付/最终修正版"
OUTPUT_DIR.mkdir(exist_ok=True)

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

# 完整标题（用于书签）
FULL_TITLES = [
    "第一章：世界是从哪儿来的？（老子、孔子、神话）",
    "第二章：为什么我和别人不一样？（孟子、告子、荀子）",
    "第三章：怎样才算“赢了”？（庄子、惠施、孙子）",
    "第四章：我能想做什么就做什么吗？（老子、韩非子、杨朱）",
    "第五章：什么是“好”的规则？（墨子、孟子、法家）",
    "第六章：心里害怕怎么办？（王阳明、禅宗、庄子）",
    "第七章：为什么他们那么爱自由？（嵇康、阮籍、王弼）",
    "第八章：烦恼是怎么来的？（慧能、神秀、禅宗）",
    "第九章：朱熹的\"宇宙大房子\"——理学家在做什么？",
    "第十章：王阳明的\"心里种花\"——良知在你心里",
    "第十一章：如何当一个\"现代中国人\"？（顾炎武、黄宗羲、龚自珍）",
    "第十二章：我们为什么要学哲学？（总结与展望）"
]

def check_dependencies():
    """检查必要工具"""
    tools = ['wkhtmltopdf', 'pdfinfo']
    for tool in tools:
        if subprocess.run(['which', tool], capture_output=True).returncode != 0:
            print(f"错误: 未找到 {tool}")
            return False
    print("✓ 依赖检查通过")
    return True

def check_files():
    """检查所有输入文件"""
    print("检查输入文件...")
    
    missing = []
    
    # 检查封面
    if not COVER_HTML.exists():
        missing.append(f"封面HTML: {COVER_HTML}")
    
    # 检查目录页
    if not TOC_HTML.exists():
        missing.append(f"目录HTML: {TOC_HTML}")
    
    # 检查样式表
    if not STYLE_CSS.exists():
        missing.append(f"样式表: {STYLE_CSS}")
    
    # 检查章节文件
    for chapter_file in CHAPTER_FILES:
        path = FIXED_CHAPTERS_DIR / chapter_file
        if not path.exists():
            missing.append(f"章节: {chapter_file}")
    
    if missing:
        print("错误: 以下文件不存在:")
        for m in missing:
            print(f"  - {m}")
        return False
    
    print(f"✓ 所有文件存在 (共 {len(CHAPTER_FILES)} 章)")
    return True

def create_cover_pdf(output_path):
    """创建封面PDF"""
    print("1. 生成封面PDF...")
    
    cmd = [
        'wkhtmltopdf',
        '--page-size', 'A4',
        '--margin-top', '0',
        '--margin-right', '0',
        '--margin-bottom', '0',
        '--margin-left', '0',
        '--disable-smart-shrinking',
        str(COVER_HTML),
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    
    if result.returncode != 0:
        print(f"错误: {result.stderr.decode('utf-8')}")
        return False
    
    print(f"  ✓ 封面PDF: {output_path.name}")
    return True

def create_toc_pdf(output_path):
    """创建目录页PDF"""
    print("2. 生成目录页PDF...")
    
    cmd = [
        'wkhtmltopdf',
        '--page-size', 'A4',
        '--margin-top', '20mm',
        '--margin-right', '20mm',
        '--margin-bottom', '20mm',
        '--margin-left', '20mm',
        str(TOC_HTML),
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    
    if result.returncode != 0:
        print(f"错误: {result.stderr.decode('utf-8')}")
        return False
    
    print(f"  ✓ 目录页PDF: {output_path.name}")
    return True

def create_chapter_pdf(html_file, output_path, chapter_title, chapter_num):
    """创建章节PDF"""
    print(f"  第{chapter_num}章: {chapter_title[:20]}...")
    
    # 构建命令 - 添加页眉显示章节标题
    cmd = [
        'wkhtmltopdf',
        '--page-size', 'A4',
        '--margin-top', '20mm',
        '--margin-right', '20mm', 
        '--margin-bottom', '20mm',
        '--margin-left', '20mm',
        '--header-center', chapter_title,
        '--header-font-size', '10',
        '--header-spacing', '10',
        '--footer-center', f'- {chapter_num} -',
        '--footer-font-size', '9',
        '--footer-spacing', '8',
        str(html_file),
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    
    if result.returncode != 0:
        print(f"    错误: {result.stderr.decode('utf-8')}")
        return False
    
    return True

def create_all_chapter_pdfs():
    """创建所有章节的PDF"""
    print("3. 生成章节PDF...")
    
    chapter_pdfs = []
    
    for i, chapter_file in enumerate(CHAPTER_FILES):
        chapter_num = i + 1
        
        # 输入HTML文件
        html_file = FIXED_CHAPTERS_DIR / chapter_file
        
        # 输出PDF文件
        pdf_file = OUTPUT_DIR / f"chapter_{chapter_num}.pdf"
        
        # 创建PDF
        if create_chapter_pdf(html_file, pdf_file, FULL_TITLES[i], chapter_num):
            chapter_pdfs.append(pdf_file)
            print(f"  ✓ 第{chapter_num}章完成")
        else:
            print(f"  ✗ 第{chapter_num}章失败")
    
    return chapter_pdfs

def merge_pdfs(pdf_files, output_path):
    """合并多个PDF文件"""
    print("4. 合并所有PDF文件...")
    
    merger = PyPDF2.PdfMerger()
    
    for pdf_file in pdf_files:
        if pdf_file.exists():
            print(f"  添加: {pdf_file.name}")
            merger.append(str(pdf_file))
        else:
            print(f"  警告: 文件不存在 {pdf_file}")
    
    print(f"  正在写入: {output_path.name}")
    merger.write(str(output_path))
    merger.close()
    
    print(f"✓ 合并完成")
    return True

def verify_pdf(pdf_path):
    """验证PDF文件"""
    print("5. 验证最终PDF...")
    
    if not pdf_path.exists():
        print(f"错误: 文件不存在 {pdf_path}")
        return False
    
    # 检查文件大小
    size = pdf_path.stat().st_size
    print(f"  文件大小: {size:,} 字节 ({size/1024/1024:.2f} MB)")
    
    # 检查页面数
    cmd = ['pdfinfo', str(pdf_path)]
    result = subprocess.run(cmd, capture_output=True)
    
    if result.returncode == 0:
        output = result.stdout.decode('utf-8')
        for line in output.split('\n'):
            if line.startswith('Pages:'):
                pages = line.split(':')[1].strip()
                print(f"  总页数: {pages}")
                break
    
    print(f"✓ 验证完成")
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("生成《儿童版中国哲学史》最终修正版PDF")
    print("=" * 60)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查文件
    if not check_files():
        return
    
    print("\n开始生成PDF文件...")
    
    # 1. 创建封面PDF
    cover_pdf = OUTPUT_DIR / "cover.pdf"
    if not create_cover_pdf(cover_pdf):
        return
    
    # 2. 创建目录页PDF
    toc_pdf = OUTPUT_DIR / "toc.pdf"
    if not create_toc_pdf(toc_pdf):
        return
    
    # 3. 创建所有章节PDF
    chapter_pdfs = create_all_chapter_pdfs()
    
    if len(chapter_pdfs) != len(CHAPTER_FILES):
        print(f"警告: 只成功生成 {len(chapter_pdfs)}/{len(CHAPTER_FILES)} 章")
    
    # 4. 合并所有PDF
    all_pdfs = [cover_pdf, toc_pdf] + chapter_pdfs
    final_pdf = OUTPUT_DIR / "儿童版中国哲学史_最终修正版.pdf"
    
    if not merge_pdfs(all_pdfs, final_pdf):
        return
    
    # 5. 验证最终PDF
    if not verify_pdf(final_pdf):
        return
    
    print("\n" + "=" * 60)
    print("✓ 生成完成！")
    print(f"最终文件: {final_pdf}")
    print(f"输出目录: {OUTPUT_DIR}")
    print("=" * 60)
    
    # 生成简短的修正说明
    print("\n修正内容总结:")
    print("1. 排版清晰度优化:")
    print("   - 对话内容独立成行，添加左侧边框和间距")
    print("   - 段落之间增加底部边距 (16px)")
    print("   - 小标题增加上下边距，确保视觉层次")
    print("2. 封面设计修正:")
    print("   - 图片全封面覆盖 (object-fit: cover)")
    print("   - 添加完整书名和副标题")
    print("   - 文字与背景对比明显，确保可读性")
    print("3. 技术实现:")
    print("   - 为对话行添加专门的CSS类 (.dialog-line)")
    print("   - 更新样式表确保所有特殊元素视觉区分清晰")
    print("   - 重新生成所有章节PDF并合并")

if __name__ == '__main__':
    main()