#!/usr/bin/env python3
"""
修复Markdown格式并准备上传
"""

import re

def fix_markdown(content):
    """修复Markdown格式"""
    # 修复标题格式 - 移除多余的#号
    content = re.sub(r'##\s*#\s*', '## ', content)
    content = re.sub(r'#\s*#\s*', '# ', content)
    
    # 修复章节标题格式
    content = re.sub(r'##\s*(第[一二三四五六七八九十\d]+章[：:\s]*)', r'## \1', content)
    
    # 清理转义的符号
    content = content.replace('\\', '')
    
    # 移除多余的横线分隔
    content = re.sub(r'\n={60,}\n', '\n\n---\n\n', content)
    
    # 修复表格格式
    content = re.sub(r'\\\|', '|', content)
    
    # 清理多余的空行
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    return content

def main():
    # 读取文件
    with open('./和古人一起想问题_完整版.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复格式
    content = fix_markdown(content)
    
    # 保存修复后的文件
    output_file = './和古人一起想问题_飞书版.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已保存修复后的文件: {output_file}")
    print(f"📊 文件大小: {len(content):,} 字符")
    
    return output_file

if __name__ == "__main__":
    main()
