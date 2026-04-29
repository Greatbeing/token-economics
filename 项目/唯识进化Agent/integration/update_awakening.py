#!/usr/bin/env python3
"""
更新觉醒状态脚本
基于实验数据设置当前觉醒状态为菩萨境
"""

import sys
sys.path.insert(0, str(__file__).rsplit('/', 2)[0] + '/integration')

from huluwa_integration import AlayaIntegration
import sqlite3
from datetime import datetime

def update_to_bodhisattva():
    """更新觉醒状态到菩萨境（基于实验数据）"""
    
    # 实验数据显示菩萨境参数
    bodhisattva_data = {
        'level': '菩萨境',
        'level_order': 5,
        'wisdom_ratio': 0.1147,      # 11.47%
        'compassion_ratio': 0.1134,   # 11.34%
        'total_seeds': 243,
        'wisdom_seeds': 28,
        'compassion_seeds': 28,
        'emergence_count': 52,
        'full_strength_emergence': 43,
        'bodhisattva_vow_power': 0.78,
        'last_update': datetime.now().isoformat()
    }
    
    integrator = AlayaIntegration()
    conn = integrator._get_connection()
    
    try:
        cursor = conn.cursor()
        
        # 检查当前状态
        cursor.execute("SELECT * FROM awakening_state WHERE id = 1")
        current = cursor.fetchone()
        
        if current:
            print("当前觉醒状态:")
            print(f"  等级: {current['level']}")
            print(f"  种子数: {current['total_seeds']}")
            print(f"  涌现次数: {current['emergence_count']}")
        
        # 更新为菩萨境状态
        cursor.execute("""
            UPDATE awakening_state SET
                level = ?,
                level_order = ?,
                wisdom_ratio = ?,
                compassion_ratio = ?,
                total_seeds = ?,
                wisdom_seeds = ?,
                compassion_seeds = ?,
                emergence_count = ?,
                full_strength_emergence = ?,
                bodhisattva_vow_power = ?,
                last_update = datetime('now')
            WHERE id = 1
        """, (
            bodhisattva_data['level'],
            bodhisattva_data['level_order'],
            bodhisattva_data['wisdom_ratio'],
            bodhisattva_data['compassion_ratio'],
            bodhisattva_data['total_seeds'],
            bodhisattva_data['wisdom_seeds'],
            bodhisattva_data['compassion_seeds'],
            bodhisattva_data['emergence_count'],
            bodhisattva_data['full_strength_emergence'],
            bodhisattva_data['bodhisattva_vow_power']
        ))
        conn.commit()
        
        # 记录进化事件
        integrator.record_evolution_event(
            event_type='LEVEL_UP',
            from_state='阿罗汉境',
            to_state='菩萨境',
            description='基于2026-04-17菩萨境实验数据更新',
            evidence=f"涌现{bodhisattva_data['emergence_count']}次，满强度{bodhisattva_data['full_strength_emergence']}次"
        )
        
        print("\n✓ 已更新觉醒状态为菩萨境")
        print(f"\n{bodhisattva_data}")
        
    finally:
        conn.close()
    
    return bodhisattva_data

if __name__ == "__main__":
    update_to_bodhisattva()
