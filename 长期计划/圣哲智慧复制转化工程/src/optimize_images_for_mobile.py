#!/usr/bin/env python3
"""
优化《儿童版中国哲学史》第一章HTML样张的图片，使其适合手机阅读
"""

import re
import base64
import os
import sys
from PIL import Image
import io
import json

def analyze_html_images(html_path):
    """分析HTML文件中的Data URI图片"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 查找Data URI图片
    pattern = r'src=\"(data:image/[^;]+;base64,[^\"]+)\"'
    matches = re.findall(pattern, html_content)
    
    print(f'找到 {len(matches)} 张Data URI图片')
    
    images_info = []
    total_size = 0
    
    for i, data_uri in enumerate(matches):
        # 解码base64数据
        header, data = data_uri.split(',', 1)
        img_data = base64.b64decode(data)
        
        # 从header提取格式
        if 'webp' in header.lower():
            fmt = 'webp'
        elif 'jpeg' in header.lower() or 'jpg' in header.lower():
            fmt = 'jpeg'
        elif 'png' in header.lower():
            fmt = 'png'
        else:
            fmt = 'unknown'
        
        # 获取图片尺寸
        try:
            img = Image.open(io.BytesIO(img_data))
            width, height = img.size
            img_format = img.format
        except Exception as e:
            width, height = 0, 0
            img_format = fmt
        
        size_kb = len(img_data) / 1024
        total_size += len(img_data)
        
        info = {
            'index': i,
            'data_uri': data_uri,
            'format': fmt,
            'original_size': len(img_data),
            'width': width,
            'height': height,
            'img_format': img_format
        }
        images_info.append(info)
        
        print(f'图片 {i+1}: {width}x{height} {fmt}, 大小={size_kb:.1f}KB')
    
    print(f'图片总大小: {total_size/1024:.1f}KB ({total_size/1024/1024:.2f}MB)')
    print(f'HTML文件大小: {os.path.getsize(html_path)/1024/1024:.2f}MB')
    
    return html_content, images_info

def compress_image(img_data, target_width=800, quality=80, format='webp'):
    """压缩图片，支持WebP和JPEG格式"""
    try:
        img = Image.open(io.BytesIO(img_data))
        
        # 计算目标高度，保持宽高比
        if img.width > target_width:
            ratio = target_width / img.width
            target_height = int(img.height * ratio)
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # 保存为压缩格式
        output_buffer = io.BytesIO()
        
        if format.lower() == 'webp':
            img.save(output_buffer, format='WEBP', quality=quality, method=6)
        elif format.lower() in ['jpeg', 'jpg']:
            # 转换为RGB模式（如果是RGBA）
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[3])
                else:
                    background.paste(img, mask=img.split()[1])
                img = background
            img.save(output_buffer, format='JPEG', quality=quality, optimize=True)
        else:
            # PNG保持原格式，但可以优化
            img.save(output_buffer, format='PNG', optimize=True)
        
        compressed_data = output_buffer.getvalue()
        output_buffer.close()
        
        return compressed_data, img.size
        
    except Exception as e:
        print(f'压缩图片时出错: {e}')
        return img_data, None

def optimize_images_for_mobile(html_content, images_info, output_dir):
    """优化图片并更新HTML内容"""
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    optimized_images = []
    total_original_size = 0
    total_optimized_size = 0
    
    for i, info in enumerate(images_info):
        print(f'\n处理图片 {i+1}...')
        
        original_size = info['original_size']
        original_format = info['format']
        total_original_size += original_size
        
        # 解码原始数据
        header, data = info['data_uri'].split(',', 1)
        original_img_data = base64.b64decode(data)
        
        # 选择目标格式：优先使用WebP，但某些情况下保持JPEG
        # WebP在保持质量的同时压缩率更高，适合移动端
        target_format = 'webp'
        
        # 压缩图片
        # 移动端目标宽度：800px（适应大多数手机屏幕）
        compressed_data, new_size = compress_image(
            original_img_data, 
            target_width=800, 
            quality=85,  # 高质量压缩
            format=target_format
        )
        
        optimized_size = len(compressed_data)
        total_optimized_size += optimized_size
        
        # 转换为Data URI
        mime_type = f'image/{target_format}'
        if target_format == 'jpg':
            mime_type = 'image/jpeg'
        
        encoded = base64.b64encode(compressed_data).decode('utf-8')
        new_data_uri = f'data:{mime_type};base64,{encoded}'
        
        # 保存优化后的图片到文件（用于备份）
        img_filename = f'image_{i+1}_optimized.{target_format}'
        img_path = os.path.join(output_dir, img_filename)
        with open(img_path, 'wb') as f:
            f.write(compressed_data)
        
        # 记录优化信息
        optimized_info = {
            'index': i,
            'original_size': original_size,
            'optimized_size': optimized_size,
            'reduction': 100 * (1 - optimized_size / original_size),
            'original_format': original_format,
            'optimized_format': target_format,
            'new_size': new_size,
            'new_data_uri': new_data_uri
        }
        optimized_images.append(optimized_info)
        
        print(f'  原始: {original_size/1024:.1f}KB ({original_format})')
        print(f'  优化: {optimized_size/1024:.1f}KB ({target_format})')
        print(f'  减少: {optimized_info["reduction"]:.1f}%')
        if new_size:
            print(f'  尺寸: {new_size[0]}x{new_size[1]}')
    
    # 在HTML中替换Data URI
    for opt_info in optimized_images:
        old_uri = images_info[opt_info['index']]['data_uri']
        new_uri = opt_info['new_data_uri']
        html_content = html_content.replace(old_uri, new_uri)
    
    print(f'\n优化总结:')
    print(f'  原始图片总大小: {total_original_size/1024:.1f}KB')
    print(f'  优化图片总大小: {total_optimized_size/1024:.1f}KB')
    print(f'  总体减少: {100 * (1 - total_optimized_size/total_original_size):.1f}%')
    
    return html_content, optimized_images

def create_mobile_css(original_css_path, output_css_path):
    """创建移动端优化的CSS文件"""
    with open(original_css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # 添加移动端媒体查询
    mobile_media_query = """
/* 移动端优化样式 */
@media screen and (max-width: 600px) {
    body {
        width: 100%;
        min-height: auto;
        margin: 0;
        padding: 15px;
        font-size: 16px; /* 稍大字号，便于手机阅读 */
    }
    
    .book-content {
        width: 100%;
        max-width: 100%;
        margin: 0 auto;
    }
    
    h1 {
        font-size: 28px;
        margin: 1.5em 0 1em 0;
    }
    
    h2 {
        font-size: 22px;
        margin: 1.2em 0 0.8em 0;
    }
    
    h3 {
        font-size: 18px;
        margin: 1em 0 0.6em 0;
    }
    
    p {
        font-size: 17px;
        line-height: 1.6;
        margin-bottom: 1.2em;
    }
    
    /* 特殊容器在移动端调整内边距 */
    .thought-theater,
    .think-about,
    .ancient-saying,
    .global-telescope,
    .wisdom-map,
    .philosophy-vocab {
        padding: 1em;
        margin: 1.2em 0;
    }
    
    /* 表格在移动端变为滚动 */
    .global-telescope .comparison-table,
    .philosophy-vocab table {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
    }
    
    /* 确保图片完全响应 */
    .chapter-illustration {
        max-width: 100% !important;
        height: auto !important;
    }
    
    .illustration-container {
        margin: 1em 0;
    }
}

/* 超小屏幕设备优化 */
@media screen and (max-width: 400px) {
    body {
        font-size: 15px;
        padding: 10px;
    }
    
    h1 {
        font-size: 24px;
    }
    
    h2 {
        font-size: 20px;
    }
    
    .thought-theater,
    .think-about,
    .ancient-saying,
    .global-telescope,
    .wisdom-map,
    .philosophy-vocab {
        padding: 0.8em;
    }
}
"""
    
    # 将移动端样式添加到原CSS末尾
    enhanced_css = css_content + mobile_media_query
    
    with open(output_css_path, 'w', encoding='utf-8') as f:
        f.write(enhanced_css)
    
    print(f'移动端CSS已创建: {output_css_path}')
    
    return enhanced_css

def generate_optimization_report(original_info, optimized_images, output_html_path, output_dir):
    """生成优化报告"""
    
    total_original = sum(info['original_size'] for info in original_info)
    total_optimized = sum(opt['optimized_size'] for opt in optimized_images)
    total_reduction = 100 * (1 - total_optimized / total_original)
    
    html_file_size = os.path.getsize(output_html_path)
    
    report = {
        'optimization_date': '2026-04-04',
        'original_html_size_mb': 3.19,
        'optimized_html_size_mb': html_file_size / 1024 / 1024,
        'image_optimization': {
            'total_original_images': len(original_info),
            'total_original_size_kb': total_original / 1024,
            'total_optimized_size_kb': total_optimized / 1024,
            'total_reduction_percent': total_reduction,
            'images': []
        },
        'mobile_optimizations': [
            '图片压缩至适合移动端加载的大小',
            '图片格式转换为WebP以获得更好的压缩比',
            '添加响应式图片属性 (max-width: 100%, height: auto)',
            '添加移动端媒体查询 (max-width: 600px)',
            '调整移动端字体大小和间距',
            '优化表格在窄屏设备的显示'
        ],
        'file_paths': {
            'optimized_html': output_html_path,
            'mobile_css': os.path.join(output_dir, 'style_mobile.css'),
            'optimized_images_dir': os.path.join(output_dir, 'images')
        }
    }
    
    for i, (orig, opt) in enumerate(zip(original_info, optimized_images)):
        report['image_optimization']['images'].append({
            'index': i+1,
            'original': {
                'format': orig['format'],
                'size_kb': orig['original_size'] / 1024,
                'dimensions': f"{orig['width']}x{orig['height']}"
            },
            'optimized': {
                'format': opt['optimized_format'],
                'size_kb': opt['optimized_size'] / 1024,
                'dimensions': f"{opt['new_size'][0]}x{opt['new_size'][1]}" if opt['new_size'] else '未知',
                'reduction_percent': opt['reduction']
            }
        })
    
    # 保存为JSON和Markdown
    report_json_path = os.path.join(output_dir, '图片优化报告.json')
    with open(report_json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 生成Markdown报告
    report_md = f"""# 图片优化报告

## 优化概述
- **优化日期**: 2026-04-04
- **目标**: 优化《儿童版中国哲学史》第一章HTML样张的图片，使其适合手机阅读
- **原始HTML文件大小**: {3.19:.2f} MB
- **优化后HTML文件大小**: {html_file_size / 1024 / 1024:.2f} MB

## 图片优化详情

### 总体统计
- 图片数量: {len(original_info)} 张
- 原始图片总大小: {total_original / 1024:.1f} KB
- 优化后图片总大小: {total_optimized / 1024:.1f} KB
- 总体压缩率: {total_reduction:.1f}%

### 各图片优化情况
| 序号 | 原始格式 | 原始大小 | 优化格式 | 优化大小 | 压缩率 | 尺寸变化 |
|------|----------|----------|----------|----------|--------|----------|
"""
    
    for img_report in report['image_optimization']['images']:
        report_md += f"""| {img_report['index']} | {img_report['original']['format']} | {img_report['original']['size_kb']:.1f}KB | {img_report['optimized']['format']} | {img_report['optimized']['size_kb']:.1f}KB | {img_report['optimized']['reduction_percent']:.1f}% | {img_report['original']['dimensions']} → {img_report['optimized']['dimensions']} |
"""
    
    report_md += f"""
## 移动端优化措施

1. **图片压缩**: 将图片压缩至适合移动端加载的大小
2. **格式转换**: 将JPEG格式转换为WebP格式，获得更好的压缩比
3. **响应式图片**: 所有图片添加 `max-width: 100%` 和 `height: auto` 属性
4. **移动端媒体查询**: 添加针对窄屏设备 (≤600px) 的CSS样式
5. **字体调整**: 移动端增大字号，提升可读性
6. **布局优化**: 调整特殊容器的内边距和边距
7. **表格优化**: 窄屏设备上表格支持水平滚动

## 文件路径

- **优化后的HTML文件**: `{output_html_path}`
- **移动端CSS文件**: `{os.path.join(output_dir, 'style_mobile.css')}`
- **优化图片目录**: `{os.path.join(output_dir, 'images')}`
- **本报告JSON版本**: `{report_json_path}`

## 测试建议

1. **移动端测试**: 在手机浏览器或开发者工具移动端模拟器中打开优化后的HTML文件
2. **加载速度**: 检查图片加载速度，确保无明显延迟
3. **视觉质量**: 确认图片压缩后无明显失真
4. **响应式布局**: 在不同屏幕宽度下测试布局适应性
"""
    
    report_md_path = os.path.join(output_dir, '图片优化报告.md')
    with open(report_md_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
    
    print(f'优化报告已生成: {report_md_path}')
    
    return report_md_path

def main():
    """主函数"""
    
    # 路径配置
    base_dir = '/app/data/files'
    original_html = os.path.join(base_dir, 'outputs/儿童哲学史/优化排版/第一章_专业排版.html')
    original_css = os.path.join(base_dir, 'outputs/儿童哲学史/优化排版/style_optimized.css')
    output_dir = os.path.join(base_dir, 'outputs/儿童哲学史/移动端优化')
    
    print('=' * 60)
    print('儿童版中国哲学史 - 第一章图片移动端优化')
    print('=' * 60)
    
    # 步骤1: 分析HTML图片
    print('\n[步骤1] 分析HTML文件中的图片...')
    html_content, images_info = analyze_html_images(original_html)
    
    # 步骤2: 优化图片
    print('\n[步骤2] 优化图片...')
    optimized_html, optimized_images = optimize_images_for_mobile(
        html_content, images_info, output_dir
    )
    
    # 步骤3: 创建移动端CSS
    print('\n[步骤3] 创建移动端CSS...')
    mobile_css_path = os.path.join(output_dir, 'style_mobile.css')
    create_mobile_css(original_css, mobile_css_path)
    
    # 步骤4: 更新HTML中的CSS引用
    optimized_html = optimized_html.replace('style_optimized.css', 'style_mobile.css')
    
    # 步骤5: 保存优化后的HTML
    print('\n[步骤4] 保存优化后的HTML文件...')
    output_html_path = os.path.join(output_dir, '第一章_移动端优化.html')
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(optimized_html)
    
    print(f'优化后的HTML已保存: {output_html_path}')
    
    # 步骤6: 生成优化报告
    print('\n[步骤5] 生成优化报告...')
    report_path = generate_optimization_report(
        images_info, optimized_images, output_html_path, output_dir
    )
    
    # 步骤7: 测试文件大小
    final_size = os.path.getsize(output_html_path) / 1024 / 1024
    print(f'\n[步骤6] 最终文件大小检查...')
    print(f'  优化后HTML文件大小: {final_size:.2f} MB')
    
    if final_size <= 1.5:
        print('  ✅ 达成目标: 文件大小 ≤ 1.5 MB')
    else:
        print(f'  ⚠️  未完全达成目标: 文件大小 {final_size:.2f} MB > 1.5 MB')
    
    print('\n' + '=' * 60)
    print('优化完成!')
    print('=' * 60)
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f'优化过程中出错: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)