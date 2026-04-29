#!/usr/bin/env python3
import subprocess
import os

input_audio = "temp/audio_final.mp3"
output_audio = "temp/audio_final_fast.mp3"
target_duration = 58.0  # 目标时长秒

# 获取当前时长
cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_audio]
result = subprocess.run(cmd, capture_output=True, text=True)
current_duration = float(result.stdout.strip())
print(f"当前音频时长: {current_duration}秒")
print(f"目标音频时长: {target_duration}秒")
speed_factor = current_duration / target_duration
print(f"需要加速倍数: {speed_factor:.2f}")

# 计算atempo滤镜链
# atempo每个最大2.0
tempo_chain = []
remaining = speed_factor
while remaining > 2.0:
    tempo_chain.append(2.0)
    remaining /= 2.0
tempo_chain.append(remaining)
print(f"atempo链: {tempo_chain}")

# 构建滤镜字符串
filter_str = ",".join([f"atempo={t:.3f}" for t in tempo_chain])
print(f"使用滤镜: {filter_str}")

# 执行加速
cmd = ["ffmpeg", "-i", input_audio, "-filter:a", filter_str, "-c:a", "libmp3lame", "-q:a", "2", output_audio]
print("执行加速命令...")
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f"错误: {result.stderr}")
else:
    print("音频加速完成")
    # 验证新时长
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", output_audio]
    result = subprocess.run(cmd, capture_output=True, text=True)
    new_duration = float(result.stdout.strip())
    print(f"新音频时长: {new_duration}秒")
    # 替换原文件
    os.rename(output_audio, input_audio)
    print(f"已替换为加速版: {input_audio}")