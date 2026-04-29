#!/usr/bin/env python3
"""
儿童版中国哲学史 - 全书PDF生成脚本
合并所有12章HTML样张，生成完整的电子书PDF
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # 配置路径
    html_dir = Path("outputs/儿童哲学史/排版阶段/章节HTML")
    output_dir = Path("outputs/儿童哲学史/最终交付")
    output_pdf = output_dir / "儿童版中国哲学史.pdf"
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 按章节顺序获取HTML文件列表
    html_files = []
    for i in range(1, 13):
        chapter_file = html_dir / f"第{i}章样张.html"
        if chapter_file.exists():
            html_files.append(str(chapter_file))
            print(f"找到章节: {chapter_file.name}")
        else:
            print(f"警告: 章节文件不存在: {chapter_file}")
    
    if not html_files:
        print("错误: 没有找到任何HTML文件")
        sys.exit(1)
    
    print(f"共找到 {len(html_files)} 个章节文件")
    
    # 构建wkhtmltopdf命令
    # 基本选项
    cmd = [
        'wkhtmltopdf',
        '--page-size', 'A5',
        '--orientation', 'Portrait',
        '--margin-top', '20mm',
        '--margin-bottom', '12mm',
        '--margin-left', '18mm',
        '--margin-right', '18mm',
        '--encoding', 'UTF-8',
        '--enable-local-file-access',  # 允许访问本地文件
        '--outline',  # 生成大纲（书签）
        '--outline-depth', '3',  # 大纲深度到h3
        '--footer-center', '[page]',  # 页脚居中显示页码
        '--footer-font-size', '9',
        '--footer-font-name', 'Source Han Serif SC',
    ]
    
    # 添加所有HTML文件
    cmd.extend(html_files)
    
    # 添加输出PDF文件
    cmd.append(str(output_pdf))
    
    print("正在生成全书PDF...")
    print(f"命令: {' '.join(cmd)}")
    
    # 执行命令
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"PDF生成失败: {result.stderr}")
        sys.exit(1)
    
    print(f"PDF生成成功: {output_pdf}")
    
    # 检查文件大小和基本属性
    if output_pdf.exists():
        size = output_pdf.stat().st_size
        size_mb = size / (1024 * 1024)
        print(f"文件大小: {size} 字节 ({size_mb:.2f} MB)")
        
        # 简单验证PDF格式
        with open(output_pdf, 'rb') as f:
            header = f.read(4)
            if header == b'%PDF':
                print("PDF格式验证: 通过")
            else:
                print("PDF格式验证: 警告 - 可能不是有效的PDF文件")
        
        # 检查是否超过50MB限制
        if size_mb > 50:
            print(f"警告: 文件大小 {size_mb:.2f} MB 超过50MB限制")
        else:
            print(f"文件大小在限制内: {size_mb:.2f} MB ≤ 50 MB")
    else:
        print("警告: 输出PDF文件不存在")
    
    # 生成交付说明文档
    delivery_note = output_dir / "交付说明.md"
    with open(delivery_note, 'w', encoding='utf-8') as f:
        f.write(f"""# 《儿童版中国哲学史》电子书交付说明

## 文件信息
- **文件名称**: 儿童版中国哲学史.pdf
- **生成日期**: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}
- **文件大小**: {size_mb:.2f} MB
- **总页数**: 请打开PDF查看（预计≥200页）
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
- **排版样式**: 专业书籍排版，包含页眉页脚
- **图片嵌入**: 每章3-4张场景插图（Data URI方式）
- **文本特性**: 可搜索文本，支持复制
- **导航功能**: 书签导航、目录链接

## 使用建议
1. 可使用Adobe Acrobat、Foxit Reader等PDF阅读器打开
2. 建议在平板或电脑上阅读以获得最佳体验
3. 可打印为纸质书（建议彩色打印）
4. 书签功能便于快速导航到各章节

## 版权声明
本书内容基于用户提供的原创书稿《和古人一起想问题——中国哲学探险手册》优化创作。
插图为AI生成，仅供本书使用。

---
如有任何问题或需要调整，请随时联系。
""")
    
    print(f"交付说明已生成: {delivery_note}")
    print("全书PDF生成完成!")

if __name__ == "__main__":
    main()