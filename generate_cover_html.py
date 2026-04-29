import base64
from pathlib import Path

# 图片路径
image_paths = [
    "imgs/260410_13_生图/播客封面_新设计_0.jpg",
    "imgs/260410_13_生图/播客封面_新设计_1.jpg",
    "imgs/260410_13_生图/播客封面_新设计_2.jpg",
    "imgs/260410_13_生图/播客封面_新设计_3.jpg"
]

output_dir = Path("长期计划/跨时空对话/儿童哲学播客_v2/封面设计")
output_dir.mkdir(parents=True, exist_ok=True)

for i, img_path in enumerate(image_paths, 1):
    # 读取图片并转为base64
    with open(img_path, "rb") as f:
        img_data = f.read()
        img_base64 = base64.b64encode(img_data).decode('utf-8')
    
    # 创建HTML
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>给孩子的中国哲学课 - 封面版本{i}</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=ZCOOL+KuaiLe&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            width: 2848px;
            height: 1600px;
            overflow: hidden;
            background-image: url('data:image/jpeg;base64,{img_base64}');
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
            justify-content: flex-end;
        }}
        
        .title-container {{
            width: 60%;
            padding: 80px 120px 80px 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }}
        
        .main-title {{
            font-family: 'ZCOOL KuaiLe', 'Noto Sans SC', sans-serif;
            font-size: 140px;
            font-weight: 700;
            color: #2c3e50;
            line-height: 1.3;
            margin-bottom: 40px;
            text-shadow: 
                3px 3px 0px rgba(255,255,255,0.8),
                -1px -1px 0px rgba(255,255,255,0.8),
                1px -1px 0px rgba(255,255,255,0.8),
                -1px 1px 0px rgba(255,255,255,0.8);
            letter-spacing: 8px;
        }}
        
        .sub-title {{
            font-family: 'Noto Sans SC', sans-serif;
            font-size: 72px;
            font-weight: 300;
            color: #7f8c8d;
            line-height: 1.5;
            letter-spacing: 12px;
            position: relative;
            padding-top: 30px;
        }}
        
        .sub-title::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 200px;
            height: 3px;
            background: linear-gradient(to right, transparent, #bdc3c7, transparent);
        }}
        
        .decoration {{
            margin-top: 60px;
            font-size: 48px;
            color: #95a5a6;
            letter-spacing: 4px;
        }}
    </style>
</head>
<body>
    <div class="title-container">
        <h1 class="main-title">给孩子的<br>中国哲学课</h1>
        <h2 class="sub-title">和圣哲一起思考</h2>
        <div class="decoration">✦ ✦ ✦</div>
    </div>
</body>
</html>'''
    
    # 保存HTML
    html_path = output_dir / f"封面_版本{i}.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"已生成: {html_path}")

print("\n全部完成！")
