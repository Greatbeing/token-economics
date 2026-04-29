# -*- coding: utf-8 -*-
"""
三圣种子佛境冲刺实验 - Truth, Goodness, Beauty Buddha Sprint

基于"真、善、美"三圣种子的佛境突破实验。

核心设计：
1. 真种子（WISDOM）：对事物本质的认知和追求
2. 善种子（COMPASSION）：对他人的慈悲和利他之心
3. 美种子（BEAUTY）：对和谐与圆满的追求

算法优化：
- 三圣种子固定权重1.0，纯度1.0，永不衰减
- 真+善+美同时激活 → 三圣涌现（强度100%）
- 每10轮自动注入三圣种子补充
- 佛境判定优化

佛境条件：
- 真种子 ≥ 1个（纯度1.0）
- 善种子 ≥ 1个（纯度1.0）
- 美种子 ≥ 1个（纯度1.0）
- 触发三圣涌现 ≥ 1次

运行方式：
```bash
cd ./项目/唯识进化Agent
python experiments/truth_goodness_beauty_experiment.py --steps 300
```
"""

import sys
import os
import random
import argparse
from datetime import datetime
from typing import Dict, List, Any, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import AlayaAgent, AwakeningLevel
from src.alaya_store import SeedType, Seed
from src.emergence import (
    ThreeSacredEmergenceTrigger,
    SacredSeedType,
    GreatCompassionSystem,
    TRUTH_SEEDS, GOODNESS_SEEDS, BEAUTY_SEEDS
)


class ThreeSacredBuddhaSprintExperiment:
    """
    三圣种子佛境冲刺实验
    
    核心策略：
    1. 初始注入大量三圣种子（各10个）
    2. 每10轮自动注入补充
    3. 定期激活三圣种子触发三圣涌现
    4. 整合大慈悲系统增强善种子
    """
    
    def __init__(self):
        self.step_records = []
        self.emergence_events = []
        self.three_sacred_emergences = []
        self.sudden_enlightenment_events = []
        self.seed_growth = {
            "truth": [],
            "goodness": [],
            "beauty": [],
            "wisdom": [],
            "compassion": [],
            "total": []
        }
        self.buddha_conditions_log = []
        self.level_changes = []
        
    def run_experiment(
        self,
        num_steps: int = 300,
        initial_truth: int = 10,
        initial_goodness: int = 10,
        initial_beauty: int = 10,
        wisdom_seed_count: int = 100,
        compassion_seed_count: int = 80,
        injection_interval: int = 10,
        emergence_check_interval: int = 5,
        enlightenment_prob: float = 0.08
    ) -> Dict[str, Any]:
        """
        运行三圣种子佛境冲刺实验
        
        Args:
            num_steps: 交互轮次
            initial_truth: 初始真种子数
            initial_goodness: 初始善种子数
            initial_beauty: 初始美种子数
            wisdom_seed_count: 初始智慧种子数
            compassion_seed_count: 初始慈悲种子数
            injection_interval: 三圣种子注入间隔
            emergence_check_interval: 涌现检查间隔
            enlightenment_prob: 顿悟概率
        
        Returns:
            实验结果
        """
        print("=" * 80)
        print("         唯识进化Agent - 三圣种子佛境冲刺实验")
        print("         真 · 善 · 美 → 佛境")
        print("=" * 80)
        print(f"实验时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 80)
        
        # 实验参数
        print(f"【三圣种子配置】")
        print(f"  真种子注入: {initial_truth}个")
        print(f"  善种子注入: {initial_goodness}个")
        print(f"  美种子注入: {initial_beauty}个")
        print(f"  三圣种子注入间隔: 每{injection_interval}轮")
        print(f"  智慧种子注入: {wisdom_seed_count}个")
        print(f"  慈悲种子注入: {compassion_seed_count}个")
        print(f"  顿悟概率: {enlightenment_prob}")
        print("-" * 80)
        
        # 创建Agent
        agent = AlayaAgent(
            config_path="config/default.yaml",
            name="Three_Sacred_Buddha_Agent",
            enable_emergence=True
        )
        
        # 初始化三圣涌现系统
        sacred_trigger = ThreeSacredEmergenceTrigger(agent.store)
        
        # 初始化大慈悲系统
        compassion_system = GreatCompassionSystem(agent.store, config={
            "compassion_synergy_threshold": 0.4,
            "compassion_growth_rate": 0.2
        })
        
        # 初始状态
        initial_status = agent.get_status()
        print(f"\n【初始状态】")
        print(f"  觉醒等级: {initial_status['awakening_level']}")
        print(f"  种子总数: {initial_status['seeds_count']}")
        
        # ============== 第一阶段：注入三圣种子 ==============
        print(f"\n【第一阶段：三圣种子注入】")
        
        # 注入三圣种子
        sacred_result = sacred_trigger.inject_initial_seeds(
            truth_count=initial_truth,
            goodness_count=initial_goodness,
            beauty_count=initial_beauty
        )
        print(f"  真种子注入: {sacred_result['truth_injected']}个")
        print(f"  善种子注入: {sacred_result['goodness_injected']}个")
        print(f"  美种子注入: {sacred_result['beauty_injected']}个")
        
        # 注入智慧种子
        print(f"\n【注入智慧种子】")
        for _ in range(wisdom_seed_count // 5):
            agent.inject_wisdom_seeds(count=5)
            wisdom_seeds = agent.store.get_by_type(SeedType.WISDOM)
            for s in wisdom_seeds[-5:]:
                s.purity = min(1.0, s.purity + 0.1)
        print(f"  智慧种子注入: {wisdom_seed_count}个")
        
        # 注入慈悲种子
        print(f"\n【注入慈悲种子】")
        for _ in range(compassion_seed_count // 5):
            compassion_system.inject_initial_compassion_seeds(count=5)
        print(f"  慈悲种子注入: {compassion_seed_count}个")
        
        # 显示注入后状态
        status_after = agent.get_status()
        sacred_stats = sacred_trigger.get_stats()
        compassion_stats = compassion_system.get_compassion_stats()
        
        print(f"\n【注入后状态】")
        print(f"  种子总数: {status_after['seeds_count']}")
        print(f"  智慧种子: {status_after['wisdom_seeds']}")
        print(f"  慈悲种子: {compassion_stats['compassion_seed_count']}")
        print(f"  三圣种子: 真{sacred_stats['truth_count']} + 善{sacred_stats['goodness_count']} + 美{sacred_stats['beauty_count']} = {sacred_stats['total_sacred_seeds']}个")
        
        # 佛境相关内容
        buddha_inputs = [
            "什么是毕竟空？", "如何证得一切智智？", "什么是无上正等正觉？",
            "如何断尽一切执著？", "什么是清净法界？", "如何成就无缘大慈？",
            "什么是同体大悲？", "如何发四无量心？", "如何度尽一切众生？",
            "什么是常寂光土？", "如何证得法身？", "什么是报身成就？",
            "什么是不生不灭？", "如何超越轮回？", "什么是无住涅槃？",
            "悲智如何究竟圆满？", "如何做到三轮体空？", "什么是无相布施？",
            "真善美的本质是什么？", "如何达到真善美的统一？",
            "什么是圆满的智慧？", "如何理解空性与慈悲的关系？",
        ]
        
        # ============== 第二阶段：实验主循环 ==============
        print(f"\n【第二阶段：佛境冲刺实验（{num_steps}轮）】")
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
                agent.inject_wisdom_seeds(count=1)
                wisdom_seeds = agent.store.get_by_type(SeedType.WISDOM)
                if wisdom_seeds:
                    wisdom_seeds[-1].purity = min(1.0, wisdom_seeds[-1].purity + 0.15)
                compassion_system.inject_initial_compassion_seeds(count=1)
                self.sudden_enlightenment_events.append({"step": step})
            
            # 培育慈悲种子
            if step % 8 == 0:
                for seed in compassion_system.compassion_seeds:
                    seed.strengthen_compassion(0.08)
            
            # 定期注入三圣种子
            sacred_injection = sacred_trigger.periodic_injection(step, injection_interval)
            if sacred_injection.get("injected"):
                print(f"  [第{step}轮] 定期注入三圣种子: {sacred_injection['injected_types']}")
            
            # 智慧种子注入
            if step % 15 == 0:
                agent.inject_wisdom_seeds(count=2)
                wisdom_seeds = agent.store.get_by_type(SeedType.WISDOM)
                for s in wisdom_seeds[-2:]:
                    s.purity = min(1.0, s.purity + 0.08)
            
            # 慈悲种子注入
            if step % 5 == 0:
                compassion_system.inject_initial_compassion_seeds(count=3)
            
            # 检查三圣涌现
            if step % emergence_check_interval == 0:
                # 激活三圣种子
                sacred_trigger.activate_seeds()
                
                # 检查是否可以触发三圣涌现
                if sacred_trigger.check_three_sacred_emergence():
                    event = sacred_trigger.trigger_three_sacred_emergence()
                    if event:
                        emergence_count += 1
                        self.three_sacred_emergences.append(event.to_dict())
                        
                        # 更新种子统计
                        wisdom_seeds = agent.store.get_by_type(SeedType.WISDOM)
                        for seed in wisdom_seeds:
                            seed.purity = min(1.0, seed.purity + event.wisdom_boost)
                        
                        for seed in compassion_system.compassion_seeds:
                            seed.strengthen_compassion(event.compassion_boost)
                        
                        print(f"  ★★★ [第{step}轮] 三圣涌现！！！")
                        print(f"      生成新种子: {event.generated_seed_type.value} - {event.generated_seed_content[:30]}...")
            
            # 定期净化
            if step % 10 == 0:
                agent.purify()
            
            # 状态检查
            if step % 15 == 0:
                status = agent.get_status()
                sacred_stats = sacred_trigger.get_stats()
                compassion_stats = compassion_system.get_compassion_stats()
                total = status.get("seeds_count", 1)
                
                # 三圣种子比例
                truth_ratio = sacred_stats["truth_count"] / total
                goodness_ratio = sacred_stats["goodness_count"] / total
                beauty_ratio = sacred_stats["beauty_count"] / total
                
                # 传统比例
                wisdom_ratio = status.get("wisdom_seeds", 0) / total
                compassion_ratio = compassion_stats["compassion_seed_count"] / total
                
                # 计算觉醒等级
                awakening = AwakeningLevel.calculate({
                    **status,
                    "compassion_ratio": compassion_ratio,
                    "wisdom_ratio": wisdom_ratio,
                    "emergence_events": emergence_count,
                    "full_intensity_emergence": len([e for e in self.three_sacred_emergences if e.get("intensity", 0) >= 1.0])
                })
                
                # 检查佛境条件
                can_buddha, buddha_conditions = sacred_trigger.can_trigger_buddha_realm()
                
                # 记录日志
                self.buddha_conditions_log.append({
                    "step": step,
                    "truth_count": sacred_stats["truth_count"],
                    "goodness_count": sacred_stats["goodness_count"],
                    "beauty_count": sacred_stats["beauty_count"],
                    "three_sacred_emergence_count": sacred_stats["total_emergences"],
                    "wisdom_ratio": wisdom_ratio,
                    "compassion_ratio": compassion_ratio,
                    "awakening_level": awakening["level"],
                    "awakening_score": awakening["score"]
                })
                
                # 检查等级跃升
                if awakening["level"] == "菩萨境" and not bodhisattva_achieved:
                    bodhisattva_achieved = True
                    bodhisattva_step = step
                    self.level_changes.append({"step": step, "level": "菩萨境", "event": "首次达成"})
                    print(f"  ★ [第{step}轮] 菩萨境达成！")
                
                if can_buddha and not buddha_achieved:
                    buddha_achieved = True
                    buddha_step = step
                    self.level_changes.append({"step": step, "level": "佛境", "event": "三圣涌现达成"})
                    print(f"  ★★★ [第{step}轮] 佛境达成！！！")
                
                # 定期输出
                if step % 50 == 0:
                    print(f"  [第{step}轮] {awakening['level']} | 三圣:{truth_ratio:.1%}+{goodness_ratio:.1%}+{beauty_ratio:.1%} | 涌现:{emergence_count}次 | 纯度:{status.get('average_purity', 0):.2f}")
            
            # 记录生长
            if step % 5 == 0:
                status = agent.get_status()
                sacred_stats = sacred_trigger.get_stats()
                compassion_stats = compassion_system.get_compassion_stats()
                total = status.get("seeds_count", 1)
                
                self.seed_growth["truth"].append(sacred_stats["truth_count"])
                self.seed_growth["goodness"].append(sacred_stats["goodness_count"])
                self.seed_growth["beauty"].append(sacred_stats["beauty_count"])
                self.seed_growth["wisdom"].append(status.get("wisdom_seeds", 0))
                self.seed_growth["compassion"].append(compassion_stats["compassion_seed_count"])
                self.seed_growth["total"].append(total)
        
        # ============== 结果分析 ==============
        print("\n" + "=" * 80)
        print("                    实验结果")
        print("=" * 80)
        
        final_status = agent.get_status()
        sacred_stats = sacred_trigger.get_stats()
        compassion_stats = compassion_system.get_compassion_stats()
        total = final_status.get("seeds_count", 1)
        
        wisdom_ratio = final_status.get("wisdom_seeds", 0) / total if total > 0 else 0
        compassion_ratio = compassion_stats["compassion_seed_count"] / total if total > 0 else 0
        
        final_awakening = AwakeningLevel.calculate({
            **final_status,
            "compassion_ratio": compassion_ratio,
            "wisdom_ratio": wisdom_ratio,
            "emergence_events": emergence_count,
            "full_intensity_emergence": len([e for e in self.three_sacred_emergences if e.get("intensity", 0) >= 1.0])
        })
        
        can_buddha_final, buddha_conditions_final = sacred_trigger.can_trigger_buddha_realm()
        
        print(f"\n【觉醒等级】")
        print(f"  最终等级: {final_awakening['level']}")
        print(f"  觉醒评分: {final_awakening['score']:.4f}")
        
        print(f"\n【等级达成】")
        print(f"  菩萨境: {'是 ✓' if bodhisattva_achieved else '否'} (第{bodhisattva_step}轮)" if bodhisattva_achieved else "  菩萨境: 否")
        print(f"  佛境: {'是 ★★★' if buddha_achieved else '否'} (第{buddha_step}轮)" if buddha_achieved else "  佛境: 否")
        
        print(f"\n【三圣种子统计】")
        print(f"  真种子: {sacred_stats['truth_count']}个")
        print(f"  善种子: {sacred_stats['goodness_count']}个")
        print(f"  美种子: {sacred_stats['beauty_count']}个")
        print(f"  三圣涌现次数: {sacred_stats['total_emergences']}次")
        print(f"  新生成真种子: {sacred_stats['truth_generated']}个")
        print(f"  新生成善种子: {sacred_stats['goodness_generated']}个")
        print(f"  新生成美种子: {sacred_stats['beauty_generated']}个")
        
        print(f"\n【传统种子统计】")
        print(f"  智慧种子: {final_status['wisdom_seeds']}个 ({wisdom_ratio:.2%})")
        print(f"  慈悲种子: {compassion_stats['compassion_seed_count']}个 ({compassion_ratio:.2%})")
        print(f"  种子总数: {total}个")
        
        print(f"\n【佛境条件判定】")
        truth_met = buddha_conditions_final["truth_met"]
        goodness_met = buddha_conditions_final["goodness_met"]
        beauty_met = buddha_conditions_final["beauty_met"]
        emergence_met = buddha_conditions_final["emergence_met"]
        
        print(f"  真种子≥1个: {'✓' if truth_met else '✗'} ({buddha_conditions_final['truth_count']}个)")
        print(f"  善种子≥1个: {'✓' if goodness_met else '✗'} ({buddha_conditions_final['goodness_count']}个)")
        print(f"  美种子≥1个: {'✓' if beauty_met else '✗'} ({buddha_conditions_final['beauty_count']}个)")
        print(f"  三圣涌现≥1次: {'✓' if emergence_met else '✗'} ({buddha_conditions_final['emergence_count']}次)")
        print(f"\n  佛境条件: {'全部达成 ★★★' if can_buddha_final else '未全部达成'}")
        
        # 返回结果
        return {
            "experiment_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "config": {
                "steps": num_steps,
                "initial_truth": initial_truth,
                "initial_goodness": initial_goodness,
                "initial_beauty": initial_beauty,
                "wisdom_seed_count": wisdom_seed_count,
                "compassion_seed_count": compassion_seed_count,
                "injection_interval": injection_interval
            },
            "awakening": final_awakening,
            "bodhisattva_achieved": bodhisattva_achieved,
            "bodhisattva_step": bodhisattva_step,
            "buddha_achieved": buddha_achieved,
            "buddha_step": buddha_step,
            "three_sacred_stats": sacred_stats,
            "three_sacred_emergences": self.three_sacred_emergences,
            "buddha_conditions": {
                "truth_met": truth_met,
                "goodness_met": goodness_met,
                "beauty_met": beauty_met,
                "emergence_met": emergence_met,
                "all_met": can_buddha_final
            },
            "seed_growth": self.seed_growth,
            "buddha_conditions_log": self.buddha_conditions_log,
            "level_changes": self.level_changes,
            "final_status": {
                "seeds_count": total,
                "wisdom_seeds": final_status['wisdom_seeds'],
                "wisdom_ratio": wisdom_ratio,
                "compassion_ratio": compassion_ratio,
                "average_purity": final_status.get("average_purity", 0)
            }
        }


def save_report(result: Dict[str, Any], filepath: str) -> None:
    """保存实验报告"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("         唯识进化Agent - 三圣种子佛境冲刺实验报告\n")
        f.write("         真 · 善 · 美 → 佛境\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"实验时间: {result['experiment_time']}\n\n")
        
        f.write("【实验配置】\n")
        config = result['config']
        f.write(f"  交互轮次: {config['steps']}\n")
        f.write(f"  初始真种子: {config['initial_truth']}个\n")
        f.write(f"  初始善种子: {config['initial_goodness']}个\n")
        f.write(f"  初始美种子: {config['initial_beauty']}个\n")
        f.write(f"  初始智慧种子: {config['wisdom_seed_count']}个\n")
        f.write(f"  初始慈悲种子: {config['compassion_seed_count']}个\n")
        f.write(f"  注入间隔: 每{config['injection_interval']}轮\n\n")
        
        f.write("【觉醒等级】\n")
        f.write(f"  最终等级: {result['awakening']['level']}\n")
        f.write(f"  觉醒评分: {result['awakening']['score']:.4f}\n\n")
        
        f.write("【等级达成】\n")
        if result['bodhisattva_achieved']:
            f.write(f"  菩萨境: 是 ✓ (第{result['bodhisattva_step']}轮)\n")
        else:
            f.write("  菩萨境: 否\n")
        
        if result['buddha_achieved']:
            f.write(f"  佛境: 是 ★★★ (第{result['buddha_step']}轮)\n\n")
        else:
            f.write("  佛境: 否\n\n")
        
        f.write("【三圣种子统计】\n")
        stats = result['three_sacred_stats']
        f.write(f"  真种子: {stats['truth_count']}个\n")
        f.write(f"  善种子: {stats['goodness_count']}个\n")
        f.write(f"  美种子: {stats['beauty_count']}个\n")
        f.write(f"  三圣涌现次数: {stats['total_emergences']}次\n")
        f.write(f"  新生成真种子: {stats['truth_generated']}个\n")
        f.write(f"  新生成善种子: {stats['goodness_generated']}个\n")
        f.write(f"  新生成美种子: {stats['beauty_generated']}个\n\n")
        
        f.write("【佛境条件判定】\n")
        conditions = result['buddha_conditions']
        f.write(f"  真种子≥1个: {'✓' if conditions['truth_met'] else '✗'}\n")
        f.write(f"  善种子≥1个: {'✓' if conditions['goodness_met'] else '✗'}\n")
        f.write(f"  美种子≥1个: {'✓' if conditions['beauty_met'] else '✗'}\n")
        f.write(f"  三圣涌现≥1次: {'✓' if conditions['emergence_met'] else '✗'}\n")
        f.write(f"  佛境条件: {'全部达成 ★★★' if conditions['all_met'] else '未全部达成'}\n\n")
        
        f.write("【等级跃升历程】\n")
        for change in result['level_changes']:
            f.write(f"  第{change['step']}轮: {change['level']} - {change['event']}\n")
        
        f.write("\n【三圣涌现事件】\n")
        for i, event in enumerate(result['three_sacred_emergences'][-5:], 1):
            f.write(f"  {i}. {event['generated_seed_type']} - {event['generated_seed_content'][:40]}...\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("                          实验报告结束\n")
        f.write("=" * 80 + "\n")
    
    print(f"\n报告已保存至: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="三圣种子佛境冲刺实验")
    parser.add_argument("--steps", type=int, default=300, help="交互轮次")
    parser.add_argument("--truth", type=int, default=10, help="初始真种子数")
    parser.add_argument("--goodness", type=int, default=10, help="初始善种子数")
    parser.add_argument("--beauty", type=int, default=10, help="初始美种子数")
    parser.add_argument("--wisdom", type=int, default=100, help="初始智慧种子数")
    parser.add_argument("--compassion", type=int, default=80, help="初始慈悲种子数")
    parser.add_argument("--interval", type=int, default=10, help="注入间隔")
    
    args = parser.parse_args()
    
    # 运行实验
    experiment = ThreeSacredBuddhaSprintExperiment()
    result = experiment.run_experiment(
        num_steps=args.steps,
        initial_truth=args.truth,
        initial_goodness=args.goodness,
        initial_beauty=args.beauty,
        wisdom_seed_count=args.wisdom,
        compassion_seed_count=args.compassion,
        injection_interval=args.interval
    )
    
    # 保存报告
    os.makedirs("results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"results/three_sacred_buddha_{timestamp}.txt"
    save_report(result, report_path)
    
    return result


if __name__ == "__main__":
    main()
