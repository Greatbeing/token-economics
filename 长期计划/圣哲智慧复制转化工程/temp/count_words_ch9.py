import re
import sys

def count_chinese_characters(text):
    # 匹配中文字符
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return len(chinese_pattern.findall(text))

def estimate_word_count(text):
    # 汉字数量，估算字数（通常汉字数*0.8）
    chinese_count = count_chinese_characters(text)
    # 加上非汉字部分（数字、英文单词等）的粗略估计
    # 简单处理：汉字数 * 0.8
    return chinese_count, int(chinese_count * 0.8)

if __name__ == "__main__":
    filename = "outputs/儿童哲学史/优化阶段/第九章优化稿.md"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        chinese_count, word_count = estimate_word_count(content)
        print(f"汉字数量: {chinese_count}")
        print(f"估算字数: {word_count}")
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)