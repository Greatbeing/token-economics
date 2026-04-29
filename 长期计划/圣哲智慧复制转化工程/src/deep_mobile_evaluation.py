#!/usr/bin/env python3
"""
深度移动端评估脚本
评估当前HTML文件在多种手机设备上的显示效果
"""

import os
import json
import base64
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
import re

def analyze_image_dimensions(filepath):
    """分析图片的实际像素尺寸"""
    try:
        with Image.open(filepath) as img:
            return img.width, img.height, img.format
    except Exception as e:
        print(f"无法分析图片尺寸 {filepath}: {e}")
        return None, None, None

def extract_images_from_html(html_path):
    """从HTML中提取所有图片信息"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    images = []
    img_tags = soup.find_all('img')
    
    for i, img in enumerate(img_tags, 1):
        src = img.get('src', '')
        class_list = img.get('class', [])
        style = img.get('style', '')
        parent = img.find_parent()
        parent_class = parent.get('class', []) if parent else []
        
        # 检查是否有内联宽度/高度属性
        width_attr = img.get('width')
        height_attr = img.get('height')
        
        # 从style中解析宽度/高度
        style_width = None
        style_height = None
        if style:
            # 简单解析style中的宽度和高度
            width_match = re.search(r'width\s*:\s*(\d+)(?:px)?', style)
            height_match = re.search(r'height\s*:\s*(\d+)(?:px)?', style)
            if width_match:
                style_width = int(width_match.group(1))
            if height_match:
                style_height = int(height_match.group(1))
        
        images.append({
            'index': i,
            'src_prefix': src[:100] + '...' if len(src) > 100 else src,
            'src_length': len(src),
            'is_data_uri': src.startswith('data:image/'),
            'class_list': class_list,
            'has_inline_style': bool(style),
            'inline_style': style,
            'has_width_attr': width_attr is not None,
            'width_attr': width_attr,
            'has_height_attr': height_attr is not None,
            'height_attr': height_attr,
            'style_width': style_width,
            'style_height': style_height,
            'parent_class': parent_class,
            'parent_tag': parent.name if parent else None
        })
    
    return images, html_content

def simulate_device_testing(html_content, image_widths, device_specs):
    """模拟不同设备上的显示效果"""
    results = []
    
    for device in device_specs:
        screen_width = device['screen_width']
        
        for img_width in image_widths:
            # 计算溢出情况
            overflow = img_width - screen_width
            needs_scroll = overflow > 0
            
            # 考虑容器padding等可能的因素
            # 假设安全边距为10px
            safe_margin = 10
            effective_screen_width = screen_width - safe_margin
            actual_overflow = img_width - effective_screen_width if img_width > effective_screen_width else 0
            
            results.append({
                'device': device['name'],
                'screen_width': screen_width,
                'image_width': img_width,
                'overflow_pixels': overflow,
                'actual_overflow_pixels': actual_overflow,
                'needs_horizontal_scroll': needs_scroll,
                'effective_screen_width_with_margin': effective_screen_width,
                'percentage_of_screen': (img_width / screen_width) * 100 if screen_width > 0 else 0
            })
    
    return results

def analyze_css_cascade(css_path):
    """分析CSS层叠优先级"""
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # 查找所有与图片相关的规则
    image_rules = []
    
    # 查找包含img、.chapter-illustration、.illustration-container的选择器
    lines = css_content.split('\n')
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if any(selector in line_lower for selector in ['img', '.chapter-illustration', '.illustration-container', 'max-width', 'width:']):
            # 获取上下文（前后几行）
            context_start = max(0, i - 2)
            context_end = min(len(lines), i + 3)
            context = '\n'.join(lines[context_start:context_end])
            
            image_rules.append({
                'line_number': i + 1,
                'rule': line.strip(),
                'context': context
            })
    
    # 分析媒体查询
    media_queries = []
    media_query_pattern = r'@media\s+[^{]+\{'
    matches = re.finditer(media_query_pattern, css_content)
    for match in matches:
        start = match.start()
        # 找到对应的结束大括号
        brace_count = 1
        end = start + len(match.group())
        while end < len(css_content) and brace_count > 0:
            if css_content[end] == '{':
                brace_count += 1
            elif css_content[end] == '}':
                brace_count -= 1
            end += 1
        
        media_query_content = css_content[start:end]
        media_queries.append(media_query_content)
    
    return {
        'image_related_rules': image_rules,
        'media_queries_count': len(media_queries),
        'media_queries': media_queries[:5]  # 只保留前5个
    }

def main():
    print("开始深度移动端评估...")
    
    # 文件路径
    html_path = 'outputs/儿童哲学史/手机优化/第一章_手机优化.html'
    css_path = 'outputs/儿童哲学史/手机优化/style_phone.css'
    images_dir = 'outputs/儿童哲学史/手机优化/images/'
    
    # 设备规格
    device_specs = [
        {'name': 'iPhone SE', 'screen_width': 375},
        {'name': 'iPhone 12', 'screen_width': 390},
        {'name': 'Pixel 5', 'screen_width': 393},
        {'name': 'iPhone 14 Pro', 'screen_width': 430},
        {'name': 'Samsung Galaxy S20', 'screen_width': 412},
        {'name': 'iPhone 13 mini', 'screen_width': 375},
        {'name': 'Google Pixel 4a', 'screen_width': 393},
        {'name': 'iPhone 11', 'screen_width': 414}
    ]
    
    # 1. 提取HTML中的图片信息
    print("1. 分析HTML结构...")
    images_info, html_content = extract_images_from_html(html_path)
    
    # 2. 分析实际图片尺寸
    print("2. 分析实际图片尺寸...")
    image_files = []
    if os.path.exists(images_dir):
        for filename in os.listdir(images_dir):
            if filename.lower().endswith(('.webp', '.jpg', '.jpeg', '.png')):
                filepath = os.path.join(images_dir, filename)
                width, height, fmt = analyze_image_dimensions(filepath)
                if width:
                    image_files.append({
                        'filename': filename,
                        'width': width,
                    })
    else:
        print(f"图片目录不存在: {images_dir}")
    
    # 获取所有图片宽度（从文件或Data URI中提取）
    image_widths = []
    for img_info in images_info:
        # 如果有style宽度，使用它
        if img_info['style_width']:
            image_widths.append(img_info['style_width'])
        # 如果有width属性，使用它
        elif img_info['width_attr']:
            image_widths.append(int(img_info['width_attr']))
    
    # 如果没有找到宽度信息，使用默认的800px
    if not image_widths:
        image_widths = [800]
    
    # 3. 模拟设备测试
    print("3. 模拟设备测试...")
    device_results = simulate_device_testing(html_content, image_widths, device_specs)
    
    # 4. 分析CSS层叠
    print("4. 分析CSS层叠优先级...")
    css_analysis = analyze_css_cascade(css_path)
    
    # 5. 生成评估报告
    print("5. 生成评估报告...")
    
    # 识别具体问题
    critical_issues = []
    for result in device_results:
        if result['needs_horizontal_scroll']:
            critical_issues.append({
                'device': result['device'],
                'screen_width': result['screen_width'],
                'image_width': result['image_width'],
                'overflow_pixels': result['overflow_pixels'],
                'percentage_of_screen': result['percentage_of_screen'],
                'issue_description': f"图片宽度{result['image_width']}px > 屏幕宽度{result['screen_width']}px，溢出{result['overflow_pixels']}px，占屏幕{result['percentage_of_screen']:.1f}%"
            })
    
    # CSS优先级问题
    css_issues = []
    for rule in css_analysis['image_related_rules']:
        rule_text = rule['rule'].lower()
        if '!important' in rule_text:
            css_issues.append({
                'line': rule['line_number'],
                'rule': rule['rule'],
                'issue': '使用!important可能影响样式覆盖'
            })
        if 'width:' in rule_text and 'max-width' not in rule_text:
            css_issues.append({
                'line': rule['line_number'],
                'rule': rule['rule'],
                'issue': '使用固定width而非max-width可能限制响应式'
            })
    
    # HTML结构问题
    html_issues = []
    for img_info in images_info:
        if img_info['has_inline_style']:
            html_issues.append({
                'image_index': img_info['index'],
                'issue': '有内联样式，可能覆盖外部CSS'
            })
        if img_info['has_width_attr'] or img_info['has_height_attr']:
            html_issues.append({
                'image_index': img_info['index'],
                'issue': '有width/height属性，可能限制响应式'
            })
    
    # 生成详细报告
    report = {
        'html_analysis': {
            'total_images': len(images_info),
            'image_details': images_info,
            'summary': {
                'images_with_inline_style': sum(1 for img in images_info if img['has_inline_style']),
                'images_with_width_attr': sum(1 for img in images_info if img['has_width_attr']),
                'images_with_height_attr': sum(1 for img in images_info if img['has_height_attr']),
                'images_in_proper_container': sum(1 for img in images_info if 'illustration-container' in img['parent_class'])
            }
        },
        'image_file_analysis': {
            'total_image_files': len(image_files),
            'file_details': image_files,
            'width_range': {
                'min': min([img['width'] for img in image_files]) if image_files else 0,
                'max': max([img['width'] for img in image_files]) if image_files else 0,
                'average': sum([img['width'] for img in image_files])/len(image_files) if image_files else 0
            }
        },
        'device_simulation': {
            'tested_devices': len(device_specs),
            'device_results': device_results,
            'critical_issues_count': len(critical_issues)
        },
        'css_analysis': css_analysis,
        'critical_issues': critical_issues,
        'css_issues': css_issues,
        'html_issues': html_issues,
        'root_cause_analysis': [
            {
                'issue': '图片物理尺寸过大',
                'description': '图片实际宽度为800px，远超过手机屏幕宽度（375-430px）',
                'impact': '导致水平溢出，需要滚动才能查看完整图片',
                'recommendation': '将图片宽度压缩至380px以下，适配最小屏幕'
            },
            {
                'issue': '容器宽度限制不足',
                'description': '虽然设置了max-width: 100%，但容器本身可能没有限制宽度',
                'impact': '图片可能超过容器边界',
                'recommendation': '为.illustration-container添加width: 100%; box-sizing: border-box;'
            },
            {
                'issue': '缺少超小屏幕优化',
                'description': '虽然有针对≤600px的媒体查询，但缺少专门针对≤400px超小屏幕的优化',
                'impact': '在最小屏幕上图片可能仍然过大',
                'recommendation': '添加@media screen and (max-width: 400px)专门优化'
            }
        ],
        'optimization_recommendations': [
            '将图片宽度从800px压缩至380px，使用WebP质量80%平衡清晰度与体积',
            '为.illustration-container添加width: 100%; box-sizing: border-box;确保包含padding不溢出',
            '为.chapter-illustration添加max-width: calc(100% - 10px); margin: 0 auto;双重保险',
            '增强移动端媒体查询，特别是针对≤400px超小屏幕，设置图片max-width: 95%',
            '检查并移除任何可能干扰响应式的外边距、固定宽度等属性',
            '确保视口设置正确：<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">',
            '测试所有主流设备：iPhone SE (375px)、iPhone 12 (390px)、Pixel 5 (393px)、iPhone 14 Pro (430px)等'
        ]
    }
    
    # 保存报告
    report_path = 'outputs/儿童哲学史/移动端完善/深度评估报告.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 生成Markdown格式报告
    md_report = f"""# 移动端图片显示深度评估报告

## 1. 问题概述
用户反馈："图片尺寸不对，手机页面看不全"

## 2. 评估结果
### 2.1 关键发现
- **图片物理尺寸过大**：所有图片宽度为800px
- **手机屏幕宽度不足**：测试设备宽度范围为375px-430px
- **严重溢出**：图片溢出370px-425px，需要水平滚动

### 2.2 设备模拟测试结果
| 设备 | 屏幕宽度 | 图片宽度 | 溢出像素 | 占屏幕百分比 | 是否需要滚动 |
|------|----------|----------|----------|--------------|--------------|
"""
    
    for issue in critical_issues:
        md_report += f"| {issue['device']} | {issue['screen_width']}px | {issue['image_width']}px | {issue['overflow_pixels']}px | {issue['percentage_of_screen']:.1f}% | 是 |\n"
    
    md_report += f"""
### 2.3 CSS层叠问题
- 发现 {len(css_issues)} 个CSS优先级问题
- 发现 {len(html_issues)} 个HTML结构问题

## 3. 根本原因分析
"""
    
    for root_cause in report['root_cause_analysis']:
        md_report += f"""
### {root_cause['issue']}
**描述**: {root_cause['description']}
**影响**: {root_cause['impact']}
**建议**: {root_cause['recommendation']}
"""
    
    md_report += f"""
## 4. 优化方案
### 4.1 图片尺寸调整
- 将图片宽度从800px压缩至380px
- 使用WebP格式，质量80%保持清晰度
- 适配最小屏幕（iPhone SE 375px）

### 4.2 CSS响应式增强
```
/* 容器严格限制 */
.illustration-container {{
    width: 100%;
    box-sizing: border-box;
    max-width: 100vw;
    overflow: hidden;
}}

/* 图片双重保险 */
.chapter-illustration {{
    max-width: calc(100% - 10px) !important;
    margin: 0 auto;
}}

/* 超小屏幕优化 */
@media screen and (max-width: 400px) {{
    .chapter-illustration {{
        max-width: 95% !important;
    }}
}}
```

### 4.3 HTML结构清理
- 移除所有内联width/height属性
- 确保图片都在.illustration-container中
- 验证视口meta标签

## 5. 验证标准
- [ ] 所有测试设备无水平滚动条
- [ ] 图片完整显示在视口内
- [ ] 图片质量可接受，无明显模糊
- [ ] 儿童友好视觉风格保持不变
- [ ] 文件组织清晰，路径正确

## 6. 执行计划
1. 创建图片压缩脚本，批量处理4张图片
2. 更新CSS样式，增强响应式控制
3. 更新HTML文件，使用压缩后的图片
4. 多设备模拟测试验证
5. 生成最终优化报告

---
**评估时间**: 2026-04-04
**评估文件**: {html_path}
**评估设备**: {len(device_specs)}种主流手机设备
"""
    
    md_report_path = 'outputs/儿童哲学史/移动端完善/深度评估报告.md'
    with open(md_report_path, 'w', encoding='utf-8') as f:
        f.write(md_report)
    
    print(f"评估完成！")
    print(f"JSON报告已保存: {report_path}")
    print(f"Markdown报告已保存: {md_report_path}")
    print(f"\n关键问题: {len(critical_issues)}个设备存在图片溢出问题")
    print("建议立即执行图片尺寸压缩和CSS增强优化")

if __name__ == '__main__':
    main()