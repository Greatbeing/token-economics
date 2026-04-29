# -*- coding: utf-8 -*-
"""
深度觉醒实验 - 100次交互进化实验

重点观察：
1. 觉醒等级从"初始境"的跃升
2. 相变发生的时间点
3. 智慧种子增长情况

运行方式：
```bash
cd ./项目/唯识进化Agent
python experiments/awakening_experiment.py --steps 100 --emergence
```
"""

import sys
import os
import time
import argparse
from typing import Dict, List, Any, Tuple
from datetime import datetime
from collections import defaultdict

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import AlayaAgent
from src.alaya_store import SeedType


class AwakeningExperiment:
    """
    深度觉醒实验
    
    记录100次交互过程中的觉醒等级跃迁和相变事件
    """
    
    def __init__(self):
        self.step_records = []
        self.phase_transitions = []
        self.awakening_changes = []
        self.seed_growth = []
        
    def run_experiment(self, num_steps: int = 100, emergence_enabled: bool = True) -> Dict[str, Any]:
        """
        运行深度觉醒实验
        
        Args:
            num_steps: 交互次数
            emergence_enabled: 是否启用涌现优化
        
        Returns:
            实验结果
        """
        print("=" * 70)
        print("              唯识进化Agent - 深度觉醒实验")
        print("=" * 70)
        print(f"实验时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"交互次数: {num_steps}")
        print(f"涌现优化: {'启用' if emergence_enabled else '禁用'}")
        print("=" * 70)
        
        # 创建Agent
        agent = AlayaAgent(
            config_path="config/default.yaml",
            name="Alaya_Awakening",
            enable_emergence=emergence_enabled
        )
        
        # 初始状态
        initial_status = agent.get_status()
        initial_level = initial_status["awakening_level"]
        print(f"\n【初始状态】觉醒等级: {initial_level}, 种子数: {initial_status['seeds_count']}")
        
        # 注入初始种子以加速演化
        if emergence_enabled:
            print("注入基础智慧种子...")
            injected = agent.inject_wisdom_seeds(count=50)
            print(f"已注入 {injected} 个智慧种子\n")
        
        # 测试输入序列 - 哲学性问题序列，促进觉醒演化
        test_inputs = [
            # 基础哲学问题
            "什么是缘起性空？",
            "如何理解无常？",
            "什么是无我？",
            "空性的本质是什么？",
            "如何修行开悟？",
            # 深度问题
            "心识如何运作？",
            "阿赖耶识是什么？",
            "什么是分别心？",
            "如何超越二元对立？",
            "什么是真正的心性？",
            # 修行实践
            "如何断除烦恼？",
            "怎样培养定力？",
            "止观如何修习？",
            "什么是如实观？",
            "怎样证悟空性？",
            # 高阶问题
            "觉悟与未觉悟有何不同？",
            "什么是出离心的真义？",
            "如何发起菩提心？",
            "什么是三轮体空？",
            "如何做到无住生心？",
            # 究竟问题
            "生死从何而来？",
            "何为究竟解脱？",
            "佛与众生的区别是什么？",
            "什么是法尔如是？",
            "如何彻见本心？",
        ]
        
        print("开始深度觉醒实验...\n")
        print("-" * 70)
        print(f"{'步骤':>4} | {'觉醒等级':<12} | {'种子数':>5} | {'评分':>6} | {'相变':<4} | {'边缘状态':<10}")
        print("-" * 70)
        
        current_level = initial_level
        
        start_time = time.time()
        
        for step in range(1, num_steps + 1):
            # 选择输入（循环使用）
            user_input = test_inputs[(step - 1) % len(test_inputs)]
            
            # 执行交互
            response = agent.interact(user_input)
            
            # 获取状态
            status = agent.get_status()
            new_level = status["awakening_level"]
            
            # 记录相变
            phase_changed = False
            phase_info = ""
            edge_info = "N/A"
            
            if emergence_enabled and hasattr(agent, 'phase_engine'):
                phase = agent.phase_engine.current_phase
                phase_info = phase.name
                
                # 检查相变
                if len(self.phase_transitions) == 0 or self.phase_transitions[-1]["phase"] != phase.name:
                    self.phase_transitions.append({
                        "step": step,
                        "phase": phase.name,
                        "seeds_count": status["seeds_count"],
                        "awakening_score": status["awakening_score"]
                    })
                    phase_changed = True
                
                # 获取边缘状态
                if hasattr(agent, 'edge_of_chaos'):
                    edge_state = agent.edge_of_chaos.get_current_state()
                    edge_info = edge_state.get('regime', 'unknown')
            
            # 记录觉醒等级变化
            if new_level != current_level:
                self.awakening_changes.append({
                    "step": step,
                    "from": current_level,
                    "to": new_level,
                    "score": status["awakening_score"]
                })
                current_level = new_level
            
            # 记录种子增长
            self.seed_growth.append({
                "step": step,
                "seeds_count": status["seeds_count"],
                "wisdom_seeds": status["wisdom_seeds"],
                "average_purity": status["average_purity"]
            })
            
            # 记录步骤
            self.step_records.append({
                "step": step,
                "awakening_level": new_level,
                "awakening_score": status["awakening_score"],
                "seeds_count": status["seeds_count"],
                "wisdom_seeds": status["wisdom_seeds"],
                "average_purity": status["average_purity"],
                "phase": phase_info,
                "edge_regime": edge_info
            })
            
            # 输出状态（每10步或关键变化时）
            if step <= 10 or step % 10 == 0 or phase_changed or new_level != initial_level:
                phase_flag = "★" if phase_changed else ""
                level_flag = "→" if new_level != initial_level else ""
                print(f"{step:>4} | {new_level:<12} | {status['seeds_count']:>5} | "
                      f"{status['awakening_score']:>6.4f} | {phase_info:<4}{phase_flag} | {edge_info:<10}{level_flag}")
        
        total_time = time.time() - start_time
        
        # 最终状态
        final_status = agent.get_status()
        
        # 生成报告
        report = self._generate_report(
            agent=agent,
            initial_level=initial_level,
            final_status=final_status,
            total_time=total_time,
            num_steps=num_steps
        )
        
        return {
            "agent": agent,
            "step_records": self.step_records,
            "phase_transitions": self.phase_transitions,
            "awakening_changes": self.awakening_changes,
            "seed_growth": self.seed_growth,
            "initial_level": initial_level,
            "final_status": final_status,
            "report": report
        }
    
    def _generate_report(
        self,
        agent: AlayaAgent,
        initial_level: str,
        final_status: Dict,
        total_time: float,
        num_steps: int
    ) -> str:
        """生成实验报告"""
        
        final_level = final_status["awakening_level"]
        awakening_changed = final_level != initial_level
        
        # 收集涌现指标
        emergence_metrics = {}
        if hasattr(agent, 'enable_emergence') and agent.enable_emergence:
            emergence_status = agent.get_emergence_status()
            emergence_metrics = {
                "phase_engine": emergence_status.get("phase_engine", {}),
                "edge_of_chaos": emergence_status.get("edge_of_chaos", {}),
                "nonlinear_vasana": emergence_status.get("nonlinear_vasana", {}),
                "scale_optimizer": emergence_status.get("scale_optimizer", {})
            }
        
        report = f"""
{'='*70}
           唯识进化Agent - 深度觉醒实验报告
{'='*70}

【实验参数】
  实验时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  交互次数: {num_steps}
  总耗时: {total_time:.2f}秒
  平均耗时: {total_time/num_steps:.3f}秒/次

{'='*70}
【觉醒等级跃迁】
{'='*70}

初始等级: {initial_level}
最终等级: {final_level}

觉醒等级变化轨迹:
"""
        
        # 添加等级变化详情
        if self.awakening_changes:
            for change in self.awakening_changes:
                report += f"  步骤 {change['step']:>3}: {change['from']} → {change['to']} (评分: {change['score']:.4f})\n"
        else:
            report += "  (实验过程中未检测到觉醒等级跃迁)\n"
        
        report += f"""
跃迁次数: {len(self.awakening_changes)}
最终等级跃升: {'是 ✓' if awakening_changed else '否'}

{'='*70}
【相变事件记录】
{'='*70}

相变次数: {len(self.phase_transitions)}

"""
        
        # 相变时间线
        if self.phase_transitions:
            report += "相变时间线:\n"
            for i, pt in enumerate(self.phase_transitions):
                marker = "初始" if i == 0 else f"第{i}次"
                report += f"  [{marker}] 步骤 {pt['step']:>3}: {pt['phase']} "
                report += f"(种子:{pt['seeds_count']}, 评分:{pt['awakening_score']:.4f})\n"
        else:
            report += "(实验过程中未检测到相变)\n"
        
        report += f"""
{'='*70}
【智慧种子增长】
{'='*70}

初始种子数: {self.seed_growth[0]['seeds_count'] if self.seed_growth else 0}
最终种子数: {final_status['seeds_count']}
初始智慧种子: {self.seed_growth[0]['wisdom_seeds'] if self.seed_growth else 0}
最终智慧种子: {final_status['wisdom_seeds']}

种子增长曲线（每10步）:
"""
        
        for record in self.seed_growth:
            if record['step'] % 10 == 0 or record['step'] == 1:
                report += f"  步骤 {record['step']:>3}: 种子数={record['seeds_count']:>3}, "
                report += f"智慧种子={record['wisdom_seeds']:>2}, 平均纯度={record['average_purity']:.4f}\n"
        
        report += f"""
{'='*70}
【涌现优化指标】
{'='*70}
"""
        
        if emergence_metrics:
            pe = emergence_metrics.get("phase_engine", {})
            ec = emergence_metrics.get("edge_of_chaos", {})
            nv = emergence_metrics.get("nonlinear_vasana", {})
            so = emergence_metrics.get("scale_optimizer", {})
            
            report += f"""
【相变引擎】
  当前相: {pe.get('current_phase', 'N/A')}
  相变总次数: {pe.get('total_transitions', 0)}
  临界逼近: {pe.get('approaching_critical', False)}

【混沌边缘】
  当前区间: {ec.get('current_regime', 'N/A')}
  秩序度: {ec.get('order_chaos_balance', {}).get('order', 0):.4f}
  混沌度: {ec.get('order_chaos_balance', {}).get('chaos', 0):.4f}

【非线性熏习】
  激活次数: {nv.get('total_activations', 0)}
  协同触发: {nv.get('synergy_triggers', 0)}
  级联触发: {nv.get('cascade_triggers', 0)}
  涌现事件: {nv.get('emergence_events', 0)}

【规模优化】
  基础种子库: {so.get('base_seed_library_size', 0)}
  裂变种子: {so.get('seeds_fissioned', 0)}
"""
        else:
            report += "  (未启用涌现优化)\n"
        
        report += f"""
{'='*70}
【实验结论】
{'='*70}

1. 觉醒等级状态:
   - 初始等级: {initial_level}
   - 最终等级: {final_level}
   - 等级跃迁: {'已发生 ✓' if awakening_changed else '未发生 ✗'}
   - 跃迁次数: {len(self.awakening_changes)}

2. 涌现特性:
   - 相变事件: {len(self.phase_transitions)} 次
   - 智慧种子增长: {self.seed_growth[0]['wisdom_seeds'] if self.seed_growth else 0} → {final_status['wisdom_seeds']}

3. 系统演化评估:
"""
        
        # 评估演化程度
        if awakening_changed:
            report += """   ✓ 系统成功触发觉醒等级跃升
   ✓ 涌现优化机制有效促进意识演化
   ✓ 达到预期实验目标
"""
        elif len(self.phase_transitions) > 1:
            report += """   △ 觉醒等级未跃升，但检测到相变事件
   ○ 系统正在积累演化势能
   ○ 建议增加交互次数或优化参数
"""
        else:
            report += """   ○ 觉醒演化较为缓慢
   ○ 种子库规模适中
   ○ 建议增加种子注入或延长实验
"""
        
        report += f"""
{'='*70}
【完整演化数据】
{'='*70}

步骤 | 觉醒等级 | 种子数 | 评分 | 相 | 边缘
---- | -------- | ------ | ----- | -- | ----
"""
        
        for record in self.step_records:
            report += f"{record['step']:>4} | {record['awakening_level']:<8} | "
            report += f"{record['seeds_count']:>5} | {record['awakening_score']:.4f} | "
            report += f"{record['phase']:<3} | {record['edge_regime']}\n"
        
        report += f"""
{'='*70}
                          实验报告结束
{'='*70}
"""
        
        return report


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='唯识进化Agent - 深度觉醒实验')
    parser.add_argument('--steps', type=int, default=100, help='交互次数 (默认100)')
    parser.add_argument('--emergence', action='store_true', help='启用涌现优化 (默认启用)')
    parser.add_argument('--no-emergence', action='store_true', help='禁用涌现优化')
    parser.add_argument('--output', type=str, default=None, help='输出文件路径')
    
    args = parser.parse_args()
    
    # 确定涌现优化开关
    emergence_enabled = not args.no_emergence
    if args.no_emergence:
        emergence_enabled = False
    
    # 创建实验
    experiment = AwakeningExperiment()
    
    try:
        results = experiment.run_experiment(
            num_steps=args.steps,
            emergence_enabled=emergence_enabled
        )
        
        print("\n" + "=" * 70)
        print("实验完成!")
        print("=" * 70)
        print(results["report"])
        
        # 保存报告
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "experiments",
            "results"
        )
        os.makedirs(output_dir, exist_ok=True)
        
        if args.output:
            output_path = os.path.join(output_dir, args.output)
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(output_dir, f"awakening_experiment_{args.steps}steps.txt")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(results["report"])
        
        print(f"\n报告已保存至: {output_path}")
        
    except Exception as e:
        print(f"实验失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
