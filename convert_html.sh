#!/bin/bash

HTML_DIR="./长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/优化版/"
OUTPUT_DIR="./converted_md"

mkdir -p $OUTPUT_DIR

for i in {1..12}; do
    input="${HTML_DIR}第${i}章样张_优化.html"
    output="${OUTPUT_DIR}/chapter_${i}.md"
    
    echo "转换第${i}章..."
    
    # 使用pandoc转换，提取纯文本
    pandoc -f html -t markdown --strip-comments \
        --wrap=none \
        --atx-headers \
        -o "$output" "$input"
    
    # 移除base64图片数据
    sed -i 's/data:image\/[^)]*//g' "$output"
    sed -i 's/\[图片: *\]/\[图片\]/g' "$output"
    
    # 清理多余空行
    sed -i '/^$/N;/^\n$/d' "$output"
    
    echo "  -> $output ($(wc -c < "$output") bytes)"
done

echo "转换完成！"
