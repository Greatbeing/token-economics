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

# 查询第八章记录
chapter_title = "第八章 烦恼是怎么来的？"
cursor.execute("SELECT feedback_summary FROM chapter_progress WHERE chapter_title = ?", (chapter_title,))
row = cursor.fetchone()

if row is None:
    print(f"未找到章节记录: {chapter_title}")
    conn.close()
    exit(1)

current_feedback = row[0]
print(f"当前反馈摘要: {current_feedback}")

# 检查是否已包含全球望远镜完善标记
if "全球望远镜栏目已完善" in current_feedback:
    print("全球望远镜栏目已完善标记已存在，无需更新")
else:
    # 追加标记
    new_feedback = current_feedback.rstrip("，;")
    if not new_feedback.endswith("；"):
        new_feedback += "；"
    new_feedback += "全球望远镜栏目已完善（对比点、差异说明、思考题、视觉指引）"
    
    # 更新数据库
    cursor.execute("UPDATE chapter_progress SET feedback_summary = ? WHERE chapter_title = ?", 
                   (new_feedback, chapter_title))
    conn.commit()
    print(f"已更新第八章进度: {new_feedback}")

# 关闭连接
conn.close()