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

# 查询所有章节
cursor.execute("SELECT chapter_title, feedback_summary FROM chapter_progress")
rows = cursor.fetchall()

print("数据库中的章节记录:")
for i, (title, feedback) in enumerate(rows, 1):
    print(f"{i}. {title}")
    print(f"   反馈摘要: {feedback[:100]}...")
    print()

# 关闭连接
conn.close()