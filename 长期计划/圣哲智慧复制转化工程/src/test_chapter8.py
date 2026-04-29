#!/usr/bin/env python3
import sys
from pathlib import Path

from generate_chapter_html import Config, generate_html

class TestConfig(Config):
    OUTPUT_DIR = Path("outputs/儿童哲学史/排版阶段/章节HTML")
    CSS_FILE = Path("outputs/儿童哲学史/排版阶段/样张/style.css")

config = TestConfig()

# 处理第八章
input_file = Path("outputs/儿童哲学史/优化阶段/第八章优化稿.md")
output_file = config.OUTPUT_DIR / "第8章样张.html"

print(f"输入文件: {input_file}")
print(f"输出文件: {output_file}")

success = generate_html(input_file, output_file, config)
if success:
    print("第八章HTML样张生成成功！")
    # 检查文件大小
    file_size = output_file.stat().st_size / 1024
    print(f"文件大小: {file_size:.1f} KB")
    # 检查图片数量
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        img_count = content.count('<img')
        print(f"图片数量: {img_count}")
else:
    print("生成失败")
    sys.exit(1)