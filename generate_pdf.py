#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
儿童版中国哲学史 - PDF生成脚本
将封面HTML和所有章节合并为一个PDF文件
"""

import os
import subprocess
from pathlib import Path

# 路径配置
BASE_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史")
OUTPUT_DIR = BASE_DIR / "移动端适配"
CHAPTERS_DIR = OUTPUT_DIR / "chapters_optimized"
FINAL_PDF = OUTPUT_DIR / "和古人一起想问题_移动端版.pdf"

# 章节列表（按顺序）
CHAPTERS = [
    ("封面", OUTPUT_DIR / "封面_移动端.html"),
    ("第1章", CHAPTERS_DIR / "第1章_mobile.html"),
    ("第2章", CHAPTERS_DIR / "第2章_mobile.html"),
    ("第3章", CHAPTERS_DIR / "第3章_mobile.html"),
    ("第4章", CHAPTERS_DIR / "第4章_mobile.html"),
    ("第5章", CHAPTERS_DIR / "第5章_mobile.html"),
    ("第6章", CHAPTERS_DIR / "第6章_mobile.html"),
    ("第7章", CHAPTERS_DIR / "第7章_mobile.html"),
    ("第8章", CHAPTERS_DIR / "第8章_mobile.html"),
    ("第9章", CHAPTERS_DIR / "第9章_mobile.html"),
    ("第10章", CHAPTERS_DIR / "第10章_mobile.html"),
    ("第11章", CHAPTERS_DIR / "第11章_mobile.html"),
    ("第12章", CHAPTERS_DIR / "第12章_mobile.html"),
]

def html_to_pdf(html_path, pdf_path):
    """使用wkhtmltopdf将HTML转换为PDF"""
    cmd = [
        'wkhtmltopdf',
        '--enable-local-file-access',  # 允许访问本地文件
        '--print-media-type',         # 使用打印样式
        '--no-stop-slow-scripts',      # 不停止慢脚本
        '--enable-javascript',         # 启用JavaScript
        '--javascript-delay', '1000',  # JavaScript延迟
        '--page-size', 'A4',
        '--orientation', 'Portrait',
        '--margin-top', '20mm',
        '--margin-bottom', '20mm',
        '--margin-left', '15mm',
        '--margin-right', '15mm',
        '--image-quality', '90',
        str(html_path),
        str(pdf_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            return True, f"成功生成 {pdf_path.name}"
        else:
            return False, f"错误: {result.stderr[:200]}"
    except subprocess.TimeoutExpired:
        return False, "超时"
    except Exception as e:
        return False, f"异常: {str(e)}"

def main():
    print("=" * 60)
    print("📄 儿童版中国哲学史 - PDF生成")
    print("=" * 60)
    
    # 检查文件是否存在
    missing = []
    for name, path in CHAPTERS:
        if not path.exists():
            missing.append((name, path))
    
    if missing:
        print("\n⚠️ 以下文件缺失:")
        for name, path in missing:
            print(f"   - {name}: {path}")
        return
    
    # 生成每个章节的PDF
    temp_pdfs = []
    
    print(f"\n📑 开始生成 {len(CHAPTERS)} 个PDF文件...\n")
    
    for i, (name, html_path) in enumerate(CHAPTERS, 1):
        pdf_path = OUTPUT_DIR / f"temp_{name}.pdf"
        temp_pdfs.append(pdf_path)
        
        print(f"[{i}/{len(CHAPTERS)}] 生成 {name} PDF...", end=" ")
        success, msg = html_to_pdf(html_path, pdf_path)
        
        if success:
            size = os.path.getsize(pdf_path) / 1024
            print(f"✅ ({size:.1f}KB)")
        else:
            print(f"❌ {msg}")
    
    # 检查总大小
    total_size = sum(os.path.getsize(p) for p in temp_pdfs) / (1024 * 1024)
    print(f"\n📊 当前总大小: {total_size:.1f}MB")
    
    if total_size > 30:
        print("⚠️ 警告: 总大小超过30MB限制")
    
    # 合并PDF（使用pdftk或简单复制第一个）
    print("\n🔗 合并PDF文件...")
    
    # 如果有pdftk，使用它；否则复制封面作为最终PDF
    if os.system("which pdftk > /dev/null 2>&1") == 0:
        # 使用pdftk合并
        pdftk_cmd = ['pdftk'] + [str(p) for p in temp_pdfs] + ['cat', 'output', str(FINAL_PDF)]
        result = os.system(' '.join(pdftk_cmd))
        if result == 0:
            print("✅ 使用pdftk合并成功")
        else:
            print("❌ pdftk合并失败，使用封面作为最终PDF")
            import shutil
            shutil.copy(temp_pdfs[0], FINAL_PDF)
    else:
        # 没有pdftk，复制封面作为最终PDF（演示用）
        import shutil
        shutil.copy(temp_pdfs[0], FINAL_PDF)
        print("⚠️ 未安装pdftk，仅复制封面作为最终PDF")
        print("   提示: 安装 pdftk 可合并多个PDF")
    
    # 清理临时文件
    for pdf in temp_pdfs:
        if pdf != FINAL_PDF:
            os.remove(pdf)
    
    # 最终统计
    if FINAL_PDF.exists():
        final_size = os.path.getsize(FINAL_PDF) / 1024
        print(f"\n✅ 最终PDF已生成:")
        print(f"   📄 {FINAL_PDF}")
        print(f"   📊 大小: {final_size:.1f}KB")
    
    print("\n" + "=" * 60)
    print("📋 生成的章节PDF文件:")
    for name, _ in CHAPTERS[1:]:  # 跳过封面
        temp_pdf = OUTPUT_DIR / f"temp_{name}.pdf"
        if temp_pdf.exists():
            size = os.path.getsize(temp_pdf) / 1024
            print(f"   {name}: {size:.1f}KB")
    print("=" * 60)

if __name__ == '__main__':
    main()
