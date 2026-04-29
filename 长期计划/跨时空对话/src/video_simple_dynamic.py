#!/usr/bin/env python3
"""
简单动态效果视频生成
分三步生成视频片段，然后拼接
"""
import subprocess
import os
import json
import sys

# 输入文件
img1 = "outputs/漫画/第三期/深夜加班的迷茫.jpg"
img2 = "outputs/漫画/第三期/夜加班遇古人.jpg"
img3 = "outputs/漫画/第三期/职场悟道图.jpg"
output = "outputs/视频/第三期短剧视频_dynamic.mp4"

# 确保目录存在
os.makedirs("temp/video_segments", exist_ok=True)
os.makedirs(os.path.dirname(output), exist_ok=True)

# 时长设置 (总时长约58秒)
scene1_duration = 18.0  # 场景1
scene2_duration = 20.0  # 场景2  
scene3_duration = 20.0  # 场景3
fps = 30

print("=== 简单动态效果视频生成 ===\n")
print(f"场景时长: 场景1={scene1_duration}秒, 场景2={scene2_duration}秒, 场景3={scene3_duration}秒")
print(f"总时长: {scene1_duration + scene2_duration + scene3_duration}秒")

# 步骤1: 生成场景1视频 (缓慢放大)
print(f"\n1. 生成场景1视频...")
scene1_cmd = [
    "ffmpeg",
    "-loop", "1", "-i", img1,
    "-t", str(scene1_duration),
    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='1+0.15*min(1,t/18)':d={}:s=1080x1920".format(int(scene1_duration * fps)),
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "23",
    "-r", str(fps),
    "-y",
    "temp/video_segments/scene1.mp4"
]

result = subprocess.run(scene1_cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f"错误: {result.stderr[:500]}")
    sys.exit(1)
print("  场景1生成成功")

# 步骤2: 生成场景2视频 (水平缓慢平移 + 轻微抖动)
print(f"\n2. 生成场景2视频...")
# 简单的水平平移效果
scene2_cmd = [
    "ffmpeg",
    "-loop", "1", "-i", img2,
    "-t", str(scene2_duration),
    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='1+0.05*sin(2*PI*t/5)':x='iw/2-(iw/zoom/2)+30*sin(2*PI*t/8)':d={}:s=1080x1920".format(int(scene2_duration * fps)),
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "23",
    "-r", str(fps),
    "-y",
    "temp/video_segments/scene2.mp4"
]

result = subprocess.run(scene2_cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f"错误: {result.stderr[:500]}")
    sys.exit(1)
print("  场景2生成成功")

# 步骤3: 生成场景3视频 (缓慢缩小)
print(f"\n3. 生成场景3视频...")
scene3_cmd = [
    "ffmpeg",
    "-loop", "1", "-i", img3,
    "-t", str(scene3_duration),
    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='1-0.15*min(1,t/20)':d={}:s=1080x1920".format(int(scene3_duration * fps)),
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "23",
    "-r", str(fps),
    "-y",
    "temp/video_segments/scene3.mp4"
]

result = subprocess.run(scene3_cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f"错误: {result.stderr[:500]}")
    sys.exit(1)
print("  场景3生成成功")

# 步骤4: 拼接三个视频片段
print(f"\n4. 拼接视频片段...")
concat_cmd = [
    "ffmpeg",
    "-i", "temp/video_segments/scene1.mp4",
    "-i", "temp/video_segments/scene2.mp4",
    "-i", "temp/video_segments/scene3.mp4",
    "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]",
    "-map", "[v]",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "23",
    "-r", str(fps),
    "-y",
    output
]

result = subprocess.run(concat_cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f"错误: {result.stderr[:500]}")
    sys.exit(1)
print("  视频拼接成功")

# 验证结果
print(f"\n5. 验证输出文件...")
if os.path.exists(output):
    probe_cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=duration,width,height",
                 "-of", "json", output]
    probe = subprocess.run(probe_cmd, capture_output=True, text=True)
    
    if probe.returncode == 0:
        info = json.loads(probe.stdout)
        stream = info["streams"][0]
        duration = float(stream["duration"])
        width = stream["width"]
        height = stream["height"]
        
        print(f"  文件: {output}")
        print(f"  时长: {duration:.2f}秒")
        print(f"  分辨率: {width}x{height}")
        
        # 检查验收标准
        passed = True
        print(f"\n验收标准检查:")
        
        if 50 <= duration <= 60:
            print(f"  ✓ 时长符合要求 (50-60秒)")
        else:
            print(f"  ⚠ 时长超出范围: {duration:.2f}秒")
            passed = False
            
        if width == 1080 and height == 1920:
            print(f"  ✓ 分辨率符合要求 (1080×1920)")
        else:
            print(f"  ⚠ 分辨率异常: {width}x{height}")
            passed = False
            
        # 检查文件大小
        file_size = os.path.getsize(output) / (1024 * 1024)
        print(f"  文件大小: {file_size:.2f}MB")
        
        if passed:
            print(f"\n✅ 视频符合所有验收标准!")
        else:
            print(f"\n⚠ 部分验收标准未满足")
    else:
        print("警告: 无法获取视频信息")
else:
    print("错误: 视频文件未生成")
    sys.exit(1)

print(f"\n=== 完成 ===")