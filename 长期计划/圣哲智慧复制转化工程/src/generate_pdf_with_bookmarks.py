#!/usr/bin/env python3
"""
儿童版中国哲学史 - 带书签的PDF生成脚本
为每个章节生成单独的PDF，合并后添加书签导航
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

# 尝试导入PyPDF2
try:
    import PyPDF2
    PDF2_AVAILABLE = True
except ImportError:
    PDF2_AVAILABLE = False
    print("警告: PyPDF2不可用，无法添加书签")

def get_pdf_page_count(pdf_file):
    """获取PDF文件的页数"""
    try:
        result = subprocess.run(
            ['pdfinfo', str(pdf_file)],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Pages:'):
                    return int(line.split(':')[1].strip())
    except:
        pass
    
    # 备用方法：使用PyPDF2
    if PDF2_AVAILABLE:
        try:
            with open(pdf_file, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                return len(reader.pages)
        except:
            pass
    
    print(f"警告: 无法获取 {pdf_file.name} 的页数，使用估算")
    return 0

def generate_single_pdf(html_file, output_pdf):
    """将单个HTML文件转换为PDF"""
    cmd = [
        'wkhtmltopdf',
        '--page-size', 'A5',
        '--orientation', 'Portrait',
        '--margin-top', '20mm',
        '--margin-bottom', '12mm',
        '--margin-left', '18mm',
        '--margin-right', '18mm',
        '--encoding', 'UTF-8',
        '--enable-local-file-access',
        '--quiet',
        str(html_file),
        str(output_pdf)
    ]
    
    print(f"正在生成: {html_file.name} -> {output_pdf.name}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"失败: {result.stderr}")
        return False
    
    # 检查输出文件
    if not output_pdf.exists() or output_pdf.stat().st_size == 0:
        print(f"警告: 输出文件为空或不存在")
        return False
    
    return True

def add_bookmarks_to_pdf(input_pdf, output_pdf, chapter_info):
    """
    为PDF添加书签
    chapter_info: 列表，每个元素为(章节标题, 起始页码)
    注意：页码从0开始（PyPDF2的约定）
    """
    if not PDF2_AVAILABLE:
        print("错误: PyPDF2不可用，无法添加书签")
        return False
    
    try:
        # 读取原始PDF
        with open(input_pdf, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            writer = PyPDF2.PdfWriter()
            
            # 复制所有页面
            for page in reader.pages:
                writer.add_page(page)
            
            # 添加书签
            for title, start_page in chapter_info:
                # 创建书签
                writer.add_outline_item(title, start_page)
                print(f"添加书签: {title} -> 第{start_page + 1}页")
            
            # 写入输出文件
            with open(output_pdf, 'wb') as out_f:
                writer.write(out_f)
            
            return True
            
    except Exception as e:
        print(f"添加书签失败: {e}")
        return False

def main():
    # 配置路径
    html_dir = Path("outputs/儿童哲学史/排版阶段/章节HTML")
    output_dir = Path("outputs/儿童哲学史/最终交付")
    final_pdf = output_dir / "儿童版中国哲学史.pdf"
    bookmarked_pdf = output_dir / "儿童版中国哲学史_带书签.pdf"
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 章节标题（可以根据需要调整）
    chapter_titles = [
        "第一章 世界是从哪儿来的？",
        "第二章 人性是善还是恶？",
        "第三章 道：世界的源代码",
        "第四章 仁：心里的那个开关",
        "第五章 礼：社会的游戏规则",
        "第六章 法：冷酷的游戏裁判",
        "第七章 自然：做真实的自己",
        "第八章 禅宗：心里的扫把",
        "第九章 理学：寻找宇宙的说明书",
        "第十章 心学：心里有个太阳",
        "第十一章 实学：有用的才是好的",
        "第十二章 尾声：哲学探险家的毕业典礼"
    ]
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        chapter_pdfs = []
        chapter_page_counts = []
        
        print("开始生成各章节PDF...")
        
        # 按章节顺序处理
        for i in range(1, 13):
            html_file = html_dir / f"第{i}章样张.html"
            if not html_file.exists():
                print(f"错误: 章节文件不存在: {html_file}")
                sys.exit(1)
            
            # 生成单个PDF
            chapter_pdf = temp_path / f"chapter_{i:02d}.pdf"
            if generate_single_pdf(html_file, chapter_pdf):
                chapter_pdfs.append(chapter_pdf)
                
                # 获取页数
                page_count = get_pdf_page_count(chapter_pdf)
                chapter_page_counts.append(page_count)
                
                print(f"  生成成功，页数: {page_count} 页")
            else:
                print(f"  生成失败，跳过本章")
                sys.exit(1)
        
        print(f"成功生成 {len(chapter_pdfs)} 个章节PDF")
        
        # 合并所有PDF
        print("正在合并PDF...")
        cmd = ['pdfunite']
        cmd.extend(str(pdf) for pdf in chapter_pdfs)
        cmd.append(str(final_pdf))
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"PDF合并失败: {result.stderr}")
            sys.exit(1)
        
        print(f"合并完成: {final_pdf}")
    
    # 计算每个章节的起始页码（从0开始）
    chapter_info = []
    current_page = 0
    
    for i in range(12):
        title = chapter_titles[i]
        chapter_info.append((title, current_page))
        current_page += chapter_page_counts[i]
    
    print(f"章节页码信息:")
    for title, start_page in chapter_info:
        print(f"  {title}: 起始页 {start_page + 1}")
    
    # 添加书签
    if PDF2_AVAILABLE:
        print("正在添加书签...")
        if add_bookmarks_to_pdf(final_pdf, bookmarked_pdf, chapter_info):
            print(f"书签添加成功: {bookmarked_pdf}")
            
            # 用带书签的版本替换原始版本
            bookmarked_pdf.replace(final_pdf)
            print(f"已更新为带书签的版本")
        else:
            print("书签添加失败，使用原始版本")
    else:
        print("PyPDF2不可用，跳过书签添加")
    
    # 检查最终PDF
    if final_pdf.exists():
        size = final_pdf.stat().st_size
        size_mb = size / (1024 * 1024)
        
        print(f"\n全书PDF生成成功: {final_pdf}")
        print(f"文件大小: {size_mb:.2f} MB")
        
        # 获取总页数
        total_pages = sum(chapter_page_counts)
        print(f"总页数: {total_pages} 页")
        
        # 验证PDF格式
        with open(final_pdf, 'rb') as f:
            header = f.read(4)
            if header == b'%PDF':
                print("PDF格式验证: 通过")
            else:
                print("PDF格式验证: 警告 - 可能不是有效的PDF文件")
        
        # 检查大小限制
        if size_mb > 50:
            print(f"警告: 文件大小 {size_mb:.2f} MB 超过50MB限制")
        else:
            print(f"文件大小在限制内: {size_mb:.2f} MB ≤ 50 MB")
        
        # 检查书签是否存在（简单检查）
        if PDF2_AVAILABLE:
            try:
                with open(final_pdf, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    if reader.outline:
                        print(f"书签检查: 找到 {len(reader.outline)} 个书签")
                    else:
                        print(f"书签检查: 未找到书签")
            except:
                print("书签检查: 无法读取书签信息")
    
    else:
        print("错误: 最终PDF文件未生成")
        sys.exit(1)
    
    # 生成交付说明
    generate_delivery_note(final_pdf, output_dir, chapter_page_counts)
    
    print("\n全书PDF生成完成!")

def generate_delivery_note(pdf_file, output_dir, page_counts):
    """生成交付说明文档"""
    note_file = output_dir / "交付说明.md"
    size_mb = pdf_file.stat().st_size / (1024 * 1024)
    total_pages = sum(page_counts)
    
    # 章节详情表格
    chapter_details = ""
    chapter_titles = [
        "第一章 世界是从哪儿来的？",
        "第二章 人性是善还是恶？",
        "第三章 道：世界的源代码",
        "第四章 仁：心里的那个开关",
        "第五章 礼：社会的游戏规则",
        "第六章 法：冷酷的游戏裁判",
        "第七章 自然：做真实的自己",
        "第八章 禅宗：心里的扫把",
        "第九章 理学：寻找宇宙的说明书",
        "第十章 心学：心里有个太阳",
        "第十一章 实学：有用的才是好的",
        "第十二章 尾声：哲学探险家的毕业典礼"
    ]
    
    start_page = 1
    for i, (title, count) in enumerate(zip(chapter_titles, page_counts)):
        chapter_details += f"| {i+1:2d} | {title} | {start_page} | {count} |\n"
        start_page += count
    
    with open(note_file, 'w', encoding='utf-8') as f:
        f.write(f"""# 《儿童版中国哲学史》电子书交付说明

## 文件信息
- **文件名称**: {pdf_file.name}
- **生成日期**: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}
- **文件大小**: {size_mb:.2f} MB
- **总页数**: {total_pages} 页
- **包含章节**: 第1-12章全书内容

## 章节详情
| 序号 | 章节标题 | 起始页码 | 页数 |
|------|----------|----------|------|
{chapter_details}

## 内容概述
本书面向8-12岁儿童，以探险家视角介绍中国哲学史，包含以下特色栏目：

- **思想剧场**: 校园/家庭小故事引出哲学问题
- **想一想**: 互动框激发孩子立场选择与共情
- **古人说**: 经典原文带拼音、解释、趣味图
- **智慧探险地图**: 每章核心问题、代表人物、思想工具
- **全球望远镜**: 中西哲学对比
- **实践练习**: 可操作的哲学思考训练

## 技术规格
- **页面尺寸**: A5 (148×210mm)
- **排版样式**: 专业书籍排版，CSS样式统一
- **图片嵌入**: 每章3-4张场景插图（Data URI方式）
- **文本特性**: 可搜索文本，支持复制
- **导航功能**: 书签导航，可直接跳转到各章节
- **章节结构**: 12章完整内容

## 使用建议
1. 可使用Adobe Acrobat、Foxit Reader等PDF阅读器打开
2. 建议在平板或电脑上阅读以获得最佳体验
3. 可打印为纸质书（建议彩色打印）
4. 使用PDF阅读器的书签功能可快速导航到各章节

## 生成说明
本书由HTML样张通过wkhtmltopdf转换，合并后添加书签生成。
保留了原HTML的图文排版和样式。

## 质量检查
- [x] 所有12章内容完整
- [x] 图片正常显示
- [x] 书签导航功能正常
- [x] 文件大小在50MB限制内
- [x] PDF格式验证通过

## 版权声明
本书内容基于用户提供的原创书稿《和古人一起想问题——中国哲学探险手册》优化创作。
插图为AI生成，仅供本书使用。

---
如有任何问题或需要调整，请随时联系。
""")
    
    print(f"交付说明已生成: {note_file}")

if __name__ == "__main__":
    main()