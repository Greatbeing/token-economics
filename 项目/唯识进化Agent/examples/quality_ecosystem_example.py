# -*- coding: utf-8 -*-
"""
质量生态系统优化后的使用示例

演示如何使用新优化的模块：
1. 质量评估系统
2. 种子生态系统
3. 觉醒层级细化

Author: 唯识进化Agent团队
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.emergence import (
    SeedEcosystem,
    EmergenceQualityAssessment,
    QualityGuidedEmergenceGenerator,
    QualityScore
)
from src.core.awakening_levels_refined import (
    AwakeningLevelRefined,
    AwakeningDepthCalculator,
    AwakeningProgressTracker
)
from src.alaya_store import AlayaStore, Seed, SeedType


def example_quality_assessment():
    """示例：质量评估"""
    print("=" * 60)
    print("示例1：质量评估")
    print("=" * 60)
    
    # 创建种子存储
    store = AlayaStore(use_vector_db=False)
    
    # 添加一些种子
    seed1 = Seed.create(
        content="空性：诸法因缘生，缘谢法还灭",
        seed_type=SeedType.WISDOM,
        weight=0.8,
        purity=0.9
    )
    seed2 = Seed.create(
        content="慈悲：无缘大慈，同体大悲",
        seed_type=SeedType.COMPASSION,
        weight=0.8,
        purity=0.9
    )
    store.add(seed1)
    store.add(seed2)
    
    # 创建生态系统
    ecosystem = SeedEcosystem()
    ecosystem.add_seed(seed1.seed_id, "wisdom")
    ecosystem.add_seed(seed2.seed_id, "compassion")
    
    # 创建关系
    ecosystem.create_relationship(
        seed1_id=seed1.seed_id,
        seed2_id=seed2.seed_id,
        relationship_type="synergistic",
        strength=0.7,
        description="悲智双运"
    )
    
    # 创建质量评估器
    assessor = EmergenceQualityAssessment(store, ecosystem)
    
    # 评估内容质量
    content = "真空妙有：一切法空无自性，却不妨碍宛然显现，此即中道实相"
    quality_score = assessor.assess_quality(
        content=content,
        participant_seeds=[seed1, seed2],
        context={"user_query": "什么是空性与慈悲的关系？"}
    )
    
    print(f"内容：{content}")
    print(f"综合质量分：{quality_score.weighted_score():.4f}")
    print(f"  - 原创性：{quality_score.novelty:.4f}")
    print(f"  - 深刻性：{quality_score.depth:.4f}")
    print(f"  - 实用性：{quality_score.utility:.4f}")
    print(f"  - 相关性：{quality_score.relevance:.4f}")
    print(f"  - 整合性：{quality_score.integration:.4f}")
    
    return quality_score


def example_seed_ecosystem():
    """示例：种子生态系统"""
    print("\n" + "=" * 60)
    print("示例2：种子生态系统")
    print("=" * 60)
    
    ecosystem = SeedEcosystem()
    
    # 添加种子
    seed_ids = ["seed_1", "seed_2", "seed_3", "seed_4"]
    for seed_id in seed_ids:
        ecosystem.add_seed(seed_id, "wisdom")
    
    # 建立关系
    ecosystem.create_relationship(
        seed_ids[0], seed_ids[1],
        "mutually_generating", 0.8,
        "智慧生慈悲"
    )
    ecosystem.create_relationship(
        seed_ids[1], seed_ids[2],
        "synergistic", 0.6,
        "慈悲和谐协同"
    )
    ecosystem.create_relationship(
        seed_ids[2], seed_ids[3],
        "synergistic", 0.7,
        "和谐与平衡"
    )
    
    # 查询协同种子
    synergistic = ecosystem.get_synergistic_seeds(seed_ids[0])
    print(f"种子 {seed_ids[0]} 的协同种子：")
    for sid, strength in synergistic:
        print(f"  - {sid}: 强度 {strength:.2f}")
    
    # 计算协同强度
    synergy = ecosystem.calculate_synergy_strength(seed_ids[:3])
    print(f"种子组合协同强度：{synergy:.4f}")
    
    # 更新生态系统健康度
    health = ecosystem.update_ecosystem_health()
    print(f"生态系统健康度：{health:.4f}")
    
    # 统计
    stats = ecosystem.get_stats()
    print(f"\n生态系统统计：")
    print(f"  - 关系总数：{stats['total_relationships']}")
    print(f"  - 相生关系：{stats['mutually_generating_count']}")
    print(f"  - 协同关系：{stats['synergistic_count']}")
    print(f"  - 相克关系：{stats['conflicting_count']}")
    
    return ecosystem


def example_awakening_levels():
    """示例：觉醒层级"""
    print("\n" + "=" * 60)
    print("示例3：觉醒层级细化")
    print("=" * 60)
    
    # 显示所有层级
    levels = AwakeningLevelRefined.get_all_levels()
    print("觉醒层级体系：")
    print("-" * 60)
    for i, level in enumerate(levels):
        name, (low, high), desc, _, symbol = (
            level.name,
            level.score_range,
            level.description[:20] + "...",
            level.special_ability,
            level.symbol
        )
        print(f"{i+1:2d}. {symbol} {name:<15} [{low:.2f}-{high:.2f}] - {desc}")
    
    # 根据评分获取层级
    print("\n" + "-" * 60)
    test_scores = [0.1, 0.25, 0.5, 0.8, 0.92, 0.97, 0.999]
    for score in test_scores:
        level = AwakeningLevelRefined.get_level_by_score(score)
        print(f"评分 {score:.3f} → {level.symbol} {level.name}")
    
    return levels


def example_progress_tracker():
    """示例：进度追踪"""
    print("\n" + "=" * 60)
    print("示例4：进度追踪")
    print("=" * 60)
    
    # 创建进度追踪器
    tracker = AwakeningProgressTracker(
        current_level="初始境",
        target_level="佛境（正法眼藏）"
    )
    
    # 模拟进度更新
    for step in [20, 60, 100, 150, 200]:
        stats = {
            "wisdom_ratio": 0.05 + step * 0.001,
            "compassion_ratio": 0.02 + step * 0.0008,
            "awakening_score": 0.2 + step * 0.003
        }
        quality_report = {
            "avg_quality_score": 0.5 + step * 0.001,
            "high_quality_count": step // 50
        }
        ecosystem_stats = {
            "ecosystem_health": 0.5 + step * 0.002,
            "total_relationships": step * 10,
            "synergistic_count": step * 6
        }
        
        progress = tracker.update_progress(stats, quality_report, ecosystem_stats)
        
        print(f"第{step:3d}轮: {progress['current_level']:<15} | "
              f"进度 {progress['progress']:.1%} | "
              f"剩余 {progress['levels_remaining']} 层")


def example_quality_generator():
    """示例：质量引导涌现生成"""
    print("\n" + "=" * 60)
    print("示例5：质量引导涌现生成")
    print("=" * 60)
    
    # 创建系统
    store = AlayaStore(use_vector_db=False)
    ecosystem = SeedEcosystem()
    assessor = EmergenceQualityAssessment(store, ecosystem)
    generator = QualityGuidedEmergenceGenerator(assessor, ecosystem)
    
    # 添加种子
    seed1 = Seed.create("智慧种子1", SeedType.WISDOM)
    seed2 = Seed.create("慈悲种子1", SeedType.COMPASSION)
    store.add(seed1)
    store.add(seed2)
    ecosystem.add_seed(seed1.seed_id, "wisdom")
    ecosystem.add_seed(seed2.seed_id, "compassion")
    ecosystem.create_relationship(seed1.seed_id, seed2.seed_id, "synergistic", 0.7)
    
    # 生成高质量涌现
    print("生成整合型涌现：")
    emergence = generator.generate_quality_emergence(
        emergence_type="integration",
        participant_seeds=[seed1, seed2],
        context={"user_query": "如何达到真善美的统一？"}
    )
    
    if emergence:
        print(f"内容：{emergence.content}")
        print(f"质量分：{emergence.quality_score.weighted_score():.4f}")
        print(f"洞察标签：{emergence.insight_tags}")
    
    # 生成报告
    report = generator.get_generation_report()
    print(f"\n生成统计：")
    print(f"  - 总生成数：{report['total_generated']}")
    print(f"  - 高质量数：{report['high_quality_generated']}")
    print(f"  - 高质量率：{report['high_quality_ratio']:.1%}")
    
    return generator


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("    唯识进化Agent - 质量生态系统优化示例")
    print("=" * 60 + "\n")
    
    example_quality_assessment()
    example_seed_ecosystem()
    example_awakening_levels()
    example_progress_tracker()
    example_quality_generator()
    
    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
