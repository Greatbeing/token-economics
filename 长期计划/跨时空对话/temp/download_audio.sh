#!/bin/bash
# 从podcast文件中提取音频URL
json_file="temp/audio_final.podcast"
# 使用python解析JSON
python3 << EOF
import json
import sys
with open('$json_file', 'r', encoding='utf-8') as f:
    data = json.load(f)
audio_uri = data.get('audio_uri', '')
print(audio_uri)
EOF