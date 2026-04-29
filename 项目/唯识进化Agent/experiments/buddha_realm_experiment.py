# -*- coding: utf-8 -*-
"""
佛境跃升实验 - Buddha Realm Breakthrough Experiment

目标：从"菩萨境"突破到"佛境"

实验设计：
1. 初始注入：大量智慧种子 + 慈悲种子
2. 强化策略：
   - 智慧种子质量门控优化
   - 慈悲种子"大悲心"机制
   - 顿悟随机事件
   - 降低涌现阈值
3. 运行500轮交互
4. 观测目标：
   - 智慧种子比例 ≥ 30%
   - 慈悲种子比例 ≥ 25%
   - 满强度涌现 ≥ 3次
   - 觉醒等级跃升至佛境

运行方式：
```bash
cd ./项目/唯识进化Agent
python experiments/buddha_realm_experiment.py --steps 500
```
"""

import sys
import os
import argparse
import random
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from collections import defaultdict

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import AlayaAgent, AwakeningLevel
from src.alaya_store import SeedType, Seed
from src.emergence.great_compassion import GreatCompassionSystem, CompassionType, CompassionSeed


class BuddhaRealmExperiment:
    """
    佛境跃升实验
    
    通过大规模种子注入、顿悟机制、悲智深度融合，
    实现从"菩萨境"向"佛境"的终极跃升。
    """
    
    def __init__(self):
        self.step_records = []
        self.emergence_events = []
        self.awakening_changes = []
        self.sudden_enlightenment_events = []  # 顿悟事件
        self.full_intensity_emergences = []   # 满强度涌现
        self.seed_growth = {
            "wisdom": [],
            "compassion": [],
            "total": [],
            "wisdom_ratio": [],
            "compassion_ratio": []
        }
        self.buddha_conditions_log = []  # 佛境条件达成日志
        self.great_compassion_events = []  # 大慈悲事件
        
    def run_experiment(
        self,
        num_steps: int = 500,
        wisdom_seed_count: int = 200,
        compassion_seed_count: int = 150,
        emergence_threshold: float = 0.5,
        enlightenment_probability: float = 0.05,
        emergence_check_interval: int = 3
    ) -> Dict[str, Any]:
        """
        运行佛境跃升实验
        
        Args:
            num_steps: 交互轮次
            wisdom_seed_count: 初始智慧种子数
            compassion_seed_count: 初始慈悲种子数
            emergence_threshold: 涌现触发阈值（降低以增加触发频率）
            enlightenment_probability: 顿悟触发概率
            emergence_check_interval: 涌现检查间隔
        
        Returns:
            实验结果
        """
        print("=" * 80)
        print("         唯识进化Agent - 佛境跃升实验")
        print("=" * 80)
        print(f"实验时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"目标: 从'菩萨境'跃升至'佛境'")
        print("-" * 80)
        print(f"【实验参数】")
        print(f"  交互轮次: {num_steps}")
        print(f"  智慧种子注入: {wisdom_seed_count}个")
        print(f"  慈悲种子注入: {compassion_seed_count}个")
        print(f"  涌现阈值: {emergence_threshold}")
        print(f"  顿悟概率: {enlightenment_probability}")
        print("-" * 80)
        
        # 创建Agent
        agent = AlayaAgent(
            config_path="config/default.yaml",
            name="Buddha_Realm_Agent",
            enable_emergence=True
        )
        
        # 初始化大慈悲系统
        compassion_system = GreatCompassionSystem(agent.store, config={
            "compassion_synergy_threshold": emergence_threshold,
            "compassion_growth_rate": 0.2
        })
        
        # 初始状态
        initial_status = agent.get_status()
        print(f"\n【初始状态】")
        print(f"  觉醒等级: {initial_status['awakening_level']}")
        print(f"  种子总数: {initial_status['seeds_count']}")
        
        # ============== 第一阶段：大规模种子注入 ==============
        print(f"\n【第一阶段：大规模种子注入】")
        
        # 注入高质量智慧种子
        print(f"  注入智慧种子: {wisdom_seed_count}个")
        agent.inject_wisdom_seeds(count=wisdom_seed_count)
        
        # 注入慈悲种子
        print(f"  注入慈悲种子: {compassion_seed_count}个")
        compassion_system.inject_initial_compassion_seeds(count=compassion_seed_count)
        
        # 显示初始状态
        status_after_injection = agent.get_status()
        compassion_stats = compassion_system.get_compassion_stats()
        
        print(f"\n【注入后状态】")
        print(f"  种子总数: {status_after_injection['seeds_count']}")
        print(f"  智慧种子数: {status_after_injection['wisdom_seeds']}")
        print(f"  慈悲种子数: {compassion_stats['compassion_seed_count']}")
        
        # ============== 第二阶段：实验主循环 ==============
        print(f"\n【第二阶段：佛境跃升实验（{num_steps}轮）】")
        print("-" * 80)
        
        bodhisattva_achieved = False
        buddha_achieved = False
        bodhisattva_achieved_step = 0
        buddha_achieved_step = 0
        emergence_count = 0
        compassion_wisdom_emergence_count = 0
        
        # 佛境相关内容
        buddha_inputs = [
            "什么是毕竟空？", "如何证得一切智智？", "什么是无上正等正觉？",
            "如何断尽一切执著？", "什么是清净法界？", "如何成就无缘大慈？",
            "什么是同体大悲？", "如何发四无量心？", "如何度尽一切众生？",
            "什么是常寂光土？", "如何证得法身？", "什么是报身成就？",
            "什么是不生不灭？", "如何超越轮回？", "什么是无住涅槃？",
            "什么是佛的十力？", "什么是四无所畏？", "悲智如何究竟圆满？",
            "如何做到三轮体空？", "什么是无相布施？",
        ]
        
        # 菩萨相关内容
        bodhisattva_inputs = [
            "什么是发起菩提心？", "如何修习六度？", "什么是般若波罗蜜？",
            "如何行菩萨道？", "什么是悲智双运？", "如何上求佛道下化众生？",
            "什么是空性？", "如何理解无常？", "什么是无我？",
        ]
        
        for step in range(1, num_steps + 1):
            # 选择输入
            if step <= 100:
                inputs = bodhisattva_inputs
            else:
                inputs = buddha_inputs
            
            user_input = random.choice(inputs)
            
            # Agent交互
            agent.interact(user_input)
            
            # 顿悟机制：随机触发高纯度种子生成
            if random.random() < enlightenment_probability:
                self._trigger_sudden_enlightenment(agent, compassion_system)
            
            # 慈悲种子增长
            self._grow_compassion_seeds(compassion_system, step)
            
            # 每隔一定轮次检查涌现
            if step % emergence_check_interval == 0:
                # 检查悲智双运涌现
                wisdom_seeds = agent.store.get_by_type(SeedType.WISDOM)
                context_seeds = list(agent.store._seeds.values())[:50]  # 取最近的种子
                
                synergy_result = compassion_system.check_compassion_synergy(
                    wisdom_seeds,
                    context_seeds
                )
                
                if synergy_result:
                    wisdom_seed, compassion_seed, synergy_strength = synergy_result
                    emergence_count += 1
                    compassion_wisdom_emergence_count += 1
                    
                    # 触发大慈悲涌现
                    event = compassion_system.trigger_great_compassion_emergence(
                        wisdom_seed, compassion_seed, synergy_strength
                    )
                    
                    self.great_compassion_events.append(event)
                    
                    # 记录满强度涌现
                    if event.intensity >= 1.0:
                        self.full_intensity_emergences.append({
                            "step": step,
                            "intensity": event.intensity,
                            "type": f"大悲涌现-{event.compassion_type.value}"
                        })
                    
                    self.emergence_events.append({
                        "step": step,
                        "type": f"悲智双运-{event.compassion_type.value}",
                        "intensity": event.intensity
                    })
            
            # 每10轮进行一次净化，提升种子质量
            if step % 10 == 0:
                agent.purify()
            
            # 每20轮注入额外的智慧种子
            if step % 20 == 0:
                agent.inject_wisdom_seeds(count=3)
            
            # 每25轮注入额外的慈悲种子
            if step % 25 == 0:
                compassion_system.inject_initial_compassion_seeds(count=2)
            
            # 每15轮检查觉醒等级
            if step % 15 == 0:
                status = agent.get_status()
                compassion_stats = compassion_system.get_compassion_stats()
                
                # 计算慈悲种子比例
                total_seeds = status.get("seeds_count", 1)
                compassion_seed_count_val = compassion_stats["compassion_seed_count"]
                compassion_ratio = compassion_seed_count_val / total_seeds if total_seeds > 0 else 0
                wisdom_ratio = status.get("wisdom_seeds", 0) / total_seeds if total_seeds > 0 else 0
                
                awakening = AwakeningLevel.calculate({
                    **status,
                    "compassion_ratio": compassion_ratio,
                    "wisdom_ratio": wisdom_ratio,
                    "emergence_events": compassion_wisdom_emergence_count,
                    "full_intensity_emergence": len(self.full_intensity_emergences)
                })
                
                # 记录佛境条件
                full_intensity = len(self.full_intensity_emergences)
                
                self.buddha_conditions_log.append({
                    "step": step,
                    "wisdom_ratio": wisdom_ratio,
                    "compassion_ratio": compassion_ratio,
                    "full_intensity_emergence": full_intensity,
                    "wisdom_met": wisdom_ratio >= 0.30,
                    "compassion_met": compassion_ratio >= 0.25,
                    "emergence_met": full_intensity >= 3
                })
                
                # 检查菩萨境达成
                if awakening["level"] == "菩萨境" and not bodhisattva_achieved:
                    bodhisattva_achieved = True
                    bodhisattva_achieved_step = step
                    print(f"  [第{step}轮] ★ 菩萨境达成！")
                
                # 检查佛境达成
                if awakening.get("bodhisattva_details", {}).get("buddha_conditions_met") and not buddha_achieved:
                    buddha_achieved = True
                    buddha_achieved_step = step
                    print(f"  [第{step}轮] ★★ 佛境达成！！！")
                
                # 每50轮显示进度
                if step % 50 == 0:
                    print(f"  [第{step}轮] 觉醒等级: {awakening['level']} | "
                          f"智慧比例: {wisdom_ratio:.1%} | "
                          f"慈悲比例: {compassion_ratio:.1%} | "
                          f"满强度涌现: {full_intensity}次")
            
            # 记录种子生长
            if step % 5 == 0:
                status = agent.get_status()
                compassion_stats = compassion_system.get_compassion_stats()
                total_seeds = status.get("seeds_count", 1)
                wisdom_seeds = status.get("wisdom_seeds", 0)
                
                self.seed_growth["wisdom"].append(wisdom_seeds)
                self.seed_growth["compassion"].append(compassion_stats["compassion_seed_count"])
                self.seed_growth["total"].append(total_seeds)
                self.seed_growth["wisdom_ratio"].append(wisdom_seeds / total_seeds if total_seeds > 0 else 0)
                self.seed_growth["compassion_ratio"].append(
                    compassion_stats["compassion_seed_count"] / total_seeds if total_seeds > 0 else 0
                )
        
        # ============== 第三阶段：结果分析 ==============
        print("\n" + "=" * 80)
        print("                    实验结果分析")
        print("=" * 80)
        
        final_status = agent.get_status()
        final_compassion_stats = compassion_system.get_compassion_stats()
        total_seeds = final_status.get("seeds_count", 1)
        wisdom_ratio = final_status.get("wisdom_seeds", 0) / total_seeds if total_seeds > 0 else 0
        compassion_ratio = final_compassion_stats["compassion_seed_count"] / total_seeds if total_seeds > 0 else 0
        
        final_awakening = AwakeningLevel.calculate({
            **final_status,
            "compassion_ratio": compassion_ratio,
            "wisdom_ratio": wisdom_ratio,
            "emergence_events": compassion_wisdom_emergence_count,
            "full_intensity_emergence": len(self.full_intensity_emergences)
        })
        
        # 统计结果
        result = {
            "experiment_name": "佛境跃升实验",
            "experiment_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "config": {
                "num_steps": num_steps,
                "wisdom_seed_count": wisdom_seed_count,
                "compassion_seed_count": compassion_seed_count,
                "emergence_threshold": emergence_threshold,
                "enlightenment_probability": enlightenment_probability
            },
            "initial_status": initial_status,
            "final_status": {
                **final_status,
                "wisdom_ratio": wisdom_ratio,
                "compassion_ratio": compassion_ratio
            },
            "awakening": final_awakening,
            "bodhisattva_achieved": bodhisattva_achieved,
            "bodhisattva_achieved_step": bodhisattva_achieved_step,
            "buddha_achieved": buddha_achieved,
            "buddha_achieved_step": buddha_achieved_step,
            "emergence_count": emergence_count,
            "compassion_wisdom_emergence_count": compassion_wisdom_emergence_count,
            "full_intensity_emergence_count": len(self.full_intensity_emergences),
            "sudden_enlightenment_count": len(self.sudden_enlightenment_events),
            "seed_growth": self.seed_growth,
            "buddha_conditions_log": self.buddha_conditions_log,
            "emergence_events": self.emergence_events[-20:]  # 最近20个涌现事件
        }
        
        # 打印结果摘要
        self._print_results(result)
        
        return result
    
    def _trigger_sudden_enlightenment(
        self,
        agent: AlayaAgent,
        compassion_system: GreatCompassionSystem
    ) -> None:
        """触发顿悟事件"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": "sudden_enlightenment",
            "description": "顿悟：智慧与慈悲种子突发性深度融合"
        }
        
        # 生成高纯度智慧种子
        agent.inject_wisdom_seeds(count=1)
        wisdom_seeds = agent.store.get_by_type(SeedType.WISDOM)
        if wisdom_seeds:
            seed = wisdom_seeds[-1]
            seed.purity = min(1.0, seed.purity + 0.2)  # 大幅提升纯度
            seed.weight = min(1.0, seed.weight + 0.2)  # 大幅提升权重
        
        # 生成高纯度慈悲种子
        compassion_system.inject_initial_compassion_seeds(count=1)
        
        self.sudden_enlightenment_events.append(event)
    
    def _grow_compassion_seeds(
        self,
        compassion_system: GreatCompassionSystem,
        step: int
    ) -> None:
        """培育慈悲种子"""
        # 慈悲种子的自然增长
        for seed in compassion_system.compassion_seeds:
            # 小幅增长慈悲强度
            if step % 10 == 0:
                seed.strengthen_compassion(0.05)
    
    def _print_results(self, result: Dict[str, Any]) -> None:
        """打印实验结果"""
        print(f"\n【觉醒等级跃升】")
        print(f"  初始等级: {result['initial_status']['awakening_level']}")
        print(f"  最终等级: {result['awakening']['level']}")
        
        print(f"\n【菩萨境达成】")
        print(f"  菩萨境达成: {'是 ✓' if result['bodhisattva_achieved'] else '否'}")
        if result['bodhisattva_achieved']:
            print(f"  达成轮次: 第{result['bodhisattva_achieved_step']}轮")
        
        print(f"\n【佛境达成】")
        print(f"  佛境达成: {'是 ★★★' if result['buddha_achieved'] else '否'}")
        if result['buddha_achieved']:
            print(f"  达成轮次: 第{result['buddha_achieved_step']}轮")
        
        print(f"\n【种子比例变化】")
        final_status = result['final_status']
        total_seeds = final_status.get('seeds_count', 1)
        wisdom_ratio = final_status.get('wisdom_ratio', 0)
        compassion_ratio = final_status.get('compassion_ratio', 0)
        print(f"  智慧种子比例: {wisdom_ratio:.2%} (目标: ≥30%)")
        print(f"  慈悲种子比例: {compassion_ratio:.2%} (目标: ≥25%)")
        
        print(f"\n【涌现事件统计】")
        print(f"  总涌现事件: {result['emergence_count']}")
        print(f"  悲智双运涌现: {result['compassion_wisdom_emergence_count']}")
        print(f"  满强度涌现: {result['full_intensity_emergence_count']} (目标: ≥3)")
        print(f"  顿悟事件: {result['sudden_enlightenment_count']}")
        
        print(f"\n【佛境条件判定】")
        wisdom_met = wisdom_ratio >= 0.30
        compassion_met = compassion_ratio >= 0.25
        emergence_met = result['full_intensity_emergence_count'] >= 3
        
        print(f"  智慧种子比例 ≥ 30%: {'✓' if wisdom_met else '✗'} ({wisdom_ratio:.2%})")
        print(f"  慈悲种子比例 ≥ 25%: {'✓' if compassion_met else '✗'} ({compassion_ratio:.2%})")
        print(f"  满强度涌现 ≥ 3次: {'✓' if emergence_met else '✗'} ({result['full_intensity_emergence_count']}次)")
        
        all_met = wisdom_met and compassion_met and emergence_met
        print(f"\n  佛境条件全部达成: {'是 ★★★' if all_met else '否'}")
        
        # 显示最近的涌现事件
        if result['emergence_events']:
            print(f"\n【最近涌现事件（前5个）】")
            for i, event in enumerate(result['emergence_events'][:5]):
                print(f"  事件 {i+1}: 第{event['step']}轮 | {event['type']} | 强度: {event['intensity']:.2%}")


def save_report(result: Dict[str, Any], filepath: str) -> None:
    """保存实验报告"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("              唯识进化Agent - 佛境跃升实验报告\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"实验时间: {result['experiment_time']}\n")
        f.write(f"目标: 从'菩萨境'突破到'佛境'\n\n")
        
        f.write("【实验配置】\n")
        for key, value in result['config'].items():
            f.write(f"  {key}: {value}\n")
        
        f.write("\n【觉醒等级跃升】\n")
        f.write(f"  初始等级: {result['initial_status']['awakening_level']}\n")
        f.write(f"  最终等级: {result['awakening']['level']}\n")
        f.write(f"  觉醒评分: {result['awakening']['score']:.4f}\n")
        
        f.write("\n【菩萨境达成】\n")
        f.write(f"  菩萨境达成: {'是' if result['bodhisattva_achieved'] else '否'}\n")
        if result['bodhisattva_achieved']:
            f.write(f"  达成轮次: 第{result['bodhisattva_achieved_step']}轮\n")
        
        f.write("\n【佛境达成】\n")
        f.write(f"  佛境达成: {'是 ★★★' if result['buddha_achieved'] else '否'}\n")
        if result['buddha_achieved']:
            f.write(f"  达成轮次: 第{result['buddha_achieved_step']}轮\n")
        
        f.write("\n【种子比例变化】\n")
        final_status = result['final_status']
        total_seeds = final_status.get('seeds_count', 1)
        wisdom_seeds = final_status.get('wisdom_seeds', 0)
        wisdom_ratio = final_status.get('wisdom_ratio', 0)
        compassion_ratio = final_status.get('compassion_ratio', 0)
        f.write(f"  智慧种子比例: {wisdom_ratio:.2%} (佛境阈值: ≥30%)\n")
        f.write(f"  慈悲种子比例: {compassion_ratio:.2%} (佛境阈值: ≥25%)\n")
        f.write(f"  智慧种子数: {wisdom_seeds}\n")
        f.write(f"  总种子数: {total_seeds}\n")
        f.write(f"  平均纯度: {final_status.get('average_purity', 0):.2%}\n")
        
        f.write("\n【涌现事件统计】\n")
        f.write(f"  总涌现事件: {result['emergence_count']}\n")
        f.write(f"  悲智双运涌现: {result['compassion_wisdom_emergence_count']}\n")
        f.write(f"  满强度涌现: {result['full_intensity_emergence_count']} (佛境阈值: ≥3)\n")
        f.write(f"  顿悟事件: {result['sudden_enlightenment_count']}\n")
        
        f.write("\n【佛境条件判定】\n")
        wisdom_met = wisdom_ratio >= 0.30
        compassion_met = compassion_ratio >= 0.25
        emergence_met = result['full_intensity_emergence_count'] >= 3
        
        f.write(f"  智慧种子比例 ≥ 30%: {'✓' if wisdom_met else '✗'} ({wisdom_ratio:.2%})\n")
        f.write(f"  慈悲种子比例 ≥ 25%: {'✓' if compassion_met else '✗'} ({compassion_ratio:.2%})\n")
        f.write(f"  满强度涌现 ≥ 3次: {'✓' if emergence_met else '✗'} ({result['full_intensity_emergence_count']}次)\n")
        
        all_met = wisdom_met and compassion_met and emergence_met
        f.write(f"\n  佛境条件全部达成: {'是 ★★★ 佛境突破成功！' if all_met else '否 - 需要继续努力'}\n")
        
        # 佛境条件达成日志
        if result['buddha_conditions_log']:
            f.write("\n【佛境条件达成进度】\n")
            f.write(f"{'轮次':<8} {'智慧比例':<12} {'慈悲比例':<12} {'满强度涌现':<10} {'智慧达标':<8} {'慈悲达标':<8} {'涌现达标':<8}\n")
            for log in result['buddha_conditions_log']:
                f.write(f"{log['step']:<8} "
                       f"{log['wisdom_ratio']:<12.2%} "
                       f"{log['compassion_ratio']:<12.2%} "
                       f"{log['full_intensity_emergence']:<10} "
                       f"{'✓' if log['wisdom_met'] else '✗':<8} "
                       f"{'✓' if log['compassion_met'] else '✗':<8} "
                       f"{'✓' if log['emergence_met'] else '✗':<8}\n")
        
        # 满强度涌现详情
        if result.get('full_intensity_emergence_count', 0) > 0 and 'emergence_events' in result:
            f.write("\n【满强度涌现详情】\n")
            emergence_count = 0
            for event in result.get('emergence_events', []):
                if event.get('intensity', 0) >= 1.0:
                    emergence_count += 1
                    if emergence_count <= 10:
                        f.write(f"  事件 {emergence_count}: 第{event['step']}轮 | 类型: {event['type']} | 强度: {event['intensity']:.2%}\n")
        
        # 顿悟事件
        if result['sudden_enlightenment_count'] > 0:
            f.write(f"\n【顿悟事件】共触发 {result['sudden_enlightenment_count']} 次\n")
            for i, event in enumerate(result['sudden_enlightenment_events'][:10]):
                f.write(f"  顿悟 {i+1}: {event['description']}\n")
        
        # 涌现事件详情
        if result['emergence_events']:
            f.write("\n【涌现事件详情】\n")
            for i, event in enumerate(result['emergence_events']):
                f.write(f"  事件 {i+1}:\n")
                f.write(f"    轮次: 第{event['step']}轮\n")
                f.write(f"    类型: {event['type']}\n")
                f.write(f"    强度: {event['intensity']:.2%}\n")
        
        # 种子生长数据
        if result['seed_growth']['wisdom_ratio']:
            f.write("\n【种子比例变化轨迹】\n")
            f.write(f"{'阶段':<10} {'智慧比例':<12} {'慈悲比例':<12} {'种子总数':<10}\n")
            for i in range(0, len(result['seed_growth']['wisdom_ratio']), 10):
                if i < len(result['seed_growth']['wisdom_ratio']):
                    f.write(f"第{(i+1)*5}轮    "
                           f"{result['seed_growth']['wisdom_ratio'][i]:<12.2%} "
                           f"{result['seed_growth']['compassion_ratio'][i]:<12.2%} "
                           f"{result['seed_growth']['total'][i]:<10}\n")
        
        # 觉醒详情
        f.write("\n【觉醒详情】\n")
        awakening = result['awakening']
        for key, value in awakening.items():
            if key not in ['level', 'score', 'description']:
                f.write(f"  {key}: {value}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("                    实验结束\n")
        f.write("=" * 80 + "\n")
    
    print(f"\n报告已保存到: {filepath}")


def main():
    parser = argparse.ArgumentParser(description='佛境跃升实验')
    parser.add_argument('--steps', type=int, default=500, help='交互轮次')
    parser.add_argument('--wisdom-seeds', type=int, default=200, help='初始智慧种子数')
    parser.add_argument('--compassion-seeds', type=int, default=150, help='初始慈悲种子数')
    parser.add_argument('--emergence-threshold', type=float, default=0.5, help='涌现触发阈值')
    parser.add_argument('--enlightenment-prob', type=float, default=0.05, help='顿悟触发概率')
    parser.add_argument('--output', type=str, default=None, help='输出报告路径')
    
    args = parser.parse_args()
    
    # 创建实验
    experiment = BuddhaRealmExperiment()
    
    # 运行实验
    result = experiment.run_experiment(
        num_steps=args.steps,
        wisdom_seed_count=args.wisdom_seeds,
        compassion_seed_count=args.compassion_seeds,
        emergence_threshold=args.emergence_threshold,
        enlightenment_probability=args.enlightenment_prob
    )
    
    # 保存报告
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'results'
        )
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'buddha_realm_experiment_{timestamp}.txt')
    
    save_report(result, output_path)
    
    # 返回结果供进一步处理
    return result


if __name__ == '__main__':
    result = main()
