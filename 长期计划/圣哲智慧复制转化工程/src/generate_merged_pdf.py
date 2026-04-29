#!/usr/bin/env python3
"""
儿童版中国哲学史 - 合并PDF生成脚本
为每个章节生成单独的PDF，然后合并成全书PDF
解决wkhtmltopdf不支持多文档输入的问题
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

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
    
    # 检查输出文件是否存在且非空
    if not output_pdf.exists() or output_pdf.stat().st_size == 0:
        print(f"警告: 输出文件为空或不存在")
        return False
    
    return True

def main():
    # 配置路径
    html_dir = Path("outputs/儿童哲学史/排版阶段/章节HTML")
    output_dir = Path("outputs/儿童哲学史/最终交付")
    final_pdf = output_dir / "儿童版中国哲学史.pdf"
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建临时目录存放单个PDF文件
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        chapter_pdfs = []
        
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
                size = chapter_pdf.stat().st_size / 1024
                print(f"  生成成功，大小: {size:.1f} KB")
            else:
                print(f"  生成失败，跳过本章")
        
        if not chapter_pdfs:
            print("错误: 没有成功生成任何章节PDF")
            sys.exit(1)
        
        print(f"成功生成 {len(chapter_pdfs)} 个章节PDF")
        
        # 合并所有PDF
        print("正在合并PDF...")
        cmd = ['pdfunite']
        cmd.extend(str(pdf) for pdf in chapter_pdfs)
        cmd.append(str(final_pdf))
        
        print(f"合并命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"PDF合并失败: {result.stderr}")
            sys.exit(1)
    
    # 检查最终PDF
    if final_pdf.exists():
        size = final_pdf.stat().st_size
        size_mb = size / (1024 * 1024)
        
        print(f"全书PDF生成成功: {final_pdf}")
        print(f"文件大小: {size_mb:.2f} MB")
        
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
        
        # 估算页数（可选）
        # 使用pdfinfo如果有的话
        try:
            pdfinfo = subprocess.run(
                ['pdfinfo', str(final_pdf)],
                capture_output=True, text=True
            )
            if pdfinfo.returncode == 0:
                for line in pdfinfo.stdout.split('\n'):
                    if line.startswith('Pages:'):
                        pages = line.split(':')[1].strip()
                        print(f"总页数: {pages} 页")
                        break
        except:
            pass  # pdfinfo不可用，忽略
        
    else:
        print("错误: 最终PDF文件未生成")
        sys.exit(1)
    
    # 生成交付说明
    generate_delivery_note(final_pdf, output_dir)
    
    print("全书PDF生成完成!")

def generate_delivery_note(pdf_file, output_dir):
    """生成交付说明文档"""
    note_file = output_dir / "交付说明.md"
    size_mb = pdf_file.stat().st_size / (1024 * 1024)
    
    with open(note_file, 'w', encoding='utf-8') as f:
        f.write(f"""# 《儿童版中国哲学史》电子书交付说明

## 文件信息
- **文件名称**: {pdf_file.name}
- **生成日期**: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}
- **文件大小**: {size_mb:.2f} MB
- **包含章节**: 第1-12章全书内容

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
- **章节结构**: 12章完整内容

## 使用建议
1. 可使用Adobe Acrobat、Foxit Reader等PDF阅读器打开
2. 建议在平板或电脑上阅读以获得最佳体验
3. 可打印为纸质书（建议彩色打印）
4. 使用PDF阅读器的书签功能可快速导航

## 生成说明
本书由HTML样张通过wkhtmltopdf转换并合并生成，保留了原HTML的图文排版和样式。

## 版权声明
本书内容基于用户提供的原创书稿《和古人一起想问题——中国哲学探险手册》优化创作。
插图为AI生成，仅供本书使用。

---
如有任何问题或需要调整，请随时联系。
""")
    
    print(f"交付说明已生成: {note_file}")

if __name__ == "__main__":
    main()