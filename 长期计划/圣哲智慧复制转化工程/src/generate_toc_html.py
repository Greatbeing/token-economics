#!/usr/bin/env python3
"""
生成《儿童版中国哲学史》目录页HTML
基于现有PDF书签信息，计算插入封面和目录后的新页码
"""

import os
import sys
from pathlib import Path

# 章节标题和原始起始页码（从书签提取）
chapter_data = [
    ("第一章 世界是从哪儿来的？", 1),
    ("第二章 人性是善还是恶？", 11),
    ("第三章 道：世界的源代码", 20),
    ("第四章 仁：心里的那个开关", 28),
    ("第五章 礼：社会的游戏规则", 37),
    ("第六章 法：冷酷的游戏裁判", 47),
    ("第七章 自然：做真实的自己", 57),
    ("第八章 禅宗：心里的扫把", 75),
    ("第九章 理学：寻找宇宙的说明书", 87),
    ("第十章 心学：心里有个太阳", 99),
    ("第十一章 实学：有用的才是好的", 111),
    ("第十二章 尾声：哲学探险家的毕业典礼", 122),
]

# 偏移量：封面(1页) + 目录(1页) = 2页
offset = 2

# 计算新页码
chapter_toc = []
for title, orig_page in chapter_data:
    new_page = orig_page + offset
    chapter_toc.append((title, new_page))

# 输出目录页HTML
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>《和古人一起想问题》目录</title>
    <link rel="stylesheet" href="style.css">
    <style>
        /* 目录页专用样式 */
        .toc-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            font-family: 'Source Han Serif SC', serif;
        }}
        
        .toc-header {{
            text-align: center;
            margin-bottom: 50px;
        }}
        
        .toc-title {{
            font-family: 'FZXiaoBiaoSong-B05S', 'FangSong', sans-serif;
            font-size: 36px;
            color: #FFB74D;
            margin-bottom: 15px;
        }}
        
        .toc-subtitle {{
            font-size: 20px;
            color: #1565C0;
            margin-bottom: 30px;
        }}
        
        .toc-list {{
            list-style-type: none;
            padding: 0;
        }}
        
        .toc-item {{
            margin-bottom: 25px;
            padding: 15px;
            border-left: 5px solid #81D4FA;
            background-color: #F9F9F9;
            border-radius: 0 10px 10px 0;
            transition: all 0.3s ease;
        }}
        
        .toc-item:hover {{
            background-color: #E1F5FE;
            transform: translateX(10px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .toc-chapter-title {{
            font-size: 20px;
            font-weight: bold;
            color: #5D4037;
            margin-bottom: 5px;
        }}
        
        .toc-page {{
            font-size: 16px;
            color: #666;
            text-align: right;
        }}
        
        .toc-footer {{
            text-align: center;
            margin-top: 60px;
            padding-top: 20px;
            border-top: 2px dashed #FFCC80;
            color: #999;
            font-size: 14px;
        }}
        
        @media (max-width: 600px) {{
            .toc-title {{
                font-size: 28px;
            }}
            .toc-item {{
                padding: 12px;
            }}
        }}
    </style>
</head>
<body>
    <div class="toc-container">
        <div class="toc-header">
            <h1 class="toc-title">《和古人一起想问题》</h1>
            <h2 class="toc-subtitle">儿童哲学探险手册</h2>
            <p style="color: #666; font-size: 18px; margin-top: 20px;">目录</p>
        </div>
        
        <ul class="toc-list">
"""

for title, page in chapter_toc:
    html_content += f"""            <li class="toc-item">
                <div class="toc-chapter-title">{title}</div>
                <div class="toc-page">第 {page} 页</div>
            </li>
"""

html_content += """        </ul>
        
        <div class="toc-footer">
            <p>一本带你探索中国哲学智慧的探险手册</p>
            <p>适合8-12岁的小小哲学家</p>
        </div>
    </div>
</body>
</html>"""

# 保存文件
output_dir = Path("outputs/儿童哲学史/最终交付")
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "目录页.html"

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"目录页已生成: {output_path}")
print("章节与页码对应关系:")
for title, page in chapter_toc:
    print(f"  {title} → 第 {page} 页")

# 同时复制样式文件到同一目录，确保wkhtmltopdf能正确加载
style_src = Path("outputs/儿童哲学史/排版阶段/章节HTML/style.css")
style_dst = output_dir / "style.css"
if style_src.exists():
    import shutil
    shutil.copy2(style_src, style_dst)
    print(f"样式文件已复制: {style_dst}")