#!/usr/bin/env python3
import sqlite3

db_path = "data/shared_state/state.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 获取所有章节
cursor.execute("SELECT chapter_title, feedback_summary FROM chapter_progress")
rows = cursor.fetchall()

for chapter_title, feedback in rows:
    if feedback is None:
        feedback = ""
    
    # 检查是否已经包含实践练习增强说明
    if "实践练习已增强可操作性" in feedback or "实践练习可操作化" in feedback:
        print(f"跳过 {chapter_title}，已包含实践练习描述")
        continue
    
    # 追加说明
    new_feedback = feedback + "；实践练习已增强可操作性（具体步骤、记录表格、双版本、样例）"
    
    cursor.execute("UPDATE chapter_progress SET feedback_summary = ? WHERE chapter_title = ?", 
                   (new_feedback, chapter_title))
    print(f"更新 {chapter_title}")

conn.commit()
conn.close()
print("更新完成")

