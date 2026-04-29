#!/usr/bin/env python3
"""测试第二章HTML生成"""

import sys
from pathlib import Path

# 添加当前目录到路径，以便导入generate_chapter_html
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.generate_chapter_html import Config, generate_html

# 自定义配置：修改输出目录
class BatchConfig(Config):
    OUTPUT_DIR = Path("outputs/儿童哲学史/排版阶段/章节HTML")
    CSS_FILE = Path("outputs/儿童哲学史/排版阶段/样张/style.css")

config = BatchConfig()

# 生成第二章
input_file = Path("outputs/儿童哲学史/优化阶段/第二章优化稿.md")
output_file = config.OUTPUT_DIR / "第二章样张.html"

success = generate_html(input_file, output_file, config)

if success:
    print("测试成功！第二章HTML样张已生成。")
    # 检查文件大小
    file_size = output_file.stat().st_size / 1024
    print(f"文件大小: {file_size:.1f} KB")
else:
    print("测试失败！")
    sys.exit(1)