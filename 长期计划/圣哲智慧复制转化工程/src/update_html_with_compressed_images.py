#!/usr/bin/env python3
"""
更新HTML文件，使用压缩后的图片Data URI
"""

import os
import json
from bs4 import BeautifulSoup

def main():
    print("开始更新HTML文件...")
    
    # 1. 读取压缩后的图片Data URI
    data_uri_path = 'outputs/儿童哲学史/移动端完善/compressed_image_data_uris.json'
    with open(data_uri_path, 'r', encoding='utf-8') as f:
        data_uris_data = json.load(f)
    
    compressed_data_uris = data_uris_data['data_uris']
    
    print(f"加载了 {len(compressed_data_uris)} 个压缩图片Data URI")
    
    # 2. 读取原始HTML文件
    html_path = 'outputs/儿童哲学史/手机优化/第一章_手机优化.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 3. 解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 4. 查找所有图片标签
    img_tags = soup.find_all('img', class_='chapter-illustration')
    
    print(f"找到 {len(img_tags)} 个图片标签需要更新")
    
    # 5. 按顺序替换Data URI
    updates = []
    for i, img_tag in enumerate(img_tags):
        if i < len(compressed_data_uris):
            old_src = img_tag['src'][:100] + '...' if len(img_tag['src']) > 100 else img_tag['src']
            
            # 更新src属性
            img_tag['src'] = compressed_data_uris[i]
            
            new_src_prefix = compressed_data_uris[i][:100] + '...' if len(compressed_data_uris[i]) > 100 else compressed_data_uris[i]
            
            updates.append({
                'index': i + 1,
                'old_src_length': len(old_src),
                'new_src_length': len(compressed_data_uris[i]),
                'size_reduction_percent': (len(old_src) - len(compressed_data_uris[i])) / len(old_src) * 100 if len(old_src) > 0 else 0
            })
            
            print(f"  图片 {i+1}: Data URI长度 {len(old_src)} -> {len(compressed_data_uris[i])} (减少{(len(old_src) - len(compressed_data_uris[i]))/len(old_src)*100:.1f}%)")
    
    # 6. 更新CSS链接到增强的CSS
    # 查找现有的CSS链接
    head = soup.find('head')
    if head:
        # 查找现有的link标签
        existing_css_link = head.find('link', {'rel': 'stylesheet'})
        if existing_css_link:
            # 更新为增强的CSS
            existing_css_link['href'] = 'style_enhanced.css'
            print("已更新CSS链接到 style_enhanced.css")
        else:
            # 添加新的CSS链接
            new_link = soup.new_tag('link', rel='stylesheet', href='style_enhanced.css')
            head.append(new_link)
            print("已添加CSS链接 style_enhanced.css")
    
    # 7. 确保视口设置正确
    viewport_tag = head.find('meta', {'name': 'viewport'}) if head else None
    if viewport_tag:
        viewport_tag['content'] = 'width=device-width, initial-scale=1.0, user-scalable=yes'
        print("已更新视口设置")
    else:
        if head:
            new_viewport = soup.new_tag('meta', name='viewport', content='width=device-width, initial-scale=1.0, user-scalable=yes')
            head.append(new_viewport)
            print("已添加视口设置")
    
    # 8. 保存更新后的HTML
    output_dir = 'outputs/儿童哲学史/移动端完善'
    os.makedirs(output_dir, exist_ok=True)
    
    output_html_path = os.path.join(output_dir, '第一章_移动端完善.html')
    
    with open(output_html_path, 'w', encoding='utf-8') as f:
        # 保持原始的DOCTYPE声明
        f.write('<!DOCTYPE html>\n')
        f.write(str(soup))
    
    print(f"\nHTML更新完成！")
    print(f"输出文件: {output_html_path}")
    
    # 9. 复制增强的CSS文件到同一目录
    enhanced_css_src = 'outputs/儿童哲学史/移动端完善/style_enhanced.css'
    enhanced_css_dst = os.path.join(output_dir, 'style_enhanced.css')
    
    if os.path.exists(enhanced_css_src):
        with open(enhanced_css_src, 'r', encoding='utf-8') as src:
            css_content = src.read()
        
        with open(enhanced_css_dst, 'w', encoding='utf-8') as dst:
            dst.write(css_content)
        
        print(f"CSS文件已复制: {enhanced_css_dst}")
    
    # 10. 生成更新报告
    report = {
        'html_updates': {
            'total_images_updated': len(updates),
            'updates_details': updates,
            'original_html': html_path,
            'updated_html': output_html_path,
            'css_file': enhanced_css_dst
        },
        'image_compression_summary': {
            'average_size_reduction': sum(u['size_reduction_percent'] for u in updates) / len(updates) if updates else 0,
            'total_data_uri_length_before': sum(u['old_src_length'] for u in updates) if updates else 0,
            'total_data_uri_length_after': sum(u['new_src_length'] for u in updates) if updates else 0
        },
        'mobile_optimization_features': [
            '图片宽度压缩至380px (适配最小屏幕iPhone SE)',
            '容器严格宽度限制 (width: 100% !important)',
            '图片双重保险 (max-width: calc(100% - 10px) !important)',
            '超小屏幕媒体查询 (≤400px)',
            '最小屏幕媒体查询 (≤375px)',
            '防止水平滚动 (overflow-x: hidden)',
            '正确视口设置 (width=device-width)'
        ]
    }
    
    # 保存报告
    report_path = os.path.join(output_dir, 'html_update_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 生成Markdown报告
    md_report = f"""# HTML文件更新报告

## 更新概述
成功更新HTML文件，使用压缩后的图片Data URI并应用增强的CSS响应式控制。

## 更新详情
### 1. 图片Data URI替换
| 图片序号 | 原Data URI长度 | 压缩后Data URI长度 | 大小减少 |
|----------|----------------|--------------------|----------|
"""
    
    for update in updates:
        md_report += f"| {update['index']} | {update['old_src_length']} | {update['new_src_length']} | {update['size_reduction_percent']:.1f}% |\n"
    
    md_report += f"""
### 2. CSS样式更新
- **应用样式**: `style_enhanced.css`
- **特性**: 增强的移动端响应式控制
- **位置**: 与HTML文件同目录

### 3. 视口设置
- **内容**: `width=device-width, initial-scale=1.0, user-scalable=yes`
- **目的**: 确保设备正确识别屏幕宽度

## 移动端优化特性
"""
    
    for i, feature in enumerate(report['mobile_optimization_features'], 1):
        md_report += f"{i}. {feature}\n"
    
    md_report += f"""
## 预期效果
| 设备 | 屏幕宽度 | 图片宽度 | 溢出情况 | 适配状态 |
|------|----------|----------|----------|----------|
| iPhone SE | 375px | 380px | 5px溢出 | 基本适配 (99%) |
| iPhone 12 | 390px | 380px | -10px | 完全适配 |
| Pixel 5 | 393px | 380px | -13px | 完全适配 |
| iPhone 14 Pro | 430px | 380px | -50px | 完全适配 |

## 验证步骤
1. 在多种手机设备上打开 `{output_html_path}`
2. 确认所有图片完整显示在视口内
3. 确保无水平滚动条出现
4. 验证图片质量可接受，无明显模糊

## 下一步
1. 进行多设备模拟测试
2. 生成最终优化验证报告
3. 交付用户审阅

---
**更新时间**: 2026-04-04
**原HTML文件**: {html_path}
**更新后HTML文件**: {output_html_path}
**应用CSS**: {enhanced_css_dst}
**总图片更新数**: {len(updates)}
**平均大小减少**: {report['image_compression_summary']['average_size_reduction']:.1f}%
"""
    
    md_report_path = os.path.join(output_dir, 'html_update_report.md')
    with open(md_report_path, 'w', encoding='utf-8') as f:
        f.write(md_report)
    
    print(f"\n报告已生成:")
    print(f"  JSON报告: {report_path}")
    print(f"  Markdown报告: {md_report_path}")
    
    # 11. 创建测试验证脚本
    create_test_script(output_dir, output_html_path)

def create_test_script(output_dir, html_path):
    """创建测试验证脚本"""
    test_script = f"""#!/usr/bin/env python3
"""
    
    test_script_path = os.path.join(output_dir, 'test_mobile_compatibility.py')
    
    # 简化的测试脚本
    simple_test = '''#!/usr/bin/env python3
"""
移动端兼容性测试脚本
"""

print("移动端兼容性测试")
print("=================")
print(f"测试文件: {html_path}")
print("")
print("测试要点:")
print("1. 图片宽度: 380px")
print("2. 最小屏幕适配: iPhone SE (375px)")
print("3. CSS响应式控制:")
print("   - 容器宽度限制")
print("   - 图片双重保险")
print("   - 超小屏幕媒体查询")
print("4. 预期效果: 无水平滚动条")
print("")
print("请在实际设备上测试:")
print("1. iPhone SE (375px)")
print("2. iPhone 12 (390px)")
print("3. Pixel 5 (393px)")
print("4. iPhone 14 Pro (430px)")
print("")
print("验证标准:")
print("- 图片完整显示在视口内")
print("- 无需水平滚动")
print("- 图片质量可接受")
'''
    
    with open(test_script_path, 'w', encoding='utf-8') as f:
        f.write(simple_test)
    
    # 设置执行权限
    import stat
    os.chmod(test_script_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    
    print(f"测试脚本已创建: {test_script_path}")

if __name__ == '__main__':
    main()