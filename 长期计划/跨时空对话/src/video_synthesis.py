#!/usr/bin/env python3
import subprocess
import os

# 输入文件路径
img1 = "outputs/视觉元素/第二期特别篇-AI焦虑门诊/孔庄AI门诊.jpg"
img2 = "outputs/视觉元素/第二期特别篇-AI焦虑门诊/古今AI压力观.jpg"
img3 = "outputs/视觉元素/第二期特别篇-AI焦虑门诊/庄蝶化AI水墨.jpg"
audio = "temp/audio.mp3"
output = "outputs/视频/第二期特别篇-AI焦虑门诊.mp4"

# 确保输出目录存在
os.makedirs(os.path.dirname(output), exist_ok=True)

# 参数
fps = 30
img1_duration = 16.0
img2_duration = 16.0
img3_duration = 16.9
xfade_duration = 1.0

# 计算总时长
total_duration = img1_duration + img2_duration + img3_duration + 2 * xfade_duration
print(f"总视频时长: {total_duration}秒")

# 构建复杂的filtergraph
filter_complex = f"""
[0:v]loop=loop=-1:size=1:start=0,trim=duration={img1_duration},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[v0];
[1:v]loop=loop=-1:size=1:start=0,trim=duration={img2_duration},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[v1];
[2:v]loop=loop=-1:size=1:start=0,trim=duration={img3_duration},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[v2];
[v0][v1]xfade=transition=fade:duration={xfade_duration}:offset={img1_duration - xfade_duration}[v01];
[v01][v2]xfade=transition=fade:duration={xfade_duration}:offset={img1_duration + img2_duration - xfade_duration}[v]
"""

# 简化：使用concat和xfade
# 另一种方法：使用concat和fade滤镜
filter_complex = f"""
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={img1_duration},setpts=PTS-STARTPTS[v0];
[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={img2_duration},setpts=PTS-STARTPTS[v1];
[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={img3_duration},setpts=PTS-STARTPTS[v2];
[v0][v1]xfade=transition=fade:duration={xfade_duration}:offset={img1_duration - xfade_duration}[v01];
[v01][v2]xfade=transition=fade:duration={xfade_duration}:offset={img1_duration + img2_duration - xfade_duration}[v]
"""

# 构建ffmpeg命令
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

print("执行命令:", " ".join(cmd))
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("错误:", result.stderr)
else:
    print("成功:", result.stdout)
    # 验证输出文件
    if os.path.exists(output):
        print(f"视频已生成: {output}")
        # 获取视频时长
        probe_cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration", "-of", "csv=p=0", output]
        probe = subprocess.run(probe_cmd, capture_output=True, text=True)
        if probe.returncode == 0:
            print(f"视频时长: {probe.stdout.strip()}秒")