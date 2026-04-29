#!/usr/bin/env python3
import PyPDF2
import sys

pdf_path = sys.argv[1] if len(sys.argv) > 1 else "outputs/儿童哲学史/最终交付/儿童版中国哲学史_A4完整版.pdf"

reader = PyPDF2.PdfReader(pdf_path)
if reader.outline:
    print("书签列表:")
    for item in reader.outline:
        if isinstance(item, dict):
            title = item.get('/Title', '无标题')
            page_num = reader.get_destination_page_number(item) + 1  # 0-based to 1-based
            print(f"  {title} → 第 {page_num} 页")
else:
    print("没有书签")

# 检查章节标题是否包含错误标题
wrong_titles = ["人性是善还是恶？", "道：世界的源代码", "仁：心里的那个开关", "礼：社会的游戏规则", 
                "法：冷酷的游戏裁判", "自然：做真实的自己", "禅宗：心里的扫把", 
                "理学：寻找宇宙的说明书", "心学：心里有个太阳", "实学：有用的才是好的",
                "尾声：哲学探险家的毕业典礼"]

correct_titles = [
    "第一章 世界是从哪儿来的？",
    "第二章 为什么我和别人不一样？",
    "第三章 怎样才算“赢了”？",
    "第四章 我能想做什么就做什么吗？",
    "第五章 什么是“好”的规则？",
    "第六章 心里害怕怎么办？",
    "第七章 为什么他们那么爱自由？",
    "第八章 烦恼是怎么来的？",
    "第九章 朱熹的\"宇宙大房子\"",
    "第十章 王阳明的\"心里种花\"",
    "第十一章 如何当一个\"现代中国人\"？",
    "第十二章 我们为什么要学哲学？"
]

print("\n检查书签标题正确性:")
if reader.outline:
    for i, item in enumerate(reader.outline):
        if isinstance(item, dict):
            title = item.get('/Title', '')
            found_wrong = any(wrong in title for wrong in wrong_titles)
            if found_wrong:
                print(f"  ❌ 发现错误标题: {title}")
            else:
                print(f"  ✓ 标题正确: {title}")
            if i < len(correct_titles):
                expected = correct_titles[i]
                if expected not in title:
                    print(f"    警告: 预期包含 '{expected}'")
else:
    print("  无法检查: 无书签")