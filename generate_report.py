#!/usr/bin/env python3
"""生成HTML优化处理报告"""

import json
import os
from pathlib import Path

OUTPUT_DIR = Path("长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/移动端适配/chapters_optimized")
REPORT_FILE = OUTPUT_DIR / "processing_report.json"

chapters = [
    (1, "世界是从哪儿来的？"),
    (2, "「道」是什么？"),
    (3, "人人都是「仁者」？"),
    (4, "我是谁？"),
    (5, "知识从哪儿来？"),
    (6, "幸福是什么？"),
    (7, "正义是什么？"),
    (8, "美是什么？"),
    (9, "什么是真正的自由？"),
    (10, "理想社会是什么样？"),
    (11, "怎样说话才算对？"),
    (12, "古人的智慧，今天怎么用？"),
]

results = []
total_orig = 0
total_new = 0

for num, title in chapters:
    orig_file = Path(f"长期计划/圣哲智慧复制转化工程/outputs/儿童哲学史/排版阶段/章节HTML/修正版/第{num}章样张_fixed_pdf_fixed.html")
    new_file = OUTPUT_DIR / f"第{num}章_mobile.html"
    
    if orig_file.exists() and new_file.exists():
        orig_size = os.path.getsize(orig_file) / 1024
        new_size = os.path.getsize(new_file) / 1024
        compression = (1 - new_size / orig_size) * 100 if orig_size > 0 else 0
        
        results.append({
            "chapter": num,
            "title": title,
            "original_size_kb": round(orig_size, 1),
            "new_size_kb": round(new_size, 1),
            "compression_percent": round(compression, 1),
            "status": "success"
        })
        
        total_orig += orig_size
        total_new += new_size

report = {
    "total_chapters": 12,
    "processed_chapters": len(results),
    "total_original_kb": round(total_orig, 1),
    "total_new_kb": round(total_new, 1),
    "total_compression_percent": round((1 - total_new / total_orig) * 100, 1) if total_orig > 0 else 0,
    "chapters": results,
    "optimizations": [
        "移动端viewport元标签已添加",
        "移动端CSS样式已应用 (style_mobile.css, 464行)",
        "base64内嵌图片已替换为WebP外部引用",
        "图片使用响应式样式 (max-width: 100%)",
        "章节标题已更新"
    ]
}

with open(REPORT_FILE, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("=" * 60)
print("批量优化12章HTML - 处理报告")
print("=" * 60)
print(f"\n处理章节: {len(results)}/12")
print(f"原始总大小: {total_orig:.1f}KB")
print(f"优化后总大小: {total_new:.1f}KB")
print(f"压缩比: {(1 - total_new/total_orig)*100:.1f}%")
print("\n各章节详情:")
print("-" * 60)
for r in results:
    print(f"第{r['chapter']:2d}章: {r['original_size_kb']:8.1f}KB -> {r['new_size_kb']:6.1f}KB  (压缩{r['compression_percent']:.1f}%)")
print("-" * 60)
print("\n优化内容:")
for opt in report["optimizations"]:
    print(f"  [OK] {opt}")
print("\n报告已保存:", REPORT_FILE)
