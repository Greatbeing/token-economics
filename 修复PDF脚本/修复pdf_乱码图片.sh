#!/bin/bash
# 修复PDF乱码和图片比例问题
# 使用正确的UTF-8编码和图片样式参数

echo "=== 开始修复PDF生成 ==="

# 设置工作目录
WORK_DIR="长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史"
HTML_DIR="$WORK_DIR/排版阶段/章节HTML/修正版"
OUTPUT_DIR="$WORK_DIR/最终交付"
CSS_FILE="$HTML_DIR/style.css"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 检查CSS是否存在
if [ ! -f "$CSS_FILE" ]; then
    echo "错误：CSS文件不存在: $CSS_FILE"
    exit 1
fi

# 检查wkhtmltopdf是否可用
if ! command -v wkhtmltopdf &> /dev/null; then
    echo "错误：wkhtmltopdf 未安装"
    exit 1
fi

# 获取中文字体列表
echo "检查系统字体..."
fc-list :lang=zh 2>/dev/null | head -5

# 创建修复后的PDF
CHAPTER_FILE="$HTML_DIR/第1章样张_fixed.html"
OUTPUT_PDF="$OUTPUT_DIR/测试_第一章_fixed.pdf"

if [ -f "$CHAPTER_FILE" ]; then
    echo "开始转换第1章为PDF..."
    
    # 使用正确的参数生成PDF
    # --enable-local-file-access: 允许访问本地文件
    # --encoding utf-8: 设置编码
    # --page-size A4: 设置页面大小
    # --orientation Portrait: 纵向
    # --print-media-type: 使用打印样式
    # --image-quality 90: 图片质量
    # --javascript-delay 2000: 等待JS执行
    
    wkhtmltopdf \
        --enable-local-file-access \
        --encoding utf-8 \
        --page-size A4 \
        --orientation Portrait \
        --print-media-type \
        --image-quality 90 \
        --javascript-delay 2000 \
        --margin-top 15mm \
        --margin-bottom 15mm \
        --margin-left 15mm \
        --margin-right 15mm \
        --title "和古人一起想问题_第一章" \
        "$CHAPTER_FILE" "$OUTPUT_PDF"
    
    if [ $? -eq 0 ]; then
        echo "PDF生成成功: $OUTPUT_PDF"
        ls -lh "$OUTPUT_PDF"
    else
        echo "PDF生成失败!"
        exit 1
    fi
else
    echo "错误：HTML文件不存在: $CHAPTER_FILE"
    exit 1
fi

echo "=== 完成 ==="
