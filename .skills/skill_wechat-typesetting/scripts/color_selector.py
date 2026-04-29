#!/usr/bin/env python3
"""
Color Scheme Selector for WeChat Articles

Automatically determines the best color scheme based on article content keywords.
"""

import re
from typing import Dict, Tuple

# Color schemes: (PRIMARY_COLOR, ACCENT_COLOR, DESCRIPTION)
COLOR_SCHEMES = {
    "tech": {
        "primary": "#1E88E5",
        "accent": "#E3F2FD",
        "name": "科技蓝",
        "description": "适合科技、商务、专业类内容",
        "keywords": [
            "科技", "技术", "AI", "人工智能", "数据", "软件", "硬件",
            "编程", "代码", "互联网", "IT", "算法", "云计算", "大数据",
            "商务", "企业", "管理", "战略", "分析", "报告", "professional",
            "technology", "business", "data", "software", "code", "internet"
        ]
    },
    "lifestyle": {
        "primary": "#A8DADC",
        "accent": "#F1FAEE",
        "name": "莫兰迪蓝",
        "description": "适合生活方式、美食、艺术类内容",
        "keywords": [
            "生活", "美食", "旅行", "摄影", "艺术", "设计", "家居", "装修",
            "咖啡", "下午茶", "手工", "DIY", "时尚", "穿搭", "美妆",
            "vlog", "日常", "分享", "lifestyle", "food", "travel", "art",
            "design", "fashion", "coffee", "photography"
        ]
    },
    "motivational": {
        "primary": "#FF6B35",
        "accent": "#FFF3E0",
        "name": "活力橙",
        "description": "适合励志、正能量、激励类内容",
        "keywords": [
            "励志", "激励", "成长", "奋斗", "梦想", "坚持", "努力", "成功",
            "正能量", "加油", "突破", "挑战", "目标", "改变", "提升",
            "motivational", "inspiration", "success", "growth", "energy",
            "positive", "achievement", "goal"
        ]
    },
    "education": {
        "primary": "#00897B",
        "accent": "#E0F2F1",
        "name": "知识青",
        "description": "适合教育、学习、知识分享类内容",
        "keywords": [
            "教育", "学习", "知识", "课程", "培训", "技能", "方法", "干货",
            "教程", "攻略", "指南", "经验", "总结", "笔记", "考试", "证书",
            "education", "learning", "knowledge", "course", "tutorial",
            "skill", "guide", "training", "study"
        ]
    },
    "luxury": {
        "primary": "#7B1FA2",
        "accent": "#F3E5F5",
        "name": "高级紫",
        "description": "适合奢侈品、高端、品质类内容",
        "keywords": [
            "奢侈", "高端", "品质", "精致", "尊贵", "定制", "限量", "私人",
            "品牌", "典藏", "珍品", "臻选", "luxury", "premium", "exclusive",
            "high-end", "quality", "elegant", "sophisticated", "VIP"
        ]
    },
    "health": {
        "primary": "#43A047",
        "accent": "#E8F5E9",
        "name": "健康绿",
        "description": "适合健康、养生、运动类内容",
        "keywords": [
            "健康", "养生", "运动", "健身", "瑜伽", "跑步", "锻炼", "营养",
            "保健", "医疗", "体检", "睡眠", "减肥", "塑身", "health",
            "fitness", "wellness", "exercise", "nutrition", "medical",
            "yoga", "workout"
        ]
    }
}

def analyze_content(text: str) -> Dict[str, int]:
    """
    Analyze article content and count keyword matches for each category.

    Args:
        text: Article content (title + body)

    Returns:
        Dictionary with category scores
    """
    text_lower = text.lower()
    scores = {}

    for category, scheme in COLOR_SCHEMES.items():
        score = 0
        for keyword in scheme["keywords"]:
            # Count occurrences of each keyword
            count = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower))
            score += count
        scores[category] = score

    return scores

def select_color_scheme(text: str) -> Tuple[str, str, str, str]:
    """
    Select the best color scheme based on article content.

    Args:
        text: Article content (title + body)

    Returns:
        Tuple of (primary_color, accent_color, scheme_name, description)
    """
    scores = analyze_content(text)

    # If no keywords matched, default to tech (most versatile)
    if all(score == 0 for score in scores.values()):
        best_category = "tech"
    else:
        # Select category with highest score
        best_category = max(scores, key=scores.get)

    scheme = COLOR_SCHEMES[best_category]
    return (
        scheme["primary"],
        scheme["accent"],
        scheme["name"],
        scheme["description"]
    )

def get_all_schemes() -> Dict:
    """Return all available color schemes."""
    return COLOR_SCHEMES

def main():
    """
    Command-line interface for testing color selection.
    """
    import sys

    if len(sys.argv) < 2:
        print("用法: python color_selector.py <文章文本文件路径>")
        print("\n或者直接传入文本:")
        print("python color_selector.py \"文章标题和内容...\"")
        print("\n可用配色方案:")
        for cat, scheme in COLOR_SCHEMES.items():
            print(f"  - {scheme['name']}: {scheme['description']}")
        sys.exit(1)

    # Read content from file or argument
    content = sys.argv[1]
    try:
        with open(content, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        # Treat as direct text input
        pass

    # Analyze and select
    primary, accent, name, desc = select_color_scheme(content)

    print(f"\n=== 推荐配色方案 ===")
    print(f"方案名称: {name}")
    print(f"适用场景: {desc}")
    print(f"主色调: {primary}")
    print(f"辅助色: {accent}")
    print(f"\n关键词匹配详情:")
    scores = analyze_content(content)
    for cat, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        if score > 0:
            print(f"  {COLOR_SCHEMES[cat]['name']}: {score}个匹配")

if __name__ == "__main__":
    main()
