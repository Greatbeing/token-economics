#!/usr/bin/env python3
import os
import sys
from PIL import Image
import json

def analyze_images():
    image_dir = "/app/data/files/outputs/儿童哲学史/移动端优化"
    webp_files = [
        "image_1_optimized.webp",
        "image_2_optimized.webp", 
        "image_3_optimized.webp",
        "image_4_optimized.webp"
    ]
    
    results = []
    for filename in webp_files:
        filepath = os.path.join(image_dir, filename)
        if os.path.exists(filepath):
            with Image.open(filepath) as img:
                width, height = img.size
                file_size = os.path.getsize(filepath)
                results.append({
                    "filename": filename,
                    "width": width,
                    "height": height,
                    "aspect_ratio": round(width/height, 3),
                    "file_size_kb": round(file_size/1024, 2),
                    "format": img.format
                })
    
    # 输出结果
    print("图片尺寸分析结果:")
    print("-" * 80)
    for r in results:
        print(f"{r['filename']}: {r['width']}×{r['height']} (宽高比:{r['aspect_ratio']}), 大小:{r['file_size_kb']}KB")
    
    # 保存为JSON
    output_path = "/app/data/files/outputs/儿童哲学史/手机优化/图片尺寸分析.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n详细结果已保存至: {output_path}")
    
    return results

if __name__ == "__main__":
    analyze_images()