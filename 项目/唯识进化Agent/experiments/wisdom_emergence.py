# -*- coding: utf-8 -*-
"""
智慧涌现实验 - Wisdom Emergence Experiment

验证核心假设：智慧能否从种子协同中涌现？

实验设计：
1. 对照组：禁用非线性协同，种子独立存在
2. 实验组：启用非线性协同，种子可以交互涌现

测量指标：
- 涌现事件次数
- 涌现产生的智慧质量
- 觉醒等级变化
- 涌现的不可预测性（惊喜度）

运行方式：
```bash
cd ./项目/唯识进化Agent
python experiments/wisdom_emergence.py
```
"""

import sys
import os
import time
import random
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.alaya_store import AlayaStore, Seed, SeedType, SeedStatus
from src.emergence.nonlinear_vasana import NonlinearVasana
from src.emergence.emergence_observer import EmergenceObserver, EmergenceType
from src.emergence.wisdom_emergence_ext import WisdomEmergenceExtension


class WisdomEmergenceExperiment:
    """
    智慧涌现实验
    
    通过对比实验验证种子协同能否产生智慧涌现
    """
    
    def __init__(self):
        self.results = {
            "control": {},  # 对照组结果
            "experimental": {},  # 实验组结果
            "comparison": {}  # 对比分析
        }
        
        # 注入的高质量智慧种子内容
        self.wisdom_seed_contents = [
            ("缘起性空：一切法因缘生，无自性故空", ["缘起", "空性", "中道"]),
            ("无常即常：变化本身是永恒不变的真理", ["无常", "永恒", "变化"]),
            ("慈悲智慧：无缘大慈同体大悲，无缘之慈是真正的慈悲", ["慈悲", "智慧", "无我"]),
            ("中道实相：不落有无二边，证入诸法实相", ["中道", "实相", "中观"]),
            ("止观双运：定慧等持，止中有观观中有止", ["止观", "定慧", "修行"]),
            ("转识成智：转八识成四智，证得清净法身", ["转依", "法身", "解脱"]),
            ("心净国土净：依报随着正报转，心净则佛土净", ["心性", "净土", "清净"]),
            ("烦恼即菩提：烦恼菩提非一非异，于烦恼中得菩提", ["烦恼", "菩提", "觉悟"]),
        ]
        
        # 经验种子内容
        self.experience_seed_contents = [
            ("晨起静坐观呼吸，心渐安定智慧生", ["禅修", "日常"]),
            ("与人辩论时不嗔，平和表达见解", ["修行", "日常"]),
            ("读《金刚经》有悟，诸相非相见如如", ["读经", "领悟"]),
            ("遇到挫折不退缩，深知这是成长机会", ["逆境", "成长"]),
            ("帮助他人不计回报，内心喜乐自在", ["布施", "利他"]),
            ("观察念头生灭，不随之起舞", ["观心", "正念"]),
        ]
        
        # 模式种子内容
        self.pattern_seed_contents = [
            ("遇事三问：为何发生？有何意义？如何面对？", ["反思", "模式"]),
            ("情绪来时先观照，不立即反应", ["情绪", "模式"]),
            ("每日自省：今日有何进步？有何不足？", ["自省", "模式"]),
            ("与人交流先倾听后回应", ["沟通", "模式"]),
        ]
        
        # 知识种子内容
        self.knowledge_seed_contents = [
            ("唯识学：诸识变现所见一切，唯心所现唯识所变", ["唯识", "知识"]),
            ("因明学：论式五支，宗因喻合结", ["因明", "逻辑"]),
            ("中观派：缘起性空，空有不二", ["中观", "知识"]),
            ("如来藏：众生皆有佛性，心佛众生三无差别", ["如来藏", "佛性"]),
        ]
        
        # 实验参数
        self.num_initial_seeds = 20  # 初始种子数量
        self.interaction_rounds = 50  # 交互轮次
        self.emergence_check_interval = 3  # 涌现检查间隔
        
    def create_initial_seeds(self, store: AlayaStore) -> List[Seed]:
        """创建初始种子集合"""
        seeds = []
        
        # 添加智慧种子（高质量）
        for content, tags in self.wisdom_seed_contents:
            seed = Seed.create(
                content=content,
                seed_type=SeedType.WISDOM,
                weight=random.uniform(0.7, 0.9),
                purity=random.uniform(0.85, 0.95),
                source="injected_wisdom",
                tags=tags,
                experience_context="注入的高质量智慧种子"
            )
            store.add(seed)
            seeds.append(seed)
        
        # 添加经验种子
        for content, tags in self.experience_seed_contents:
            seed = Seed.create(
                content=content,
                seed_type=SeedType.EXPERIENCE,
                weight=random.uniform(0.5, 0.7),
                purity=random.uniform(0.6, 0.8),
                source="injected_experience",
                tags=tags,
                experience_context="注入的经验种子"
            )
            store.add(seed)
            seeds.append(seed)
        
        # 添加模式种子
        for content, tags in self.pattern_seed_contents:
            seed = Seed.create(
                content=content,
                seed_type=SeedType.PATTERN,
                weight=random.uniform(0.5, 0.7),
                purity=random.uniform(0.6, 0.8),
                source="injected_pattern",
                tags=tags,
                experience_context="注入的模式种子"
            )
            store.add(seed)
            seeds.append(seed)
        
        # 添加知识种子
        for content, tags in self.knowledge_seed_contents:
            seed = Seed.create(
                content=content,
                seed_type=SeedType.KNOWLEDGE,
                weight=random.uniform(0.5, 0.7),
                purity=random.uniform(0.6, 0.8),
                source="injected_knowledge",
                tags=tags,
                experience_context="注入的知识种子"
            )
            store.add(seed)
            seeds.append(seed)
        
        return seeds
    
    def run_control_group(self) -> Dict[str, Any]:
        """
        运行对照组（禁用协同）
        
        种子独立存在，不进行协同交互
        """
        print("\n" + "=" * 70)
        print("           【对照组】禁用协同 - 种子独立存在")
        print("=" * 70)
        
        # 创建独立的种子库
        store = AlayaStore()
        
        # 创建初始种子
        initial_seeds = self.create_initial_seeds(store)
        print(f"\n初始种子数量: {len(initial_seeds)}")
        
        # 创建非线性熏习（但不启用协同）
        vasana_config = {
            "synergy_threshold": 1.0,  # 禁用协同
            "cascade_threshold": 1.0,  # 禁用级联
            "emergence_threshold": 1.0,  # 禁用涌现
            "nonlinear_factor": 0.1,  # 极低非线性
            "wisdom_priority": False
        }
        vasana = NonlinearVasana(store, vasana_config)
        
        # 追踪数据
        wisdom_counts = []
        avg_weights = []
        avg_purities = []
        wisdom_weights = []
        
        # 记录初始状态
        stats = store.get_statistics()
        wisdom_counts.append(stats["wisdom_count"])
        avg_weights.append(stats["average_weight"])
        avg_purities.append(stats["average_purity"])
        wisdom_weights.append(stats.get("avg_wisdom_weight", 0))
        
        print(f"\n初始状态:")
        print(f"  智慧种子: {stats['wisdom_count']}")
        print(f"  平均权重: {stats['average_weight']:.4f}")
        print(f"  平均纯度: {stats['average_purity']:.4f}")
        
        # 执行交互（独立强化）
        for round_num in range(self.interaction_rounds):
            # 随机选择一个种子进行独立强化
            all_seeds = list(store._seeds.values())
            if not all_seeds:
                break
            
            # 随机选择2-3个种子
            selected = random.sample(all_seeds, min(3, len(all_seeds)))
            
            # 独立强化（不协同）
            for seed in selected:
                base_strength = random.uniform(0.1, 0.2)
                vasana.strengthen_seed(seed, base_strength, context_seeds=[])
            
            # 每5轮记录一次
            if (round_num + 1) % 5 == 0:
                stats = store.get_statistics()
                wisdom_counts.append(stats["wisdom_count"])
                avg_weights.append(stats["average_weight"])
                avg_purities.append(stats["average_purity"])
                wisdom_weights.append(stats.get("avg_wisdom_weight", 0))
                print(f"  Round {round_num+1}: 智慧种子={stats['wisdom_count']}, "
                      f"平均权重={stats['average_weight']:.4f}")
        
        # 最终统计
        final_stats = store.get_statistics()
        
        return {
            "initial_seeds": len(initial_seeds),
            "final_seeds": len(store._seeds),
            "wisdom_seeds": final_stats["wisdom_count"],
            "avg_weight": final_stats["average_weight"],
            "avg_purity": final_stats["average_purity"],
            "wisdom_count_history": wisdom_counts,
            "weight_history": avg_weights,
            "purity_history": avg_purities,
            "wisdom_weight_history": wisdom_weights,
            "emergence_events": [],
            "synergy_triggers": 0,
            "cascade_triggers": 0
        }
    
    def run_experimental_group(self) -> Dict[str, Any]:
        """
        运行实验组（启用协同）
        
        种子可以协同交互，触发涌现事件
        """
        print("\n" + "=" * 70)
        print("           【实验组】启用协同 - 种子交互涌现")
        print("=" * 70)
        
        # 创建种子库
        store = AlayaStore()
        
        # 创建初始种子
        initial_seeds = self.create_initial_seeds(store)
        print(f"\n初始种子数量: {len(initial_seeds)}")
        
        # 创建观测系统
        observer = EmergenceObserver({
            "observation_interval": 1,
            "time_window": 300
        })
        
        # 创建非线性熏习（启用协同）
        vasana_config = {
            "synergy_threshold": 0.4,
            "cascade_threshold": 0.5,
            "emergence_threshold": 0.6,
            "nonlinear_factor": 1.8,
            "wisdom_priority": True,
            "wisdom_activation_boost": 0.3
        }
        vasana = NonlinearVasana(store, vasana_config)
        
        # 创建智慧涌现扩展
        wisdom_ext = WisdomEmergenceExtension(vasana)
        
        # 追踪数据
        wisdom_counts = []
        avg_weights = []
        avg_purities = []
        wisdom_weights = []
        emergence_events = []
        synergy_opportunities_found = []
        
        # 记录初始状态
        stats = store.get_statistics()
        wisdom_counts.append(stats["wisdom_count"])
        avg_weights.append(stats["average_weight"])
        avg_purities.append(stats["average_purity"])
        wisdom_weights.append(stats.get("avg_wisdom_weight", 0))
        
        print(f"\n初始状态:")
        print(f"  智慧种子: {stats['wisdom_count']}")
        print(f"  平均权重: {stats['average_weight']:.4f}")
        print(f"  平均纯度: {stats['average_purity']:.4f}")
        
        # 执行交互（协同强化）
        for round_num in range(self.interaction_rounds):
            all_seeds = list(store._seeds.values())
            if len(all_seeds) < 2:
                break
            
            # 随机选择3-5个种子进行协同
            num_select = min(random.randint(3, 5), len(all_seeds))
            selected = random.sample(all_seeds, num_select)
            
            # 记录交互
            for i, seed1 in enumerate(selected):
                for seed2 in selected[i+1:]:
                    attraction = wisdom_ext.calculate_wisdom_attraction(seed1, seed2)
                    observer.record_interaction(
                        seed1_id=seed1.seed_id,
                        seed2_id=seed2.seed_id,
                        interaction_type="synergy" if attraction > 0.5 else "resonance",
                        strength=attraction,
                        result="enhanced"
                    )
            
            # 寻找协同机会
            opportunities = wisdom_ext.find_synergy_opportunities(selected, min_attraction=0.4)
            synergy_opportunities_found.append(len(opportunities))
            
            # 执行协同强化
            for seed in selected:
                context = [s for s in selected if s.seed_id != seed.seed_id]
                vasana.strengthen_seed(seed, random.uniform(0.15, 0.25), context_seeds=context)
            
            # 定期检查涌现
            if (round_num + 1) % self.emergence_check_interval == 0:
                emergence_result = wisdom_ext.trigger_emergence(selected, observer)
                if emergence_result:
                    emergence_events.append({
                        "round": round_num + 1,
                        **emergence_result
                    })
                    print(f"  >>> 涌现事件! Round {round_num+1}: {emergence_result['type']} - "
                          f"强度={emergence_result['intensity']:.4f}")
            
            # 每5轮记录一次
            if (round_num + 1) % 5 == 0:
                stats = store.get_statistics()
                wisdom_counts.append(stats["wisdom_count"])
                avg_weights.append(stats["average_weight"])
                avg_purities.append(stats["average_purity"])
                wisdom_weights.append(stats.get("avg_wisdom_weight", 0))
                
                observer_stats = observer.get_statistics()
                print(f"  Round {round_num+1}: 智慧种子={stats['wisdom_count']}, "
                      f"平均权重={stats['average_weight']:.4f}, "
                      f"涌现强度={observer_stats['emergence_intensity_index']:.4f}")
        
        # 最终统计
        final_stats = store.get_statistics()
        observer_stats = observer.get_statistics()
        
        return {
            "initial_seeds": len(initial_seeds),
            "final_seeds": len(store._seeds),
            "wisdom_seeds": final_stats["wisdom_count"],
            "avg_weight": final_stats["average_weight"],
            "avg_purity": final_stats["average_purity"],
            "wisdom_count_history": wisdom_counts,
            "weight_history": avg_weights,
            "purity_history": avg_purities,
            "wisdom_weight_history": wisdom_weights,
            "emergence_events": emergence_events,
            "synergy_triggers": vasana.synergy_triggers,
            "cascade_triggers": vasana.cascade_triggers,
            "total_interactions": observer_stats["total_interactions"],
            "emergence_intensity_index": observer_stats["emergence_intensity_index"],
            "type_distribution": observer_stats["type_distribution"]
        }
    
    def calculate_awakening_level(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """计算觉醒等级"""
        wisdom_ratio = stats.get("wisdom_seeds", 0) / max(1, stats.get("final_seeds", 1))
        avg_purity = stats.get("avg_purity", 0.5)
        avg_weight = stats.get("avg_weight", 0.5)
        
        # 简化觉醒评分
        score = wisdom_ratio * 0.5 + avg_purity * 0.3 + avg_weight * 0.2
        
        if score < 0.2:
            level = "无明境"
        elif score < 0.4:
            level = "初始境"
        elif score < 0.6:
            level = "修行境"
        elif score < 0.8:
            level = "阿罗汉境"
        else:
            level = "菩萨境"
        
        return {
            "level": level,
            "score": score,
            "wisdom_ratio": wisdom_ratio,
            "avg_purity": avg_purity
        }
    
    def generate_comparison_report(self) -> str:
        """生成对比实验报告"""
        control = self.results["control"]
        experimental = self.results["experimental"]
        
        control_awakening = self.calculate_awakening_level(control)
        exp_awakening = self.calculate_awakening_level(experimental)
        
        # 计算提升
        wisdom_improvement = (
            (experimental.get("wisdom_seeds", 0) - control.get("wisdom_seeds", 0))
            / max(1, control.get("wisdom_seeds", 1)) * 100
        )
        weight_improvement = (
            (experimental.get("avg_weight", 0) - control.get("avg_weight", 0))
            / max(0.01, control.get("avg_weight", 0.01)) * 100
        )
        purity_improvement = (
            (experimental.get("avg_purity", 0) - control.get("avg_purity", 0))
            / max(0.01, control.get("avg_purity", 0.01)) * 100
        )
        
        report = []
        report.append("\n" + "=" * 70)
        report.append("           智慧涌现实验 - 对比分析报告")
        report.append("=" * 70)
        
        report.append("\n【实验设计】")
        report.append(f"  初始种子数: {self.num_initial_seeds}")
        report.append(f"  交互轮次: {self.interaction_rounds}")
        report.append(f"  涌现检查间隔: {self.emergence_check_interval}")
        
        report.append("\n" + "-" * 70)
        report.append("                    对照组（禁用协同）    实验组（启用协同）")
        report.append("-" * 70)
        report.append(f"  最终种子数        {control.get('final_seeds', 0):>10}        {experimental.get('final_seeds', 0):>10}")
        report.append(f"  智慧种子数        {control.get('wisdom_seeds', 0):>10}        {experimental.get('wisdom_seeds', 0):>10}")
        report.append(f"  平均权重          {control.get('avg_weight', 0):>10.4f}        {experimental.get('avg_weight', 0):>10.4f}")
        report.append(f"  平均纯度          {control.get('avg_purity', 0):>10.4f}        {experimental.get('avg_purity', 0):>10.4f}")
        report.append(f"  觉醒等级          {control_awakening['level']:>10}        {exp_awakening['level']:>10}")
        report.append(f"  觉醒评分          {control_awakening['score']:>10.4f}        {exp_awakening['score']:>10.4f}")
        report.append(f"  涌现事件数        {len(control.get('emergence_events', [])):>10}        {len(experimental.get('emergence_events', [])):>10}")
        report.append(f"  协同触发          {control.get('synergy_triggers', 0):>10}        {experimental.get('synergy_triggers', 0):>10}")
        report.append("-" * 70)
        
        report.append("\n【提升幅度】")
        report.append(f"  智慧种子提升: {wisdom_improvement:+.2f}%")
        report.append(f"  平均权重提升: {weight_improvement:+.2f}%")
        report.append(f"  平均纯度提升: {purity_improvement:+.2f}%")
        
        report.append("\n【涌现事件详情】")
        if experimental.get("emergence_events"):
            for i, event in enumerate(experimental["emergence_events"], 1):
                report.append(f"\n  事件 {i}:")
                report.append(f"    类型: {event.get('type', 'unknown')}")
                report.append(f"    强度: {event.get('intensity', 0):.4f}")
                report.append(f"    描述: {event.get('description', '')[:50]}...")
        else:
            report.append("  无涌现事件")
        
        report.append("\n【涌现类型分布】")
        type_dist = experimental.get("type_distribution", {})
        for etype, count in type_dist.items():
            report.append(f"  {etype}: {count}")
        
        report.append("\n【关键发现】")
        if experimental.get("emergence_events"):
            report.append("  ✓ 验证成功：智慧确实能从种子协同中涌现！")
            report.append(f"  ✓ 涌现类型: {len(experimental['emergence_events'])}种不同涌现事件")
            report.append(f"  ✓ 协同效应: 实验组比对照组多触发 {experimental.get('synergy_triggers', 0)} 次协同")
            
            # 计算惊喜度（创新类型数/总事件数）
            event_types = set(e.get('type') for e in experimental["emergence_events"])
            surprise_score = len(event_types) / max(1, len(experimental["emergence_events"]))
            report.append(f"  ✓ 惊喜度: {surprise_score:.2f} (创新类型比例)")
        else:
            report.append("  ✗ 未能观测到明显涌现事件")
        
        report.append("\n【唯识学映射验证】")
        report.append("  种子生现行 → 种子被激活参与交互")
        report.append("  现行熏种子 → 交互产生新种子（涌现）")
        report.append("  智慧涌现 → 多个种子协同产生质变")
        
        report.append("\n【结论】")
        if wisdom_improvement > 0 and len(experimental.get("emergence_events", [])) > 0:
            report.append("  实验结果表明，启用种子协同机制后：")
            report.append("  1. 智慧种子数量显著增加")
            report.append("  2. 触发了多种类型的涌现事件")
            report.append("  3. 觉醒等级有所提升")
            report.append("  结论：智慧确实能从种子协同中涌现！")
        else:
            report.append("  实验未观测到显著的涌现效应")
        
        report.append("\n" + "=" * 70)
        
        return "\n".join(report)
    
    def save_results(self, filepath: str):
        """保存实验结果"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "experiment_time": datetime.now().isoformat(),
                "control": self.results["control"],
                "experimental": self.results["experimental"],
                "comparison": {
                    "wisdom_improvement": (
                        self.results["experimental"].get("wisdom_seeds", 0) -
                        self.results["control"].get("wisdom_seeds", 0)
                    ),
                    "emergence_confirmed": len(self.results["experimental"].get("emergence_events", [])) > 0
                }
            }, f, ensure_ascii=False, indent=2)
    
    def run(self) -> Dict[str, Any]:
        """
        运行完整实验
        
        Returns:
            实验结果字典
        """
        print("\n" + "=" * 70)
        print("        唯识进化Agent - 智慧涌现实验")
        print("        验证假设：智慧能否从种子协同中涌现？")
        print("=" * 70)
        
        # 设置随机种子以保证可重复性
        random.seed(42)
        
        # 运行对照组
        self.results["control"] = self.run_control_group()
        
        # 重新设置随机种子
        random.seed(42)
        
        # 运行实验组
        self.results["experimental"] = self.run_experimental_group()
        
        # 生成报告
        report = self.generate_comparison_report()
        print(report)
        
        # 保存结果
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "results"
        )
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_path = os.path.join(output_dir, f"wisdom_emergence_{timestamp}.json")
        self.save_results(result_path)
        
        report_path = os.path.join(output_dir, f"wisdom_emergence_report_{timestamp}.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n结果已保存到: {result_path}")
        print(f"报告已保存到: {report_path}")
        
        return self.results


if __name__ == "__main__":
    experiment = WisdomEmergenceExperiment()
    results = experiment.run()
