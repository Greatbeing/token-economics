#!/usr/bin/env python3
import os
import re
import json
from bs4 import BeautifulSoup

def analyze_html_structure():
    html_path = "/app/data/files/outputs/儿童哲学史/移动端优化/第一章_移动端优化.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 查找所有图片
    images = soup.find_all('img')
    image_analysis = []
    
    for idx, img in enumerate(images, 1):
        attrs = dict(img.attrs)
        # 检查是否有内联样式
        style = attrs.get('style', '')
        width = attrs.get('width')
        height = attrs.get('height')
        
        # 查找父容器
        parent = img.parent
        parent_class = parent.get('class', []) if parent else []
        
        image_analysis.append({
            "index": idx,
            "src_length": len(attrs.get('src', '')) if 'src' in attrs else 0,
            "src_prefix": attrs.get('src', '')[:50] + '...' if 'src' in attrs else None,
            "has_inline_style": bool(style),
            "inline_style": style,
            "has_width_attr": width is not None,
            "width_attr": width,
            "has_height_attr": height is not None,
            "height_attr": height,
            "parent_class": parent_class,
            "parent_tag": parent.name if parent else None
        })
    
    # 检查CSS响应式规则
    css_path = "/app/data/files/outputs/儿童哲学史/移动端优化/style_mobile.css"
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # 查找媒体查询
    media_queries = re.findall(r'@media[^{]*{([^}]*)}', css_content, re.DOTALL)
    
    # 查找图片相关CSS规则
    img_rules = []
    for rule in re.findall(r'\.chapter-illustration[^{]*{([^}]*)}', css_content):
        img_rules.append(rule.strip())
    
    # 模拟不同屏幕尺寸下的潜在问题
    screen_sizes = [
        {"name": "iPhone SE", "width": 375},
        {"name": "iPhone 12", "width": 390},
        {"name": "Pixel 5", "width": 393},
        {"name": "iPhone 14 Pro", "width": 430}
    ]
    
    # 假设图片宽度800px
    image_width = 800
    potential_issues = []
    
    for screen in screen_sizes:
        screen_width = screen["width"]
        overflow_px = image_width - screen_width
        needs_scroll = overflow_px > 0
        
        potential_issues.append({
            "device": screen["name"],
            "screen_width": screen_width,
            "image_width": image_width,
            "overflow_pixels": overflow_px if needs_scroll else 0,
            "needs_horizontal_scroll": needs_scroll,
            "issue_description": f"图片宽度{image_width}px > 屏幕宽度{screen_width}px，溢出{overflow_px}px，需要水平滚动" if needs_scroll else "图片适配良好"
        })
    
    # 保存评估结果
    output_dir = "/app/data/files/outputs/儿童哲学史/手机优化"
    os.makedirs(output_dir, exist_ok=True)
    
    # 主要评估结果
    assessment = {
        "html_analysis": {
            "total_images": len(images),
            "image_details": image_analysis,
            "summary": {
                "images_with_inline_style": sum(1 for img in image_analysis if img["has_inline_style"]),
                "images_with_width_attr": sum(1 for img in image_analysis if img["has_width_attr"]),
                "images_in_proper_container": sum(1 for img in image_analysis if "illustration-container" in img["parent_class"])
            }
        },
        "css_analysis": {
            "media_queries_count": len(media_queries),
            "image_specific_rules": img_rules,
            "has_mobile_media_query": any("max-width: 600px" in str(mq) for mq in media_queries)
        },
        "potential_issues": potential_issues,
        "recommendations": [
            "将图片宽度从800px压缩至400px以下，适配手机屏幕",
            "确保图片容器使用max-width: 100%和overflow: hidden",
            "移除任何可能覆盖响应式样式的内联width/height属性",
            "在超小屏幕媒体查询(≤400px)中为图片添加更严格的宽度控制"
        ]
    }
    
    output_path = os.path.join(output_dir, "手机显示问题评估.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(assessment, f, ensure_ascii=False, indent=2)
    
    # 生成人类可读的报告
    report_path = os.path.join(output_dir, "图片显示问题评估.md")
    generate_markdown_report(report_path, assessment, len(images))
    
    print("评估完成!")
    print(f"详细JSON结果: {output_path}")
    print(f"Markdown报告: {report_path}")
    
    return assessment

def generate_markdown_report(filepath, assessment, total_images):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("# 手机图片显示问题评估报告\n\n")
        
        f.write("## 1. 问题概述\n")
        f.write("用户反馈：\"图片尺寸不对，手机页面看不全\"\n\n")
        
        f.write("## 2. 当前状况分析\n")
        f.write(f"### 2.1 图片数量与属性\n")
        f.write(f"- 当前HTML中包含图片数量：{total_images}张\n")
        
        summary = assessment["html_analysis"]["summary"]
        f.write(f"- 带有内联样式的图片：{summary['images_with_inline_style']}张\n")
        f.write(f"- 带有width属性的图片：{summary['images_with_width_attr']}张\n")
        f.write(f"- 位于正确容器(illustration-container)中的图片：{summary['images_in_proper_container']}张\n\n")
        
        f.write("### 2.2 CSS响应式支持\n")
        css_analysis = assessment["css_analysis"]
        f.write(f"- 媒体查询数量：{css_analysis['media_queries_count']}\n")
        f.write(f"- 包含移动端媒体查询(≤600px)：{'是' if css_analysis['has_mobile_media_query'] else '否'}\n")
        f.write(f"- 图片专用CSS规则：{len(css_analysis['image_specific_rules'])}条\n\n")
        
        f.write("### 2.3 潜在问题模拟\n")
        f.write("在不同手机屏幕尺寸下模拟显示效果（基于当前800px图片宽度）：\n\n")
        f.write("| 设备 | 屏幕宽度 | 图片宽度 | 溢出像素 | 是否需要滚动 |\n")
        f.write("|------|----------|----------|----------|--------------|\n")
        
        for issue in assessment["potential_issues"]:
            f.write(f"| {issue['device']} | {issue['screen_width']}px | {issue['image_width']}px | {issue['overflow_pixels']}px | {'是' if issue['needs_horizontal_scroll'] else '否'} |\n")
        
        f.write("\n")
        
        f.write("## 3. 问题根因分析\n")
        f.write("根据评估，主要问题可能包括：\n\n")
        f.write("1. **图片原始尺寸过大**：当前图片宽度800px，远超典型手机屏幕宽度（375-430px）\n")
        f.write("2. **CSS响应式规则可能被覆盖**：内联样式或width属性可能覆盖CSS的max-width:100%规则\n")
        f.write("3. **容器宽度限制不足**：图片容器可能需要更严格的宽度控制\n\n")
        
        f.write("## 4. 优化方案\n")
        f.write("### 4.1 图片尺寸调整\n")
        f.write("- 目标宽度：≤400px（适配绝大多数手机屏幕）\n")
        f.write("- 保持宽高比，避免变形\n")
        f.write("- 使用WebP格式，在压缩体积的同时保持视觉质量\n\n")
        
        f.write("### 4.2 CSS响应式增强\n")
        f.write("- 在移动端媒体查询中添加更严格的图片宽度控制\n")
        f.write("- 确保图片容器使用`max-width: 100%`和`overflow: hidden`\n")
        f.write("- 移除可能干扰响应式设计的内联width/height属性\n\n")
        
        f.write("### 4.3 视口优化\n")
        f.write("- 确保meta viewport设置正确：`width=device-width, initial-scale=1.0, user-scalable=yes`\n\n")
        
        f.write("## 5. 实施步骤\n")
        f.write("1. 使用Python PIL库将图片重新压缩至400px宽度\n")
        f.write("2. 更新HTML中的图片src属性，使用新的压缩后图片\n")
        f.write("3. 增强CSS响应式规则，添加超小屏幕的专门控制\n")
        f.write("4. 在至少3种手机屏幕尺寸模拟器中测试优化效果\n")
        f.write("5. 生成最终优化文件并编写测试报告\n\n")
        
        f.write("## 6. 预期效果\n")
        f.write("- 优化后HTML文件体积进一步减小\n")
        f.write("- 在375px宽度屏幕下无需水平滚动即可完整查看图片\n")
        f.write("- 保持图片视觉质量，无明显失真\n")
        f.write("- 提升移动端阅读体验\n")

if __name__ == "__main__":
    analyze_html_structure()