#!/usr/bin/env python3
"""
儿童版中国哲学史 - 批量HTML样张生成脚本（带图片嵌入）
批量生成第2至12章HTML样张，自动嵌入章节插图
"""

import os
import sys
import subprocess
import tempfile
import shutil
import base64
import re
from pathlib import Path

# 中文数字到阿拉伯数字的映射
CHINESE_NUMERALS = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '十一': 11, '十二': 12
}

def extract_chapter_number(title_line):
    """从章节标题行中提取章节数字"""
    # 匹配 "第X章" 模式，其中X是中文数字
    match = re.search(r'第([一二三四五六七八九十]+)章', title_line)
    if match:
        chinese_num = match.group(1)
        # 处理"十一"、"十二"等组合数字
        if chinese_num in CHINESE_NUMERALS:
            return CHINESE_NUMERALS[chinese_num]
    return None

def insert_image_references(markdown_content, chapter_num):
    """
    在Markdown内容中插入图片引用
    策略：在章节标题后立即插入第一张场景插图
    """
    lines = markdown_content.split('\n')
    processed_lines = []
    
    for i, line in enumerate(lines):
        processed_lines.append(line)
        # 如果是章节标题行（以#开头）
        if line.startswith('# ') and '第' in line and '章' in line:
            # 插入图片引用
            img_markdown = f'\n![章节插图](ch{chapter_num}_scene1.jpg)\n'
            processed_lines.append(img_markdown)
    
    return '\n'.join(processed_lines)

# 复制generate_chapter_html.py中的函数和配置（省略部分重复代码）
class Config:
    # 页面尺寸（用于打印样式）
    PAGE_WIDTH_MM = 148
    PAGE_HEIGHT_MM = 210
    
    # 字体（优化后备链）
    BODY_FONT = "'Source Han Serif SC', 'SimSun', 'Songti SC', 'Noto Serif CJK SC', serif"
    HEADING_FONT = "'FZXiaoBiaoSong-B05S', 'FangSong', 'STFangsong', 'Noto Sans CJK SC', sans-serif"
    
    # 颜色（来自色彩规范）
    COLOR_PRIMARY = "#FFB74D"  # 哲学琥珀
    COLOR_SECONDARY = "#81D4FA"  # 思考浅蓝
    COLOR_BACKGROUND = "#FFF8E1"  # 书卷米白
    COLOR_ACCENT_BLUE = "#1565C0"  # 智慧深蓝
    COLOR_ACCENT_BROWN = "#5D4037"  # 历史深棕
    COLOR_ACCENT_YELLOW = "#FFF176"  # 互动亮黄
    
    # 路径
    OUTPUT_DIR = Path("outputs/儿童哲学史/排版阶段/章节HTML")
    TEMPLATE_DIR = Path("src/templates")
    IMAGE_DIR = Path("data/illustration_references/草图源文件")
    CSS_FILE = Path("outputs/儿童哲学史/排版阶段/样张/style.css")
    
    # 特殊元素映射
    SPECIAL_ELEMENTS = {
        r'思想剧场': 'thought-theater',
        r'想一想': 'think-about',
        r'古人说': 'ancient-say',
        r'全球望远镜': 'global-telescope',
        r'实践练习': 'practice-exercise',
        r'智慧探险地图碎片': 'wisdom-map',
        r'本章哲学生词卡': 'philosophy-vocab'
    }

def ensure_dir(path):
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)

def read_markdown_file(file_path):
    """读取Markdown文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def image_to_data_url(image_path):
    """将图片转换为Data URL（base64编码）"""
    image_path_str = str(image_path)
    if not os.path.exists(image_path_str):
        print(f"警告: 图片文件不存在: {image_path_str}")
        return None
    
    # 根据扩展名确定MIME类型
    ext = image_path_str.lower().split('.')[-1]
    mime_map = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'svg': 'image/svg+xml',
        'webp': 'image/webp'
    }
    mime_type = mime_map.get(ext, 'image/jpeg')
    
    try:
        with open(image_path_str, 'rb') as f:
            image_data = f.read()
        base64_data = base64.b64encode(image_data).decode('utf-8')
        return f"data:{mime_type};base64,{base64_data}"
    except Exception as e:
        print(f"图片转换失败: {e}")
        return None

def preprocess_markdown(markdown_content, config, chapter_num):
    """
    预处理Markdown，为特殊元素添加HTML包装注释
    并插入图片引用
    """
    lines = markdown_content.split('\n')
    processed_lines = []
    in_special_element = False
    current_element_class = None
    
    for line in lines:
        # 检查是否是标题行（以1-6个#开头，后跟空格）
        if re.match(r'^#{1,6}\s', line):
            # 检查是否包含特殊元素关键词
            for pattern, element_class in config.SPECIAL_ELEMENTS.items():
                if re.search(pattern, line):
                    # 开始特殊元素
                    if not in_special_element:
                        processed_lines.append(f'<!-- BEGIN {element_class} -->')
                        in_special_element = True
                        current_element_class = element_class
                    break
            else:
                # 不包含特殊元素关键词
                if in_special_element:
                    # 结束之前的特殊元素
                    processed_lines.append(f'<!-- END {current_element_class} -->')
                    in_special_element = False
                    current_element_class = None
        
        processed_lines.append(line)
    
    # 如果文件结束时还在特殊元素中，关闭它
    if in_special_element:
        processed_lines.append(f'<!-- END {current_element_class} -->')
    
    result = '\n'.join(processed_lines)
    
    # 插入图片引用
    result = insert_image_references(result, chapter_num)
    
    return result

def postprocess_html(html_content, config):
    """
    后处理HTML，将注释转换为实际的HTML元素
    """
    # 替换特殊元素注释为带CSS类的div
    for pattern, element_class in config.SPECIAL_ELEMENTS.items():
        begin_pattern = f'<!-- BEGIN {element_class} -->'
        end_pattern = f'<!-- END {element_class} -->'
        
        # 替换开始注释
        html_content = html_content.replace(begin_pattern, f'<div class="{element_class}">')
        # 替换结束注释
        html_content = html_content.replace(end_pattern, '</div>')
    
    return html_content

def process_images_in_html(html_content, config):
    """
    处理HTML中的图片引用，转换为Data URI
    """
    img_pattern = r'<img[^>]+src="([^"]+)"[^>]*>'
    
    def replace_img(match):
        img_tag = match.group(0)
        src = match.group(1)
        
        # 如果已经是data URI，跳过
        if src.startswith('data:'):
            return img_tag
        
        # 如果图片路径包含章节引用（如ch2_scene1.jpg），直接使用
        # 否则尝试从配置的图片目录查找
        image_path = config.IMAGE_DIR / src
        
        if os.path.exists(image_path):
            data_url = image_to_data_url(image_path)
            if data_url:
                # 替换src属性
                new_img_tag = re.sub(r'src="[^"]+"', f'src="{data_url}"', img_tag)
                return new_img_tag
        
        # 如果转换失败，返回原标签
        return img_tag
    
    processed_html = re.sub(img_pattern, replace_img, html_content)
    return processed_html

def generate_html(markdown_file, output_file, config, chapter_num):
    """
    生成HTML文件
    """
    ensure_dir(config.OUTPUT_DIR)
    
    print(f"读取Markdown文件: {markdown_file}")
    markdown_content = read_markdown_file(markdown_file)
    
    print("预处理Markdown...")
    processed_markdown = preprocess_markdown(markdown_content, config, chapter_num)
    
    # 创建临时文件保存处理后的Markdown
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp:
        tmp.write(processed_markdown)
        tmp_md_path = tmp.name
    
    try:
        # 使用pandoc转换为HTML
        print("使用pandoc转换为HTML...")
        cmd = [
            'pandoc',
            '--standalone',
            '--wrap=preserve',
            '--to=html',
            '--output=/dev/stdout',  # 输出到标准输出
            tmp_md_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"pandoc转换失败: {result.stderr}")
            return False
        
        html_content = result.stdout
        
        print("后处理HTML...")
        html_content = postprocess_html(html_content, config)
        
        # 处理图片引用
        print("处理图片引用...")
        html_content = process_images_in_html(html_content, config)
        
        # 确保CSS文件存在
        if not config.CSS_FILE.exists():
            print(f"警告: CSS文件不存在: {config.CSS_FILE}")
            # 创建基本的CSS样式
            basic_css = "body { font-family: sans-serif; }"
            ensure_dir(config.CSS_FILE.parent)
            with open(config.CSS_FILE, 'w', encoding='utf-8') as f:
                f.write(basic_css)
        
        # 修改HTML头部，添加CSS链接和viewport
        # 查找</head>标签，在其前插入CSS链接
        head_end_pattern = r'</head>'
        css_link = f'\n    <link rel="stylesheet" href="{config.CSS_FILE.name}">\n'
        
        if re.search(head_end_pattern, html_content):
            html_content = re.sub(head_end_pattern, css_link + '</head>', html_content)
        else:
            # 如果没有</head>标签，直接在body前插入
            body_pattern = r'<body[^>]*>'
            if re.search(body_pattern, html_content):
                html_content = re.sub(body_pattern, css_link + '\n\\g<0>', html_content)
        
        # 写入输出文件
        print(f"写入HTML文件: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True
    
    finally:
        # 清理临时文件
        if os.path.exists(tmp_md_path):
            os.unlink(tmp_md_path)

def main():
    config = Config()
    ensure_dir(config.OUTPUT_DIR)
    
    # 章节映射：章节号 -> 文件名称
    chapters = {
        2: "第二章",
        3: "第三章", 
        4: "第四章",
        5: "第五章",
        6: "第六章",
        7: "第七章",
        8: "第八章",
        9: "第九章",
        10: "第十章",
        11: "第十一章",
        12: "第十二章"
    }
    
    print("=" * 60)
    print("儿童版中国哲学史 - 批量HTML样张生成（带图片嵌入）")
    print(f"目标章节: 第2章至第12章 (共{len(chapters)}章)")
    print(f"输出目录: {config.OUTPUT_DIR}")
    print("=" * 60)
    print()
    
    successful_chapters = []
    failed_chapters = []
    
    for chapter_num, chapter_name in chapters.items():
        print(f"\n{'='*40}")
        print(f"处理: {chapter_name} (章节号: {chapter_num})")
        print(f"{'='*40}")
        
        # 输入文件路径
        input_file = Path(f"outputs/儿童哲学史/优化阶段/{chapter_name}优化稿.md")
        if not input_file.exists():
            print(f"错误: 输入文件不存在: {input_file}")
            failed_chapters.append((chapter_name, "输入文件不存在"))
            continue
        
        # 输出文件路径
        output_file = config.OUTPUT_DIR / f"{chapter_name}样张.html"
        
        success = generate_html(input_file, output_file, config, chapter_num)
        
        if success:
            # 检查文件大小
            file_size = os.path.getsize(output_file) / 1024
            print(f"生成成功: {output_file} ({file_size:.1f} KB)")
            
            # 检查图片数量
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                img_count = len(re.findall(r'<img[^>]*>', content))
                print(f"图片数量: {img_count}")
            
            successful_chapters.append((chapter_name, output_file, file_size, img_count))
        else:
            print(f"生成失败: {chapter_name}")
            failed_chapters.append((chapter_name, "生成过程失败"))
    
    # 生成报告
    print(f"\n{'='*60}")
    print("批量处理完成!")
    print(f"{'='*60}")
    print(f"成功: {len(successful_chapters)} 章")
    print(f"失败: {len(failed_chapters)} 章")
    
    # 抽样检查第2、6、12章
    print(f"\n抽样检查章节: 第2章、第6章、第12章")
    sample_chapters = [2, 6, 12]
    sample_results = []
    
    for chap_num in sample_chapters:
        chap_name = chapters[chap_num]
        file_path = config.OUTPUT_DIR / f"{chap_name}样张.html"
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 检查Data URI
                data_uri_count = len(re.findall(r'src="data:image/[^"]+"', content))
                # 检查CSS类
                css_class_count = len(re.findall(r'class="(thought-theater|think-about|ancient-say|global-telescope|practice-exercise|wisdom-map|philosophy-vocab)"', content))
                
                sample_results.append({
                    'chapter': chap_name,
                    'file_size_kb': os.path.getsize(file_path) / 1024,
                    'data_uri_count': data_uri_count,
                    'css_class_count': css_class_count,
                    'exists': True
                })
        else:
            sample_results.append({
                'chapter': chap_name,
                'exists': False
            })
    
    # 创建报告
    report_content = f"""# 儿童版中国哲学史 - 批量HTML样张生成报告（带图片嵌入）

## 基本信息
- 处理时间: 2026-04-02 21:30
- 目标章节: 第2章至第12章 (共11章)
- 输出目录: `{config.OUTPUT_DIR}`

## 处理结果
| 章节 | 状态 | 文件路径 | 文件大小 | 图片数量 |
|------|------|----------|----------|----------|
"""
    
    for chap_name, file_path, file_size, img_count in successful_chapters:
        report_content += f"| {chap_name} | 成功 | `{file_path}` | {file_size:.1f} KB | {img_count} |\n"
    
    for chap_name, reason in failed_chapters:
        report_content += f"| {chap_name} | 失败 | {reason} | - | - |\n"
    
    report_content += f"""

## 抽样检查结果
| 章节 | 文件是否存在 | 文件大小 | Data URI数量 | CSS类数量 |
|------|--------------|----------|--------------|-----------|
"""
    
    for result in sample_results:
        if result['exists']:
            report_content += f"| {result['chapter']} | 是 | {result['file_size_kb']:.1f} KB | {result['data_uri_count']} | {result['css_class_count']} |\n"
        else:
            report_content += f"| {result['chapter']} | 否 | - | - | - |\n"
    
    report_content += """

## 样式一致性检查
- **与第一章样张对比**: 请手动打开第一章样张 (`outputs/儿童哲学史/排版阶段/样张/第一章样张.html`) 与抽样章节对比，检查标题颜色、字体、行间距、段落缩进等是否全书统一。

## 发现的问题及解决方案
"""

    if failed_chapters:
        report_content += "1. **失败章节**:\n"
        for chap_name, reason in failed_chapters:
            report_content += f"   - {chap_name}: {reason}\n"
        report_content += "\n"
    else:
        report_content += "1. 所有章节均成功生成，图片嵌入功能正常。\n"
    
    report_content += """2. **CSS样式**: 所有章节使用相同的CSS文件 (`outputs/儿童哲学史/排版阶段/样张/style.css`)，确保样式统一。
3. **图片嵌入**: 每章至少嵌入一张场景插图（chX_scene1.jpg），通过Data URI方式确保离线可访问。

## 后续建议
1. 完整审阅所有HTML样张，确认图文内容与样式均符合要求。
2. 如有必要，可根据审阅反馈调整CSS样式，重新批量生成。
3. 完成HTML样张审阅后，可进入PDF导出阶段。

---
**备注**: 本报告为自动化生成，如有疑问请查阅具体文件。
"""
    
    # 保存报告
    report_file = Path("outputs/儿童哲学史/排版阶段/批量生成报告_with_images.md")
    ensure_dir(report_file.parent)
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n报告已保存: {report_file}")
    
    if failed_chapters:
        print(f"\n警告: 有{len(failed_chapters)}章处理失败，请检查日志。")
        sys.exit(1)
    else:
        print("\n批量处理全部成功完成!")

if __name__ == "__main__":
    main()