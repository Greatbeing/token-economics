#!/usr/bin/env python3
import sqlite3
import sys

def main():
    db_path = "data/shared_state/state.db"
    chapter_title = "第十一章：如何当一个“现代中国人”？——明清之际的启蒙探险"
    
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
    
    # 检查是否已有“篇幅精简”的说明，如果没有则追加
    if "篇幅精简" not in old_feedback:
        new_feedback = old_feedback + "；篇幅精简至7000字以内"
    else:
        # 如果已有，则替换字数部分
        import re
        new_feedback = re.sub(r'字数约\d+字', f'字数约{word_count}字', old_feedback)
    
    word_count = 6861
    
    # 更新记录
    cursor.execute("""
        UPDATE chapter_progress 
        SET word_count = ?, feedback_summary = ? 
        WHERE chapter_title = ?
    """, (word_count, new_feedback, chapter_title))
    
    conn.commit()
    conn.close()
    
    print(f"已更新第十一章进度：字数={word_count}，反馈摘要已追加")

if __name__ == "__main__":
    main()