#!/usr/bin/env python3
import subprocess
import os

# 输入文件路径
img1 = "outputs/漫画/第三期/深夜加班的迷茫.jpg"
img2 = "outputs/漫画/第三期/夜加班遇古人.jpg"
img3 = "outputs/漫画/第三期/职场悟道图.jpg"
audio = "temp/audio_cropped.mp3"
output = "outputs/视频/第三期短剧视频.mp4"

os.makedirs(os.path.dirname(output), exist_ok=True)

# 每张图片显示时长（秒）
durations = [16.0, 19.0, 20.0]

# 创建concat列表文件
concat_list = "temp/concat_list.txt"
with open(concat_list, 'w') as f:
    for i, img in enumerate([img1, img2, img3]):
        f.write(f"file '{img}'\n")
        f.write(f"duration {durations[i]}\n")
    # 最后一行需要重复最后一个文件，但不设置duration
    f.write(f"file '{img3}'\n")

# 构建ffmpeg命令：先创建无声视频，再混音
temp_video = "temp/video_noaudio.mp4"
cmd1 = [
    "ffmpeg",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_list,
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "23",
    "-pix_fmt", "yuv420p",
    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1",
    "-r", "30",
    "-y",
    temp_video
]

print("执行步骤1：创建无声视频")
result1 = subprocess.run(cmd1, capture_output=True, text=True)
if result1.returncode != 0:
    print("错误:", result1.stderr)
    exit(1)
else:
    print("无声视频生成成功")

# 步骤2：混音
cmd2 = [
    "ffmpeg",
    "-i", temp_video,
    "-i", audio,
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "128k",
    "-shortest",
    "-y",
    output
]

print("执行步骤2：混音")
result2 = subprocess.run(cmd2, capture_output=True, text=True)
if result2.returncode != 0:
    print("错误:", result2.stderr)
    exit(1)
else:
    print("视频合成成功")

# 验证输出
if os.path.exists(output):
    print(f"视频已生成: {output}")
    # 获取视频时长
    probe_v = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration", "-of", "csv=p=0", output]
    probe = subprocess.run(probe_v, capture_output=True, text=True)
    if probe.returncode == 0:
        print(f"视频时长: {probe.stdout.strip()}秒")
    # 验证分辨率
    probe_r = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", output]
    probe = subprocess.run(probe_r, capture_output=True, text=True)
    if probe.returncode == 0:
        print(f"分辨率: {probe.stdout.strip()}")
else:
    print("视频生成失败")