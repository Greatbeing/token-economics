#!/usr/bin/env python3
"""
清理修正版HTML文件中的内嵌对话CSS
确保使用外部CSS样式
"""

import re
from pathlib import Path

# 路径配置
BASE_DIR = Path.cwd()
CHAPTERS_DIR = BASE_DIR / "outputs/儿童哲学史/排版阶段/章节HTML/修正版"
BACKUP_DIR = CHAPTERS_DIR / "备份"
BACKUP_DIR.mkdir(exist_ok=True)

# 要删除的内嵌对话CSS模式
DIALOG_CSS_PATTERN = r'/\* 对话样式 \*/[\s\S]*?\.thought-theater \.dialog-line strong \{[\s\S]*?color: #FF9800;[\s\S]*?\}'

def clean_html_file(file_path):
    """清理单个HTML文件的内嵌对话CSS"""
    print(f"处理: {file_path.name}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 备份原文件
    backup_file = BACKUP_DIR / file_path.name
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 查找并删除内嵌对话CSS
    # 先查找特定的对话CSS块
    dialog_css_match = re.search(DIALOG_CSS_PATTERN, content)
    
    if dialog_css_match:
        print("  找到内嵌对话CSS，正在删除...")
        # 删除匹配的CSS块
        cleaned_content = re.sub(DIALOG_CSS_PATTERN, '', content)
        
        # 保存清理后的文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"  已清理并保存: {file_path.name}")
        return True
    else:
        print("  未找到内嵌对话CSS，跳过")
        return False

def main():
    print("清理修正版HTML文件中的内嵌对话CSS...")
    
    # 获取所有修正版HTML文件
    html_files = sorted([f for f in CHAPTERS_DIR.iterdir() if f.name.endswith('_fixed.html')])
    
    if not html_files:
        print("错误: 未找到修正版HTML文件")
        return
    
    print(f"找到 {len(html_files)} 个修正版HTML文件")
    
    cleaned_count = 0
    for file_path in html_files:
        if clean_html_file(file_path):
            cleaned_count += 1
    
    print(f"\n清理完成！")
    print(f"  处理文件数: {len(html_files)}")
    print(f"  清理文件数: {cleaned_count}")
    print(f"  备份保存在: {BACKUP_DIR}")

if __name__ == '__main__':
    main()