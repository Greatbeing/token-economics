#!/usr/bin/env python3
"""
解析HTML文件并提取文本和图片
"""
import os
import re
import base64

# HTML文件路径
html_path = "长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/最终交付/和古人一起想问题_完整版_v4.html"
# 图片目录
img_dir = "长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/最终交付/images/"
# 输出目录
output_dir = "长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/最终交付/"

# 读取HTML文件
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

print(f"HTML文件读取完成，大小: {len(html_content)} 字符")

# 提取所有图片
# 1. 提取base64图片
base64_images = re.findall(r'src="data:image/([^;]+);base64,([^"]+)"', html_content)
print(f"找到 {len(base64_images)} 个base64图片")

# 2. 提取外部图片引用 (images/目录中的图片)
external_images = re.findall(r'images/([^"]+\.(?:jpg|jpeg|png|gif))', html_content)
external_images = list(set(external_images))  # 去重
print(f"找到 {len(external_images)} 个外部图片引用")

# 创建图片映射 - 从文件名到章节
image_mapping = []
for img in external_images:
    filename = img if isinstance(img, str) else img[0] if isinstance(img, tuple) else str(img)
    # 解析章节编号
    match = re.match(r'chapter(\d+)_img(\d+)', filename)
    if match:
        chapter = int(match.group(1))
        img_num = int(match.group(2))
        image_mapping.append({
            'filename': filename,
            'chapter': chapter,
            'img_num': img_num,
            'full_path': os.path.join(img_dir, filename)
        })

image_mapping.sort(key=lambda x: (x['chapter'], x['img_num']))
print(f"图片映射创建完成，共 {len(image_mapping)} 张图片")

# 保存图片映射到文件
import json
with open(os.path.join(output_dir, 'image_mapping.json'), 'w', encoding='utf-8') as f:
    json.dump(image_mapping, f, ensure_ascii=False, indent=2)

print("图片映射已保存")

# 提取HTML文本内容（去除所有标签和base64）
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.in_script = False
        self.in_style = False
        
    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style']:
            self.in_script = True
            
    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.in_script = False
            
    def handle_data(self, data):
        if not self.in_script:
            self.text_parts.append(data)

# 提取纯文本
parser = TextExtractor()
parser.feed(html_content)
text_content = '\n'.join(parser.text_parts)

# 清理文本
text_content = re.sub(r'\n{3,}', '\n\n', text_content)
text_content = text_content.strip()

# 保存文本内容
text_output_path = os.path.join(output_dir, 'content_text.txt')
with open(text_output_path, 'w', encoding='utf-8') as f:
    f.write(text_content)

print(f"文本内容已保存到: {text_output_path}")

# 统计信息
print(f"\n=== 统计信息 ===")
print(f"HTML文件大小: {len(html_content)} 字符")
print(f"Base64图片数量: {len(base64_images)}")
print(f"外部图片数量: {len(external_images)}")
print(f"文本内容长度: {len(text_content)} 字符")
