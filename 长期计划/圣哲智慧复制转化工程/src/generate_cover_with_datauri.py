#!/usr/bin/env python3
"""
生成A4尺寸PDF封面，使用Data URI嵌入封面图片
解决wkhtmltopdf安全限制导致的图片访问失败问题
"""

import base64
from pathlib import Path

# 路径配置
BASE_DIR = Path.cwd()
COVER_IMAGE = BASE_DIR / "outputs/儿童哲学史/最终交付/封面设计.jpg"
OUTPUT_HTML = BASE_DIR / "outputs/儿童哲学史/最终交付/cover_final_datauri.html"
OUTPUT_PDF = BASE_DIR / "outputs/儿童哲学史/最终交付/cover_final.pdf"

def image_to_data_uri(image_path):
    """将图片转换为Data URI格式"""
    if not image_path.exists():
        raise FileNotFoundError(f"封面图片不存在: {image_path}")
    
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # 获取图片MIME类型（根据扩展名）
    ext = image_path.suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
    }
    mime_type = mime_types.get(ext, 'image/jpeg')
    
    # Base64编码
    base64_data = base64.b64encode(image_data).decode('utf-8')
    return f"data:{mime_type};base64,{base64_data}"

def generate_cover_html(data_uri):
    """生成封面HTML"""
    html_template = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>儿童版中国哲学史 - 封面</title>
    <style>
        @page {{
            size: A4;
            margin: 0;
        }}
        
        body {{
            margin: 0;
            padding: 0;
            width: 210mm;
            height: 297mm;
            font-family: 'FZXiaoBiaoSong-B05S', 'FangSong', 'STFangsong', 'Noto Sans CJK SC', sans-serif;
            position: relative;
            overflow: hidden;
        }}
        
        .cover-background {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url("{data_uri}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            filter: brightness(0.95);
            z-index: 1;
        }}
        
        .title-overlay {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80%;
            max-width: 600px;
            background-color: rgba(255, 255, 255, 0.92);
            padding: 50px 60px;
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
            text-align: center;
            z-index: 2;
        }}
        
        .main-title {{
            font-size: 56px;
            font-weight: bold;
            color: #FF6B35;
            margin-bottom: 20px;
            line-height: 1.2;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .subtitle {{
            font-size: 42px;
            color: #1565C0;
            margin-bottom: 25px;
            line-height: 1.3;
        }}
        
        .description {{
            font-size: 24px;
            color: #333333;
            line-height: 1.6;
            margin-bottom: 10px;
        }}
        
        .age-range {{
            font-size: 20px;
            color: #666666;
            margin-top: 25px;
            font-style: italic;
        }}
        
        /* 打印优化 */
        @media print {{
            body {{
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
        }}
    </style>
</head>
<body>
    <div class="cover-background"></div>
    <div class="title-overlay">
        <h1 class="main-title">儿童版中国哲学史</h1>
        <h2 class="subtitle">和古人一起想问题</h2>
        <div class="description">
            一本带你探索中国哲学智慧的探险手册
        </div>
        <div class="age-range">
            适合8-12岁的小小哲学家
        </div>
    </div>
</body>
</html>'''
    return html_template

def convert_html_to_pdf(html_file, pdf_file):
    """使用wkhtmltopdf将HTML转换为PDF"""
    import subprocess
    
    cmd = [
        'wkhtmltopdf',
        '--page-size', 'A4',
        '--orientation', 'Portrait',
        '--margin-top', '0',
        '--margin-right', '0',
        '--margin-bottom', '0',
        '--margin-left', '0',
        '--disable-smart-shrinking',
        '--dpi', '300',
        '--encoding', 'UTF-8',
        str(html_file),
        str(pdf_file)
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"错误: {result.stderr}")
        raise RuntimeError(f"PDF转换失败: {result.stderr}")
    
    print(f"PDF生成成功: {pdf_file}")
    return True

def main():
    print("生成A4尺寸PDF封面...")
    
    # 确保输出目录存在
    OUTPUT_PDF.parent.mkdir(exist_ok=True)
    
    # 将图片转换为Data URI
    print(f"读取封面图片: {COVER_IMAGE}")
    data_uri = image_to_data_uri(COVER_IMAGE)
    print("图片已转换为Data URI格式")
    
    # 生成HTML
    html_content = generate_cover_html(data_uri)
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML封面已生成: {OUTPUT_HTML}")
    
    # 转换为PDF
    print("正在转换为PDF...")
    convert_html_to_pdf(OUTPUT_HTML, OUTPUT_PDF)
    
    # 验证PDF尺寸
    print("\n验证PDF文件...")
    if OUTPUT_PDF.exists():
        # 使用pdfinfo验证尺寸
        import subprocess
        result = subprocess.run(['pdfinfo', str(OUTPUT_PDF)], capture_output=True, text=True)
        print(result.stdout)
        
        # 检查文件大小
        file_size = OUTPUT_PDF.stat().st_size / 1024
        print(f"PDF文件大小: {file_size:.1f} KB")
        
        print(f"\n封面生成完成！")
        print(f"  HTML文件: {OUTPUT_HTML}")
        print(f"  PDF文件: {OUTPUT_PDF}")
    else:
        print("错误: PDF文件未生成")

if __name__ == '__main__':
    main()