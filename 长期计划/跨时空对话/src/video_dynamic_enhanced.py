#!/usr/bin/env python3
"""
第三期视频动态效果增强版
基于原视频合成脚本，添加zoompan实现镜头运动
"""
import subprocess
import os
import json
import sys

# 输入文件路径
img1 = "outputs/漫画/第三期/深夜加班的迷茫.jpg"
img2 = "outputs/漫画/第三期/夜加班遇古人.jpg"
img3 = "outputs/漫画/第三期/职场悟道图.jpg"
audio = "temp/audio.mp3"
output = "outputs/视频/第三期短剧视频_dynamic.mp4"

# 确保输出目录存在
os.makedirs(os.path.dirname(output), exist_ok=True)

# 参数设置 - 调整时长以满足50-60秒要求
fps = 30
scene1_duration = 18.0  # 场景1：内耗爆发
scene2_duration = 20.0  # 场景2：圣贤降临
scene3_duration = 20.0  # 场景3：智慧融合
total_duration = scene1_duration + scene2_duration + scene3_duration
xfade_duration = 1.0

print(f"=== 第三期视频动态效果增强 ===\n")
print(f"场景时长:")
print(f"  场景1: {scene1_duration}秒 (内耗爆发)")
print(f"  场景2: {scene2_duration}秒 (圣贤降临)")
print(f"  场景3: {scene3_duration}秒 (智慧融合)")
print(f"  总时长: {total_duration}秒")

# 检查输入文件
for img in [img1, img2, img3]:
    if not os.path.exists(img):
        print(f"错误: 找不到图片文件 {img}")
        sys.exit(1)

# 检查音频文件
if not os.path.exists(audio):
    print("警告: 未找到音频文件，将生成无声视频")
    # 创建静音音频
    silent_cmd = [
        "ffmpeg", "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-t", str(total_duration), "-y", "temp/silent.mp3"
    ]
    subprocess.run(silent_cmd, capture_output=True)
    audio = "temp/silent.mp3"

# 构建filtergraph - 为每个场景添加不同的zoompan效果
filter_complex = f"""
# 场景1: 缓慢放大推镜，聚焦小张脸部 (从1.0到1.2)
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  trim=duration={scene1_duration},
  zoompan=z='1+0.2*min(1,t/{scene1_duration})':d={int(scene1_duration*fps)}:s=1080x1920,
  setpts=PTS-STARTPTS[v1];

# 场景2: 水平缓慢平移 + 轻微抖动 (模拟角色微动画)
[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  trim=duration={scene2_duration},
  zoompan=z='1+0.05*sin(2*PI*t/4)':x='iw/2-(iw/zoom/2)+30*sin(2*PI*t/6)':d={int(scene2_duration*fps)}:s=1080x1920,
  setpts=PTS-STARTPTS[v2];

# 场景3: 缓慢缩小拉远，呈现宏观视角 (从1.0到0.85)
[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  trim=duration={scene3_duration},
  zoompan=z='1-0.15*min(1,t/{scene3_duration})':d={int(scene3_duration*fps)}:s=1080x1920,
  setpts=PTS-STARTPTS[v3];

# 添加转场效果 (淡入淡出)
[v1][v2]xfade=transition=fade:duration={xfade_duration}:offset={scene1_duration - xfade_duration}[v12];
[v12][v3]xfade=transition=fade:duration={xfade_duration}:offset={scene1_duration + scene2_duration - xfade_duration}[v]
"""

print(f"\n生成动态效果视频...")

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

# 打印简化的命令信息
print("执行ffmpeg命令...")

# 执行命令
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f"错误: {result.stderr[:1000]}")
    
    # 如果动态效果失败，回退到静态拼接但保证时长
    print("\n动态效果失败，回退到静态拼接保证时长...")
    static_filter = f"""
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  trim=duration={scene1_duration},setpts=PTS-STARTPTS[v1];
[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  trim=duration={scene2_duration},setpts=PTS-STARTPTS[v2];
[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  trim=duration={scene3_duration},setpts=PTS-STARTPTS[v3];
[v1][v2]xfade=transition=fade:duration={xfade_duration}:offset={scene1_duration - xfade_duration}[v12];
[v12][v3]xfade=transition=fade:duration={xfade_duration}:offset={scene1_duration + scene2_duration - xfade_duration}[v]
"""
    
    cmd_static = [
        "ffmpeg",
        "-loop", "1", "-i", img1,
        "-loop", "1", "-i", img2,
        "-loop", "1", "-i", img3,
        "-i", audio,
        "-filter_complex", static_filter,
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
    
    result = subprocess.run(cmd_static, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"静态拼接也失败: {result.stderr[:500]}")
        sys.exit(1)
    else:
        print("静态拼接成功 (保证时长)")
else:
    print("动态效果视频生成成功")

# 验证输出文件
print(f"\n验证输出文件...")
if os.path.exists(output):
    # 获取视频信息
    probe_cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=duration,width,height,avg_frame_rate",
                 "-of", "json", output]
    probe = subprocess.run(probe_cmd, capture_output=True, text=True)
    
    if probe.returncode == 0:
        info = json.loads(probe.stdout)
        if "streams" in info and len(info["streams"]) > 0:
            stream = info["streams"][0]
            duration = float(stream["duration"])
            width = stream["width"]
            height = stream["height"]
            frame_rate = stream["avg_frame_rate"]
            
            print(f"  文件: {output}")
            print(f"  时长: {duration:.2f}秒")
            print(f"  分辨率: {width}x{height}")
            print(f"  帧率: {frame_rate}")
            
            # 检查验收标准
            checks = []
            if 50 <= duration <= 60:
                checks.append(("✓ 时长符合要求 (50-60秒)", True))
            else:
                checks.append((f"⚠ 时长超出范围: {duration:.2f}秒", False))
                
            if width == 1080 and height == 1920:
                checks.append(("✓ 分辨率符合要求 (1080×1920)", True))
            else:
                checks.append((f"⚠ 分辨率异常: {width}x{height}", False))
            
            # 检查文件大小
            file_size = os.path.getsize(output) / (1024 * 1024)  # MB
            print(f"  文件大小: {file_size:.2f}MB")
            
            # 动态效果描述
            print(f"\n动态效果设计:")
            print(f"  场景1: 缓慢放大推镜 (zoom 1.0→1.2)，聚焦小张脸部")
            print(f"  场景2: 水平平移 + 正弦抖动，模拟角色微动画")
            print(f"  场景3: 缓慢缩小拉远 (zoom 1.0→0.85)，呈现宏观视角")
            print(f"  转场: {xfade_duration}秒淡入淡出效果")
            
            print(f"\n验收标准检查:")
            for check, passed in checks:
                print(f"  {check}")
            
            if all(passed for _, passed in checks):
                print(f"\n✅ 视频符合所有验收标准!")
            else:
                print(f"\n⚠ 部分验收标准未满足")
        else:
            print("警告: 无法解析视频流信息")
    else:
        print("警告: 无法获取视频信息")
else:
    print(f"错误: 视频文件未生成")
    sys.exit(1)

print(f"\n=== 完成 ===")