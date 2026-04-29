#!/usr/bin/env python3
import sqlite3
import sys

# 连接数据库
db_path = 'data/shared_state/state.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查表是否存在
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chapter_progress'")
if not cursor.fetchone():
    print("chapter_progress表不存在")
    sys.exit(1)

# 更新第四章记录（章节标题需要确定）
# 先查看现有章节
cursor.execute("SELECT chapter_title, feedback_summary FROM chapter_progress")
rows = cursor.fetchall()
print("当前章节记录:")
for row in rows:
    print(row)

# 更新第四章：章节标题可能是“第四章 我能想做什么就做什么吗？”或类似
ch4_title = "第四章 我能想做什么就做什么吗？"
cursor.execute("SELECT chapter_title FROM chapter_progress WHERE chapter_title = ?", (ch4_title,))
if cursor.fetchone():
    # 更新现有记录
    cursor.execute("""
        UPDATE chapter_progress 
        SET feedback_summary = feedback_summary || '；全球望远镜栏目已完善（对比点、差异说明、思考题、视觉指引）'
        WHERE chapter_title = ?
    """, (ch4_title,))
    print(f"已更新第四章: {ch4_title}")
else:
    print(f"未找到第四章记录: {ch4_title}")

# 更新第五章
ch5_title = "第五章 什么是“好”的规则？"
cursor.execute("SELECT chapter_title FROM chapter_progress WHERE chapter_title = ?", (ch5_title,))
if cursor.fetchone():
    cursor.execute("""
        UPDATE chapter_progress 
        SET feedback_summary = feedback_summary || '；全球望远镜栏目已完善（对比点、差异说明、思考题、视觉指引）'
        WHERE chapter_title = ?
    """, (ch5_title,))
    print(f"已更新第五章: {ch5_title}")
else:
    print(f"未找到第五章记录: {ch5_title}")

# 更新第六章
ch6_title = "第六章：心里害怕怎么办？（王阳明、禅宗、庄子）"
cursor.execute("SELECT chapter_title FROM chapter_progress WHERE chapter_title = ?", (ch6_title,))
if cursor.fetchone():
    cursor.execute("""
        UPDATE chapter_progress 
        SET feedback_summary = feedback_summary || '；全球望远镜栏目已完善（对比点、差异说明、思考题、视觉指引）'
        WHERE chapter_title = ?
    """, (ch6_title,))
    print(f"已更新第六章: {ch6_title}")
else:
    print(f"未找到第六章记录: {ch6_title}")

# 提交事务
conn.commit()

# 再次查询确认
cursor.execute("SELECT chapter_title, feedback_summary FROM chapter_progress")
updated_rows = cursor.fetchall()
print("\n更新后的章节记录:")
for row in updated_rows:
    print(row)

conn.close()
print("数据库更新完成")