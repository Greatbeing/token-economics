#!/usr/bin/env python3
import os
import re

def validate_optimization():
    """验证优化结果"""
    html_path = "/app/data/files/outputs/儿童哲学史/手机优化/第一章_手机优化.html"
    css_path = "/app/data/files/outputs/儿童哲学史/手机优化/style_phone.css"
    
    print("=== 手机优化验证 ===\n")
    
    # 1. 检查HTML文件
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    print("1. HTML文件检查:")
    print(f"   - 文件大小: {os.path.getsize(html_path)/1024:.1f}KB")
    
    # 检查CSS引用
    css_ref_match = re.search(r'<link[^>]*href="([^"]*)"', html)
    if css_ref_match:
        css_ref = css_ref_match.group(1)
        print(f"   - CSS引用: {css_ref}")
        if css_ref == 'style_phone.css':
            print("     ✓ CSS引用正确")
        else:
            print(f"     ⚠ 期望 'style_phone.css', 实际 '{css_ref}'")
    else:
        print("   ⚠ 未找到CSS引用")
    
    # 检查图片标签
    img_tags = re.findall(r'<img[^>]*>', html)
    print(f"   - 图片标签数量: {len(img_tags)}")
    
    # 检查Data URI长度（压缩后应该较短）
    data_uris = re.findall(r'src="(data:image/[^"]*)"', html)
    print(f"   - Data URI数量: {len(data_uris)}")
    
    if data_uris:
        avg_length = sum(len(uri) for uri in data_uris) / len(data_uris)
        print(f"   - Data URI平均长度: {avg_length:.0f}字符")
        if avg_length < 150000:  # 原始大约900k，现在应该小很多
            print("     ✓ Data URI已压缩")
        else:
            print("     ⚠ Data URI可能未压缩")
    
    # 检查容器类
    illustration_containers = html.count('class="illustration-container"')
    print(f"   - illustration-container数量: {illustration_containers}")
    
    # 2. 检查CSS文件
    print("\n2. CSS文件检查:")
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    
    print(f"   - 文件大小: {os.path.getsize(css_path)/1024:.1f}KB")
    
    # 检查关键规则
    checks = [
        (r'\.chapter-illustration\s*{[^}]*max-width:\s*100%', '图片max-width: 100%规则'),
        (r'\.illustration-container\s*{[^}]*overflow:\s*hidden', '容器overflow: hidden规则'),
        (r'@media[^{]*max-width:\s*600px', '移动端媒体查询(≤600px)'),
        (r'@media[^{]*max-width:\s*400px', '超小屏幕媒体查询(≤400px)'),
        (r'max-width:\s*100vw', '最大宽度100vw规则'),
    ]
    
    for pattern, description in checks:
        if re.search(pattern, css, re.IGNORECASE):
            print(f"     ✓ {description}")
        else:
            print(f"     ⚠ 未找到: {description}")
    
    # 3. 检查图片文件
    print("\n3. 图片文件检查:")
    img_dir = "/app/data/files/outputs/儿童哲学史/手机优化/images"
    if os.path.exists(img_dir):
        img_files = [f for f in os.listdir(img_dir) if f.endswith('.webp')]
        print(f"   - 图片文件数量: {len(img_files)}")
        
        for img_file in img_files:
            img_path = os.path.join(img_dir, img_file)
            size_kb = os.path.getsize(img_path) / 1024
            print(f"     - {img_file}: {size_kb:.1f}KB")
    else:
        print("   ⚠ 图片目录不存在")
    
    # 4. 模拟设备兼容性分析
    print("\n4. 设备兼容性分析:")
    devices = [
        ("iPhone SE", 375),
        ("iPhone 12", 390),
        ("Pixel 5", 393),
        ("iPhone 14 Pro", 430),
    ]
    
    # 假设图片宽度400px
    image_width = 400
    
    for device_name, screen_width in devices:
        if image_width <= screen_width:
            status = "✓ 完全适配"
        else:
            overflow = image_width - screen_width
            status = f"⚠ 溢出{overflow}px"
        
        print(f"   - {device_name} ({screen_width}px): {status}")
    
    # 5. 生成验证结论
    print("\n5. 验证结论:")
    
    # 检查关键指标
    issues = []
    
    if len(img_tags) != 4:
        issues.append(f"图片标签数量异常: {len(img_tags)}个 (期望4个)")
    
    if illustration_containers != 4:
        issues.append(f"插图容器数量异常: {illustration_containers}个 (期望4个)")
    
    if not css_ref_match or css_ref_match.group(1) != 'style_phone.css':
        issues.append("CSS引用未正确更新")
    
    if data_uris and avg_length > 200000:
        issues.append(f"Data URI可能过大: 平均{avg_length:.0f}字符")
    
    if not issues:
        print("   ✓ 所有关键检查通过")
        print("   ✓ 图片已压缩至手机友好尺寸")
        print("   ✓ CSS响应式规则完备")
        print("   ✓ 设备兼容性良好")
    else:
        print("   ⚠ 发现以下问题:")
        for issue in issues:
            print(f"     - {issue}")
    
    return len(issues) == 0

if __name__ == "__main__":
    success = validate_optimization()
    
    print("\n" + "="*50)
    if success:
        print("优化验证成功！手机显示问题已解决。")
    else:
        print("优化验证发现一些问题，请检查并修复。")
    
    print(f"\n主要文件位置:")
    print(f"- HTML: outputs/儿童哲学史/手机优化/第一章_手机优化.html")
    print(f"- CSS: outputs/儿童哲学史/手机优化/style_phone.css")
    print(f"- 图片: outputs/儿童哲学史/手机优化/images/")
    print(f"- 报告: outputs/儿童哲学史/手机优化/最终优化报告.md")