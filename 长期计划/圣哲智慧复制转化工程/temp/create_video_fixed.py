import os
import subprocess
import glob

# 获取当前工作目录
base_dir = '/app/data/files'
os.chdir(base_dir)

# 路径设置
image_dir = 'temp/视频素材/庄子/图片'
audio_file = 'temp/视频素材/庄子/音频/配音_trimmed.mp3'
output_video = 'outputs/圣贤智慧包/庄子/视频/庄子讲故事能力解读.mp4'

# 确保输出目录存在
os.makedirs(os.path.dirname(output_video), exist_ok=True)

# 获取图片文件，按 scene_01.jpg, scene_02.jpg 排序
image_files = sorted(glob.glob(os.path.join(image_dir, 'scene_*.jpg')))
print(f"找到 {len(image_files)} 张图片")

if len(image_files) == 0:
    raise FileNotFoundError("未找到图片文件")

# 创建处理后的图片目录
processed_dir = os.path.join(image_dir, 'processed')
os.makedirs(processed_dir, exist_ok=True)

# 使用ffmpeg批量调整图片尺寸
for i, img_path in enumerate(image_files):
    output_path = os.path.join(processed_dir, f'scene_{i+1:02d}.jpg')
    cmd = [
        'ffmpeg', '-i', img_path,
        '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2',
        '-y', output_path
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"调整图片 {i+1}: {os.path.basename(img_path)}")

# 获取音频时长
cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', audio_file]
result = subprocess.run(cmd, capture_output=True, text=True)
audio_duration = float(result.stdout.strip())
print(f"剪切后音频时长: {audio_duration} 秒")

# 每张图片显示时间
num_images = len(image_files)
image_duration = audio_duration / num_images
print(f"每张图片显示 {image_duration:.2f} 秒")

# 创建FFmpeg输入文件列表
list_file = os.path.join(processed_dir, 'input.txt')
with open(list_file, 'w', encoding='utf-8') as f:
    for i in range(num_images):
        img_path = os.path.join(processed_dir, f'scene_{i+1:02d}.jpg')
        # 使用绝对路径
        abs_path = os.path.abspath(img_path)
        f.write(f"file '{abs_path}'\n")
        f.write(f"duration {image_duration}\n")
    # 最后一张图片需要额外写一次（ffmpeg要求）
    last_path = os.path.abspath(os.path.join(processed_dir, f'scene_{num_images:02d}.jpg'))
    f.write(f"file '{last_path}'\n")

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