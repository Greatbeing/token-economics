#!/usr/bin/env python3
import subprocess
import os

img1 = "outputs/漫画/第三期/深夜加班的迷茫.jpg"
img2 = "outputs/漫画/第三期/夜加班遇古人.jpg"
img3 = "outputs/漫画/第三期/职场悟道图.jpg"
audio = "temp/audio_cropped.mp3"
output = "outputs/视频/第三期短剧视频_fade.mp4"

os.makedirs(os.path.dirname(output), exist_ok=True)

# 每张图片显示时长
d1, d2, d3 = 16.0, 19.0, 20.0
xf = 1.0

# 构建filtergraph
filter_complex = f"""
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={d1},setpts=PTS-STARTPTS[v0];
[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={d2},setpts=PTS-STARTPTS[v1];
[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={d3},setpts=PTS-STARTPTS[v2];
[v0][v1]xfade=transition=fade:duration={xf}:offset={d1 - xf}[v01];
[v01][v2]xfade=transition=fade:duration={xf}:offset={d1 + d2 - xf}[v]
"""

cmd = [
    "ffmpeg",
    "-loop", "1", "-i", img1,
    "-loop", "1", "-i", img2,
    "-loop", "1", "-i", img3,
    "-i", audio,
    "-filter_complex", filter_complex,
    "-map", "[v]",
    "-map", "3:a",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "23",
    "-c:a", "aac",
    "-b:a", "128k",
    "-shortest",
    "-y",
    output
]

print("执行命令...")
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("错误:", result.stderr)
else:
    print("成功")
    if os.path.exists(output):
        print(f"视频已生成: {output}")
        # 验证视频时长
        probe_v = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration", "-of", "csv=p=0", output]
        probe = subprocess.run(probe_v, capture_output=True, text=True)
        if probe.returncode == 0:
            print(f"视频时长: {probe.stdout.strip()}秒")
        # 验证分辨率
        probe_r = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", output]
        probe = subprocess.run(probe_r, capture_output=True, text=True)
        if probe.returncode == 0:
            print(f"分辨率: {probe.stdout.strip()}")