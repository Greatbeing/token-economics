import os
import subprocess
from PIL import Image
import glob

# 路径设置
image_dir = 'temp/视频素材/庄子/图片'
audio_file = 'temp/视频素材/庄子/音频/配音.mp3'
output_video = 'outputs/圣贤智慧包/庄子/视频/庄子讲故事能力解读.mp4'

# 确保输出目录存在
os.makedirs(os.path.dirname(output_video), exist_ok=True)

# 获取图片文件，按 scene_01.jpg, scene_02.jpg 排序
image_files = sorted(glob.glob(os.path.join(image_dir, 'scene_*.jpg')))
print(f"找到 {len(image_files)} 张图片")

if len(image_files) == 0:
    raise FileNotFoundError("未找到图片文件")

# 处理图片：调整尺寸为1920x1080，保持宽高比，填充背景
processed_dir = os.path.join(image_dir, 'processed')
os.makedirs(processed_dir, exist_ok=True)

processed_files = []
for i, img_path in enumerate(image_files):
    img = Image.open(img_path)
    # 计算目标尺寸
    target_width, target_height = 1920, 1080
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height
    
    if img_ratio > target_ratio:
        # 图片更宽，按高度缩放
        new_height = target_height
        new_width = int(target_height * img_ratio)
    else:
        # 图片更高，按宽度缩放
        new_width = target_width
        new_height = int(target_width / img_ratio)
    
    # 缩放
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # 创建新画布，填充黑色背景（或其它颜色）
    canvas = Image.new('RGB', (target_width, target_height), (0, 0, 0))
    # 将缩放后的图片粘贴到画布中央
    offset = ((target_width - new_width) // 2, (target_height - new_height) // 2)
    canvas.paste(img_resized, offset)
    
    # 保存处理后的图片
    processed_path = os.path.join(processed_dir, f'scene_{i+1:02d}.jpg')
    canvas.save(processed_path, quality=95)
    processed_files.append(processed_path)
    print(f"处理图片 {i+1}: {img_path} -> {processed_path}")

# 计算音频时长，确定每张图片显示时间
# 使用ffprobe获取音频时长
cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', audio_file]
result = subprocess.run(cmd, capture_output=True, text=True)
audio_duration = float(result.stdout.strip())
print(f"音频时长: {audio_duration} 秒")

# 每张图片显示时间（秒）
num_images = len(processed_files)
image_duration = audio_duration / num_images
print(f"每张图片显示 {image_duration:.2f} 秒")

# 创建FFmpeg输入文件列表
list_file = os.path.join(processed_dir, 'input.txt')
with open(list_file, 'w') as f:
    for img in processed_files:
        f.write(f"file '{img}'\n")
        f.write(f"duration {image_duration}\n")
    # 最后一张图片需要额外写一次（ffmpeg要求）
    f.write(f"file '{processed_files[-1]}'\n")

# 使用FFmpeg合成视频
ffmpeg_cmd = [
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', list_file,
    '-i', audio_file,
    '-c:v', 'libx264',
    '-preset', 'medium',
    '-crf', '23',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-shortest',
    '-pix_fmt', 'yuv420p',
    output_video
]

print("开始合成视频...")
subprocess.run(ffmpeg_cmd, check=True)

print(f"视频生成完成: {output_video}")
print(f"视频文件大小: {os.path.getsize(output_video) / (1024*1024):.2f} MB")

# 验证视频文件
if os.path.exists(output_video):
    print("✅ 视频文件创建成功")
else:
    print("❌ 视频文件创建失败")