#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from generate_chapter_html import match_title_line

# 测试第八章特定映射
line = "## 禅宗故事时间：慧能的传奇"
target = "## 禅宗故事时间"
print(f"line: '{line}'")
print(f"target: '{target}'")
result = match_title_line(line, target)
print(f"匹配结果: {result}")

# 测试其他章节
test_cases = [
    ("## 第一营区：良知信号站（王阳明）", "## 第一站", True),
    ("## 第一课时：梁启超", "## 第一站", True),
    ("## 第二营区：不二法门屋（禅宗）", "## 第二站", True),
    ("## 第二课时：冯友兰", "## 第二站", True),
    ("## 第三营区：木鸡修炼场（庄子）", "## 第三站", True),
    ("## 第三课时：龚自珍", "## 第三站", True),
]

print("\n其他测试:")
for line, target, expected in test_cases:
    result = match_title_line(line, target)
    passed = result == expected
    print(f"{'通过' if passed else '失败'}: line='{line}', target='{target}', expected={expected}, got={result}")