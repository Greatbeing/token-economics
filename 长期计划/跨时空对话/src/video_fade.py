#!/usr/bin/env python3
import subprocess
import os

img1 = "outputs/视觉元素/第二期特别篇-AI焦虑门诊/孔庄AI门诊.jpg"
img2 = "outputs/视觉元素/第二期特别篇-AI焦虑门诊/古今AI压力观.jpg"
img3 = "outputs/视觉元素/第二期特别篇-AI焦虑门诊/庄蝶化AI水墨.jpg"
audio = "temp/audio.mp3"
output = "outputs/视频/第二期特别篇-AI焦虑门诊_fade.mp4"

os.makedirs(os.path.dirname(output), exist_ok=True)

# 获取音频时长
probe_cmd = ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=duration", "-of", "csv=p=0", audio]
probe = subprocess.run(probe_cmd, capture_output=True, text=True)
if probe.returncode != 0:
    audio_duration = 50.0
else:
    audio_duration = float(probe.stdout.strip())
print(f"音频时长: {audio_duration}秒")

segment_duration = audio_duration / 3.0
print(f"每张图片显示时长: {segment_duration}秒")

# 构建filtergraph，包含淡入淡出效果
# 淡入持续时间1秒，淡出持续时间1秒
fade_duration = 1.0
filter_complex = f"""
[0:v]loop=loop=-1:size=1:start=0,trim=duration={segment_duration},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fade=t=in:st=0:d={fade_duration}[v0];
[1:v]loop=loop=-1:size=1:start=0,trim=duration={segment_duration},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fade=t=in:st=0:d={fade_duration},fade=t=out:st={segment_duration - fade_duration}:d={fade_duration}[v1];
[2:v]loop=loop=-1:size=1:start=0,trim=duration={segment_duration},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fade=t=out:st={segment_duration - fade_duration}:d={fade_duration}[v2];
[v0][v1][v2]concat=n=3:v=1:a=0[v]
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
    "-crf", "20",  # 提高质量
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