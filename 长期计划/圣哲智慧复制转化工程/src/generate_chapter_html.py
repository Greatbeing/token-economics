#!/usr/bin/env python3
"""
儿童版中国哲学史 - HTML样张生成脚本
基于优化版脚本，生成适合网页浏览的HTML样张
"""

import os
import sys
import subprocess
import tempfile
import shutil
import base64
import re
from pathlib import Path

# 配置参数
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
    OUTPUT_DIR = Path("outputs/儿童哲学史/排版阶段/样张")
    TEMPLATE_DIR = Path("src/templates")
    IMAGE_DIR = Path("data/illustration_references/草图源文件")
    CSS_FILE = Path("outputs/儿童哲学史/排版阶段/样张/style.css")
    MAPPING_FILE = Path("data/illustration_references/chapter_illustration_mapping.json")
    
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

def load_illustration_mapping(mapping_file):
    """加载章节-插图映射表"""
    import json
    if not mapping_file.exists():
        print(f"警告: 映射表文件不存在: {mapping_file}")
        return None
    with open(mapping_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_chapter_number(text):
    """从文本中提取章节数字（中文或阿拉伯数字）"""
    import re
    # 匹配 "第X章" 模式，其中X是中文数字
    match = re.search(r'第([一二三四五六七八九十]+)章', text)
    if match:
        chinese_num = match.group(1)
        chinese_numerals = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
            '十一': 11, '十二': 12
        }
        if chinese_num in chinese_numerals:
            return chinese_numerals[chinese_num]
    # 如果未找到，尝试阿拉伯数字
    match = re.search(r'第(\d+)章', text)
    if match:
        return int(match.group(1))
    return None

def match_title_line(line, target_title):
    """
    灵活匹配标题行与目标标题
    支持变体: '第一站'、'第一营区'、'第一课时'等
    """
    # 去除开头的#和空格
    line_stripped = line.strip()
    if not line_stripped.startswith('#'):
        return False
    
    # 提取标题文本（去掉#和空格）
    title_match = re.match(r'^#+\s*(.*)', line_stripped)
    if not title_match:
        return False
    title_text = title_match.group(1).strip()
    
    # 目标标题格式（如 '## 第一站'）
    target_match = re.match(r'^#+\s*(.*)', target_title.strip())
    if not target_match:
        return False
    target_text = target_match.group(1).strip()
    
    # 如果完全一致，直接返回True
    if title_text == target_text:
        return True
    
    # 特殊处理：思想剧场、想一想等
    special_patterns = {
        '思想剧场': r'思想剧场',
        '想一想': r'想一想',
        '全球望远镜': r'全球望远镜',
        '实践练习': r'实践练习',
        '古人说': r'古人说',
        '禅宗故事时间': r'禅宗故事时间',
    }
    
    for key, pattern in special_patterns.items():
        if key in target_text:
            # 检查标题中是否包含该关键词
            return bool(re.search(pattern, title_text))
    
    # 处理数字站点的变体
    # 匹配中文数字：第一、第二、第三
    num_pattern = r'(第一|第二|第三)'
    num_match = re.search(num_pattern, target_text)
    if not num_match:
        # 如果没有数字部分，使用通用前缀匹配
        # 检查标题文本是否以目标文本开头（忽略冒号等后缀）
        if title_text.startswith(target_text):
            return True
        # 或者目标文本是标题文本的子串
        if target_text in title_text:
            return True
        return False
    
    num_str = num_match.group(1)  # 如 '第一'
    
    # 检查标题中是否包含相同的数字
    if num_str not in title_text:
        return False
    
    # 检查类型变体
    # 目标类型：'站'、'营区'、'课时'等
    type_variants = {
        '站': ['站', '营区', '课时'],
        '营区': ['站', '营区', '课时'],
        '课时': ['站', '营区', '课时'],
    }
    
    # 提取目标类型（数字后的第一个字）
    target_type = target_text[len(num_str):].strip('：: ')
    if not target_type:
        # 如果目标类型为空（如'第一'后面没有字），则只要数字匹配即可
        return True
    
    # 获取该类型可接受的变体
    variants = type_variants.get(target_type, [target_type])
    
    # 检查标题中数字后是否包含任一变体
    # 构造模式：数字后跟可选的冒号/空格，然后是变体
    for variant in variants:
        pattern = num_str + r'[：:\s]*' + variant
        if re.search(pattern, title_text):
            return True
    
    return False

def insert_images_into_markdown(markdown_content, chapter_num, mapping, config):
    """根据映射表在Markdown中插入图片"""
    if mapping is None:
        return markdown_content
    
    # 查找当前章节的映射数据
    chapter_data = None
    for ch in mapping.get("chapters", []):
        if ch.get("chapter_number") == chapter_num:
            chapter_data = ch
            break
    
    if not chapter_data or not chapter_data.get("scenes"):
        print(f"警告: 第{chapter_num}章没有插图映射数据")
        return markdown_content
    
    # 获取位置标签映射
    position_labels = mapping.get("position_labels", {})
    
    # 章节特定标题映射（覆盖通用映射）
    chapter_specific_titles = {
        8: {
            "after_second_station": "## 禅宗故事时间",
        }
    }
    
    # 获取章节特定映射（如果有）
    chapter_overrides = chapter_specific_titles.get(chapter_num, {})
    
    lines = markdown_content.split('\n')
    new_lines = []
    
    # 为每个场景插入图片
    for scene in chapter_data["scenes"]:
        position_label = scene.get("position_label")
        file_name = scene.get("file_name")
        alt_text = scene.get("alt_text", "")
        
        if not position_label or not file_name:
            continue
        
        # 查找对应的标题行，优先使用章节特定映射
        target_title = chapter_overrides.get(position_label)
        if not target_title:
            target_title = position_labels.get(position_label)
        if not target_title:
            print(f"警告: 未知的位置标签: {position_label}")
            continue
        
        # 在lines中查找匹配的标题
        inserted = False
        for i, line in enumerate(lines):
            if match_title_line(line, target_title):
                # 在标题行后插入图片
                # 确保不重复插入（检查下一行是否已经是图片）
                if i+1 < len(lines) and lines[i+1].startswith("!["):
                    print(f"跳过: 第{i+1}行可能已有图片")
                else:
                    # 构造图片Markdown
                    image_path = config.IMAGE_DIR / file_name
                    data_url = image_to_data_url(image_path)
                    if data_url:
                        img_markdown = f'![{alt_text}]({data_url})'
                        new_lines.append(line)
                        new_lines.append(img_markdown)
                        inserted = True
                        # 标记已处理的行，避免重复处理同一标题
                        lines[i] = ""  # 清空已处理的标题行
                    else:
                        new_lines.append(line)
                break
        
        if not inserted:
            # 如果未找到标题，保留原行
            print(f"警告: 未找到标题 '{target_title}'，无法插入图片 {file_name}")
    
    # 添加未处理的行
    for line in lines:
        if line != "":
            new_lines.append(line)
    
    return '\n'.join(new_lines)

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

def preprocess_markdown(markdown_content, config, mapping=None, chapter_num=None):
    """
    预处理Markdown，为特殊元素添加HTML包装注释，并插入图片
    策略：识别任何包含特殊元素关键词的标题，添加注释标记
    """
    # 第一步：插入图片（如果提供了映射表和章节号）
    if mapping is not None and chapter_num is not None:
        markdown_content = insert_images_into_markdown(markdown_content, chapter_num, mapping, config)
    
    # 第二步：为特殊元素添加HTML包装注释
    lines = markdown_content.split('\n')
    processed_lines = []
    in_special_element = False
    current_element_class = None
    
    for line in lines:
        # 检查是否是标题行（以1-6个#开头，后跟空格）
        if re.match(r'^#{1,6}\s', line):
            # 提取标题文本（去除#和空格）
            title_text = re.sub(r'^#{1,6}\s*', '', line).strip()
            
            # 检查是否匹配特殊元素
            matched = False
            for pattern, element_class in config.SPECIAL_ELEMENTS.items():
                if re.search(pattern, title_text):
                    # 如果已经在特殊元素中，先关闭前一个
                    if in_special_element:
                        processed_lines.append(f'<!-- END {current_element_class} -->')
                    
                    # 开始新的特殊元素
                    processed_lines.append(line)
                    processed_lines.append(f'<!-- BEGIN {element_class} -->')
                    in_special_element = True
                    current_element_class = element_class
                    matched = True
                    break
            
            if not matched:
                # 如果不是特殊元素，但当前在特殊元素中，需要先关闭
                if in_special_element:
                    processed_lines.append(f'<!-- END {current_element_class} -->')
                    in_special_element = False
                    current_element_class = None
                processed_lines.append(line)
        
        else:
            processed_lines.append(line)
    
    # 如果文件结束时仍在特殊元素中，需要关闭
    if in_special_element:
        processed_lines.append(f'<!-- END {current_element_class} -->')
    
    return '\n'.join(processed_lines)

def postprocess_html(html_content, config):
    """
    后处理HTML，将注释标记替换为div包装
    """
    # 使用正则表达式替换注释标记
    processed_html = html_content
    
    # 替换所有 BEGIN 注释为对应的div开始标签
    for pattern, element_class in config.SPECIAL_ELEMENTS.items():
        begin_pattern = f'<!-- BEGIN {element_class} -->'
        end_pattern = f'<!-- END {element_class} -->'
        
        # 替换开始标记
        processed_html = processed_html.replace(
            begin_pattern,
            f'<div class="{element_class}">'
        )
        # 替换结束标记
        processed_html = processed_html.replace(
            end_pattern,
            '</div>'
        )
    
    return processed_html

def process_images_in_html(html_content, config):
    """
    处理HTML中的图片引用，将相对路径转换为Data URL
    查找所有<img src="...">标签，如果src是相对路径，则转换为Data URL
    """
    # 查找所有img标签
    img_pattern = r'<img\s+[^>]*src="([^"]+)"[^>]*>'
    
    def replace_img(match):
        img_tag = match.group(0)
        src = match.group(1)
        
        # 如果已经是Data URL，直接返回
        if src.startswith('data:image'):
            return img_tag
        
        # 如果是相对路径，尝试转换为绝对路径
        # 假设图片位于IMAGE_DIR目录下
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

def generate_html(markdown_file, output_file, config):
    """
    生成HTML文件
    """
    ensure_dir(config.OUTPUT_DIR)
    
    print(f"读取Markdown文件: {markdown_file}")
    markdown_content = read_markdown_file(markdown_file)
    
    # 从Markdown内容提取章节编号
    first_line = markdown_content.split('\n')[0]
    chapter_num = extract_chapter_number(first_line)
    if chapter_num is None:
        # 从文件名提取
        file_name = Path(markdown_file).name
        chapter_num = extract_chapter_number(file_name)
    
    print(f"检测到章节编号: {chapter_num}")
    
    # 加载映射表
    mapping = None
    if config.MAPPING_FILE.exists():
        mapping = load_illustration_mapping(config.MAPPING_FILE)
    else:
        print("警告: 映射表文件不存在，将不会插入插图")
    
    print("预处理Markdown...")
    processed_markdown = preprocess_markdown(markdown_content, config, mapping, chapter_num)
    
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
    
    # 输入文件：第一章优化稿
    input_file = Path("outputs/儿童哲学史/优化阶段/第一章优化稿.md")
    if not input_file.exists():
        print(f"错误: 输入文件不存在: {input_file}")
        sys.exit(1)
    
    # 输出文件：第一章HTML样张
    output_file = config.OUTPUT_DIR / "第一章样张.html"
    
    print("=" * 60)
    print("儿童版中国哲学史 - HTML样张生成")
    print("=" * 60)
    print(f"输入文件: {input_file}")
    print(f"输出文件: {output_file}")
    print(f"CSS文件: {config.CSS_FILE}")
    print()
    
    success = generate_html(input_file, output_file, config)
    
    if success:
        print("\n" + "=" * 60)
        print("HTML样张生成成功!")
        print(f"文件位置: {output_file}")
        print("=" * 60)
        
        # 检查文件大小
        file_size = os.path.getsize(output_file) / 1024
        print(f"HTML文件大小: {file_size:.1f} KB")
        
        # 检查CSS是否链接
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'rel="stylesheet"' in content:
                print("CSS链接: 已添加")
            else:
                print("CSS链接: 未找到")
        
        # 检查图片数量
        img_count = len(re.findall(r'<img[^>]*>', content))
        print(f"图片数量: {img_count}")
        
    else:
        print("\nHTML样张生成失败!")
        sys.exit(1)

if __name__ == "__main__":
    main()