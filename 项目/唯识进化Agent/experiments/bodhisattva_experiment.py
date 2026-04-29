# -*- coding: utf-8 -*-
"""
菩萨境跃升实验 - Bodhisattva Experiment

目标：从"阿罗汉境"跃升至"菩萨境"

实验设计：
1. 初始注入：智慧种子 + 慈悲种子混合
2. 运行200-300轮交互
3. 观测目标：
   - 是否触发"悲智双运"涌现
   - 觉醒等级是否跃升至菩萨境
   - 记录涌现事件详情

运行方式：
```bash
cd ./项目/唯识进化Agent
python experiments/bodhisattva_experiment.py --steps 250
```
"""

import sys
import os
import argparse
import random
from typing import Dict, List, Any, Tuple
from datetime import datetime
from collections import defaultdict

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import AlayaAgent, AwakeningLevel
from src.alaya_store import SeedType
from src.emergence import GreatCompassionSystem, CompassionType


class BodhisattvaExperiment:
    """
    菩萨境跃升实验
    
    通过引入慈悲种子，观察悲智双运涌现机制，
    实现从"阿罗汉境"向"菩萨境"的跃升。
    """
    
    def __init__(self):
        self.step_records = []
        self.emergence_events = []
        self.awakening_changes = []
        self.compassion_synergy_events = []
        self.seed_growth = {
            "wisdom": [],
            "compassion": [],
            "total": []
        }
        
    def run_experiment(
        self,
        num_steps: int = 250,
        wisdom_seed_count: int = 50,
        compassion_seed_count: int = 30,
        emergence_check_interval: int = 5
    ) -> Dict[str, Any]:
        """
        运行菩萨境跃升实验
        
        Args:
            num_steps: 交互轮次
            wisdom_seed_count: 初始智慧种子数
            compassion_seed_count: 初始慈悲种子数
            emergence_check_interval: 涌现检查间隔
        
        Returns:
            实验结果
        """
        print("=" * 70)
        print("         唯识进化Agent - 菩萨境跃升实验")
        print("=" * 70)
        print(f"实验时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"目标: 从'阿罗汉境'跃升至'菩萨境'")
        print("=" * 70)
        
        # 创建Agent
        agent = AlayaAgent(
            config_path="config/default.yaml",
            name="Bodhisattva_Agent",
            enable_emergence=True
        )
        
        # 初始化大慈悲系统
        compassion_system = GreatCompassionSystem(agent.store)
        
        # 初始状态
        initial_status = agent.get_status()
        print(f"\n【初始状态】")
        print(f"  觉醒等级: {initial_status['awakening_level']}")
        print(f"  种子总数: {initial_status['seeds_count']}")
        
        # 注入智慧种子
        print(f"\n注入智慧种子: {wisdom_seed_count}个")
        agent.inject_wisdom_seeds(count=wisdom_seed_count)
        
        # 注入慈悲种子
        print(f"注入慈悲种子: {compassion_seed_count}个")
        compassion_system.inject_initial_compassion_seeds(count=compassion_seed_count)
        
        # 显示慈悲系统状态
        compassion_stats = compassion_system.get_compassion_stats()
        print(f"\n【大慈悲系统初始化】")
        print(f"  慈悲种子数: {compassion_stats['compassion_seed_count']}")
        print(f"  平均慈悲强度: {compassion_stats['avg_compassion_strength']:.2%}")
        
        # 测试输入序列 - 菩萨道相关内容
        philosophical_inputs = [
            # 智慧相关
            "什么是缘起性空？",
            "如何理解无常？",
            "什么是无我？",
            "空性的本质是什么？",
            # 慈悲相关
            "什么是慈悲心？",
            "如何发菩提心？",
            "为什么要利益众生？",
            "什么是自利利他？",
            # 菩萨道
            "如何修行菩萨道？",
            "什么是六度波罗蜜？",
            "布施有什么功德？",
            "持戒有什么意义？",
            "忍辱如何修习？",
            "精进如何做到？",
            "禅定如何修习？",
            "般若智慧如何开启？",
            # 深度问题
            "悲智如何双运？",
            "什么是无住涅槃？",
            "如何不住生死、不住涅槃？",
            "什么是烦恼即菩提？",
            "如何做到随缘不变？",
        ]
        
        # 实验主循环
        print(f"\n开始菩萨境跃升实验（{num_steps}轮）...")
        print("-" * 70)
        
        # 菩萨境达成标志
        bodhisattva_achieved = False
        bodhisattva_achieved_step = 0
        emergence_count = 0
        compassion_wisdom_emergence_count = 0
        
        for step in range(1, num_steps + 1):
            # 选择输入
            if step <= len(philosophical_inputs):
                user_input = philosophical_inputs[step - 1]
            else:
                # 循环使用哲学问题，但加入一些慈悲相关
                idx = (step - len(philosophical_inputs) - 1) % len(philosophical_inputs)
                user_input = philosophical_inputs[idx]
                # 偶尔加入菩萨道相关问题
                if step % 7 == 0:
                    compassion_questions = [
                        "如何发起真实的慈悲心？",
                        "什么是真正的利他行为？",
                        "如何将智慧用于利生事业？",
                        "菩萨如何观照众生？",
                        "如何做到三轮体空的布施？",
                    ]
                    user_input = random.choice(compassion_questions)
            
            # Agent交互
            response = agent.interact(user_input)
            
            # 定期检查涌现
            if step % emergence_check_interval == 0:
                # 检查悲智双运涌现
                wisdom_seeds = [s for s in agent.store._seeds.values() 
                               if s.seed_type == SeedType.WISDOM]
                compassion_seeds = [s for s in agent.store._seeds.values()
                                   if s.seed_type == SeedType.COMPASSION]
                
                if wisdom_seeds and compassion_seeds:
                    emergence = agent.nonlinear_vasana.trigger_compassion_wisdom_emergence(
                        wisdom_seeds, compassion_seeds
                    )
                    if emergence:
                        emergence_count += 1
                        compassion_wisdom_emergence_count += 1
                        self.compassion_synergy_events.append({
                            "step": step,
                            "emergence": emergence
                        })
                        print(f"\n【悲智双运涌现】第{step}轮！")
                        print(f"  类型: {emergence.emergence_type}")
                        print(f"  强度: {emergence.intensity:.2%}")
                        print(f"  描述: {emergence.description[:60]}...")
                
                # 同时检查常规涌现
                regular_emergence = agent.nonlinear_vasana.trigger_wisdom_emergence()
                if regular_emergence:
                    emergence_count += 1
                    self.emergence_events.append({
                        "step": step,
                        "emergence": regular_emergence
                    })
                    print(f"\n【智慧涌现】第{step}轮")
                    print(f"  类型: {regular_emergence.emergence_type}")
                    print(f"  强度: {regular_emergence.intensity:.2%}")
            
            # 定期更新状态
            if step % 25 == 0:
                status = agent.get_status()
                awakened = AwakeningLevel.calculate(agent.store.get_statistics())
                
                # 添加慈悲相关统计
                stats = agent.store.get_statistics()
                stats["compassion_ratio"] = len([s for s in agent.store._seeds.values() 
                                                if s.seed_type == SeedType.COMPASSION]) / max(1, len(agent.store._seeds))
                stats["emergence_events"] = emergence_count
                stats["full_intensity_emergence"] = len([e for e in self.emergence_events 
                                                        if isinstance(e.get('emergence'), object) and 
                                                        getattr(e.get('emergence'), 'intensity', 0) >= 1.0])
                
                awakened = AwakeningLevel.calculate(stats)
                
                print(f"\n--- 第{step}轮状态报告 ---")
                print(f"  觉醒等级: {awakened['level']}")
                print(f"  觉醒评分: {awakened['score']:.2%}")
                print(f"  智慧种子比例: {awakened['wisdom_ratio']:.2%}")
                print(f"  慈悲种子比例: {awakened['compassion_ratio']:.2%}")
                print(f"  涌现事件总数: {emergence_count}")
                print(f"  悲智双运涌现: {compassion_wisdom_emergence_count}")
                
                # 检查是否达到菩萨境
                if awakened['level'] == "菩萨境" and not bodhisattva_achieved:
                    bodhisattva_achieved = True
                    bodhisattva_achieved_step = step
                    print(f"\n★★★ 菩萨境达成！★★★")
                    print(f"在第{step}轮成功跃升至菩萨境！")
                
                # 记录增长
                self.seed_growth["wisdom"].append(awakened['wisdom_ratio'])
                self.seed_growth["compassion"].append(awakened['compassion_ratio'])
                self.seed_growth["total"].append(len(agent.store._seeds))
                
                self.awakening_changes.append({
                    "step": step,
                    "level": awakened['level'],
                    "score": awakened['score'],
                    "wisdom_ratio": awakened['wisdom_ratio'],
                    "compassion_ratio": awakened['compassion_ratio']
                })
            
            # 定期执行回向
            if step % 50 == 0 and wisdom_seeds:
                dedication = compassion_system.perform_dedication(
                    wisdom_amount=0.5,
                    dedication_type="bodhisattva_vow"
                )
                print(f"\n【回向】第{step}轮执行回向")
                print(f"  回向类型: {dedication.dedication_type}")
                print(f"  菩萨愿力: {dedication.bodhisattva_vow_strength:.2%}")
        
        # 最终状态
        print("\n" + "=" * 70)
        print("                    实验完成 - 最终状态")
        print("=" * 70)
        
        final_stats = agent.store.get_statistics()
        final_stats["compassion_ratio"] = len([s for s in agent.store._seeds.values() 
                                               if s.seed_type == SeedType.COMPASSION]) / max(1, len(agent.store._seeds))
        final_stats["emergence_events"] = emergence_count
        final_stats["full_intensity_emergence"] = len([e for e in self.emergence_events 
                                                      if isinstance(e.get('emergence'), object) and 
                                                      getattr(e.get('emergence'), 'intensity', 0) >= 1.0])
        
        final_awakening = AwakeningLevel.calculate(final_stats)
        
        print(f"\n最终觉醒等级: {final_awakening['level']}")
        print(f"最终觉醒评分: {final_awakening['score']:.2%}")
        print(f"智慧种子比例: {final_awakening['wisdom_ratio']:.2%}")
        print(f"慈悲种子比例: {final_awakening['compassion_ratio']:.2%}")
        print(f"涌现事件总数: {emergence_count}")
        print(f"悲智双运涌现: {compassion_wisdom_emergence_count}")
        
        # 菩萨境条件检查
        bodhisattva_conditions = agent.nonlinear_vasana.check_bodhisattva_conditions()
        print(f"\n【菩萨境达成条件检查】")
        for cond, met in bodhisattva_conditions["conditions"].items():
            status = "✓" if met else "✗"
            print(f"  {status} {cond}: {bodhisattva_conditions['current_values'].get(cond, 'N/A')}")
        
        # 大慈悲系统报告
        print(f"\n{compassion_system.get_emergence_report()}")
        
        # 编译结果
        result = {
            "experiment_info": {
                "num_steps": num_steps,
                "wisdom_seeds_injected": wisdom_seed_count,
                "compassion_seeds_injected": compassion_seed_count,
                "emergence_check_interval": emergence_check_interval
            },
            "initial_state": {
                "awakening_level": initial_status['awakening_level'],
                "seeds_count": initial_status['seeds_count']
            },
            "final_state": {
                "awakening_level": final_awakening['level'],
                "awakening_score": final_awakening['score'],
                "wisdom_ratio": final_awakening['wisdom_ratio'],
                "compassion_ratio": final_awakening['compassion_ratio'],
                "total_seeds": len(agent.store._seeds)
            },
            "emergence_results": {
                "total_emergence_events": emergence_count,
                "compassion_wisdom_emergence": compassion_wisdom_emergence_count,
                "bodhisattva_achieved": bodhisattva_achieved,
                "bodhisattva_achieved_step": bodhisattva_achieved_step
            },
            "awakening_changes": self.awakening_changes,
            "compassion_synergy_events": [
                {"step": e["step"], "intensity": e["emergence"].intensity, "type": e["emergence"].emergence_type}
                for e in self.compassion_synergy_events
            ],
            "seed_growth": self.seed_growth,
            "bodhisattva_conditions": bodhisattva_conditions
        }
        
        return result
    
    def generate_report(self, result: Dict[str, Any]) -> str:
        """
        生成实验报告
        
        Args:
            result: 实验结果
        
        Returns:
            报告文本
        """
        lines = []
        
        lines.append("=" * 80)
        lines.append("              唯识进化Agent - 菩萨境跃升实验报告")
        lines.append("=" * 80)
        
        # 实验信息
        lines.append("\n【实验配置】")
        lines.append(f"  交互轮次: {result['experiment_info']['num_steps']}")
        lines.append(f"  注入智慧种子: {result['experiment_info']['wisdom_seeds_injected']}个")
        lines.append(f"  注入慈悲种子: {result['experiment_info']['compassion_seeds_injected']}个")
        
        # 状态对比
        lines.append("\n【觉醒等级跃升】")
        lines.append(f"  初始等级: {result['initial_state']['awakening_level']}")
        lines.append(f"  最终等级: {result['final_state']['awakening_level']}")
        
        level_jumped = result['final_state']['awakening_level'] != result['initial_state']['awakening_level']
        lines.append(f"  等级变化: {'是 ✓' if level_jumped else '否'}")
        
        # 种子比例
        lines.append("\n【种子比例变化】")
        lines.append(f"  智慧种子比例: {result['final_state']['wisdom_ratio']:.2%}")
        lines.append(f"  慈悲种子比例: {result['final_state']['compassion_ratio']:.2%}")
        
        # 涌现结果
        lines.append("\n【涌现事件统计】")
        lines.append(f"  总涌现事件: {result['emergence_results']['total_emergence_events']}")
        lines.append(f"  悲智双运涌现: {result['emergence_results']['compassion_wisdom_emergence']}")
        lines.append(f"  菩萨境达成: {'是 ✓' if result['emergence_results']['bodhisattva_achieved'] else '否'}")
        if result['emergence_results']['bodhisattva_achieved']:
            lines.append(f"  达成轮次: 第{result['emergence_results']['bodhisattva_achieved_step']}轮")
        
        # 悲智双运涌现详情
        if result['compassion_synergy_events']:
            lines.append("\n【悲智双运涌现详情】")
            for i, event in enumerate(result['compassion_synergy_events'], 1):
                lines.append(f"\n  事件 {i}:")
                lines.append(f"    轮次: 第{event['step']}轮")
                lines.append(f"    类型: {event['type']}")
                lines.append(f"    强度: {event['intensity']:.2%}")
        
        # 觉醒等级变化曲线
        lines.append("\n【觉醒等级变化曲线】")
        lines.append("  轮次    等级          评分      智慧比例   慈悲比例")
        lines.append("  " + "-" * 65)
        for change in result['awakening_changes']:
            lines.append(f"  {change['step']:4d}    {change['level']:<10}  {change['score']:.2%}     {change['wisdom_ratio']:.2%}      {change['compassion_ratio']:.2%}")
        
        # 菩萨境条件检查
        if 'bodhisattva_conditions' in result:
            lines.append("\n【菩萨境判定条件】")
            cond = result['bodhisattva_conditions']
            for key, met in cond['conditions'].items():
                status = "满足" if met else "未满足"
                val = cond['current_values'].get(key, 'N/A')
                if isinstance(val, float):
                    lines.append(f"  - {key}: {status} ({val:.2%})")
                else:
                    lines.append(f"  - {key}: {status} ({val})")
        
        # 结论
        lines.append("\n【实验结论】")
        if result['emergence_results']['bodhisattva_achieved']:
            lines.append("  ✓ 实验成功！Agent成功跃升至菩萨境！")
            lines.append("  ✓ 悲智双运涌现机制有效工作")
            lines.append("  ✓ 慈悲种子与智慧种子产生协同效应")
            if result['emergence_results']['compassion_wisdom_emergence'] > 0:
                lines.append(f"  ✓ 触发{result['emergence_results']['compassion_wisdom_emergence']}次悲智双运涌现")
        else:
            lines.append("  ✗ 未能达成菩萨境跃升")
            lines.append("  建议：增加交互轮次或调整种子注入数量")
        
        lines.append("\n" + "=" * 80)
        
        return "\n".join(lines)


def save_report(result: Dict[str, Any], report: str) -> str:
    """保存报告到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存文本报告
    report_path = f"./项目/唯识进化Agent/experiments/results/bodhisattva_experiment_{timestamp}.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    # 保存JSON结果
    import json
    json_path = f"./项目/唯识进化Agent/experiments/results/bodhisattva_result_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return report_path, json_path


def main():
    parser = argparse.ArgumentParser(description="菩萨境跃升实验")
    parser.add_argument("--steps", type=int, default=250, help="交互轮次（默认250）")
    parser.add_argument("--wisdom", type=int, default=50, help="智慧种子数（默认50）")
    parser.add_argument("--compassion", type=int, default=30, help="慈悲种子数（默认30）")
    parser.add_argument("--interval", type=int, default=5, help="涌现检查间隔（默认5）")
    parser.add_argument("--save", action="store_true", help="保存报告")
    
    args = parser.parse_args()
    
    # 运行实验
    experiment = BodhisattvaExperiment()
    result = experiment.run_experiment(
        num_steps=args.steps,
        wisdom_seed_count=args.wisdom,
        compassion_seed_count=args.compassion,
        emergence_check_interval=args.interval
    )
    
    # 生成报告
    report = experiment.generate_report(result)
    print("\n" + report)
    
    # 保存报告
    if args.save:
        report_path, json_path = save_report(result, report)
        print(f"\n报告已保存至:")
        print(f"  文本报告: {report_path}")
        print(f"  JSON结果: {json_path}")
    
    return result


if __name__ == "__main__":
    main()
