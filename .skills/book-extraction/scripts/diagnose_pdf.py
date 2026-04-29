#!/usr/bin/env python3
"""
PDF导出问题诊断工具
帮助用户诊断PDF导出相关的问题
"""

import sys
from pathlib import Path

def check_dependencies():
    """检查依赖库"""
    print("=== 检查依赖库 ===")
    deps = ['markdown', 'docx', 'weasyprint']
    missing = []
    
    for dep in deps:
        try:
            if dep == 'docx':
                import docx
                print(f"✓ python-docx 已安装")
            elif dep == 'weasyprint':
                import weasyprint
                print(f"✓ weasyprint 已安装")
            else:
                __import__(dep)
                print(f"✓ {dep} 已安装")
        except ImportError:
            print(f"✗ {dep} 未安装")
            missing.append(dep)
    
    return missing

def check_fonts():
    """检查系统字体"""
    print("\n=== 检查系统字体 ===")
    try:
        import subprocess
        result = subprocess.run(['fc-list', ':lang=zh'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout:
            fonts = result.stdout.strip().split('\n')[:5]  # 只显示前5个
            print(f"✓ 系统包含 {len(result.stdout.split(chr(10)))} 个中文字体")
            print("  示例字体:")
            for font in fonts[:3]:
                font_name = font.split(':')[1].strip()
                print(f"    - {font_name}")
            return True
        else:
            print("✗ 系统缺少中文字体")
            return False
    except Exception as e:
        print(f"⚠ 无法检查字体: {e}")
        return None

def test_pdf_generation():
    """测试PDF生成"""
    print("\n=== 测试PDF生成 ===")
    try:
        from weasyprint import HTML
        from markdown import markdown
        
        # 创建简单的测试内容
        html_content = markdown("# 测试标题\n\n这是一个测试段落。")
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #333; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        test_file = Path("pdf-test-output.pdf")
        HTML(string=full_html).write_pdf(str(test_file))
        
        if test_file.exists():
            file_size = test_file.stat().st_size
            print(f"✓ PDF生成成功，文件大小: {file_size} 字节")
            print(f"  文件路径: {test_file.absolute()}")
            
            # 删除测试文件
            test_file.unlink()
            return True
        else:
            print("✗ PDF文件未生成")
            return False
    except Exception as e:
        print(f"✗ PDF生成失败: {e}")
        return False

def main():
    print("PDF导出问题诊断工具\n")
    print("="*50)
    
    # 检查依赖
    missing_deps = check_dependencies()
    if missing_deps:
        print(f"\n❌ 缺少依赖库: {', '.join(missing_deps)}")
        print("请运行: pip install " + " ".join(missing_deps))
        return
    
    # 检查字体
    has_fonts = check_fonts()
    
    # 测试PDF生成
    pdf_ok = test_pdf_generation()
    
    # 给出建议
    print("\n" + "="*50)
    print("=== 诊断结果与建议 ===")
    
    if pdf_ok and has_fonts:
        print("✓ PDF导出功能正常")
        print("\n如果生成的PDF显示空白，可能原因：")
        print("1. PDF阅读器问题：尝试使用不同的PDF阅读器（如Adobe Reader）")
        print("2. 内容格式问题：检查Markdown内容是否正确")
        print("3. 编码问题：确保输入文件使用UTF-8编码")
    elif pdf_ok and not has_fonts:
        print("⚠ PDF可以生成，但系统缺少中文字体")
        print("\n建议安装中文字体：")
        print("  - Ubuntu/Debian: sudo apt install fonts-noto-cjk")
        print("  - CentOS/RHEL: sudo yum install google-noto-sans-cjk-fonts")
        print("  - macOS: 系统已包含中文字体")
        print("\n或者使用Word格式导出后再转换为PDF")
    elif not pdf_ok:
        print("❌ PDF生成失败")
        print("\n可能原因：")
        print("1. weasyprint依赖不完整")
        print("2. 系统缺少必要的图形库")
        print("\n建议：")
        print("  - 使用Word格式导出后再转换为PDF")
        print("  - 或者检查weasyprint的依赖安装")
    
    print("\n=== 替代方案 ===")
    print("如果PDF导出持续有问题，建议：")
    print("1. 导出为Word格式（.docx）")
    print("2. 在Word中打开文件")
    print("3. 使用Word的\"另存为PDF\"功能")
    print("这样可以获得更好的兼容性和格式控制。")

if __name__ == '__main__':
    main()
