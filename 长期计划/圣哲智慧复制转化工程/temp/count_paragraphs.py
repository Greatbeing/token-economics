import re
import sys

def count_chinese_chars(text):
    """统计中文字符数（包括中文标点？通常只计汉字）"""
    # 匹配中文字符（包括中文标点），但这里按之前脚本逻辑只计汉字
    # 使用正则匹配汉字 \u4e00-\u9fff
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)

def main():
    file_path = "outputs/儿童哲学史/优化阶段/第六章优化稿.md"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按空行分割段落
    paragraphs = content.split('\n\n')
    
    para_counts = []
    for i, para in enumerate(paragraphs):
        if not para.strip():
            continue
        count = count_chinese_chars(para)
        if count > 0:
            para_counts.append((i, count, para[:100]))
    
    # 按字数降序排序
    para_counts.sort(key=lambda x: x[1], reverse=True)
    
    print("段落字数排名（前20）：")
    for i, (idx, count, preview) in enumerate(para_counts[:20]):
        print(f"{i+1}. 段落{idx}: {count}字 - {preview}...")
    
    # 总字数
    total = sum(count for _, count, _ in para_counts)
    print(f"\n总中文字数（段落合计）: {total}")
    
    # 验证与之前统计一致
    total_all = count_chinese_chars(content)
    print(f"全文中文字数: {total_all}")

if __name__ == '__main__':
    main()