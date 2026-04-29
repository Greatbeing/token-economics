#!/usr/bin/env python3
import os

# 完整原始标题（从原始目录中提取）
full_titles = [
    "第一章：世界是从哪儿来的？（老子、孔子、神话）",
    "第二章：为什么我和别人不一样？（孟子、告子、荀子）",
    "第三章：怎样才算\"赢了\"？（庄子、惠施、孙子）",
    "第四章：我能想做什么就做什么吗？（老子、韩非子、杨朱）",
    "第五章：什么是\"好\"的规则？（墨子、孟子、法家）",
    "第六章：心里害怕怎么办？（王阳明、禅宗、庄子）",
    "第七章：为什么他们那么爱自由？（嵇康、阮籍、王弼）",
    "第八章：烦恼是怎么来的？（慧能、神秀、禅宗）",
    "第九章：朱熹的\"宇宙大房子\"——理学家在做什么？",
    "第十章：王阳明的\"心里种花\"——良知在你心里",
    "第十一章：如何当一个\"现代中国人\"？（顾炎武、黄宗羲、龚自珍）",
    "第十二章：我们为什么要学哲学？（总结与展望）"
]

# 页码（基于A4 PDF）
page_numbers = [4, 9, 14, 18, 23, 29, 35, 45, 51, 57, 63, 69]

# 生成HTML
html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>《和古人一起想问题》完整目录</title>
    <link rel="stylesheet" href="style.css">
    <style>
        /* 目录页专用样式 */
        .toc-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            font-family: 'Source Han Serif SC', serif;
        }
        
        .toc-header {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .toc-title {
            font-family: 'FZXiaoBiaoSong-B05S', 'FangSong', sans-serif;
            font-size: 36px;
            color: #FFB74D;
            margin-bottom: 15px;
        }
        
        .toc-subtitle {
            font-size: 20px;
            color: #1565C0;
            margin-bottom: 30px;
        }
        
        .toc-list {
            list-style-type: none;
            padding: 0;
        }
        
        .toc-item {
            margin-bottom: 25px;
            padding: 15px;
            border-left: 5px solid #81D4FA;
            background-color: #F9F9F9;
            border-radius: 0 10px 10px 0;
            transition: all 0.3s ease;
        }
        
        .toc-item:hover {
            background-color: #E1F5FE;
            transform: translateX(10px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .toc-chapter-title {
            font-size: 20px;
            font-weight: bold;
            color: #5D4037;
            margin-bottom: 5px;
            line-height: 1.4;
        }
        
        .toc-philosophers {
            font-size: 16px;
            color: #666;
            font-style: italic;
            margin-bottom: 8px;
        }
        
        .toc-page {
            font-size: 16px;
            color: #666;
            text-align: right;
            font-weight: bold;
        }
        
        .toc-footer {
            text-align: center;
            margin-top: 60px;
            padding-top: 20px;
            border-top: 2px dashed #FFCC80;
            color: #999;
            font-size: 14px;
        }
        
        @media (max-width: 600px) {
            .toc-title {
                font-size: 28px;
            }
            .toc-item {
                padding: 12px;
            }
            .toc-chapter-title {
                font-size: 18px;
            }
        }
    </style>
</head>
<body>
    <div class="toc-container">
        <div class="toc-header">
            <h1 class="toc-title">《和古人一起想问题》</h1>
            <h2 class="toc-subtitle">中国哲学探险手册</h2>
            <p style="color: #666; font-size: 18px; margin-top: 20px;">完整目录</p>
        </div>
        
        <ul class="toc-list">
'''

# 添加章节项目
for i, (title, page_num) in enumerate(zip(full_titles, page_numbers)):
    # 分离主标题和哲学家信息
    if '（' in title and '）' in title:
        main_title = title.split('（')[0]
        philosophers = title.split('（')[1].rstrip('）')
    elif '——' in title:
        main_title = title.split('——')[0]
        philosophers = title.split('——')[1]
    else:
        main_title = title
        philosophers = ""
    
    html_content += f'''            <li class="toc-item">
                <div class="toc-chapter-title">{main_title}</div>
'''
    if philosophers:
        html_content += f'''                <div class="toc-philosophers">{philosophers}</div>
'''
    html_content += f'''                <div class="toc-page">第 {page_num} 页</div>
            </li>
'''

html_content += '''        </ul>
        
        <div class="toc-footer">
            <p>一本带你探索中国哲学智慧的探险手册</p>
            <p>适合8-12岁的小小哲学家</p>
        </div>
    </div>
</body>
</html>'''

# 保存文件
output_dir = "outputs/儿童哲学史/最终交付"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "目录页_完整版.html")

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"完整目录页已生成: {output_path}")
print(f"共 {len(full_titles)} 章，使用了原始完整标题格式。")

# 显示部分内容供验证
print("\n前3章标题:")
for i in range(3):
    print(f"  {full_titles[i]} → 第 {page_numbers[i]} 页")