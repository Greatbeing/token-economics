from PIL import Image, ImageDraw, ImageFont
import os

# 图片路径
image_paths = [
    "imgs/260410_12_生图/播客封面_横版_0.jpg",
    "imgs/260410_12_生图/播客封面_横版_1.jpg",
    "imgs/260410_12_生图/播客封面_横版_2.jpg",
    "imgs/260410_12_生图/播客封面_横版_3.jpg"
]

# 主标题和副标题
main_title = "给孩子的中国哲学课"
sub_title = "和圣哲一起思考"

# 尝试加载中文字体
def get_font(size, bold=False):
    font_paths = [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Windows/Fonts/msyh.ttc",
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    
    return ImageFont.load_default()

# 处理每张图片
for i, img_path in enumerate(image_paths):
    if not os.path.exists(img_path):
        print(f"图片不存在: {img_path}")
        continue
    
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    
    width, height = img.size
    
    # 字体大小（根据图片高度调整）
    main_font_size = int(height * 0.09)
    sub_font_size = int(height * 0.06)
    
    main_font = get_font(main_font_size, bold=True)
    sub_font = get_font(sub_font_size)
    
    # 文字放在右侧区域
    # 右侧区域从 70% 宽度开始
    right_area_start = int(width * 0.70)
    right_area_width = width - right_area_start
    right_area_center = right_area_start + right_area_width // 2
    
    # 计算文字位置（垂直居中）
    # 主标题
    main_bbox = draw.textbbox((0, 0), main_title, font=main_font)
    main_width = main_bbox[2] - main_bbox[0]
    main_height = main_bbox[3] - main_bbox[1]
    main_x = right_area_center - main_width // 2
    main_y = height // 2 - main_height - int(height * 0.08)
    
    # 副标题
    sub_bbox = draw.textbbox((0, 0), sub_title, font=sub_font)
    sub_width = sub_bbox[2] - sub_bbox[0]
    sub_height = sub_bbox[3] - sub_bbox[1]
    sub_x = right_area_center - sub_width // 2
    sub_y = height // 2 + int(height * 0.08)
    
    # 绘制文字
    shadow_color = (0, 0, 0, 200)
    main_color = (255, 215, 0)  # 金色
    sub_color = (255, 255, 255)  # 白色
    
    # 主标题 - 阴影
    for adj_x in range(-4, 5):
        for adj_y in range(-4, 5):
            if adj_x != 0 or adj_y != 0:
                draw.text((main_x + adj_x, main_y + adj_y), main_title, 
                         font=main_font, fill=shadow_color)
    
    # 主标题
    draw.text((main_x, main_y), main_title, font=main_font, fill=main_color)
    
    # 副标题 - 阴影
    for adj_x in range(-3, 4):
        for adj_y in range(-3, 4):
            if adj_x != 0 or adj_y != 0:
                draw.text((sub_x + adj_x, sub_y + adj_y), sub_title, 
                         font=sub_font, fill=shadow_color)
    
    # 副标题
    draw.text((sub_x, sub_y), sub_title, font=sub_font, fill=sub_color)
    
    # 保存
    output_path = f"imgs/260410_12_生图/播客封面_横版_带标题_{i}.jpg"
    img.save(output_path, quality=95)
    print(f"已保存: {output_path}")

print("\n完成！")
