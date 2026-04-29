#!/usr/bin/env python3
"""
合并并清理所有章节的Markdown文件
"""

import os
import re

def clean_markdown(content):
    """清理Markdown内容"""
    # 移除pandoc生成的div标记
    content = re.sub(r':::\s*\{\.?[a-z-]+\}', '', content)
    content = re.sub(r':::\s*', '', content)
    
    # 修复转义的#号
    content = content.replace('\\#', '#')
    
    # 清理多余的空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # 清理图片标记中的空链接
    content = re.sub(r'!\[([^\]]*)\]\(\s*\)', r'[图片: \1]', content)
    
    # 确保标题前后有空行
    content = re.sub(r'([^\n])\n(#{1,6}\s)', r'\1\n\n\2', content)
    content = re.sub(r'(#{1,6}\s[^\n]+)\n([^\n#])', r'\1\n\n\2', content)
    
    return content.strip()

def merge_chapters():
    """合并所有章节"""
    md_dir = "./converted_md"
    
    all_content = []
    chapter_titles = []
    
    for i in range(1, 13):
        filepath = os.path.join(md_dir, f"chapter_{i}.md")
        
        if not os.path.exists(filepath):
            print(f"警告: 文件不存在 {filepath}")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 清理内容
        content = clean_markdown(content)
        
        # 提取章节标题（从内容中）
        title_match = re.search(r'#\s*第[一二三四五六七八九十\d]+章[：:\s]*([^\n]+)', content)
        if title_match:
            title = title_match.group(0).strip()
        else:
            # 尝试其他格式
            title = f"第{i}章"
        
        chapter_titles.append(title)
        all_content.append(content)
        
        print(f"处理第{i}章: {title[:30]}... ({len(content)} 字符)")
    
    return all_content, chapter_titles

def save_final_document(contents, titles, output_file):
    """保存最终文档"""
    with open(output_file, 'w', encoding='utf-8') as f:
        # 不写主标题，因为上传时会作为文档标题
        f.write("《和古人一起想问题》中国哲学探险手册\n\n")
        f.write("---\n\n")
        f.write("这是一本带你穿越时空、和古代智者对话的书。每一章，你都会遇见一位中国哲学家，和他们一起思考那些困扰人类几千年的大问题。\n\n")
        f.write("---\n\n")
        
        for i, (title, content) in enumerate(zip(titles, contents), 1):
            # 添加章节分隔
            f.write(f"\n\n{'='*60}\n\n")
            # 添加章节标题（二级标题）
            f.write(f"## {title}\n\n")
            # 写入章节内容
            f.write(content)
    
    print(f"\n✅ 已保存到: {output_file}")
    print(f"📊 总计: {len(contents)} 章")

if __name__ == "__main__":
    contents, titles = merge_chapters()
    save_final_document(contents, titles, "./和古人一起想问题_完整版.md")
    
    # 统计
    total_chars = sum(len(c) for c in contents)
    print(f"📝 总字符数: {total_chars:,}")
    
    print("\n📚 章节目录:")
    for i, title in enumerate(titles, 1):
        print(f"  {i}. {title}")
