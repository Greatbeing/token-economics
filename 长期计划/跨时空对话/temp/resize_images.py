#!/usr/bin/env python3
import os
import sys
from PIL import Image

def resize_images(input_dir, output_dir, target_width=1080, target_height=1920):
    """
    将input_dir目录下的所有jpg图片调整尺寸到target_width×target_height，保存到output_dir
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            try:
                img = Image.open(input_path)
                # 调整尺寸，使用LANCZOS高质量缩放
                img_resized = img.resize((target_width, target_height), Image.LANCZOS)
                img_resized.save(output_path, quality=95)
                print(f"已调整尺寸: {filename} -> {target_width}x{target_height}")
            except Exception as e:
                print(f"处理{filename}时出错: {e}")
    
    print("所有图片尺寸调整完成。")

if __name__ == "__main__":
    # 默认参数
    input_dir = "outputs/漫画/第三周第一期"
    output_dir = "outputs/漫画/第三周第一期_resized"
    
    # 如果命令行有参数，使用第一个参数作为输入目录
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    resize_images(input_dir, output_dir)