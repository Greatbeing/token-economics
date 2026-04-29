#!/usr/bin/env python3
"""
第三期视频动态效果增强 - 最终版本
实现镜头运动和简单微动画
"""
import subprocess
import os
import json
import sys

# 输入文件路径
img1 = "outputs/漫画/第三期/深夜加班的迷茫.jpg"  # 场景1
img2 = "outputs/漫画/第三期/夜加班遇古人.jpg"  # 场景2  
img3 = "outputs/漫画/第三期/职场悟道图.jpg"  # 场景3
audio = "temp/audio.mp3"  # 音频文件
output = "outputs/视频/第三期短剧视频_dynamic.mp4"

# 确保输出目录存在
os.makedirs(os.path.dirname(output), exist_ok=True)

# 参数设置
fps = 30
scene1_duration = 18.0  # 场景1时长
scene2_duration = 22.0  # 场景2时长  
scene3_duration = 20.0  # 场景3时长
total_duration = scene1_duration + scene2_duration + scene3_duration
xfade_duration = 1.0  # 转场时长

print(f"=== 第三期视频动态效果增强 ===\n")
print(f"场景分配:")
print(f"  场景1: {scene1_duration}秒 (内耗爆发)")
print(f"  场景2: {scene2_duration}秒 (圣贤降临)")
print(f"  场景3: {scene3_duration}秒 (智慧融合)")
print(f"  总时长: {total_duration}秒")
print(f"  转场: {xfade_duration}秒淡入淡出")

# 检查输入文件
for img in [img1, img2, img3]:
    if not os.path.exists(img):
        print(f"错误: 找不到图片文件 {img}")
        sys.exit(1)

# 检查音频文件，如果不存在则创建静音
if not os.path.exists(audio):
    print("警告: 未找到音频文件，将使用静音音频")
    # 创建静音音频
    silent_cmd = [
        "ffmpeg", "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-t", str(total_duration), "-y", "temp/silent.mp3"
    ]
    subprocess.run(silent_cmd, capture_output=True)
    audio = "temp/silent.mp3"

# 构建filtergraph
# 使用更简单的zoompan表达式
filter_complex = f"""
# 场景1: 缓慢放大推镜 (从1.0到1.2)
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  trim=duration={scene1_duration},
  zoompan=z='1+0.2*(t/{scene1_duration})':d={int(scene1_duration*fps)}:s=1080x1920,
  setpts=PTS-STARTPTS[v1];

# 场景2: 水平平移 + 轻微抖动模拟微动画
[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  trim=duration={scene2_duration},
  split=2[scene2_base][scene2_mask];

# 基础场景2视频
[scene2_base]setpts=PTS-STARTPTS[scene2_base_pts];

# 为孔子添加轻微上下浮动 (微动画)
[scene2_mask]crop=200:300:300:500,  # 估计的孔子区域
  zoompan=z='1+0.05*sin(2*PI*t/3)':d={int(scene2_duration*fps)}:s=200x300,
  setpts=PTS-STARTPTS[confucius_anim];

# 为庄子添加轻微缩放 (微动画)  
[scene2_mask]crop=200:300:600:500,  # 估计的庄子区域
  zoompan=z='1+0.05*sin(2*PI*t/4+0.5)':d={int(scene2_duration*fps)}:s=200x300,
  setpts=PTS-STARTPTS[zhuangzi_anim];

# 叠加动画到基础视频
[scene2_base_pts][confucius_anim]overlay=300:500:enable='between(t,5,8)'[scene2_with_confucius];
[scene2_with_confucius][zhuangzi_anim]overlay=600:500:enable='between(t,12,15)'[scene2_final];

# 场景3: 缓慢缩小拉远 (从1.0到0.8)
[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  trim=duration={scene3_duration},
  zoompan=z='1-0.2*(t/{scene3_duration})':d={int(scene3_duration*fps)}:s=1080x1920,
  setpts=PTS-STARTPTS[v3];

# 添加转场效果
[v1][scene2_final]xfade=transition=fade:duration={xfade_duration}:offset={scene1_duration - xfade_duration}[v12];
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

# 打印简化的命令
print("执行命令: ffmpeg [输入文件] -filter_complex ...")

# 执行命令
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f"错误: {result.stderr[:1000]}")
    print("\n尝试更简单的方案...")
    
    # 备用方案: 只做简单的zoompan效果
    simple_filter = f"""
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  trim=duration={scene1_duration},
  zoompan=z='1+0.1*(t/{scene1_duration})':d={int(scene1_duration*fps)}:s=1080x1920,
  setpts=PTS-STARTPTS[v1];
[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  trim=duration={scene2_duration},
  zoompan=z='1+0.05*sin(2*PI*t/5)':x='iw/2-(iw/zoom/2)+50*sin(2*PI*t/7)':d={int(scene2_duration*fps)}:s=1080x1920,
  setpts=PTS-STARTPTS[v2];
[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  trim=duration={scene3_duration},
  zoompan=z='1-0.15*(t/{scene3_duration})':d={int(scene3_duration*fps)}:s=1080x1920,
  setpts=PTS-STARTPTS[v3];
[v1][v2]xfade=transition=fade:duration={xfade_duration}:offset={scene1_duration - xfade_duration}[v12];
[v12][v3]xfade=transition=fade:duration={xfade_duration}:offset={scene1_duration + scene2_duration - xfade_duration}[v]
"""
    
    cmd_simple = [
        "ffmpeg",
        "-loop", "1", "-i", img1,
        "-loop", "1", "-i", img2,
        "-loop", "1", "-i", img3,
        "-i", audio,
        "-filter_complex", simple_filter,
        "-map", "[v]",
        "-map", "3:a",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crst", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        "-y",
        output
    ]
    
    result = subprocess.run(cmd_simple, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"备用方案也失败: {result.stderr[:1000]}")
        print("\n尝试最简单的静态图片拼接...")
        
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
            print(f"静态拼接也失败: {result.stderr[:1000]}")
            sys.exit(1)
        else:
            print("静态图片拼接成功")
    else:
        print("简单动态效果生成成功")
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