#!/usr/bin/env python3
import base64
import re
import sys

# 图片路径
image_paths = {
    "旅行路线图.jpg": "outputs/images/徐霞客/旅行路线图.jpg",
    "徐霞客肖像.png": "outputs/images/徐霞客/徐霞客肖像.png",
    "山水画.png": "outputs/images/徐霞客/山水画.png"
}

# 读取图片并转换为base64
def image_to_base64(image_path):
    with open(image_path, 'rb') as f:
        img_data = f.read()
        b64 = base64.b64encode(img_data).decode('utf-8')
        # 根据文件扩展名确定MIME类型
        if image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
            mime = 'image/jpeg'
        elif image_path.lower().endswith('.png'):
            mime = 'image/png'
        else:
            mime = 'application/octet-stream'
        return f'data:{mime};base64,{b64}'

# 生成映射
base64_map = {}
for key, path in image_paths.items():
    try:
        base64_map[key] = image_to_base64(path)
        print(f"成功转换: {key}")
    except Exception as e:
        print(f"转换失败 {key}: {e}")
        sys.exit(1)

# 读取HTML文件
html_file = "outputs/文章/徐霞客公众号长文.html"
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 替换三个img标签
# 第一个: 旅行路线图.jpg
html_content = re.sub(
    r'src="\.\./images/徐霞客/旅行路线图\.jpg"',
    f'src="{base64_map["旅行路线图.jpg"]}"',
    html_content
)

# 第二个: 徐霞客肖像.png
html_content = re.sub(
    r'src="\.\./images/徐霞客/徐霞客肖像\.png"',
    f'src="{base64_map["徐霞客肖像.png"]}"',
    html_content
)

# 第三个: 山水画.png
html_content = re.sub(
    r'src="\.\./images/徐霞客/山水画\.png"',
    f'src="{base64_map["山水画.png"]}"',
    html_content
)

# 写入文件
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML文件已更新，图片src已替换为base64 data URI。")

# 验证替换
count1 = html_content.count(base64_map["旅行路线图.jpg"])
count2 = html_content.count(base64_map["徐霞客肖像.png"])
count3 = html_content.count(base64_map["山水画.png"])
print(f"旅行路线图.jpg 出现次数: {count1}")
print(f"徐霞客肖像.png 出现次数: {count2}")
print(f"山水画.png 出现次数: {count3}")