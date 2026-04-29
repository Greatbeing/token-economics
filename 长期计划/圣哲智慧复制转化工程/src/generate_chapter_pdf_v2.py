#!/usr/bin/env python3
"""
儿童版中国哲学史 - 章节PDF生成脚本
基于排版规划方案，将Markdown章节转换为PDF样张
使用pandoc转换为HTML，再用wkhtmltopdf生成PDF
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

# 配置参数
class Config:
    # 页面尺寸
    PAGE_WIDTH_MM = 148
    PAGE_HEIGHT_MM = 210
    
    # 字体（后备方案）
    BODY_FONT = "'Source Han Serif SC', 'SimSun', serif"
    HEADING_FONT = "'FZXiaoBiaoSong-B05S', 'FangSong', sans-serif"
    
    # 颜色（来自色彩规范）
    COLOR_PRIMARY = "#FFB74D"  # 哲学琥珀
    COLOR_SECONDARY = "#81D4FA"  # 思考浅蓝
    COLOR_BACKGROUND = "#FFF8E1"  # 书卷米白
    COLOR_ACCENT_BLUE = "#1565C0"  # 智慧深蓝
    COLOR_ACCENT_BROWN = "#5D4037"  # 历史深棕
    COLOR_ACCENT_YELLOW = "#FFF176"  # 互动亮黄
    
    # 路径
    OUTPUT_DIR = Path("outputs/儿童哲学史/排版阶段/样张")
    TEMPLATE_DIR = Path("src/templates")
    IMAGE_DIR = Path("data/illustration_references/草图源文件")

def ensure_dir(path):
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)

def read_markdown_file(file_path):
    """读取Markdown文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_css(config):
    """生成CSS样式"""
    css = f"""
/* 儿童版中国哲学史 - 排版样式 */
/* 基于排版规划方案 v1.0 */

@page {{
    size: {config.PAGE_WIDTH_MM}mm {config.PAGE_HEIGHT_MM}mm;
    margin: 20mm 18mm 12mm 18mm; /* 天头 20mm, 订口 18mm, 地脚 12mm, 切口 18mm */
}}

body {{
    font-family: {config.BODY_FONT};
    font-size: 13pt; /* 小4号 */
    line-height: 1.5;
    color: #333333;
    background-color: white;
    margin: 0;
    padding: 0;
}}

/* 标题系统 */
h1 {{
    font-family: {config.HEADING_FONT};
    font-size: 24pt;
    color: {config.COLOR_PRIMARY};
    margin-top: 30pt;
    margin-bottom: 20pt;
    text-align: center;
    page-break-before: always;
}}

h2 {{
    font-family: {config.HEADING_FONT};
    font-size: 18pt;
    color: {config.COLOR_ACCENT_BLUE};
    margin-top: 24pt;
    margin-bottom: 16pt;
    border-bottom: 2px solid {config.COLOR_SECONDARY};
    padding-bottom: 4pt;
}}

h3 {{
    font-family: {config.BODY_FONT};
    font-size: 15pt;
    font-weight: bold;
    color: {config.COLOR_ACCENT_BROWN};
    margin-top: 18pt;
    margin-bottom: 12pt;
}}

h4 {{
    font-family: {config.BODY_FONT};
    font-size: 13pt;
    font-weight: bold;
    color: #333333;
    margin-top: 12pt;
    margin-bottom: 8pt;
}}

/* 段落 */
p {{
    text-align: justify;
    text-indent: 2em;
    margin-top: 6pt;
    margin-bottom: 6pt;
}}

/* 特殊元素 */
.thought-theater {{
    background-color: {config.COLOR_BACKGROUND};
    border: 1px dashed #FFCC80;
    border-left: 4px solid #FFCC80;
    padding: 12pt;
    margin: 16pt 0;
    page-break-inside: avoid;
}}

.think-about {{
    background-color: #E1F5FE;
    border: 2px solid {config.COLOR_SECONDARY};
    border-left: 6px solid {config.COLOR_SECONDARY};
    padding: 12pt;
    margin: 16pt 0;
    page-break-inside: avoid;
}}

.ancient-say {{
    background-color: #F5F5F5;
    border-left: 4px solid {config.COLOR_ACCENT_BLUE};
    padding: 12pt;
    margin: 16pt 0;
}}

.ancient-say .original {{
    font-family: {config.BODY_FONT};
    font-size: 14pt;
    font-weight: bold;
    color: {config.COLOR_ACCENT_BLUE};
    margin-bottom: 8pt;
}}

.ancient-say .pinyin {{
    font-family: Arial, sans-serif;
    font-size: 10pt;
    color: #666666;
    margin-bottom: 8pt;
}}

.global-telescope {{
    background-color: #F5F5F5;
    border-left: 3px solid #A5D6A7;
    padding: 12pt;
    margin: 16pt 0;
}}

.practice-exercise {{
    background-color: {config.COLOR_ACCENT_YELLOW};
    border-top: 2px solid #FFF176;
    padding: 12pt;
    margin: 16pt 0;
}}

/* 表格 */
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 12pt 0;
    page-break-inside: avoid;
}}

th {{
    background-color: {config.COLOR_SECONDARY};
    color: white;
    padding: 6pt;
    text-align: left;
    font-weight: bold;
}}

td {{
    border: 1px solid #ddd;
    padding: 6pt;
}}

/* 代码块 */
pre {{
    background-color: #f5f5f5;
    border: 1px solid #ccc;
    padding: 12pt;
    overflow: auto;
    font-family: 'Courier New', monospace;
    font-size: 11pt;
    page-break-inside: avoid;
}}

code {{
    font-family: 'Courier New', monospace;
    background-color: #f5f5f5;
    padding: 2pt 4pt;
    border-radius: 3pt;
}}

/* 图片 */
img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 12pt auto;
    page-break-inside: avoid;
}}

/* 列表 */
ul, ol {{
    margin: 12pt 0;
    padding-left: 24pt;
}}

li {{
    margin: 4pt 0;
    text-align: justify;
}}

/* 分隔线 */
hr {{
    border: none;
    border-top: 2px solid {config.COLOR_SECONDARY};
    margin: 24pt 0;
}}

/* 页眉页脚 */
@media print {{
    @page :first {{
        @top-left {{
            content: "儿童版中国哲学史";
            font-family: {config.BODY_FONT};
            font-size: 9pt;
            color: {config.COLOR_PRIMARY};
        }}
    }}
    
    @page {{
        @top-left {{
            content: "第一章 世界是从哪儿来的？";
            font-family: {config.BODY_FONT};
            font-size: 9pt;
            color: {config.COLOR_PRIMARY};
        }}
        @bottom-center {{
            content: counter(page);
            font-family: {config.BODY_FONT};
            font-size: 9pt;
            color: {config.COLOR_PRIMARY};
        }}
    }}
}}
"""
    return css

def convert_markdown_to_html(markdown_content, css_content, image_path=None):
    """使用pandoc将Markdown转换为HTML"""
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as md_file:
        md_file.write(markdown_content)
        md_path = md_file.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False, encoding='utf-8') as css_file:
        css_file.write(css_content)
        css_path = css_file.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as html_file:
        html_path = html_file.name
    
    try:
        # 构建pandoc命令
        cmd = [
            'pandoc',
            md_path,
            '-f', 'markdown',
            '-t', 'html5',
            '--css', css_path,
            '--self-contained',
            '--standalone',
            '-o', html_path,
            '--metadata', 'pagetitle="儿童版中国哲学史 第一章"'
        ]
        
        # 如果指定了图片，添加图片资源
        if image_path and os.path.exists(image_path):
            # 在Markdown中插入图片引用
            # 这里我们将在HTML后处理中插入，所以先忽略
            pass
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Pandoc转换失败: {result.stderr}")
            return None
        
        # 读取生成的HTML
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 如果指定了图片，在HTML中插入图片
        if image_path and os.path.exists(image_path):
            # 简单的图片插入：在第一个h2标签后插入
            img_html = f'<div class="chapter-image"><img src="{image_path}" alt="第一章场景插图"></div>'
            # 寻找第一个h2标签的位置
            h2_pos = html_content.find('<h2')
            if h2_pos != -1:
                # 找到h2标签结束位置
                h2_end = html_content.find('</h2>', h2_pos)
                if h2_end != -1:
                    insert_pos = h2_end + 5  # 在</h2>之后
                    html_content = html_content[:insert_pos] + '\n' + img_html + '\n' + html_content[insert_pos:]
        
        return html_content
    
    finally:
        # 清理临时文件
        for path in [md_path, css_path, html_path]:
            try:
                os.unlink(path)
            except:
                pass

def convert_html_to_pdf(html_content, output_pdf_path, config):
    """使用wkhtmltopdf将HTML转换为PDF"""
    # 创建临时HTML文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as html_file:
        html_file.write(html_content)
        html_path = html_file.name
    
    try:
        # 构建wkhtmltopdf命令
        cmd = [
            'wkhtmltopdf',
            '--page-size', 'A5',
            '--orientation', 'Portrait',
            '--margin-top', '20mm',
            '--margin-bottom', '12mm',
            '--margin-left', '18mm',
            '--margin-right', '18mm',
            '--encoding', 'UTF-8',
            '--no-outline',
            '--enable-local-file-access',  # 允许访问本地文件
            html_path,
            str(output_pdf_path)
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"PDF生成失败: {result.stderr}")
            return False
        
        return True
    
    finally:
        try:
            os.unlink(html_path)
        except:
            pass

def main():
    """主函数"""
    config = Config()
    
    # 确保输出目录存在
    ensure_dir(config.OUTPUT_DIR)
    
    # 输入文件路径
    chapter_file = Path("outputs/儿童哲学史/优化阶段/第一章优化稿.md")
    image_file = config.IMAGE_DIR / "ch1_scene1.jpg"
    
    # 输出文件路径
    output_pdf = config.OUTPUT_DIR / "第一章样张.pdf"
    
    if not chapter_file.exists():
        print(f"错误: 章节文件不存在: {chapter_file}")
        sys.exit(1)
    
    print(f"正在处理章节: {chapter_file}")
    print(f"使用图片: {image_file if image_file.exists() else '图片不存在'}")
    print(f"输出PDF: {output_pdf}")
    
    # 1. 读取Markdown内容
    markdown_content = read_markdown_file(chapter_file)
    print(f"章节内容长度: {len(markdown_content)} 字符")
    
    # 2. 生成CSS
    css_content = generate_css(config)
    
    # 3. 转换为HTML
    print("正在转换为HTML...")
    html_content = convert_markdown_to_html(markdown_content, css_content, image_file if image_file.exists() else None)
    
    if html_content is None:
        print("HTML转换失败")
        sys.exit(1)
    
    print(f"HTML内容长度: {len(html_content)} 字符")
    
    # 保存HTML用于调试
    debug_html = config.OUTPUT_DIR / "第一章样张_debug.html"
    with open(debug_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"调试HTML已保存: {debug_html}")
    
    # 4. 转换为PDF
    print("正在生成PDF...")
    success = convert_html_to_pdf(html_content, output_pdf, config)
    
    if success:
        print(f"PDF生成成功: {output_pdf}")
        
        # 检查文件大小
        if output_pdf.exists():
            size = output_pdf.stat().st_size
            print(f"PDF文件大小: {size} 字节 ({size/1024:.1f} KB)")
            
            # 简单内容验证
            with open(output_pdf, 'rb') as f:
                header = f.read(4)
                if header == b'%PDF':
                    print("PDF文件格式验证: 通过")
                else:
                    print("PDF文件格式验证: 警告 - 可能不是有效的PDF文件")
        else:
            print("警告: 输出PDF文件不存在")
    else:
        print("PDF生成失败")
        sys.exit(1)
    
    print("处理完成!")

if __name__ == "__main__":
    main()