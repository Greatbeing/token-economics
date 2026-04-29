#!/usr/bin/env python3
import re

# 读取第一章HTML样张
with open("outputs/儿童哲学史/排版阶段/章节HTML/第1章样张.html", 'r', encoding='utf-8') as f:
    content = f.read()

# 检查关键CSS类
css_classes_to_check = [
    "thought-theater",
    "think-about",
    "ancient-say",
    "global-telescope",
    "wisdom-map"
]

print("检查CSS类是否存在:")
for css_class in css_classes_to_check:
    # 查找class属性中包含该CSS类的
    pattern = f'class=[\'"][^\'"]*{css_class}[^\'"]*[\'"]'
    matches = re.findall(pattern, content, re.IGNORECASE)
    if matches:
        print(f"  ✓ {css_class}: 找到 {len(matches)} 处")
        if len(matches) <= 3:
            for match in matches[:2]:
                print(f"    示例: {match[:100]}")
    else:
        print(f"  ✗ {css_class}: 未找到")

# 检查字体栈
print("\n检查字体栈:")
font_patterns = [
    "Source Han Serif SC",
    "SimSun",
    "Songti SC",
    "Noto Serif CJK SC",
    "FZXiaoBiaoSong-B05S",
    "FangSong",
    "STFangsong"
]

for font in font_patterns:
    if font in content:
        print(f"  ✓ {font}: 存在")
    else:
        print(f"  ✗ {font}: 不存在")

# 检查图片嵌入
print("\n检查图片嵌入:")
img_pattern = r'<img[^>]*src=[\'"]([^\'"]+)[\'"][^>]*>'
img_matches = re.findall(img_pattern, content)
print(f"  找到 {len(img_matches)} 个图片标签")
for i, src in enumerate(img_matches[:3]):
    if src.startswith('data:image'):
        print(f"    图片 {i+1}: Data URI (嵌入式)")
    else:
        print(f"    图片 {i+1}: {src[:100]}...")

# 检查特殊元素
print("\n检查特殊元素:")
elements = [
    ("思想剧场", "thought-theater"),
    ("想一想", "think-about"),
    ("古人说", "ancient-say"),
    ("全球望远镜", "global-telescope")
]

for text, css_class in elements:
    if text in content:
        print(f"  ✓ 文本 '{text}' 存在")
    else:
        print(f"  ✗ 文本 '{text}' 不存在")