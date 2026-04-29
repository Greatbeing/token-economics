#!/bin/bash
set -e

# 创建目录
mkdir -p temp/resized
mkdir -p outputs/视频

# 图片文件数组
images=(
    "outputs/视觉元素/第一期/古今快递Q版.jpg"
    "outputs/视觉元素/第一期/情绪垃圾箱.jpg"
    "outputs/视觉元素/第一期/消费观转变.jpg"
    "outputs/视觉元素/第一期/简福金言.jpg"
)

# 调整图片大小至1080x1920
for i in "${!images[@]}"; do
    input="${images[$i]}"
    output="temp/resized/img$(printf '%03d' $((i+1))).jpg"
    ffmpeg -i "$input" -vf "scale=1080:1920:force_original_aspect_ratio=pad,format=rgb24" -y "$output" 2>/dev/null
    echo "调整大小: $input -> $output"
done

# 音频文件
audio="temp/audio.mp3"
# 获取音频时长
duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$audio")
echo "音频时长: $duration 秒"

# 计算每张图片的持续时间
num_images=${#images[@]}
image_duration=$(echo "$duration / $num_images" | bc -l)
echo "每张图片显示时间: $image_duration 秒"

# 创建图片列表文件（concat格式）
list_file="temp/image_list.txt"
> "$list_file"
for i in $(seq 1 $num_images); do
    echo "file 'temp/resized/img$(printf '%03d' $i).jpg'" >> "$list_file"
    echo "duration $image_duration" >> "$list_file"
done

# 使用concat协议合成视频（图片序列）
temp_video="temp/video_noaudio.mp4"
ffmpeg -f concat -safe 0 -i "$list_file" -c:v libx264 -pix_fmt yuv420p -vf "fps=30" -y "$temp_video" 2>/dev/null

# 合并音频
output_video="outputs/视频/第一期-欲望管理.mp4"
ffmpeg -i "$temp_video" -i "$audio" -c:v copy -c:a aac -shortest -y "$output_video" 2>/dev/null

echo "视频合成完成: $output_video"

# 验证视频信息
ffprobe -v error -show_entries format=duration,stream=codec_type,height,width -of default=noprint_wrappers=1 "$output_video"