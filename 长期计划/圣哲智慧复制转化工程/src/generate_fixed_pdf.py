#!/usr/bin/env python3
"""
生成修正后的PDF，解决排版清晰度和封面问题
"""

import os
import subprocess
import tempfile
from pathlib import Path
import PyPDF2

# 路径配置
BASE_DIR = Path.cwd()
INPUT_MD_DIR = BASE_DIR / "outputs/儿童哲学史/排版阶段/优化后Markdown"
COVER_JPG = BASE_DIR / "outputs/儿童哲学史/最终交付/封面设计.jpg"
OUTPUT_DIR = BASE_DIR / "outputs/儿童哲学史/最终交付/修正版"
OUTPUT_DIR.mkdir(exist_ok=True)

# 章节文件列表（按顺序）
CHAPTER_FILES = [
    "第一章优化稿.md",
    "第二章优化稿.md",
    "第三章优化稿.md",
    "第四章优化稿.md",
    "第五章优化稿.md",
    "第六章优化稿.md",
    "第七章优化稿.md",
    "第八章优化稿.md",
    "第九章优化稿.md",
    "第十章优化稿.md",
    "第十一章优化稿.md",
    "第十二章优化稿.md"
]

# 完整原始标题（用于书签）
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
    tools = ['wkhtmltopdf', 'pdfinfo', 'pandoc']
    for tool in tools:
        if subprocess.run(['which', tool], capture_output=True).returncode != 0:
            print(f"错误: 未找到 {tool}")
            return False
    print("✓ 依赖检查通过")
    return True

def create_dialog_css():
    """创建对话专用的CSS样式"""
    return """
/* 对话样式 - 确保分行清晰 */
.dialog-line {
    margin-bottom: 16px;
    padding-left: 20px;
    border-left: 3px solid #81D4FA;
    line-height: 1.6;
}

.dialog-role {
    font-weight: bold;
    color: #1565C0;
    display: inline-block;
    min-width: 60px;
}

/* 确保段落之间有足够间距 */
p {
    margin-bottom: 16px !important;
    text-indent: 2em;
}

/* 对话段落特殊处理 */
p strong:first-child {
    color: #1565C0;
}

/* 思想剧场内的对话 */
.thought-theater .dialog-line {
    margin-bottom: 12px;
    padding-left: 15px;
    border-left-color: #FFCC80;
}

.thought-theater .dialog-role {
    color: #FF9800;
}

/* 小标题分行 */
h3, h4, h5, h6 {
    margin-top: 24px !important;
    margin-bottom: 12px !important;
    page-break-after: avoid;
}

/* 特殊元素视觉区分 */
.thought-theater, .think-about, .ancient-say, .global-telescope, .practice-exercise {
    margin-top: 25px !important;
    margin-bottom: 25px !important;
}
"""

def convert_markdown_to_html(md_file, html_file, chapter_num):
    """将Markdown转换为HTML，并应用对话优化"""
    print(f"  转换第{chapter_num}章")
    
    # 读取Markdown内容
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 预处理对话：确保每个对话行都是独立段落
    lines = md_content.split('\n')
    processed_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 检测对话行：**角色**：（内容）
        if re.match(r'^\*\*.*?\*\*：', stripped):
            # 确保前面有空行（如果不是第一个元素且前一行不是空行）
            if i > 0 and processed_lines and processed_lines[-1].strip() != '':
                processed_lines.append('')
            
            # 添加对话行
            # 将 **角色**： 转换为 <strong>角色</strong>：
            # 并包装在div中
            processed_line = re.sub(r'\*\*(.*?)\*\*：', r'<div class="dialog-line"><span class="dialog-role">\1</span>：', stripped)
            processed_line += '</div>'
            processed_lines.append(processed_line)
            
            # 确保后面有空行
            if i < len(lines) - 1 and lines[i+1].strip() != '':
                processed_lines.append('')
        else:
            processed_lines.append(line)
    
    # 重新组合
    processed_md = '\n'.join(processed_lines)
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
        tmp.write(processed_md)
        tmp_path = tmp.name
    
    try:
        # 使用pandoc转换，添加CSS
        css_content = create_dialog_css()
        
        # 构建pandoc命令
        cmd = [
            'pandoc',
            tmp_path,
            '-f', 'markdown',
            '-t', 'html5',
            '--self-contained',
            '--css', '-',  # 从标准输入读取CSS
            '-o', str(html_file)
        ]
        
        # 运行pandoc，传递CSS
        result = subprocess.run(cmd, input=css_content.encode('utf-8'), 
                              capture_output=True)
        
        if result.returncode != 0:
            print(f"    pandoc错误: {result.stderr.decode('utf-8')}")
            return False
            
        print(f"    ✓ 已生成: {html_file.name}")
        return True
        
    finally:
        # 清理临时文件
        os.unlink(tmp_path)

def create_cover_pdf(output_path):
    """创建封面PDF"""
    print("创建封面...")
    
    # 使用现有的修正封面HTML
    cover_html = BASE_DIR / "outputs/儿童哲学史/最终交付/cover_fixed.html"
    
    if not cover_html.exists():
        print("错误: 封面HTML不存在")
        return False
    
    # 使用wkhtmltopdf转换
    cmd = [
        'wkhtmltopdf',
        '--page-size', 'A4',
        '--margin-top', '0',
        '--margin-right', '0',
        '--margin-bottom', '0',
        '--margin-left', '0',
        '--disable-smart-shrinking',
        str(cover_html),
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    
    if result.returncode != 0:
        print(f"封面生成错误: {result.stderr.decode('utf-8')}")
        return False
    
    print("  ✓ 封面已生成")
    return True

def create_toc_pdf(output_path):
    """创建目录页PDF"""
    print("创建目录页...")
    
    # 使用现有的完整目录HTML
    toc_html = BASE_DIR / "outputs/儿童哲学史/最终交付/目录页_完整版.html"
    
    if not toc_html.exists():
        print("错误: 目录HTML不存在")
        return False
    
    cmd = [
        'wkhtmltopdf',
        '--page-size', 'A4',
        '--margin-top', '20mm',
        '--margin-right', '20mm',
        '--margin-bottom', '20mm',
        '--margin-left', '20mm',
        str(toc_html),
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    
    if result.returncode != 0:
        print(f"目录页生成错误: {result.stderr.decode('utf-8')}")
        return False
    
    print("  ✓ 目录页已生成")
    return True

def convert_html_to_pdf(html_file, pdf_file, chapter_title):
    """将HTML转换为PDF"""
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
        str(html_file),
        str(pdf_file)
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    
    if result.returncode != 0:
        print(f"    PDF生成错误: {result.stderr.decode('utf-8')}")
        return False
    
    return True

def merge_pdfs(pdf_files, output_path):
    """合并多个PDF文件"""
    print("合并PDF文件...")
    
    merger = PyPDF2.PdfMerger()
    
    for pdf_file in pdf_files:
        if pdf_file.exists():
            merger.append(str(pdf_file))
    
    merger.write(str(output_path))
    merger.close()
    
    print(f"✓ 合并完成: {output_path.name}")
    return True

def main():
    """主函数"""
    print("开始生成修正版PDF...")
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查输入文件
    missing = []
    for chapter_file in CHAPTER_FILES:
        path = INPUT_MD_DIR / chapter_file
        if not path.exists():
            missing.append(path)
    
    if missing:
        print("错误: 以下文件不存在:")
        for m in missing:
            print(f"  - {m}")
        return
    
    print(f"✓ 所有输入文件存在")
    
    # 创建封面PDF
    cover_pdf = OUTPUT_DIR / "cover.pdf"
    if not create_cover_pdf(cover_pdf):
        print("封面生成失败")
        return
    
    # 创建目录页PDF
    toc_pdf = OUTPUT_DIR / "toc.pdf"
    if not create_toc_pdf(toc_pdf):
        print("目录页生成失败")
        return
    
    # 转换各章节
    chapter_pdfs = []
    
    for i, chapter_file in enumerate(CHAPTER_FILES):
        chapter_num = i + 1
        
        print(f"处理第{chapter_num}章...")
        
        # 输入文件
        md_file = INPUT_MD_DIR / chapter_file
        
        # 输出HTML文件
        html_file = OUTPUT_DIR / f"chapter_{chapter_num}.html"
        
        # 转换Markdown到HTML
        if not convert_markdown_to_html(md_file, html_file, chapter_num):
            print(f"第{chapter_num}章转换失败")
            continue
        
        # 转换HTML到PDF
        pdf_file = OUTPUT_DIR / f"chapter_{chapter_num}.pdf"
        if not convert_html_to_pdf(html_file, pdf_file, FULL_TITLES[i]):
            print(f"第{chapter_num}章PDF生成失败")
            continue
        
        chapter_pdfs.append(pdf_file)
        print(f"✓ 第{chapter_num}章完成")
    
    # 合并所有PDF
    all_pdfs = [cover_pdf, toc_pdf] + chapter_pdfs
    final_pdf = OUTPUT_DIR / "儿童版中国哲学史_修正排版.pdf"
    
    if not merge_pdfs(all_pdfs, final_pdf):
        print("合并失败")
        return
    
    # 验证结果
    print(f"\n修正版PDF已生成:")
    print(f"  {final_pdf}")
    print(f"  总文件数: {len(all_pdfs)}")
    
    # 检查文件大小
    if final_pdf.exists():
        size = final_pdf.stat().st_size
        print(f"  文件大小: {size:,} 字节 ({size/1024/1024:.2f} MB)")
    
    print("\n✓ 修正完成！")

if __name__ == '__main__':
    import re
    main()