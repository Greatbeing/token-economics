#!/usr/bin/env python3
import sqlite3

db_path = 'data/shared_state/state.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 第六章标题
ch6_title = "第六章 心里害怕怎么办？"

# 检查是否存在
cursor.execute("SELECT chapter_title, feedback_summary FROM chapter_progress WHERE chapter_title = ?", (ch6_title,))
row = cursor.fetchone()
if row:
    print(f"找到第六章记录: {row}")
    # 更新
    cursor.execute("""
        UPDATE chapter_progress 
        SET feedback_summary = feedback_summary || '；全球望远镜栏目已完善（对比点、差异说明、思考题、视觉指引）'
        WHERE chapter_title = ?
    """, (ch6_title,))
    conn.commit()
    print("第六章数据库记录已更新")
else:
    print("未找到第六章记录")

# 验证
cursor.execute("SELECT chapter_title, feedback_summary FROM chapter_progress WHERE chapter_title = ?", (ch6_title,))
updated = cursor.fetchone()
print("更新后:", updated)

conn.close()