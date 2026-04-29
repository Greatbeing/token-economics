#!/usr/bin/env python3
"""
图片压缩脚本
将图片压缩至手机友好尺寸（380px宽）
"""

import os
from PIL import Image
import json

def compress_image(input_path, output_path, target_width=380, quality=80):
    """
    压缩图片到目标宽度
    """
    try:
        # 打开图片
        with Image.open(input_path) as img:
            # 计算新高度以保持宽高比
            original_width, original_height = img.size
            aspect_ratio = original_height / original_width
            target_height = int(target_width * aspect_ratio)
            
            # 调整尺寸
            resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # 保存为WebP格式
            resized_img.save(output_path, 'WEBP', quality=quality)
            
            # 获取压缩后文件大小
            compressed_size = os.path.getsize(output_path) / 1024  # KB
            
            return {
                'success': True,
                'original_size': (original_width, original_height),
                'compressed_size': (target_width, target_height),
                'file_size_kb': compressed_size,
                'format': 'WEBP',
                'quality': quality
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def create_data_uri(image_path):
    """
    创建图片的Data URI
    """
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # 编码为base64
        import base64
        base64_data = base64.b64encode(image_data).decode('utf-8')
        
        # 确定MIME类型
        if image_path.lower().endswith('.webp'):
            mime_type = 'image/webp'
        elif image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
            mime_type = 'image/jpeg'
        elif image_path.lower().endswith('.png'):
            mime_type = 'image/png'
        else:
            mime_type = 'image/webp'
        
        data_uri = f'data:{mime_type};base64,{base64_data}'
        
        return {
            'success': True,
            'data_uri': data_uri,
            'length': len(data_uri)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    print("开始压缩图片以适应手机屏幕...")
    
    # 输入输出路径
    input_dir = 'outputs/儿童哲学史/手机优化/images/'
    output_dir = 'outputs/儿童哲学史/移动端完善/images/'
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 图片文件列表
    image_files = [
        'phone_image_1_optimized.webp',
        'phone_image_2_optimized.webp',
        'phone_image_3_optimized.webp',
        'phone_image_4_optimized.webp'
    ]
    
    results = []
    data_uris = []
    
    for i, filename in enumerate(image_files, 1):
        input_path = os.path.join(input_dir, filename)
        
        if not os.path.exists(input_path):
            print(f"警告: 文件不存在: {input_path}")
            continue
        
        # 输出文件名
        output_filename = f'phone_image_{i}_compressed.webp'
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"处理图片 {i}/{len(image_files)}: {filename}")
        
        # 压缩图片
        result = compress_image(input_path, output_path, target_width=380, quality=80)
        
        if result['success']:
            # 创建Data URI
            data_uri_result = create_data_uri(output_path)
            
            if data_uri_result['success']:
                results.append({
                    'index': i,
                    'original_filename': filename,
                    'compressed_filename': output_filename,
                    'original_width': result['original_size'][0],
                    'original_height': result['original_size'][1],
                    'compressed_width': result['compressed_size'][0],
                    'compressed_height': result['compressed_size'][1],
                    'file_size_kb': result['file_size_kb'],
                    'format': result['format'],
                    'quality': result['quality'],
                    'data_uri_length': data_uri_result['length']
                })
                
                data_uris.append({
                    'index': i,
                    'data_uri': data_uri_result['data_uri'][:100] + '...' if len(data_uri_result['data_uri']) > 100 else data_uri_result['data_uri']
                })
                
                print(f"  成功: {result['original_size'][0]}x{result['original_size'][1]} -> {result['compressed_size'][0]}x{result['compressed_size'][1]}")
                print(f"  文件大小: {result['file_size_kb']:.2f}KB")
            else:
                print(f"  失败: 创建Data URI时出错: {data_uri_result['error']}")
        else:
            print(f"  失败: 压缩图片时出错: {result['error']}")
    
    # 保存压缩结果
    if results:
        # JSON报告
        report_path = os.path.join('outputs/儿童哲学史/移动端完善', '图片压缩报告.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump({
                'compression_results': results,
                'summary': {
                    'total_images': len(results),
                    'average_width': sum(r['compressed_width'] for r in results) / len(results) if results else 0,
                    'average_height': sum(r['compressed_height'] for r in results) / len(results) if results else 0,
                    'average_file_size_kb': sum(r['file_size_kb'] for r in results) / len(results) if results else 0,
                    'total_file_size_kb': sum(r['file_size_kb'] for r in results) if results else 0
                },
                'data_uris_preview': data_uris
            }, f, ensure_ascii=False, indent=2)
        
        # Markdown报告
        md_report = f"""# 图片压缩报告

## 压缩参数
- **目标宽度**: 380px
- **输出格式**: WebP
- **质量**: 80%
- **适配设备**: 最小屏幕iPhone SE (375px)

## 压缩结果
| 序号 | 原图尺寸 | 压缩后尺寸 | 文件大小 | 压缩比 |
|------|----------|------------|----------|--------|
"""
        
        for r in results:
            original_area = r['original_width'] * r['original_height']
            compressed_area = r['compressed_width'] * r['compressed_height']
            compression_ratio = (1 - compressed_area / original_area) * 100
            
            md_report += f"| {r['index']} | {r['original_width']}×{r['original_height']} | {r['compressed_width']}×{r['compressed_height']} | {r['file_size_kb']:.2f}KB | {compression_ratio:.1f}% |\n"
        
        # 计算总体统计
        total_original_size = sum(r['original_width'] * r['original_height'] for r in results)
        total_compressed_size = sum(r['compressed_width'] * r['compressed_height'] for r in results)
        overall_ratio = (1 - total_compressed_size / total_original_size) * 100 if total_original_size > 0 else 0
        
        md_report += f"""
## 总体统计
- **图片总数**: {len(results)}
- **平均宽度**: {sum(r['compressed_width'] for r in results) / len(results):.1f}px
- **平均高度**: {sum(r['compressed_height'] for r in results) / len(results):.1f}px
- **总文件大小**: {sum(r['file_size_kb'] for r in results):.2f}KB
- **总体压缩率**: {overall_ratio:.1f}%

## 对手机显示的改善
### 压缩前
- 图片宽度: 800px
- 最小屏幕宽度: 375px (iPhone SE)
- 溢出像素: 425px (213% 屏幕宽度)

### 压缩后
- 图片宽度: 380px
- 最小屏幕宽度: 375px (iPhone SE)
- 溢出像素: 5px (101% 屏幕宽度)
- **改善效果**: 从需要大幅水平滚动到基本适配屏幕

## 下一步
1. 更新CSS样式，增强响应式控制
2. 更新HTML文件，使用压缩后的Data URI图片
3. 进行多设备模拟测试验证

---
**压缩时间**: 2026-04-04
**输出目录**: {output_dir}
"""
        
        md_report_path = os.path.join('outputs/儿童哲学史/移动端完善', '图片压缩报告.md')
        with open(md_report_path, 'w', encoding='utf-8') as f:
            f.write(md_report)
        
        print(f"\n压缩完成！")
        print(f"压缩后的图片保存在: {output_dir}")
        print(f"JSON报告: {report_path}")
        print(f"Markdown报告: {md_report_path}")
        
        # 返回Data URI用于HTML更新
        full_data_uris = []
        for r in results:
            output_path = os.path.join(output_dir, f'phone_image_{r["index"]}_compressed.webp')
            data_uri_result = create_data_uri(output_path)
            if data_uri_result['success']:
                full_data_uris.append(data_uri_result['data_uri'])
        
        # 保存完整的Data URI
        data_uri_path = os.path.join('outputs/儿童哲学史/移动端完善', 'compressed_image_data_uris.json')
        with open(data_uri_path, 'w', encoding='utf-8') as f:
            json.dump({'data_uris': full_data_uris}, f, ensure_ascii=False, indent=2)
        
        print(f"完整的Data URI已保存: {data_uri_path}")
        
        return full_data_uris
    else:
        print("没有图片成功压缩")
        return []

if __name__ == '__main__':
    main()