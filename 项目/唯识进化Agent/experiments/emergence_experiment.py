# -*- coding: utf-8 -*-
"""
涌现优化对比实验【质量优先策略验证】

对比优化前后的效果：
1. 种子纯度分布对比
2. 觉醒等级跃升对比
3. 智慧种子生成对比
4. 质量门控效果对比

运行方式：
```bash
cd ./项目/唯识进化Agent
python experiments/emergence_experiment.py
```
"""

import sys
import os
import time
import random
from typing import Dict, List, Any
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import AlayaAgent
from src.alaya_store import SeedType


class QualityFirstExperiment:
    """
    质量优先策略对比实验
    
    对比"数量优先"(优化前) vs "质量优先"(优化后)策略
    """
    
    def __init__(self):
        self.results = {
            "before_optimization": {},
            "after_optimization": {}
        }
    
    def run_experiment(self, num_interactions: int = 100) -> Dict[str, Any]:
        """
        运行对比实验
        
        Args:
            num_interactions: 交互次数
        
        Returns:
            实验结果
        """
        print("=" * 70)
        print("            唯识进化Agent - 质量优先策略对比实验")
        print("=" * 70)
        
        # 测试样本
        test_inputs = [
            "什么是缘起性空？",
            "如何修行才能开悟？",
            "请解释无常的道理",
            "慈悲心如何培养？",
            "什么是无我和空性？",
            "修行中遇到烦恼怎么办？",
            "如何做到活在当下？",
            "禅定有什么好处？",
            "如何理解诸行无常？",
            "怎样才能减少执著？",
            "布施有什么意义？",
            "正念冥想怎么做？",
            "什么是止观双运？",
            "如何培养感恩心？",
            "怎样看待生活中的困难？",
            "缘起法的核心是什么？",
            "如何对治嗔恨心？",
            "什么是戒定慧三学？",
            "如何修习慈悲观？",
            "怎样理解生死轮回？",
        ]
        
        # 循环使用测试输入
        inputs = (test_inputs * ((num_interactions // len(test_inputs)) + 1))[:num_interactions]
        
        # ========== 实验1：优化前（原始参数）==========
        print("\n【实验1】优化前（原始参数）")
        print("-" * 50)
        
        # 创建Agent时禁用涌现优化，使用原始的纯度计算
        agent_before = AlayaAgent(
            config_path="config/default.yaml",
            name="Alaya_Before",
            enable_emergence=False
        )
        
        # 记录初始状态
        initial_status = agent_before.get_status()
        print(f"  初始状态: 种子={initial_status['seeds_count']}, "
              f"觉醒={initial_status['awakening_level']}, "
              f"评分={initial_status['awakening_score']:.3f}")
        
        start_time = time.time()
        self._run_interactions(agent_before, inputs, desc="优化前")
        time_before = time.time() - start_time
        
        stats_before = self._collect_stats(agent_before, prefix="before")
        self.results["before_optimization"] = stats_before
        self.results["before_optimization"]["time"] = time_before
        
        final_before = agent_before.get_status()
        print(f"  最终状态: 种子={final_before['seeds_count']}, "
              f"觉醒={final_before['awakening_level']}, "
              f"评分={final_before['awakening_score']:.3f}")
        print(f"  完成用时: {time_before:.2f}秒")
        
        # ========== 实验2：优化后（质量优先策略）==========
        print("\n【实验2】优化后（质量优先策略）")
        print("-" * 50)
        
        agent_after = AlayaAgent(
            config_path="config/default.yaml",
            name="Alaya_After",
            enable_emergence=True
        )
        
        # 先注入一些基础智慧种子
        print("  注入基础智慧种子...")
        injected = agent_after.inject_wisdom_seeds(count=30)
        print(f"  已注入 {injected} 个智慧种子")
        
        # 记录初始状态
        initial_status = agent_after.get_status()
        print(f"  初始状态: 种子={initial_status['seeds_count']}, "
              f"觉醒={initial_status['awakening_level']}, "
              f"评分={initial_status['awakening_score']:.3f}")
        
        start_time = time.time()
        self._run_interactions(agent_after, inputs, desc="优化后")
        time_after = time.time() - start_time
        
        stats_after = self._collect_stats(agent_after, prefix="after")
        self.results["after_optimization"] = stats_after
        self.results["after_optimization"]["time"] = time_after
        
        final_after = agent_after.get_status()
        print(f"  最终状态: 种子={final_after['seeds_count']}, "
              f"觉醒={final_after['awakening_level']}, "
              f"评分={final_after['awakening_score']:.3f}")
        print(f"  完成用时: {time_after:.2f}秒")
        
        # ========== 生成对比报告 ==========
        report = self._generate_comparison_report()
        
        return {
            "before_optimization": self.results["before_optimization"],
            "after_optimization": self.results["after_optimization"],
            "report": report
        }
    
    def _run_interactions(
        self,
        agent: AlayaAgent,
        inputs: List[str],
        desc: str
    ) -> None:
        """运行交互"""
        history = []
        
        for i, user_input in enumerate(inputs):
            agent.interact(user_input)
            history.append(agent.get_status())
            
            # 每20次交互输出一次状态
            if (i + 1) % 20 == 0:
                status = agent.get_status()
                print(f"  [{desc}] 交互{i+1}: 种子={status['seeds_count']}, "
                      f"觉醒={status['awakening_level']}, "
                      f"评分={status['awakening_score']:.3f}, "
                      f"纯度={status['average_purity']:.3f}")
                
                # 如果启用涌现优化，每20次检查一次涌现状态
                if hasattr(agent, 'enable_emergence') and agent.enable_emergence:
                    if hasattr(agent, 'edge_of_chaos'):
                        edge_state = agent.edge_of_chaos.maintain_edge()
                        print(f"         边缘状态={edge_state['current_regime']}, "
                              f"秩序={edge_state['order']:.3f}, "
                              f"混沌={edge_state['chaos']:.3f}")
        
        # 记录历史
        return history
    
    def _collect_stats(self, agent: AlayaAgent, prefix: str) -> Dict[str, Any]:
        """收集统计数据"""
        status = agent.get_status()
        store_stats = agent.store.get_statistics()
        
        stats = {
            "interaction_count": status["interaction_count"],
            "seeds_count": status["seeds_count"],
            "average_purity": status["average_purity"],
            "awakening_level": status["awakening_level"],
            "awakening_score": status["awakening_score"],
            "wisdom_seeds": store_stats.get("wisdom_count", 0),
            "wisdom_ratio": store_stats.get("wisdom_ratio", 0),
            "high_quality_ratio": store_stats.get("high_quality_ratio", 0),
            "contaminated_seeds": store_stats.get("contaminated_seeds", 0),
            "type_distribution": store_stats.get("type_distribution", {})
        }
        
        # 如果有涌现模块，添加更多统计
        if hasattr(agent, 'enable_emergence') and agent.enable_emergence:
            emergence_status = agent.get_emergence_status()
            stats["emergence"] = {
                "nonlinear_vasana": emergence_status.get("nonlinear_vasana", {}),
                "edge_of_chaos": emergence_status.get("edge_of_chaos", {}),
            }
        
        return stats
    
    def _generate_comparison_report(self) -> str:
        """生成对比报告"""
        before = self.results["before_optimization"]
        after = self.results["after_optimization"]
        
        # 计算改进比例
        def improvement(new_val, old_val):
            if old_val == 0:
                return float('inf') if new_val > 0 else 0
            return ((new_val - old_val) / old_val) * 100
        
        # 计算评分变化
        score_change = after.get("awakening_score", 0) - before.get("awakening_score", 0)
        
        # 判断是否达到目标
        target_achieved = after.get("awakening_level", "") in ["初始境", "修行境", "阿罗汉境", "菩萨境", "涅槃境"]
        
        report = f"""
{'='*70}
                     质量优先策略对比实验报告
{'='*70}

实验时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
实验参数: {before['interaction_count']} 次交互

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                            核心指标对比
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

指标                    优化前          优化后          变化
────────────────────────────────────────────────────────────
觉醒等级                {before.get('awakening_level', 'N/A'):<12}    {after.get('awakening_level', 'N/A'):<12}    {'→' if score_change >= 0 else '↓'} {abs(score_change):.3f}
觉醒评分                {before.get('awakening_score', 0):.3f}           {after.get('awakening_score', 0):.3f}           {score_change:+.3f}
平均纯度                {before.get('average_purity', 0):.3f}           {after.get('average_purity', 0):.3f}           {improvement(after.get('average_purity', 0), before.get('average_purity', 0)):+.1f}%
智慧种子数              {before.get('wisdom_seeds', 0):<12}    {after.get('wisdom_seeds', 0):<12}    {improvement(after.get('wisdom_seeds', 0), before.get('wisdom_seeds', 0)):+.1f}%
智慧种子比例            {before.get('wisdom_ratio', 0):.3f}           {after.get('wisdom_ratio', 0):.3f}           {improvement(after.get('wisdom_ratio', 0), before.get('wisdom_ratio', 0)):+.1f}%
高质量种子比例          {before.get('high_quality_ratio', 0):.3f}           {after.get('high_quality_ratio', 0):.3f}           {improvement(after.get('high_quality_ratio', 0), before.get('high_quality_ratio', 0)):+.1f}%
染污种子数              {before.get('contaminated_seeds', 0):<12}    {after.get('contaminated_seeds', 0):<12}    {improvement(after.get('contaminated_seeds', 0), before.get('contaminated_seeds', 0)):+.1f}%
种子总数                {before.get('seeds_count', 0):<12}    {after.get('seeds_count', 0):<12}    {improvement(after.get('seeds_count', 0), before.get('seeds_count', 0)):+.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                          种子类型分布对比
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

种子类型          优化前      优化后
────────────────────────────────────
"""
        
        before_dist = before.get("type_distribution", {})
        after_dist = after.get("type_distribution", {})
        
        all_types = set(before_dist.keys()) | set(after_dist.keys())
        for seed_type in all_types:
            before_count = before_dist.get(seed_type, 0)
            after_count = after_dist.get(seed_type, 0)
            report += f"{seed_type:<12}    {before_count:<8}    {after_count}\n"
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                            结论
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【优化效果】
1. 觉醒等级: {'提升至 ' + after.get('awakening_level', 'N/A') if target_achieved else '未能提升'}
2. 觉醒评分: {score_change:+.3f} ({'改善' if score_change > 0 else '下降'})
3. 智慧种子比例: {after.get('wisdom_ratio', 0):.1%} ({'达标' if after.get('wisdom_ratio', 0) > 0.1 else '偏低'})
4. 质量门控: 染污种子数 {after.get('contaminated_seeds', 0)} vs {before.get('contaminated_seeds', 0)}

【关键发现】
- 优化后智慧种子比例为 {after.get('wisdom_ratio', 0):.1%}
- 优化后高质量种子比例为 {after.get('high_quality_ratio', 0):.1%}
- 觉醒评分公式: wisdom_ratio × 0.5 + high_quality_ratio × 0.3 + avg_purity × 0.2

【目标达成】
{'✅ 稳定在"初始境"或更高层级' if target_achieved else '❌ 未达到"初始境"目标'}

实验完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}
"""
        
        return report


def main():
    """主函数"""
    print("\n" + "="*70)
    print("           唯识进化Agent - 质量优先进化策略优化实验")
    print("="*70 + "\n")
    
    experiment = QualityFirstExperiment()
    results = experiment.run_experiment(num_interactions=100)
    
    # 打印报告
    print(results["report"])
    
    # 保存报告
    report_path = "./项目/唯识进化Agent/experiments/results/quality_first_experiment.txt"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(results["report"])
    
    print(f"\n报告已保存到: {report_path}")
    
    return results


if __name__ == "__main__":
    main()
