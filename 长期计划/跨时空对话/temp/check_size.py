import os
from PIL import Image

dir_path = "outputs/漫画/第三周第一期"
for fname in os.listdir(dir_path):
    if fname.lower().endswith('.jpg') or fname.lower().endswith('.jpeg'):
        path = os.path.join(dir_path, fname)
        img = Image.open(path)
        print(f"{fname}: {img.size[0]}x{img.size[1]}")