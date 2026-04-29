import sqlite3
import os

# 数据库路径
db_path = "data/shared_state/state.db"

# 确保数据库文件存在
if not os.path.exists(db_path):
    print(f"数据库文件不存在: {db_path}")
    exit(1)

# 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 更新第八章
chapter_title = "第八章"
cursor.execute("SELECT feedback_summary FROM chapter_progress WHERE chapter_title = ?", (chapter_title,))
row = cursor.fetchone()

if row is None:
    print(f"未找到章节记录: {chapter_title}")
else:
    current_feedback = row[0]
    print(f"第八章当前反馈摘要: {current_feedback}")
    
    if "全球望远镜栏目已完善" in current_feedback:
        print("第八章全球望远镜栏目已完善标记已存在")
    else:
        new_feedback = current_feedback.rstrip("，;")
        if not new_feedback.endswith("；"):
            new_feedback += "；"
        new_feedback += "全球望远镜栏目已完善（对比点、差异说明、思考题、视觉指引）"
        
        cursor.execute("UPDATE chapter_progress SET feedback_summary = ? WHERE chapter_title = ?", 
                       (new_feedback, chapter_title))
        print(f"已更新第八章进度: {new_feedback[:100]}...")

# 更新第九章
chapter_title = "第九章：朱熹的“宇宙大房子”——理学家在做什么？"
cursor.execute("SELECT feedback_summary FROM chapter_progress WHERE chapter_title = ?", (chapter_title,))
row = cursor.fetchone()

if row is None:
    print(f"未找到章节记录: {chapter_title}")
else:
    current_feedback = row[0]
    print(f"第九章当前反馈摘要: {current_feedback}")
    
    if "全球望远镜栏目已完善" in current_feedback:
        print("第九章全球望远镜栏目已完善标记已存在")
    else:
        new_feedback = current_feedback.rstrip("，;")
        if not new_feedback.endswith("；"):
            new_feedback += "；"
        new_feedback += "全球望远镜栏目已完善（对比点、差异说明、思考题、视觉指引）"
        
        cursor.execute("UPDATE chapter_progress SET feedback_summary = ? WHERE chapter_title = ?", 
                       (new_feedback, chapter_title))
        print(f"已更新第九章进度: {new_feedback[:100]}...")

# 提交事务并关闭连接
conn.commit()
conn.close()
print("数据库更新完成")