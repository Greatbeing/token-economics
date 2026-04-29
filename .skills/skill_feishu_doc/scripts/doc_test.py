#!/usr/bin/env python3
import json
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])

from create_doc import create_doc
from fetch_doc import fetch_doc
from update_doc import update_doc


def fetch_doc_example():
    result = fetch_doc(doc_id="NK66dh2J5oQ8swxo6SdcdAdsn7c")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def update_doc_append_example():
    result = update_doc(
        doc_id="NK66dh2J5oQ8swxo6SdcdAdsn7c",
        mode="append",
        markdown="""

## 更新日志

- 2024-01-15: 初始化项目计划
- 2024-01-16: 完成需求分析"""
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


def update_doc_replace_range_example():
    result = update_doc(
        doc_id="NK66dh2J5oQ8swxo6SdcdAdsn7c",
        mode="replace_range",
        markdown="""## 新目标

- 目标 A（已完成）
- 目标 B（进行中）
- 目标 C（待开始）""",
        selection_by_title="目标"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


def create_project_plan():
    result = create_doc(
        title="项目计划",
        markdown="""## 目标

- 目标 1
- 目标 2

## 时间表

| 阶段 | 时间 |
|------|------|
| 开发 | 1周 |
| 测试 | 2周 |"""
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    update_doc_replace_range_example()
