# -*- coding: utf-8 -*-
"""
佛境冲刺实验 - Buddha Realm Sprint Experiment

针对佛境跃升的专项强化实验

问题分析（基于上次实验）：
- 智慧种子比例: 18.13% (需要 ≥30%) - 需要提升约70%
- 慈悲种子比例: 3.19% (需要 ≥25%) - 需要大幅提升约7倍
- 满强度涌现: 27次 ✓ - 已达标

关键发现：
- 慈悲种子比例持续下降（从21.84%降到3.43%）
- 智慧种子增长跟不上总种子增长
- 需要专门强化慈悲种子注入

实验策略：
1. 大幅增加慈悲种子注入（每5轮注入一次）
2. 减少普通种子生成，专注高质量种子
3. 增加顿悟触发概率
4. 降低涌现阈值
"""

import sys
import os
import random
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import AlayaAgent, AwakeningLevel
from src.alaya_store import SeedType, Seed
from src.emergence.great_compassion import GreatCompassionSystem, CompassionType


class BuddhaRealmSprintExperiment:
    """佛境冲刺实验"""
    
    def __init__(self):
        self.emergence_events = []
        self.full_intensity_emergences = []
        self.sudden_enlightenment_events = []
        self.seed_growth = {"wisdom": [], "compassion": [], "total": [], "wisdom_ratio": [], "compassion_ratio": []}
        self.buddha_conditions_log = []
        self.great_compassion_events = []
        
    def run_experiment(
        self,
        num_steps: int = 300,
        initial_wisdom: int = 300,
        initial_compassion: int = 300,
        compassion_injection_interval: int = 5,
        wisdom_injection_interval: int = 15,
        enlightenment_prob: float = 0.08
    ) -> dict:
        """运行佛境冲刺实验"""
        print("=" * 80)
        print("         唯识进化Agent - 佛境冲刺实验")
        print("=" * 80)
        print(f"【激进参数】")
        print(f"  慈悲种子注入间隔: 每{compassion_injection_interval}轮")
        print(f"  智慧种子注入间隔: 每{wisdom_injection_interval}轮")
        print(f"  顿悟概率: {enlightenment_prob}")
        print("-" * 80)
        
        # 创建Agent
        agent = AlayaAgent(config_path="config/default.yaml", name="Buddha_Sprint", enable_emergence=True)
        
        # 慈悲系统
        compassion_system = GreatCompassionSystem(agent.store, config={
            "compassion_synergy_threshold": 0.4,  # 降低阈值
            "compassion_growth_rate": 0.25
        })
        
        # 初始状态
        print(f"\n【初始状态】")
        print(f"  种子总数: {agent.get_status()['seeds_count']}")
        
        # 大量注入种子
        print(f"\n【种子注入】")
        print(f"  智慧种子: {initial_wisdom}个")
        for _ in range(initial_wisdom // 5):
            agent.inject_wisdom_seeds(count=5)
            # 提升纯度
            wisdom_seeds = agent.store.get_by_type(SeedType.WISDOM)
            for s in wisdom_seeds[-5:]:
                s.purity = min(1.0, s.purity + 0.15)
        
        print(f"  慈悲种子: {initial_compassion}个")
        for _ in range(initial_compassion // 5):
            compassion_system.inject_initial_compassion_seeds(count=5)
        
        # 显示注入后状态
        status = agent.get_status()
        compassion_stats = compassion_system.get_compassion_stats()
        print(f"\n【注入后状态】")
        print(f"  总种子: {status['seeds_count']}")
        print(f"  智慧种子: {status['wisdom_seeds']}")
        print(f"  慈悲种子: {compassion_stats['compassion_seed_count']}")
        
        # 佛境相关内容
        buddha_inputs = [
            "什么是毕竟空？", "如何证得一切智智？", "什么是无上正等正觉？",
            "如何断尽一切执著？", "什么是清净法界？", "如何成就无缘大慈？",
            "什么是同体大悲？", "如何发四无量心？", "如何度尽一切众生？",
            "什么是常寂光土？", "如何证得法身？", "什么是报身成就？",
            "什么是不生不灭？", "如何超越轮回？", "什么是无住涅槃？",
            "悲智如何究竟圆满？", "如何做到三轮体空？", "什么是无相布施？",
        ]
        
        print(f"\n【实验进行中】（{num_steps}轮）...")
        print("-" * 80)
        
        bodhisattva_achieved = False
        buddha_achieved = False
        bodhisattva_step = 0
        buddha_step = 0
        emergence_count = 0
        
        for step in range(1, num_steps + 1):
            # Agent交互
            agent.interact(random.choice(buddha_inputs))
            
            # 顿悟机制
            if random.random() < enlightenment_prob:
                # 顿悟：生成高纯度种子
                agent.inject_wisdom_seeds(count=1)
                wisdom_seeds = agent.store.get_by_type(SeedType.WISDOM)
                if wisdom_seeds:
                    wisdom_seeds[-1].purity = min(1.0, wisdom_seeds[-1].purity + 0.2)
                compassion_system.inject_initial_compassion_seeds(count=1)
                self.sudden_enlightenment_events.append({"step": step})
            
            # 培育慈悲种子
            for seed in compassion_system.compassion_seeds:
                if step % 8 == 0:
                    seed.strengthen_compassion(0.08)
            
            # 慈悲种子注入（关键：高频注入）
            if step % compassion_injection_interval == 0:
                compassion_system.inject_initial_compassion_seeds(count=3)
            
            # 智慧种子注入
            if step % wisdom_injection_interval == 0:
                agent.inject_wisdom_seeds(count=2)
                wisdom_seeds = agent.store.get_by_type(SeedType.WISDOM)
                if wisdom_seeds:
                    for s in wisdom_seeds[-2:]:
                        s.purity = min(1.0, s.purity + 0.1)
            
            # 检查涌现
            if step % 3 == 0:
                wisdom_seeds = agent.store.get_by_type(SeedType.WISDOM)
                context_seeds = list(agent.store._seeds.values())[:30]
                
                result = compassion_system.check_compassion_synergy(wisdom_seeds, context_seeds)
                if result:
                    wisdom_s, compassion_s, strength = result
                    event = compassion_system.trigger_great_compassion_emergence(wisdom_s, compassion_s, strength)
                    emergence_count += 1
                    self.great_compassion_events.append(event)
                    
                    if event.intensity >= 1.0:
                        self.full_intensity_emergences.append({"step": step, "intensity": event.intensity})
                    
                    self.emergence_events.append({
                        "step": step, "type": f"大悲涌现-{event.compassion_type.value}", "intensity": event.intensity
                    })
            
            # 定期净化
            if step % 10 == 0:
                agent.purify()
            
            # 每15轮检查状态
            if step % 15 == 0:
                status = agent.get_status()
                compassion_stats = compassion_system.get_compassion_stats()
                total = status.get("seeds_count", 1)
                wisdom_ratio = status.get("wisdom_seeds", 0) / total
                compassion_ratio = compassion_stats["compassion_seed_count"] / total
                
                awakening = AwakeningLevel.calculate({
                    **status,
                    "compassion_ratio": compassion_ratio,
                    "wisdom_ratio": wisdom_ratio,
                    "emergence_events": emergence_count,
                    "full_intensity_emergence": len(self.full_intensity_emergences)
                })
                
                self.buddha_conditions_log.append({
                    "step": step, "wisdom_ratio": wisdom_ratio, "compassion_ratio": compassion_ratio,
                    "full_intensity_emergence": len(self.full_intensity_emergences),
                    "wisdom_met": wisdom_ratio >= 0.30,
                    "compassion_met": compassion_ratio >= 0.25,
                    "emergence_met": len(self.full_intensity_emergences) >= 3
                })
                
                # 检查等级
                if awakening["level"] == "菩萨境" and not bodhisattva_achieved:
                    bodhisattva_achieved = True
                    bodhisattva_step = step
                    print(f"  [第{step}轮] ★ 菩萨境达成！")
                
                if awakening.get("bodhisattva_details", {}).get("buddha_conditions_met") and not buddha_achieved:
                    buddha_achieved = True
                    buddha_step = step
                    print(f"  [第{step}轮] ★★ 佛境达成！！！")
                
                if step % 50 == 0:
                    print(f"  [第{step}轮] {awakening['level']} | 智慧:{wisdom_ratio:.1%} | 慈悲:{compassion_ratio:.1%} | 满强度:{len(self.full_intensity_emergences)}次")
            
            # 记录生长
            if step % 5 == 0:
                status = agent.get_status()
                compassion_stats = compassion_system.get_compassion_stats()
                total = status.get("seeds_count", 1)
                self.seed_growth["wisdom"].append(status.get("wisdom_seeds", 0))
                self.seed_growth["compassion"].append(compassion_stats["compassion_seed_count"])
                self.seed_growth["total"].append(total)
                self.seed_growth["wisdom_ratio"].append(status.get("wisdom_seeds", 0) / total if total > 0 else 0)
                self.seed_growth["compassion_ratio"].append(compassion_stats["compassion_seed_count"] / total if total > 0 else 0)
        
        # 结果分析
        print("\n" + "=" * 80)
        print("                    实验结果")
        print("=" * 80)
        
        final_status = agent.get_status()
        final_compassion = compassion_system.get_compassion_stats()
        total = final_status.get("seeds_count", 1)
        wisdom_ratio = final_status.get("wisdom_seeds", 0) / total if total > 0 else 0
        compassion_ratio = final_compassion["compassion_seed_count"] / total if total > 0 else 0
        
        final_awakening = AwakeningLevel.calculate({
            **final_status,
            "compassion_ratio": compassion_ratio,
            "wisdom_ratio": wisdom_ratio,
            "emergence_events": emergence_count,
            "full_intensity_emergence": len(self.full_intensity_emergences)
        })
        
        print(f"\n【觉醒等级】")
        print(f"  最终等级: {final_awakening['level']}")
        print(f"  觉醒评分: {final_awakening['score']:.4f}")
        
        print(f"\n【等级达成】")
        print(f"  菩萨境: {'是 ✓' if bodhisattva_achieved else '否'} (第{bodhisattva_step}轮)" if bodhisattva_achieved else "  菩萨境: 否")
        print(f"  佛境: {'是 ★★★' if buddha_achieved else '否'} (第{buddha_step}轮)" if buddha_achieved else "  佛境: 否")
        
        print(f"\n【种子比例】")
        wisdom_met = wisdom_ratio >= 0.30
        compassion_met = compassion_ratio >= 0.25
        emergence_met = len(self.full_intensity_emergences) >= 3
        
        print(f"  智慧: {wisdom_ratio:.2%} (目标≥30%) {'✓' if wisdom_met else '✗'}")
        print(f"  慈悲: {compassion_ratio:.2%} (目标≥25%) {'✓' if compassion_met else '✗'}")
        print(f"  满强度涌现: {len(self.full_intensity_emergences)}次 (目标≥3) {'✓' if emergence_met else '✗'}")
        print(f"\n  佛境条件: {'全部达成 ★★★' if (wisdom_met and compassion_met and emergence_met) else '未全部达成'}")
        
        return {
            "experiment_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "config": {"steps": num_steps, "initial_wisdom": initial_wisdom, "initial_compassion": initial_compassion},
            "initial_wisdom_ratio": 0, "final_wisdom_ratio": wisdom_ratio,
            "final_compassion_ratio": compassion_ratio,
            "awakening": final_awakening,
            "bodhisattva_achieved": bodhisattva_achieved, "bodhisattva_step": bodhisattva_step,
            "buddha_achieved": buddha_achieved, "buddha_step": buddha_step,
            "emergence_count": emergence_count,
            "full_intensity_count": len(self.full_intensity_emergences),
            "wisdom_met": wisdom_met, "compassion_met": compassion_met, "emergence_met": emergence_met,
            "seed_growth": self.seed_growth,
            "buddha_conditions_log": self.buddha_conditions_log,
            "emergence_events": self.emergence_events[-15:]
        }


def save_sprint_report(result: dict, filepath: str):
    """保存冲刺实验报告"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("              唯识进化Agent - 佛境冲刺实验报告\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"实验时间: {result['experiment_time']}\n")
        f.write(f"实验配置: {result['config']}\n\n")
        
        f.write("【觉醒等级】\n")
        f.write(f"  最终等级: {result['awakening']['level']}\n")
        f.write(f"  觉醒评分: {result['awakening']['score']:.4f}\n\n")
        
        f.write("【等级达成】\n")
        f.write(f"  菩萨境: {'是' if result['bodhisattva_achieved'] else '否'} (第{result['bodhisattva_step']}轮)\n")
        f.write(f"  佛境: {'是 ★★★' if result['buddha_achieved'] else '否'} (第{result['buddha_step']}轮)\n\n")
        
        f.write("【佛境条件判定】\n")
        f.write(f"  智慧种子比例≥30%: {'✓' if result['wisdom_met'] else '✗'} ({result['final_wisdom_ratio']:.2%})\n")
        f.write(f"  慈悲种子比例≥25%: {'✓' if result['compassion_met'] else '✗'} ({result['final_compassion_ratio']:.2%})\n")
        f.write(f"  满强度涌现≥3次: {'✓' if result['emergence_met'] else '✗'} ({result['full_intensity_count']}次)\n\n")
        
        all_met = result['wisdom_met'] and result['compassion_met'] and result['emergence_met']
        f.write(f"  佛境条件: {'全部达成 ★★★ 佛境突破成功！' if all_met else '未全部达成 - 需要继续努力'}\n\n")
        
        if result['buddha_conditions_log']:
            f.write("\n【进度追踪】\n")
            f.write(f"{'轮次':<8} {'智慧比例':<12} {'慈悲比例':<12} {'满强度':<8} 判定\n")
            for log in result['buddha_conditions_log']:
                status = "佛境" if (log['wisdom_met'] and log['compassion_met'] and log['emergence_met']) else \
                         "菩萨境" if (log['wisdom_met'] and log['compassion_met']) else \
                         "菩萨境?" if (log['wisdom_met'] and log['emergence_met']) else \
                         "进行中"
                f.write(f"{log['step']:<8} {log['wisdom_ratio']:<12.2%} {log['compassion_ratio']:<12.2%} "
                       f"{log['full_intensity_emergence']:<8} {status}\n")
        
        if result['emergence_events']:
            f.write("\n【涌现事件】\n")
            for e in result['emergence_events']:
                f.write(f"  第{e['step']}轮: {e['type']} 强度{e['intensity']:.0%}\n")
        
        f.write("\n" + "=" * 80 + "\n")
    
    print(f"\n报告已保存: {filepath}")


def main():
    experiment = BuddhaRealmSprintExperiment()
    result = experiment.run_experiment(
        num_steps=300,
        initial_wisdom=300,
        initial_compassion=300,
        compassion_injection_interval=5,
        wisdom_injection_interval=15,
        enlightenment_prob=0.08
    )
    
    # 保存报告
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = "./项目/唯识进化Agent/experiments/results"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"buddha_sprint_{timestamp}.txt")
    save_sprint_report(result, filepath)
    
    return result


if __name__ == '__main__':
    main()
