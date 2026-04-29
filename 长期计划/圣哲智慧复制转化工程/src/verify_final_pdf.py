#!/usr/bin/env python3
import PyPDF2
import sys

pdf_path = sys.argv[1] if len(sys.argv) > 1 else "outputs/儿童哲学史/最终交付/儿童版中国哲学史_最终完整版.pdf"

print(f"验证PDF: {pdf_path}")
print("=" * 60)

reader = PyPDF2.PdfReader(pdf_path)

# 1. 基本信息
print("1. 基本信息:")
print(f"   页数: {len(reader.pages)}")
print(f"   文件大小: {os.path.getsize(pdf_path) / (1024 * 1024):.2f} MB")

# 2. 书签检查
print("\n2. 书签检查:")
if reader.outline:
    print("   书签列表:")
    for i, item in enumerate(reader.outline):
        if isinstance(item, dict):
            title = item.get('/Title', '无标题')
            page_num = reader.get_destination_page_number(item) + 1
            print(f"     {i+1:2d}. {title} → 第 {page_num} 页")
            
            # 检查是否使用完整标题
            full_titles = [
                "第一章：世界是从哪儿来的？（老子、孔子、神话）",
                "第二章：为什么我和别人不一样？（孟子、告子、荀子）",
                "第三章：怎样才算“赢了”？（庄子、惠施、孙子）",
                "第四章：我能想做什么就做什么吗？（老子、韩非子、杨朱）",
                "第五章：什么是“好”的规则？（墨子、孟子、法家）",
                "第六章：心里害怕怎么办？（王阳明、禅宗、庄子）",
                "第七章：为什么他们那么爱自由？（嵇康、阮籍、王弼）",
                "第八章：烦恼是怎么来的？（慧能、神秀、禅宗）",
                "第九章：朱熹的\"宇宙大房子\"——理学家在做什么？",
                "第十章：王阳明的\"心里种花\"——良知在你心里",
                "第十一章：如何当一个\"现代中国人\"？（顾炎武、黄宗羲、龚自珍）",
                "第十二章：我们为什么要学哲学？（总结与展望）"
            ]
            
            if i < len(full_titles) and title == full_titles[i]:
                print(f"       ✓ 与完整标题匹配")
            elif i < len(full_titles):
                print(f"       ✗ 与完整标题不匹配")
                print(f"         预期: {full_titles[i]}")
                print(f"         实际: {title}")
else:
    print("   无书签")

# 3. 检查关键页面内容
print("\n3. 关键页面内容检查:")
key_pages = [3, 8, 13, 17, 22, 28, 34, 44, 50, 56, 62, 68]  # 0-based

for page_idx in key_pages:
    if page_idx < len(reader.pages):
        page = reader.pages[page_idx]
        text = page.extract_text()
        lines = text.split('\n')
        
        print(f"   第 {page_idx+1} 页 (章节开始页):")
        for line in lines[:3]:  # 显示前3行
            if line.strip():
                print(f"      \"{line[:80]}\"")
        print()

# 4. 检查特殊元素
print("\n4. 特殊元素检查:")
special_elements = ["思想剧场", "想一想", "古人说", "全球望远镜"]
found_elements = []

for i, page in enumerate(reader.pages):
    text = page.extract_text()
    for element in special_elements:
        if element in text and element not in found_elements:
            found_elements.append(element)
    
    if len(found_elements) == len(special_elements):
        break

print("   找到的特殊元素:")
for element in special_elements:
    if element in found_elements:
        print(f"     ✓ {element}")
    else:
        print(f"     ✗ {element}")

print("\n" + "=" * 60)
print("验证完成!")

import os