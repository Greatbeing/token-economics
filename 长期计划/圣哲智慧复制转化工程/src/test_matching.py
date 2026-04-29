#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_chapter_html import match_title_line

# 测试用例
test_cases = [
    # (line, target_title, expected_result)
    ("## 第一站", "## 第一站", True),
    ("## 第一站：孟子", "## 第一站", True),
    ("## 第一营区：良知信号站（王阳明）", "## 第一站", True),
    ("## 第一课时：梁启超", "## 第一站", True),
    ("## 第二站", "## 第二站", True),
    ("## 第二营区：不二法门屋（禅宗）", "## 第二站", True),
    ("## 第二课时：冯友兰", "## 第二站", True),
    ("## 第三站", "## 第三站", True),
    ("## 第三营区：木鸡修炼场（庄子）", "## 第三站", True),
    ("## 第三课时：龚自珍", "## 第三站", True),
    ("## 思想剧场", "## 思想剧场", True),
    ("## 思想剧场：小敏的烦恼侦探所", "## 思想剧场", True),
    ("## 想一想", "## 想一想", True),
    ("## 想一想（互动升级版）", "## 想一想", True),
    ("## 全球望远镜", "## 全球望远镜", True),
    ("## 全球望远镜：中西心灵探险对话", "## 全球望远镜", True),
    ("## 实践练习", "## 实践练习", True),
    ("## 实践练习：6章主题实践", "## 实践练习", True),
    # 不匹配的用例
    ("## 第四站", "## 第一站", False),
    ("## 第一营", "## 第一站", False),
    ("## 第一", "## 第一站", False),
    ("## 思想剧场", "## 第一站", False),
]

print("测试匹配函数...")
all_passed = True
for i, (line, target, expected) in enumerate(test_cases, 1):
    result = match_title_line(line, target)
    passed = result == expected
    if not passed:
        all_passed = False
        print(f"测试 {i} 失败: line='{line}', target='{target}', expected={expected}, got={result}")
    else:
        print(f"测试 {i} 通过")

if all_passed:
    print("所有测试通过！")
else:
    print("部分测试失败")
    sys.exit(1)