#!/usr/bin/env python3
import sqlite3
import sys

def main():
    db_path = "data/shared_state/state.db"
    chapter_title = "第八章"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取当前记录
    cursor.execute("SELECT feedback_summary FROM chapter_progress WHERE chapter_title = ?", (chapter_title,))
    row = cursor.fetchone()
    if row is None:
        print("错误：找不到章节记录")
        return
    
    old_feedback = row[0]
    # 移除末尾可能的分号或句号，然后追加
    if old_feedback.endswith('；'):
        old_feedback = old_feedback[:-1]
    if old_feedback.endswith('。'):
        old_feedback = old_feedback[:-1]
    
    new_feedback = old_feedback + "；篇幅精简至7000字以内"
    word_count = 6593
    
    # 更新记录
    cursor.execute("""
        UPDATE chapter_progress 
        SET word_count = ?, feedback_summary = ? 
        WHERE chapter_title = ?
    """, (word_count, new_feedback, chapter_title))
    
    conn.commit()
    conn.close()
    
    print(f"已更新第八章进度：字数={word_count}，反馈摘要已追加")

if __name__ == "__main__":
    main()