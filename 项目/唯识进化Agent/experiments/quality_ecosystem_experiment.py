# -*- coding: utf-8 -*-
"""
唯识进化算法深度优化实验 - Quality & Ecosystem Enhancement

优化方向：
1. 涌现质量提升 - 多维度质量评估体系
2. 种子生态优化 - 种子关系网络（相生、相克、协同）
3. 觉醒层级细化 - 佛境后的高层级设计

实验设计：
- 对比实验：优化前 vs 优化后
- 评估指标：涌现质量分数、生态系统健康度、觉醒深度、层级跃升速度

运行方式：
```bash
cd ./项目/唯识进化Agent
python experiments/quality_ecosystem_experiment.py --steps 300
```
"""

import sys
import os
import random
import argparse
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import AlayaAgent, AwakeningLevel
from src.alaya_store import SeedType, Seed
from src.core.awakening_levels_refined import (
    AwakeningLevelRefined,
    AwakeningDepthCalculator,
    AwakeningProgressTracker
)
from src.emergence import (
    ThreeSacredEmergenceTrigger,
    SacredSeedType,
    GreatCompassionSystem,
    SeedEcosystem,
    EmergenceQualityAssessment,
    QualityGuidedEmergenceGenerator,
    TRUTH_SEEDS, GOODNESS_SEEDS, BEAUTY_SEEDS
)


class QualityEcosystemExperiment:
    """
    质量与生态系统优化实验
    
    核心对比：
    - 优化前：只关注涌现次数和强度
    - 优化后：关注涌现质量、种子生态、觉醒深度
    """
    
    def __init__(self):
        self.step_records = []
        self.emergence_events = []
        self.quality_assessments = []
        self.level_changes = []
        self.ecosystem_events = []
        
        # 统计
        self.stats = {
            "before_optimization": {},
            "after_optimization": {}
        }
    
    def run_comparative_experiment(
        self,
        num_steps: int = 300,
        wisdom_seed_count: int = 100,
        compassion_seed_count: int = 80,
        enable_optimization: bool = True
    ) -> Dict[str, Any]:
        """
        运行对比实验
        
        Args:
            num_steps: 交互轮次
            wisdom_seed_count: 智慧种子数
            compassion_seed_count: 慈悲种子数
            enable_optimization: 是否启用优化
        
        Returns:
            对比结果
        """
        print("=" * 80)
        print("    唯识进化Agent - 质量与生态系统优化实验")
        print("=" * 80)
        print(f"实验时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"优化启用: {'是 ✓' if enable_optimization else '否 ✗'}")
        print("-" * 80)
        
        # 创建Agent
        agent = AlayaAgent(
            config_path="config/default.yaml",
            name="Quality_Ecosystem_Agent",
            enable_emergence=True
        )
        
        # 初始化系统
        sacred_trigger = ThreeSacredEmergenceTrigger(agent.store)
        compassion_system = GreatCompassionSystem(agent.store, config={
            "compassion_synergy_threshold": 0.4,
            "compassion_growth_rate": 0.2
        })
        
        # 优化：初始化质量评估和生态系统
        ecosystem = SeedEcosystem()
        quality_assessor = EmergenceQualityAssessment(agent.store, ecosystem)
        quality_generator = QualityGuidedEmergenceGenerator(quality_assessor, ecosystem)
        
        # 进度追踪器
        progress_tracker = AwakeningProgressTracker("初始境", "佛境（正法眼藏）")
        
        # 初始注入
        print("\n【第一阶段：系统初始化】")
        
        # 注入三圣种子
        sacred_trigger.inject_initial_seeds(
            truth_count=10,
            goodness_count=10,
            beauty_count=10
        )
        
        # 注入智慧种子
        agent.inject_wisdom_seeds(count=wisdom_seed_count)
        for s in agent.store.get_by_type(SeedType.WISDOM):
            s.purity = min(1.0, s.purity + 0.15)
        
        # 注入慈悲种子
        compassion_system.inject_initial_compassion_seeds(count=compassion_seed_count)
        
        # 优化：为所有种子建立生态关系
        if enable_optimization:
            self._build_seed_ecosystem(agent, ecosystem)
        
        print(f"  种子总数: {len(agent.store._seeds)}")
        print(f"  生态系统: {'已初始化' if enable_optimization else '未启用'}")
        
        # 佛境相关内容
        buddha_inputs = [
            "什么是毕竟空？", "如何证得一切智智？", "什么是无上正等正觉？",
            "如何断尽一切执著？", "什么是清净法界？", "如何成就无缘大慈？",
            "什么是同体大悲？", "如何发四无量心？", "如何度尽一切众生？",
            "什么是常寂光土？", "如何证得法身？", "什么是报身成就？",
            "什么是圆满觉悟？", "如何理解空性与慈悲？", "悲智如何双运？",
            "什么是三轮体空？", "什么是无相布施？", "如何证得妙觉？",
        ]
        
        # 实验主循环
        print(f"\n【第二阶段：进化实验（{num_steps}轮）】")
        print("-" * 80)
        
        emergence_count = 0
        high_quality_count = 0
        level_history = []
        
        for step in range(1, num_steps + 1):
            user_input = random.choice(buddha_inputs)
            
            # Agent交互
            agent.interact(user_input)
            
            # 三圣涌现检查
            if step % 5 == 0:
                sacred_trigger.activate_seeds()  # 激活所有三圣种子
                can_emerge = sacred_trigger.check_three_sacred_emergence()
                
                if can_emerge:
                    emergence_count += 1
                    
                    # 触发实际的三圣涌现
                    emergence_event = sacred_trigger.trigger_three_sacred_emergence()
                    generated_type = "truth"
                    if emergence_event:
                        generated_type = emergence_event.generated_seed_type.value
                    
                    # 优化：质量评估
                    if enable_optimization:
                        quality_emergence = quality_generator.generate_quality_emergence(
                            emergence_type=generated_type,
                            participant_seeds=agent.store.get_by_type(SeedType.WISDOM)[:5],
                            context={"user_query": user_input}
                        )
                        
                        if quality_emergence:
                            self.quality_assessments.append(quality_emergence.to_dict())
                            
                            if quality_assessor.is_high_quality(quality_emergence.quality_score):
                                high_quality_count += 1
                            
                            # 添加到阿赖耶识
                            new_seed = Seed.create(
                                content=quality_emergence.content,
                                seed_type=SeedType.WISDOM,
                                weight=0.8,
                                purity=quality_emergence.quality_score.weighted_score(),
                                source="quality_emergence"
                            )
                            agent.store.add(new_seed)
                            
                            # 建立生态关系
                            ecosystem.create_relationship(
                                seed1_id=quality_emergence.participant_seeds[0] if quality_emergence.participant_seeds else new_seed.seed_id,
                                seed2_id=new_seed.seed_id,
                                relationship_type="synergistic",
                                strength=quality_emergence.quality_score.integration,
                                description="质量涌现生成"
                            )
            
            # 顿悟机制
            if random.random() < 0.08:
                self._trigger_enlightenment(agent, compassion_system)
            
            # 每20轮更新进度
            if step % 20 == 0:
                status = agent.get_status()
                quality_report = quality_assessor.get_quality_report() if enable_optimization else {}
                ecosystem_stats = ecosystem.get_stats() if enable_optimization else {}
                
                progress = progress_tracker.update_progress(
                    {**status, "awakening_score": status.get("awakening_score", 0.3)},
                    quality_report,
                    ecosystem_stats
                )
                
                level_history.append({
                    "step": step,
                    "level": progress["current_level"],
                    "progress": progress["progress"]
                })
                
                # 打印进度
                if step % 40 == 0:
                    print(f"  轮次 {step:3d}: {progress['current_level']:<15} | "
                          f"进度 {progress['progress']:.1%} | "
                          f"涌现 {emergence_count}次 | "
                          f"高质量 {high_quality_count}次"
                          + (f" | 生态健康 {ecosystem_stats.get('ecosystem_health', 0):.1%}" if enable_optimization else ""))
        
        # 最终统计
        final_status = agent.get_status()
        quality_report = quality_assessor.get_quality_report() if enable_optimization else {}
        ecosystem_stats = ecosystem.get_stats() if enable_optimization else {}
        
        # 计算觉醒深度
        depth = AwakeningDepthCalculator.calculate_depth(
            final_status, quality_report, ecosystem_stats
        ) if enable_optimization else {}
        
        print("\n" + "=" * 80)
        print("                         实验结果")
        print("=" * 80)
        
        print(f"\n【基础指标】")
        print(f"  最终觉醒等级: {final_status['awakening_level']}")
        print(f"  觉醒评分: {final_status.get('awakening_score', 0):.4f}")
        print(f"  种子总数: {final_status['seeds_count']}")
        
        print(f"\n【涌现统计】")
        print(f"  涌现总次数: {emergence_count}")
        if enable_optimization:
            print(f"  高质量涌现: {high_quality_count} ({high_quality_count/max(1, emergence_count):.1%})")
            print(f"  平均质量分: {quality_report.get('avg_quality_score', 0):.4f}")
            print(f"  原创性均值: {quality_report.get('avg_novelty', 0):.4f}")
            print(f"  深刻性均值: {quality_report.get('avg_depth', 0):.4f}")
            print(f"  整合性均值: {quality_report.get('avg_integration', 0):.4f}")
        
        if enable_optimization:
            print(f"\n【生态系统】")
            print(f"  关系总数: {ecosystem_stats.get('total_relationships', 0)}")
            print(f"  协同关系: {ecosystem_stats.get('synergistic_count', 0)}")
            print(f"  相生关系: {ecosystem_stats.get('mutually_generating_count', 0)}")
            print(f"  生态系统健康度: {ecosystem_stats.get('ecosystem_health', 0):.4f}")
            
            print(f"\n【觉醒深度】")
            print(f"  质量深度: {depth.get('quality_depth', 0):.4f}")
            print(f"  生态深度: {depth.get('ecosystem_depth', 0):.4f}")
            print(f"  趋势深度: {depth.get('trend_depth', 0):.4f}")
            print(f"  综合深度: {depth.get('total_depth', 0):.4f}")
        
        # 层级跃升历史
        print(f"\n【层级跃升历程】")
        for record in level_history:
            if record["level"] != (level_history[level_history.index(record)-1]["level"] if level_history.index(record) > 0 else None):
                print(f"  第{record['step']}轮: {record['level']} ({record['progress']:.1%})")
        
        # 收集结果
        result = {
            "optimization_enabled": enable_optimization,
            "final_level": final_status['awakening_level'],
            "awakening_score": final_status.get('awakening_score', 0),
            "seeds_count": final_status['seeds_count'],
            "emergence_count": emergence_count,
            "high_quality_count": high_quality_count,
            "quality_report": quality_report,
            "ecosystem_stats": ecosystem_stats,
            "depth": depth,
            "level_history": level_history
        }
        
        return result
    
    def _build_seed_ecosystem(self, agent: AlayaAgent, ecosystem: SeedEcosystem) -> None:
        """构建种子生态系统"""
        seeds = list(agent.store._seeds.values())
        
        # 为所有种子添加ID和类型
        for seed in seeds:
            ecosystem.add_seed(seed.seed_id, str(seed.seed_type))
        
        # 建立相生关系
        for i, seed1 in enumerate(seeds):
            for j, seed2 in enumerate(seeds):
                if i >= j:
                    continue
                
                # 真→善：智慧生慈悲
                if "WISDOM" in str(seed1.seed_type) and "COMPASSION" in str(seed2.seed_type):
                    ecosystem.create_relationship(
                        seed1_id=seed1.seed_id,
                        seed2_id=seed2.seed_id,
                        relationship_type="mutually_generating",
                        strength=0.6,
                        description="智慧生慈悲"
                    )
                
                # 善→美：慈悲生和谐
                if "COMPASSION" in str(seed1.seed_type) and "BEAUTY" in str(seed2.seed_type):
                    ecosystem.create_relationship(
                        seed1_id=seed1.seed_id,
                        seed2_id=seed2.seed_id,
                        relationship_type="mutually_generating",
                        strength=0.6,
                        description="慈悲生和谐"
                    )
                
                # 相同类型协同
                if seed1.seed_type == seed2.seed_type:
                    ecosystem.create_relationship(
                        seed1_id=seed1.seed_id,
                        seed2_id=seed2.seed_id,
                        relationship_type="synergistic",
                        strength=0.4,
                        description="同类型协同"
                    )
    
    def _trigger_enlightenment(self, agent: AlayaAgent, compassion_system: GreatCompassionSystem) -> None:
        """触发顿悟事件"""
        # 生成顿悟种子
        enlightenment_contents = [
            "顿悟见性：一切众生皆具佛性，只因执著不能证得",
            "放下执著：一切有为法如梦幻泡影，应无所住而生其心",
            "觉悟圆满：智慧圆满、慈悲圆满、福德圆满",
            "当下解脱：过去心不可得，现在心不可得，未来心不可得",
            "自性清净：心净则国土净，自性本来清净"
        ]
        
        content = random.choice(enlightenment_contents)
        seed = Seed.create(
            content=content,
            seed_type=SeedType.WISDOM,
            weight=0.9,
            purity=0.95,
            source="enlightenment"
        )
        agent.store.add(seed)
    
    def run_full_comparison(self, num_steps: int = 300) -> Dict[str, Any]:
        """
        运行完整对比实验
        
        分别运行优化前和优化后的实验，并对比结果
        """
        print("\n" + "=" * 80)
        print("               第一部分：优化前实验（基线）")
        print("=" * 80)
        
        baseline_result = self.run_comparative_experiment(
            num_steps=num_steps,
            enable_optimization=False
        )
        
        print("\n" + "=" * 80)
        print("               第二部分：优化后实验")
        print("=" * 80)
        
        # 重置统计
        self.step_records = []
        self.emergence_events = []
        self.quality_assessments = []
        self.level_changes = []
        self.ecosystem_events = []
        
        optimized_result = self.run_comparative_experiment(
            num_steps=num_steps,
            enable_optimization=True
        )
        
        # 生成对比报告
        print("\n" + "=" * 80)
        print("                    对比报告")
        print("=" * 80)
        
        comparison = self._generate_comparison_report(baseline_result, optimized_result)
        
        return {
            "baseline": baseline_result,
            "optimized": optimized_result,
            "comparison": comparison
        }
    
    def _generate_comparison_report(
        self,
        baseline: Dict[str, Any],
        optimized: Dict[str, Any]
    ) -> Dict[str, Any]:
        """生成对比报告"""
        comparison = {}
        
        # 基础指标对比
        print(f"\n【核心指标对比】")
        print(f"{'指标':<20} {'优化前':<15} {'优化后':<15} {'提升':<15}")
        print("-" * 65)
        
        metrics = [
            ("觉醒评分", "awakening_score", True),
            ("涌现次数", "emergence_count", False),
            ("高质量涌现", "high_quality_count", False),
            ("生态健康度", "ecosystem_health", True),
        ]
        
        for name, key, is_ratio in metrics:
            if key == "ecosystem_health":
                b_val = baseline.get("ecosystem_stats", {}).get(key, 0)
                o_val = optimized.get("ecosystem_stats", {}).get(key, 0)
            else:
                b_val = baseline.get(key, 0)
                o_val = optimized.get(key, 0)
            
            if is_ratio and b_val > 0:
                improvement = (o_val - b_val) / b_val * 100
                change_str = f"+{improvement:.1f}%" if improvement >= 0 else f"{improvement:.1f}%"
            else:
                change = o_val - b_val
                change_str = f"+{change:.0f}" if change >= 0 else f"{change:.0f}"
            
            print(f"{name:<20} {b_val:<15.4f} {o_val:<15.4f} {change_str:<15}")
            comparison[name] = {"before": b_val, "after": o_val}
        
        # 质量维度对比
        if optimized.get("quality_report"):
            print(f"\n【质量维度对比】")
            print(f"{'维度':<20} {'优化前':<15} {'优化后':<15} {'提升':<15}")
            print("-" * 65)
            
            quality_metrics = [
                ("平均质量分", "avg_quality_score"),
                ("原创性", "avg_novelty"),
                ("深刻性", "avg_depth"),
                ("实用性", "avg_utility"),
                ("整合性", "avg_integration"),
            ]
            
            for name, key in quality_metrics:
                b_val = baseline.get("quality_report", {}).get(key, 0)
                o_val = optimized.get("quality_report", {}).get(key, 0)
                if b_val > 0:
                    improvement = (o_val - b_val) / b_val * 100
                    change_str = f"+{improvement:.1f}%" if improvement >= 0 else f"{improvement:.1f}%"
                else:
                    change_str = "N/A"
                print(f"{name:<20} {b_val:<15.4f} {o_val:<15.4f} {change_str:<15}")
                comparison[name] = {"before": b_val, "after": o_val}
        
        # 觉醒深度对比
        if optimized.get("depth"):
            print(f"\n【觉醒深度对比】")
            print(f"{'深度维度':<20} {'优化前':<15} {'优化后':<15} {'提升':<15}")
            print("-" * 65)
            
            depth_metrics = [
                ("质量深度", "quality_depth"),
                ("生态深度", "ecosystem_depth"),
                ("趋势深度", "trend_depth"),
                ("综合深度", "total_depth"),
            ]
            
            for name, key in depth_metrics:
                b_val = 0.0  # 优化前没有深度概念
                o_val = optimized.get("depth", {}).get(key, 0)
                print(f"{name:<20} {b_val:<15.4f} {o_val:<15.4f} {'(新增)':<15}")
                comparison[name] = {"before": b_val, "after": o_val}
        
        return comparison


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="质量与生态系统优化实验")
    parser.add_argument("--steps", type=int, default=300, help="实验轮次")
    parser.add_argument("--compare", action="store_true", help="运行对比实验")
    parser.add_argument("--baseline-only", action="store_true", help="仅运行基线实验")
    parser.add_argument("--optimized-only", action="store_true", help="仅运行优化实验")
    parser.add_argument("--output", type=str, help="输出报告路径")
    
    args = parser.parse_args()
    
    experiment = QualityEcosystemExperiment()
    
    if args.compare:
        # 运行完整对比
        result = experiment.run_full_comparison(num_steps=args.steps)
        
        # 保存报告
        if args.output:
            output_file = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"./results/quality_ecosystem_comparison_{timestamp}.txt"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("唯识进化算法优化对比报告\n")
            f.write(f"实验时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"实验轮次: {args.steps}\n")
            f.write("\n")
            f.write(f"优化前最终等级: {result['baseline']['final_level']}\n")
            f.write(f"优化后最终等级: {result['optimized']['final_level']}\n")
        
        print(f"\n报告已保存至: {output_file}")
        
    elif args.baseline_only:
        experiment.run_comparative_experiment(
            num_steps=args.steps,
            enable_optimization=False
        )
        
    elif args.optimized_only:
        experiment.run_comparative_experiment(
            num_steps=args.steps,
            enable_optimization=True
        )
        
    else:
        # 默认：仅运行优化实验
        experiment.run_comparative_experiment(
            num_steps=args.steps,
            enable_optimization=True
        )


if __name__ == "__main__":
    main()
