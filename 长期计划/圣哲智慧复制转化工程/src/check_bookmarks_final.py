#!/usr/bin/env python3
import PyPDF2
import os

pdf_path = "outputs/儿童哲学史/最终交付/儿童版中国哲学史_最终完整版.pdf"

reader = PyPDF2.PdfReader(pdf_path)

# 预期的完整标题
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

print("检查书签:")
print("-" * 60)

if reader.outline:
    for i, item in enumerate(reader.outline):
        if isinstance(item, dict):
            title = item.get('/Title', '无标题')
            page_num = reader.get_destination_page_number(item) + 1
            
            if i < len(full_titles):
                expected = full_titles[i]
                if title == expected:
                    print(f"✓ 第{i+1:2d}章: 正确")
                    print(f"   标题: {title}")
                    print(f"   页码: 第 {page_num} 页")
                else:
                    print(f"✗ 第{i+1:2d}章: 不匹配!")
                    print(f"   预期: {expected}")
                    print(f"   实际: {title}")
                    print(f"   页码: 第 {page_num} 页")
            else:
                print(f"? 第{i+1:2d}个书签: {title} → 第 {page_num} 页")
        print()
else:
    print("无书签")

# 检查文件大小
size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
print(f"文件大小: {size_mb:.2f} MB")
print(f"总页数: {len(reader.pages)} 页")