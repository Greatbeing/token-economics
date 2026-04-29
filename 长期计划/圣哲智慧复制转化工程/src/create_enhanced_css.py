#!/usr/bin/env python3
"""
创建增强CSS文件
"""

import os

def main():
    # 读取现有的CSS
    with open('outputs/儿童哲学史/手机优化/style_phone.css', 'r', encoding='utf-8') as f:
        original_css = f.read()
    
    # 增强规则
    enhancement = """
/* =================================================================== */
/* 移动端严格响应式控制 - 增强版 */
/* 确保在手机设备上图片完全适配，无水平滚动 */
/* =================================================================== */

/* 1. 容器严格宽度限制 - 防止任何溢出 */
.illustration-container {
    width: 100% !important;
    box-sizing: border-box !important;
    max-width: 100vw !important;
    overflow: hidden !important;
    padding-left: 5px !important;
    padding-right: 5px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* 2. 图片双重保险 - 强制响应式 */
.chapter-illustration {
    max-width: calc(100% - 10px) !important;
    height: auto !important;
    display: block !important;
    margin-left: auto !important;
    margin-right: auto !important;
    border-radius: 6px !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
}

/* 3. 全局图片安全控制 */
img {
    max-width: 100% !important;
    height: auto !important;
}

/* 4. 内容容器确保不溢出 */
.book-content {
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 auto !important;
    padding: 0 5px !important;
    box-sizing: border-box !important;
}

/* 5. 防止任何水平滚动 */
body {
    overflow-x: hidden !important;
    max-width: 100vw !important;
}

/* =================================================================== */
/* 超小屏幕设备专门优化 (≤400px) */
/* =================================================================== */
@media screen and (max-width: 400px) {
    /* 进一步缩小图片以适配最小屏幕 */
    .chapter-illustration {
        max-width: 95% !important;
    }
    
    /* 减少容器内边距 */
    .illustration-container {
        padding-left: 3px !important;
        padding-right: 3px !important;
    }
    
    /* 调整字体大小确保可读性 */
    body {
        font-size: 15px !important;
        padding: 10px !important;
    }
    
    h1 {
        font-size: 24px !important;
    }
    
    h2 {
        font-size: 20px !important;
    }
    
    h3 {
        font-size: 17px !important;
    }
    
    /* 表格在小屏幕上滚动 */
    .global-telescope .comparison-table,
    .philosophy-vocab table {
        display: block !important;
        overflow-x: auto !important;
        white-space: nowrap !important;
    }
}

/* =================================================================== */
/* 最小屏幕设备额外优化 (≤375px) - iPhone SE等 */
/* =================================================================== */
@media screen and (max-width: 375px) {
    /* 为最小屏幕设备额外优化 */
    .chapter-illustration {
        max-width: 92% !important;
    }
    
    /* 进一步减少内边距 */
    .illustration-container {
        padding-left: 2px !important;
        padding-right: 2px !important;
    }
    
    /* 微调字体大小 */
    body {
        font-size: 14px !important;
        padding: 8px !important;
    }
    
    h1 {
        font-size: 22px !important;
    }
    
    h2 {
        font-size: 19px !important;
    }
    
    h3 {
        font-size: 16px !important;
    }
}

/* =================================================================== */
/* 打印优化 - 保持响应式 */
/* =================================================================== */
@media print {
    .chapter-illustration {
        max-width: 100% !important;
        box-shadow: none !important;
    }
    
    .illustration-container {
        page-break-inside: avoid !important;
    }
}
"""
    
    # 合并CSS
    enhanced_css = original_css + enhancement
    
    # 确保输出目录存在
    output_dir = 'outputs/儿童哲学史/移动端完善'
    os.makedirs(output_dir, exist_ok=True)
    
    # 写入文件
    output_path = os.path.join(output_dir, 'style_enhanced.css')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(enhanced_css)
    
    print(f"增强CSS已创建: {output_path}")
    print(f"文件大小: {len(enhanced_css)/1024:.2f}KB")
    
    # 同时创建一个更简洁的移动端专用CSS
    mobile_only_css = """
/* 儿童版中国哲学史 - 移动端专用样式 */
/* 专为手机设备优化，确保图片完全适配 */

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: "宋体", "SimSun", serif;
    font-size: 16px;
    line-height: 1.6;
    color: #333;
    background-color: #fff;
    padding: 15px;
    max-width: 100vw;
    overflow-x: hidden;
}

.book-content {
    width: 100%;
    max-width: 100%;
    margin: 0 auto;
}

/* 标题 */
h1 {
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 28px;
    font-weight: bold;
    text-align: center;
    margin: 1.5em 0 1em 0;
    color: #2c3e50;
}

h2 {
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 22px;
    font-weight: bold;
    margin: 1.2em 0 0.8em 0;
    color: #34495e;
    border-left: 4px solid #3498db;
    padding-left: 0.5em;
}

h3 {
    font-family: "黑体", "SimHei", sans-serif;
    font-size: 18px;
    font-weight: bold;
    margin: 1em 0 0.6em 0;
    color: #2c3e50;
}

/* 段落 */
p {
    margin: 0 0 1.2em 0;
    text-indent: 2em;
}

/* 插图容器 - 严格限制 */
.illustration-container {
    width: 100%;
    max-width: 100vw;
    overflow: hidden;
    padding: 0 5px;
    margin: 1.5em auto;
    text-align: center;
}

.illustration-title {
    font-family: "黑体", sans-serif;
    font-size: 14px;
    color: #2c3e50;
    margin-bottom: 0.5em;
    font-weight: bold;
}

/* 图片 - 强制响应式 */
.chapter-illustration {
    max-width: calc(100% - 10px) !important;
    height: auto !important;
    display: block;
    margin: 0 auto;
    border-radius: 6px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.illustration-caption {
    font-size: 13px;
    color: #7f8c8d;
    font-style: italic;
    margin-top: 0.5em;
}

/* 特殊元素 */
.thought-theater,
.think-about,
.ancient-saying,
.global-telescope,
.wisdom-map,
.philosophy-vocab {
    padding: 1em;
    margin: 1.2em 0;
    border-radius: 8px;
    page-break-inside: avoid;
}

/* 表格响应式 */
.global-telescope .comparison-table,
.philosophy-vocab table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
}

/* 超小屏幕优化 (≤400px) */
@media screen and (max-width: 400px) {
    body {
        font-size: 15px;
        padding: 10px;
    }
    
    h1 { font-size: 24px; }
    h2 { font-size: 20px; }
    h3 { font-size: 17px; }
    
    .chapter-illustration {
        max-width: 95% !important;
    }
    
    .illustration-container {
        padding: 0 3px;
    }
}

/* 最小屏幕优化 (≤375px) - iPhone SE */
@media screen and (max-width: 375px) {
    body {
        font-size: 14px;
        padding: 8px;
    }
    
    h1 { font-size: 22px; }
    h2 { font-size: 19px; }
    h3 { font-size: 16px; }
    
    .chapter-illustration {
        max-width: 92% !important;
    }
    
    .illustration-container {
        padding: 0 2px;
    }
}
"""
    
    mobile_css_path = os.path.join(output_dir, 'style_mobile_only.css')
    with open(mobile_css_path, 'w', encoding='utf-8') as f:
        f.write(mobile_only_css)
    
    print(f"移动端专用CSS已创建: {mobile_css_path}")

if __name__ == '__main__':
    main()