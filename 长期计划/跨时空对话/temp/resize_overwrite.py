import os
from PIL import Image

dir_path = "outputs/漫画/第三周第一期"
target_size = (1080, 1920)

for fname in os.listdir(dir_path):
    if fname.lower().endswith('.jpg') or fname.lower().endswith('.jpeg'):
        path = os.path.join(dir_path, fname)
        try:
            img = Image.open(path)
            img_resized = img.resize(target_size, Image.LANCZOS)
            img_resized.save(path, quality=95)
            print(f"调整尺寸: {fname}")
        except Exception as e:
            print(f"错误 {fname}: {e}")

print("完成")