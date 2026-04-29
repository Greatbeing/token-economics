#!/usr/bin/env python3
"""
第三期视频动态效果增强脚本
基于优化后的剧本和现有漫画素材，生成具有动态效果的视频
解决用户反馈的'视频主要是图片'问题
"""
import subprocess
import os
import json

# 输入文件路径
img1 = "outputs/漫画/第三期/深夜加班的迷茫.jpg"  # 场景1：内耗爆发
img2 = "outputs/漫画/第三期/夜加班遇古人.jpg"  # 场景2：圣贤降临
img3 = "outputs/漫画/第三期/职场悟道图.jpg"  # 场景3：智慧融合
audio = "temp/audio.mp3"  # 音频文件（如果存在）
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

print(f"视频参数:")
print(f"  场景1时长: {scene1_duration}秒")
print(f"  场景2时长: {scene2_duration}秒")
print(f"  场景3时长: {scene3_duration}秒")
print(f"  总时长: {total_duration}秒")
print(f"  转场时长: {xfade_duration}秒")

# 检查音频文件是否存在
audio_input = []
audio_map = []
if os.path.exists(audio):
    audio_input = ["-i", audio]
    audio_map = ["-map", "3:a"]
    print(f"使用音频文件: {audio}")
else:
    print("警告: 未找到音频文件，将生成无声视频")

# 构建复杂的filtergraph
# 场景1: 缓慢推镜，从全景推到小张脸部特写
# zoompan滤镜: zoom从1.0逐渐增加到1.3，持续整个场景1时长
zoom1_rate = 1.3  # 最终放大倍数
zoom1_frames = int(scene1_duration * fps)

# 场景2: 缓慢平移，从左（孔子）到右（庄子）
# 使用crop和scroll组合实现水平平移
# 假设图片宽度1600，我们需要显示1080宽度，所以可以移动520像素
scroll2_pixels = 520  # 水平移动像素数
scroll2_speed = scroll2_pixels / (scene2_duration * fps)  # 每帧移动像素

# 场景3: 镜头环绕和拉远
# 使用zoompan实现zoom out效果，同时轻微旋转
zoom3_rate = 0.8  # 最终缩小倍数
zoom3_frames = int(scene3_duration * fps)

# 构建filtergraph字符串
filter_complex = f"""
# 场景1处理: 放大推镜
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  zoompan=z='min(zoom+0.01,{zoom1_rate})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={zoom1_frames}:s=1080x1920,
  trim=duration={scene1_duration},setpts=PTS-STARTPTS[v1];

# 场景2处理: 水平平移
[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  scroll=horizontal=-{scroll2_pixels}*(t/{scene2_duration}):vertical=0,
  trim=duration={scene2_duration},setpts=PTS-STARTPTS[v2];

# 场景3处理: 缩小拉远
[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  zoompan=z='if(lte(zoom,1.0),{zoom3_rate},max(zoom-0.005,{zoom3_rate}))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={zoom3_frames}:s=1080x1920,
  trim=duration={scene3_duration},setpts=PTS-STARTPTS[v3];

# 添加转场效果
[v1][v2]xfade=transition=fade:duration={xfade_duration}:offset={scene1_duration - xfade_duration}[v12];
[v12][v3]xfade=transition=fade:duration={xfade_duration}:offset={scene1_duration + scene2_duration - xfade_duration}[v]
"""

print("生成视频...")

# 构建ffmpeg命令
cmd = [
    "ffmpeg",
    "-loop", "1", "-i", img1,
    "-loop", "1", "-i", img2,
    "-loop", "1", "-i", img3,
    *audio_input,
    "-filter_complex", filter_complex,
    "-map", "[v]",
    *audio_map,
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "23",
    "-c:a", "aac" if audio_input else "copy",
    "-b:a", "128k" if audio_input else None,
    "-shortest",
    "-y",
    output
]

# 移除None值
cmd = [arg for arg in cmd if arg is not None]

print("执行命令:", " ".join(cmd[:20]) + "..." if len(cmd) > 20 else " ".join(cmd))

result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("错误:", result.stderr[:500])
    # 尝试更简单的方法
    print("\n尝试备用方案...")
    # 使用简单的zoompan效果
    filter_complex_simple = f"""
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={scene1_duration},zoompan=z='1+0.3*sin(0.5*PI*t/{scene1_duration})':d={zoom1_frames}:s=1080x1920,setpts=PTS-STARTPTS[v1];
[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={scene2_duration},zoompan=z=1:x='iw/2-(iw/zoom/2)+100*sin(0.5*PI*t/{scene2_duration})':d={int(scene2_duration*fps)}:s=1080x1920,setpts=PTS-STARTPTS[v2];
[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={scene3_duration},zoompan=z='1-0.2*sin(0.5*PI*t/{scene3_duration})':d={zoom3_frames}:s=1080x1920,setpts=PTS-STARTPTS[v3];
[v1][v2]xfade=transition=fade:duration={xfade_duration}:offset={scene1_duration - xfade_duration}[v12];
[v12][v3]xfade=transition=fade:duration={xfade_duration}:offset={scene1_duration + scene2_duration - xfade_duration}[v]
"""
    cmd_simple = [
        "ffmpeg",
        "-loop", "1", "-i", img1,
        "-loop", "1", "-i", img2,
        "-loop", "1", "-i", img3,
        *audio_input,
        "-filter_complex", filter_complex_simple,
        "-map", "[v]",
        *audio_map,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac" if audio_input else "copy",
        "-b:a", "128k" if audio_input else None,
        "-shortest",
        "-y",
        output
    ]
    cmd_simple = [arg for arg in cmd_simple if arg is not None]
    result = subprocess.run(cmd_simple, capture_output=True, text=True)
    if result.returncode != 0:
        print("备用方案也失败:", result.stderr[:500])
        # 最后尝试：简单的静态图片拼接
        print("\n尝试最简单的静态拼接...")
        filter_complex_static = f"""
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={scene1_duration},setpts=PTS-STARTPTS[v1];
[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={scene2_duration},setpts=PTS-STARTPTS[v2];
[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={scene3_duration},setpts=PTS-STARTPTS[v3];
[v1][v2]xfade=transition=fade:duration={xfade_duration}:offset={scene1_duration - xfade_duration}[v12];
[v12][v3]xfade=transition=fade:duration={xfade_duration}:offset={scene1_duration + scene2_duration - xfade_duration}[v]
"""
        cmd_static = [
            "ffmpeg",
            "-loop", "1", "-i", img1,
            "-loop", "1", "-i", img2,
            "-loop", "1", "-i", img3,
            *audio_input,
            "-filter_complex", filter_complex_static,
            "-map", "[v]",
            *audio_map,
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac" if audio_input else "copy",
            "-b:a", "128k" if audio_input else None,
            "-shortest",
            "-y",
            output
        ]
        cmd_static = [arg for arg in cmd_static if arg is not None]
        result = subprocess.run(cmd_static, capture_output=True, text=True)
        if result.returncode != 0:
            print("所有方案均失败:", result.stderr[:500])
            exit(1)
        else:
            print("静态拼接成功")
else:
    print("动态效果视频生成成功")

# 验证输出文件
if os.path.exists(output):
    print(f"\n视频已生成: {output}")
    # 获取视频时长
    probe_cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration,width,height", "-of", "json", output]
    probe = subprocess.run(probe_cmd, capture_output=True, text=True)
    if probe.returncode == 0:
        info = json.loads(probe.stdout)
        stream = info["streams"][0]
        duration = float(stream["duration"])
        width = stream["width"]
        height = stream["height"]
        print(f"  时长: {duration:.2f}秒")
        print(f"  分辨率: {width}x{height}")
        
        # 检查是否符合验收标准
        if 50 <= duration <= 60:
            print("  ✓ 时长符合要求 (50-60秒)")
        else:
            print(f"  ⚠ 时长超出范围: {duration:.2f}秒")
            
        if width == 1080 and height == 1920:
            print("  ✓ 分辨率符合要求 (1080×1920)")
        else:
            print(f"  ⚠ 分辨率异常: {width}x{height}")
    else:
        print("警告: 无法获取视频信息")
else:
    print("错误: 视频文件未生成")
    exit(1)

print("\n完成!")