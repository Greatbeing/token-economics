#!/usr/bin/env python3
import subprocess
import os
import sys
from pathlib import Path

# 配置
image_dir = Path("outputs/漫画/第三周第一期")
output_dir = Path("outputs/视频")
output_dir.mkdir(parents=True, exist_ok=True)
video_output = output_dir / "第三周第一期视频.mp4"

# 图片顺序（根据剧本推测）
image_order = [
    "孔张向上管理.jpg",
    "职场小透明.jpg",
    "孔圣言教图.jpg",
    "孔张对话.jpg",
    "孔讲贡献点.jpg",
    "行笃敬量化成果.jpg",
    "孔圣汇报提醒.jpg",
    "古今清单交接.jpg"
]

# 检查图片是否存在
images = []
for img_name in image_order:
    img_path = image_dir / img_name
    if not img_path.exists():
        print(f"警告：图片不存在 {img_path}")
        # 尝试查找实际文件名（大小写可能不同）
        found = list(image_dir.glob(img_name.replace(".jpg", "*.jpg")))
        if found:
            img_path = found[0]
            print(f"使用找到的图片: {img_path.name}")
        else:
            print(f"跳过 {img_name}")
            continue
    images.append(str(img_path))

if len(images) < 1:
    print("错误：没有找到图片")
    sys.exit(1)

# 计算每张图片显示时长（总目标50秒）
target_duration = 50.0
duration_per_image = target_duration / len(images)
print(f"图片数量: {len(images)}")
print(f"每张图片显示时长: {duration_per_image:.2f}秒")

# 创建临时列表文件
list_file = Path("temp/concat_list.txt")
list_file.parent.mkdir(exist_ok=True)
with open(list_file, 'w', encoding='utf-8') as f:
    for img in images:
        f.write(f"file '{img}'\n")
        f.write(f"duration {duration_per_image}\n")
    # 最后一张图片需要额外一行（concat要求）
    f.write(f"file '{images[-1]}'\n")

# 第一步：将图片合成为视频（无音频）
print("步骤1：合成图片视频...")
temp_video = Path("temp/video_no_audio.mp4")
cmd1 = [
    "ffmpeg", "-f", "concat", "-safe", "0", "-i", str(list_file),
    "-vf", "fps=25,format=yuv420p,scale=1080:1920",  # 确保9:16竖屏
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "25",
    "-y", str(temp_video)
]
print("执行:", " ".join(cmd1))
result1 = subprocess.run(cmd1, capture_output=True, text=True)
if result1.returncode != 0:
    print("ffmpeg错误:", result1.stderr)
    sys.exit(1)
print("图片视频生成完成")

# 第二步：准备背景音乐
bgm_path = Path("temp/audio.mp3")
if not bgm_path.exists():
    print("警告：背景音乐文件不存在，将生成简单的背景音乐")
    # 生成一个50秒的柔和音乐
    cmd_bgm = [
        "ffmpeg", "-f", "lavfi", "-i",
        "sine=frequency=440:duration=50:volume=0.1",
        "-c:a", "libmp3lame", "-q:a", "4", "-y", str(bgm_path)
    ]
    subprocess.run(cmd_bgm, capture_output=True)
    print("已生成背景音乐")
else:
    print("使用现有背景音乐文件")

# 截取背景音乐到视频长度
bgm_cut = Path("temp/bgm_cut.mp3")
cmd2 = [
    "ffmpeg", "-i", str(bgm_path), "-t", str(target_duration),
    "-af", "afade=t=in:st=0:d=1,afade=t=out:st=" + str(target_duration-1) + ":d=1",
    "-y", str(bgm_cut)
]
print("截取背景音乐...")
subprocess.run(cmd2, capture_output=True)

# 第三步：生成音效（结尾叮声）
beep_path = Path("temp/beep.mp3")
cmd_beep = [
    "ffmpeg", "-f", "lavfi", "-i",
    "sine=frequency=1000:duration=0.5:volume=0.3",
    "-c:a", "libmp3lame", "-y", str(beep_path)
]
subprocess.run(cmd_beep, capture_output=True)

# 将音效放置在视频结尾（例如最后1秒）
beep_delay = target_duration - 0.5  # 在结束前0.5秒开始
beep_filtered = Path("temp/beep_delayed.mp3")
cmd_beep_delay = [
    "ffmpeg", "-i", str(beep_path), "-af", f"adelay={int(beep_delay*1000)}|{int(beep_delay*1000)}",
    "-y", str(beep_filtered)
]
subprocess.run(cmd_beep_delay, capture_output=True)

# 第四步：合并所有音频（背景音乐 + 音效）
mixed_audio = Path("temp/mixed_audio.mp3")
cmd_mix = [
    "ffmpeg", "-i", str(bgm_cut), "-i", str(beep_filtered),
    "-filter_complex", "amix=inputs=2:duration=first",
    "-y", str(mixed_audio)
]
print("混合音频...")
subprocess.run(cmd_mix, capture_output=True)

# 第五步：将音频与视频合并
print("步骤5：合并音视频...")
cmd3 = [
    "ffmpeg", "-i", str(temp_video), "-i", str(mixed_audio),
    "-c:v", "copy", "-c:a", "aac", "-shortest",
    "-y", str(video_output)
]
print("执行:", " ".join(cmd3))
result3 = subprocess.run(cmd3, capture_output=True, text=True)
if result3.returncode != 0:
    print("合并错误:", result3.stderr)
    sys.exit(1)

# 检查输出文件
if video_output.exists():
    # 获取视频时长
    cmd_check = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(video_output)]
    result = subprocess.run(cmd_check, capture_output=True, text=True)
    if result.returncode == 0:
        duration = float(result.stdout.strip())
        print(f"视频生成成功！文件: {video_output}")
        print(f"视频时长: {duration:.2f}秒")
        if 50 <= duration <= 52:
            print("时长符合要求 (50-52秒)")
        else:
            print("警告：时长不符合要求")
    else:
        print("无法读取视频时长")
else:
    print("错误：视频文件未生成")
    sys.exit(1)

print("完成！")