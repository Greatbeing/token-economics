#!/usr/bin/env python3
"""
合并封面、目录页和12章PDF为完整的最终电子书
添加书签导航
"""

import PyPDF2
from pathlib import Path

# 路径配置
BASE_DIR = Path.cwd()

# 输入文件
COVER_PDF = BASE_DIR / "outputs/儿童哲学史/最终交付/cover_final.pdf"
TOC_PDF = BASE_DIR / "outputs/儿童哲学史/最终交付/目录页.pdf"
CHAPTERS_DIR = BASE_DIR / "outputs/儿童哲学史/最终交付/章节PDF"

# 输出文件
FINAL_PDF = BASE_DIR / "outputs/儿童哲学史/最终交付/儿童版中国哲学史_最终修正版.pdf"

# 完整标题（用于书签） - 必须与原始目录完全一致
FULL_TITLES = [
    "第一章：世界是从哪儿来的？（老子、孔子、神话）",
    "第二章：为什么我和别人不一样？（孟子、告子、荀子）",
    "第三章：怎样才算“赢了”？（庄子、惠施、孙子）",
    "第四章：我能想做什么就做什么吗？（老子、韩非子、杨朱）",
    "第五章：什么是“好”的规则？（墨子、孟子、法家）",
    "第六章：心里害怕怎么办？（王阳明、禅宗、庄子）",
    "第七章：为什么他们那么爱自由？（嵇康、阮籍、王弼）",
    "第八章：烦恼是怎么来的？（慧能、神秀、禅宗）",
    "第九章：朱熹的“宇宙大房子”——理学家在做什么？",
    "第十章：王阳明的“心里种花”——良知在你心里",
    "第十一章：如何当一个“现代中国人”？（顾炎武、黄宗羲、龚自珍）",
    "第十二章：我们为什么要学哲学？"
]

# 章节PDF文件列表（按顺序）
CHAPTER_FILES = [
    CHAPTERS_DIR / "第1章.pdf",
    CHAPTERS_DIR / "第2章.pdf",
    CHAPTERS_DIR / "第3章.pdf",
    CHAPTERS_DIR / "第4章.pdf",
    CHAPTERS_DIR / "第5章.pdf",
    CHAPTERS_DIR / "第6章.pdf",
    CHAPTERS_DIR / "第7章.pdf",
    CHAPTERS_DIR / "第8章.pdf",
    CHAPTERS_DIR / "第9章.pdf",
    CHAPTERS_DIR / "第10章.pdf",
    CHAPTERS_DIR / "第11章.pdf",
    CHAPTERS_DIR / "第12章.pdf"
]

def validate_files():
    """验证所有输入文件是否存在"""
    missing_files = []
    
    if not COVER_PDF.exists():
        missing_files.append(f"封面PDF: {COVER_PDF}")
    
    if not TOC_PDF.exists():
        missing_files.append(f"目录页PDF: {TOC_PDF}")
    
    for i, chapter_file in enumerate(CHAPTER_FILES, 1):
        if not chapter_file.exists():
            missing_files.append(f"第{i}章PDF: {chapter_file}")
    
    if missing_files:
        print("错误: 以下文件缺失:")
        for f in missing_files:
            print(f"  - {f}")
        return False
    
    print("所有输入文件验证通过")
    return True

def merge_pdfs_with_bookmarks():
    """合并PDF并添加书签"""
    print("开始合并PDF文件...")
    
    # 创建PDF写入器
    writer = PyPDF2.PdfWriter()
    
    # 添加封面
    print(f"添加封面: {COVER_PDF.name}")
    cover_reader = PyPDF2.PdfReader(str(COVER_PDF))
    writer.append(cover_reader)
    
    # 封面书签
    cover_bookmark = writer.add_outline_item("封面", 0)
    
    # 添加目录页
    print(f"添加目录页: {TOC_PDF.name}")
    toc_reader = PyPDF2.PdfReader(str(TOC_PDF))
    toc_start_page = len(writer.pages)
    writer.append(toc_reader)
    
    # 目录书签
    toc_bookmark = writer.add_outline_item("完整目录", toc_start_page)
    
    # 添加各章节并创建书签
    for i, (chapter_file, title) in enumerate(zip(CHAPTER_FILES, FULL_TITLES)):
        print(f"添加{title}")
        
        # 读取章节PDF
        chapter_reader = PyPDF2.PdfReader(str(chapter_file))
        
        # 记录章节开始页面
        chapter_start_page = len(writer.pages)
        
        # 添加章节所有页面
        writer.append(chapter_reader)
        
        # 添加章节书签
        writer.add_outline_item(title, chapter_start_page, parent=toc_bookmark)
        
        # 输出章节页数信息
        chapter_pages = len(chapter_reader.pages)
        print(f"  页数: {chapter_pages} (从PDF第{chapter_start_page + 1}页开始)")
    
    # 写入最终PDF文件
    print(f"\n写入最终PDF文件: {FINAL_PDF}")
    with open(FINAL_PDF, 'wb') as f:
        writer.write(f)
    
    # 验证输出文件
    if FINAL_PDF.exists():
        final_reader = PyPDF2.PdfReader(str(FINAL_PDF))
        total_pages = len(final_reader.pages)
        file_size = FINAL_PDF.stat().st_size / 1024
        
        print(f"\n合并完成!")
        print(f"  总页数: {total_pages}")
        print(f"  文件大小: {file_size:.1f} KB")
        print(f"  输出路径: {FINAL_PDF}")
        
        # 检查书签数量
        if hasattr(final_reader, 'outline') and final_reader.outline:
            bookmark_count = len(final_reader.outline)
            print(f"  书签数量: {bookmark_count}")
        else:
            print(f"  警告: 未检测到书签")
        
        return True
    else:
        print("错误: 最终PDF文件未生成")
        return False

def verify_pdf_completeness():
    """验证PDF完整性"""
    print("\n验证最终PDF完整性...")
    
    if not FINAL_PDF.exists():
        print("错误: 最终PDF文件不存在")
        return False
    
    try:
        reader = PyPDF2.PdfReader(str(FINAL_PDF))
        total_pages = len(reader.pages)
        
        # 检查页数是否足够（封面+目录+12章）
        if total_pages < 70:
            print(f"警告: 总页数较少 ({total_pages}页)，可能缺少内容")
        else:
            print(f"页数检查通过: {total_pages}页")
        
        # 检查可搜索文本
        if reader.metadata:
            print(f"元数据: {reader.metadata.get('/Title', '无标题')}")
        
        # 尝试提取第一页文本
        if total_pages > 0:
            first_page = reader.pages[0]
            text = first_page.extract_text()
            if text and len(text.strip()) > 0:
                print("文本可提取: 是")
            else:
                print("警告: 第一页无文本内容")
        
        # 检查目录页是否包含完整标题
        if total_pages > 1:
            toc_page = reader.pages[1]  # 假设目录页是第二页
            toc_text = toc_page.extract_text()
            
            # 检查是否包含关键标题
            check_titles = ["第一章", "第二章", "第三章", "世界是从哪儿来的", "为什么我和别人不一样"]
            found_count = 0
            for check in check_titles:
                if check in toc_text:
                    found_count += 1
            
            if found_count >= 3:
                print("目录内容检查: 通过")
            else:
                print("警告: 目录页可能缺少关键标题")
        
        return True
        
    except Exception as e:
        print(f"验证出错: {e}")
        return False

def main():
    print("合并封面、目录和12章PDF为完整电子书")
    print("=" * 60)
    
    # 验证文件
    if not validate_files():
        return False
    
    # 合并PDF
    if not merge_pdfs_with_bookmarks():
        return False
    
    # 验证完整性
    verify_pdf_completeness()
    
    print("\n最终电子书生成完成!")
    print(f"文件位置: {FINAL_PDF}")
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)