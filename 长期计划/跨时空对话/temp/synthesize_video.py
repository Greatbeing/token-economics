#!/usr/bin/env python3
import os
import json
import subprocess
import sys
from pathlib import Path

# 读取podcast文件
podcast_path = "outputs/音频/第一期欲望管理.podcast"
with open(podcast_path, 'r', encoding='utf-8') as f:
    podcast_data = json.load(f)

audio_uri = podcast_data.get("audio_uri")
duration_ms = podcast_data.get("duration_ms")
print(f"音频URI: {audio_uri}")
print(f"音频时长: {duration_ms} ms ({duration_ms/1000:.2f} 秒)")

# 构造完整URL
full_url = f"https://space-static.coze.site/{audio_uri}"
print(f"完整URL: {full_url}")

# 下载音频文件
audio_path = "temp/audio.mp3"
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
response = requests.get(full_url, headers=headers)
if response.status_code == 200:
    with open(audio_path, 'wb') as f:
        f.write(response.content)
    print(f"音频下载成功: {audio_path}")
else:
    print(f"下载失败，状态码: {response.status_code}")
    print(response.text[:200])
    sys.exit(1)

# 图片目录
image_dir = "outputs/视觉元素/第一期"
image_files = [
    "古今快递Q版.jpg",
    "情绪垃圾箱.jpg",
    "消费观转变.jpg",
    "简福金言.jpg"
]
image_paths = [os.path.join(image_dir, f) for f in image_files]
for p in image_paths:
    if not os.path.exists(p):
        print(f"图片不存在: {p}")
        sys.exit(1)

# 调整图片大小为1080x1920（如果需要）
resized_dir = "temp/resized"
os.makedirs(resized_dir, exist_ok=True)
resized_paths = []
for i, img in enumerate(image_paths):
    out = os.path.join(resized_dir, f"{i+1:03d}.jpg")
    # 使用ffmpeg调整大小
    cmd = ["ffmpeg", "-i", img, "-vf", "scale=1080:1920", "-y", out]
    subprocess.run(cmd, check=True)
    resized_paths.append(out)
    print(f"调整大小: {img} -> {out}")

# 创建图片列表文件
list_file = "temp/image_list.txt"
with open(list_file, 'w') as f:
    for rp in resized_paths:
        f.write(f"file '{rp}'\n")

# 计算每张图片的持续时间（总音频时长除以图片数量）
audio_duration = duration_ms / 1000.0  # 秒
num_images = len(resized_paths)
image_duration = audio_duration / num_images
print(f"每张图片显示时间: {image_duration:.2f} 秒")

# 使用ffmpeg合成视频（图片序列+音频）
output_video = "outputs/视频/第一期-欲望管理.mp4"
os.makedirs(os.path.dirname(output_video), exist_ok=True)

# 构建ffmpeg命令：将图片列表作为输入，每张图片持续指定时间，同时混入音频
cmd = [
    "ffmpeg",
    "-f", "concat",
    "-safe", "0",
    "-i", list_file,
    "-i", audio_path,
    "-vf", f"setpts={image_duration}*PTS",  # 调整每张图片的显示时间
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-shortest",
    "-y",
    output_video
]
print("执行命令:", " ".join(cmd))
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("FFmpeg错误:")
    print(result.stderr)
    sys.exit(1)

print(f"视频合成成功: {output_video}")
print("完成。")