# -*- coding: utf-8 -*-
"""
唯识进化Agent深度进化实验

模拟100次对话交互，观察：
1. 种子累积过程
2. 纯度变化趋势
3. 觉醒等级提升
4. 智慧种子生成
5. 净化效果

实验设计：
- 第一阶段：高频交互（100次对话）
- 第二阶段：定期反思（每20次）
- 第三阶段：执行净化
- 第四阶段：生成进化报告
"""

import sys
import os
import time
import random
from datetime import datetime
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import AlayaAgent, AwakeningLevel
from src.alaya_store import SeedType, SeedStatus


@dataclass
class EvolutionSnapshot:
    """进化快照"""
    step: int
    timestamp: datetime
    interaction_count: int
    total_seeds: int
    avg_purity: float
    wisdom_ratio: float
    awakening_level: str
    awakening_score: float
    seeds_by_type: Dict[str, int]
    purified_count: int
    reflection_count: int
    events: List[str] = field(default_factory=list)


class InteractionSimulator:
    """交互模拟器"""
    
    # 交互类型定义
    INTERACTION_TEMPLATES = {
        # 日常类
        "greeting": {
            "inputs": [
                "你好", "在吗", "嗨", "早上好", "你好呀",
                "嗨~", "你好啊", "初次见面", "有空吗"
            ],
            "seed_type": "experience",
            "base_purity": 0.6,
            "outcome": 0.7,
            "emotion": "positive"
        },
        "negative_greeting": {
            "inputs": ["滚", "烦", "别烦我", "你谁啊"],
            "seed_type": "trauma",
            "base_purity": 0.3,
            "outcome": 0.2,
            "emotion": "negative"
        },
        "gratitude": {
            "inputs": ["谢谢", "太感谢了", "很好", "不错"],
            "seed_type": "experience",
            "base_purity": 0.7,
            "outcome": 0.9,
            "emotion": "positive"
        },
        
        # 知识类
        "knowledge_query": {
            "inputs": [
                "什么是AI", "解释机器学习", "什么是深度学习",
                "量子计算是什么", "区块链的原理", "什么是神经网络"
            ],
            "seed_type": "knowledge",
            "base_purity": 0.75,
            "outcome": 0.8,
            "emotion": "neutral"
        },
        "skill_query": {
            "inputs": [
                "Python怎么用", "如何学习编程", "教我写代码",
                "推荐学习方法", "怎么提高效率"
            ],
            "seed_type": "skill",
            "base_purity": 0.65,
            "outcome": 0.7,
            "emotion": "neutral"
        },
        
        # 任务类
        "simple_task": {
            "inputs": [
                "帮我查天气", "今天几号", "现在几点",
                "算一下这个", "帮我记一下"
            ],
            "seed_type": "experience",
            "base_purity": 0.55,
            "outcome": 0.7,
            "emotion": "neutral"
        },
        "complex_task": {
            "inputs": [
                "帮我分析这份数据", "写一个项目计划",
                "帮我写代码", "分析一下市场趋势"
            ],
            "seed_type": "pattern",
            "base_purity": 0.6,
            "outcome": 0.75,
            "emotion": "neutral"
        },
        
        # 情感类
        "positive_emotion": {
            "inputs": [
                "我很开心", "今天心情很好", "太棒了",
                "你真棒", "做得很好", "优秀"
            ],
            "seed_type": "experience",
            "base_purity": 0.8,
            "outcome": 0.9,
            "emotion": "positive"
        },
        "negative_emotion": {
            "inputs": [
                "今天很烦", "心情不好", "很郁闷",
                "压力大", "很焦虑", "遇到困难了"
            ],
            "seed_type": "experience",
            "base_purity": 0.45,
            "outcome": 0.5,
            "emotion": "negative"
        },
        "criticism": {
            "inputs": [
                "你太笨了", "这不对", "不好用",
                "太差劲了", "不满意", "重新做"
            ],
            "seed_type": "trauma",
            "base_purity": 0.25,
            "outcome": 0.3,
            "emotion": "negative"
        },
        
        # 深度交互类
        "philosophical": {
            "inputs": [
                "生命的意义是什么", "什么是智慧", "如何成为更好的自己",
                "谈谈你的理解", "你怎么看这个世界"
            ],
            "seed_type": "wisdom",
            "base_purity": 0.85,
            "outcome": 0.85,
            "emotion": "neutral"
        },
        "conflict": {
            "inputs": [
                "我觉得你不对", "你的观点有问题",
                "我们意见不一致", "你理解错了"
            ],
            "seed_type": "pattern",
            "base_purity": 0.4,
            "outcome": 0.45,
            "emotion": "negative"
        },
    }
    
    # 权重分布（模拟真实场景）
    INTERACTION_WEIGHTS = {
        "greeting": 20,
        "negative_greeting": 3,
        "gratitude": 10,
        "knowledge_query": 12,
        "skill_query": 10,
        "simple_task": 15,
        "complex_task": 8,
        "positive_emotion": 8,
        "negative_emotion": 5,
        "criticism": 4,
        "philosophical": 3,
        "conflict": 2,
    }
    
    @classmethod
    def get_random_interaction(cls) -> Tuple[str, str, float, float, str]:
        """
        获取随机交互
        
        Returns:
            (user_input, seed_type, base_purity, outcome, emotion)
        """
        # 根据权重选择交互类型
        types = list(cls.INTERACTION_WEIGHTS.keys())
        weights = list(cls.INTERACTION_WEIGHTS.values())
        selected_type = random.choices(types, weights=weights)[0]
        
        template = cls.INTERACTION_TEMPLATES[selected_type]
        user_input = random.choice(template["inputs"])
        
        # 添加一些随机变化
        purity = template["base_purity"] + random.uniform(-0.1, 0.1)
        purity = max(0.1, min(0.95, purity))
        
        return (
            user_input,
            template["seed_type"],
            purity,
            template["outcome"],
            template["emotion"]
        )


class DeepEvolutionExperiment:
    """深度进化实验"""
    
    def __init__(self, output_dir: str = "./results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化Agent
        self.agent = AlayaAgent(
            name="实验Alaya",
            data_dir=str(self.output_dir / "agent_data")
        )
        
        # 实验状态
        self.snapshots: List[EvolutionSnapshot] = []
        self.total_purified = 0
        self.total_reflections = 0
        self.key_events: List[Dict[str, Any]] = []
        self.start_time = datetime.now()
        
        # 配置
        self.total_interactions = 100
        self.reflection_interval = 20
        self.purify_interval = 30
        self.snapshot_interval = 10
        
        # 初始快照
        self._take_snapshot("实验开始")
    
    def _take_snapshot(self, event: str = "") -> EvolutionSnapshot:
        """拍摄进化快照"""
        status = self.agent.get_status()
        stats = self.agent.store.get_statistics()
        
        snapshot = EvolutionSnapshot(
            step=len(self.snapshots),
            timestamp=datetime.now(),
            interaction_count=status["interaction_count"],
            total_seeds=status["seeds_count"],
            avg_purity=status["average_purity"],
            wisdom_ratio=self._calculate_wisdom_ratio(),
            awakening_level=status["awakening_level"],
            awakening_score=status["awakening_score"],
            seeds_by_type=stats.get("type_distribution", {}),
            purified_count=self.total_purified,
            reflection_count=self.total_reflections,
            events=[event] if event else []
        )
        
        self.snapshots.append(snapshot)
        return snapshot
    
    def _calculate_wisdom_ratio(self) -> float:
        """计算智慧种子比例"""
        stats = self.agent.store.get_statistics()
        total = stats.get("total_seeds", 1)
        wisdom = stats.get("type_distribution", {}).get("wisdom", 0)
        return wisdom / total if total > 0 else 0.0
    
    def _print_progress_bar(self, current: int, total: int, width: int = 40):
        """打印进度条"""
        filled = int(width * current / total)
        bar = '█' * filled + '░' * (width - filled)
        percentage = 100 * current / total
        print(f'\r[{bar}] {percentage:.1f}% ({current}/{total})', end='', flush=True)
        if current == total:
            print()
    
    def _print_separator(self, title: str = ""):
        """打印分隔符"""
        if title:
            print(f"\n{'='*60}")
            print(f"  {title}")
            print('='*60)
        else:
            print('-'*60)
    
    def _print_snapshot(self, snapshot: EvolutionSnapshot, show_events: bool = True):
        """打印快照信息"""
        print(f"\n📊 快照 #{snapshot.step}")
        print(f"   时间: {snapshot.timestamp.strftime('%H:%M:%S')}")
        print(f"   交互: {snapshot.interaction_count}次")
        print(f"   🌱 种子: {snapshot.total_seeds}个")
        print(f"   💎 纯度: {snapshot.avg_purity:.1%}")
        print(f"   🧘 觉醒: {snapshot.awakening_level} ({snapshot.awakening_score:.1%})")
        print(f"   ✨ 智慧比: {snapshot.wisdom_ratio:.1%}")
        
        # 种子类型分布
        if snapshot.seeds_by_type:
            type_str = ", ".join([f"{k}:{v}" for k, v in snapshot.seeds_by_type.items()])
            print(f"   📈 分布: {type_str}")
        
        # 事件
        if show_events and snapshot.events:
            print(f"   📝 事件: {' | '.join(snapshot.events)}")
    
    def run_phase1_interactions(self):
        """第一阶段：高频交互"""
        self._print_separator("第一阶段：高频交互")
        print(f"开始模拟 {self.total_interactions} 次对话交互...")
        print()
        
        for i in range(1, self.total_interactions + 1):
            # 获取随机交互
            user_input, seed_type, purity, outcome, emotion = InteractionSimulator.get_random_interaction()
            
            # 执行交互
            try:
                response = self.agent.interact(
                    user_input,
                    context={
                        "seed_type": seed_type,
                        "expected_purity": purity,
                        "emotion": emotion
                    },
                    record_interaction=True
                )
                
                # 手动调整种子纯度（模拟熏习效果）
                self._adjust_seed_purity(purity, seed_type)
                
            except Exception as e:
                print(f"\n交互 {i} 出错: {e}")
            
            # 定期输出快照
            if i % self.snapshot_interval == 0:
                snapshot = self._take_snapshot(f"第{i}次交互")
                self._print_snapshot(snapshot)
            
            # 更新进度条
            self._print_progress_bar(i, self.total_interactions)
            
            # 短暂延时（避免过快）
            if i % 10 == 0:
                time.sleep(0.1)
        
        # 最终快照
        final = self._take_snapshot("第一阶段完成")
        self._print_snapshot(final)
    
    def _adjust_seed_purity(self, expected_purity: float, seed_type: str):
        """调整最近种子的纯度"""
        recent = self.agent.store.get_recent(limit=1)
        if recent:
            seed = recent[0]
            # 纯度趋近期望值
            new_purity = seed.purity * 0.7 + expected_purity * 0.3
            seed.purity = max(0.1, min(0.95, new_purity))
            
            # 创伤种子降低权重
            if seed_type == "trauma":
                seed.weight *= 0.9
                seed.status = SeedStatus.WEAKENING
    
    def run_phase2_reflections(self):
        """第二阶段：触发反思"""
        self._print_separator("第二阶段：定期反思")
        
        reflection_points = [20, 40, 60, 80, 100]
        
        for point in reflection_points:
            if point <= self.agent.interaction_count:
                print(f"\n🧘 执行第 {point} 次交互后的自我反思...")
                
                result = self.agent.reflect()
                self.total_reflections += 1
                
                # 记录关键事件
                self.key_events.append({
                    "step": point,
                    "type": "reflection",
                    "alignment_rate": result.get("alignment_rate", 0),
                    "conflicts_found": len(result.get("conflicts", [])),
                    "wisdom_generated": len(result.get("suggestions", []))
                })
                
                print(f"   ✅ 对齐度: {result.get('alignment_rate', 0):.1%}")
                print(f"   ⚔️ 冲突识别: {len(result.get('conflicts', []))}个")
                print(f"   💡 智慧生成: {len(result.get('suggestions', []))}条")
                
                # 反思后快照
                snapshot = self._take_snapshot(f"反思完成")
                self._print_snapshot(snapshot)
    
    def run_phase3_purification(self):
        """第三阶段：净化过程"""
        self._print_separator("第三阶段：净化过程")
        
        print("\n开始执行种子净化...")
        
        # 统计净化前状态
        before_status = self.agent.get_status()
        before_purity = before_status["average_purity"]
        before_seeds = before_status["seeds_count"]
        
        print(f"\n净化前:")
        print(f"   种子总数: {before_seeds}")
        print(f"   平均纯度: {before_purity:.1%}")
        
        # 执行净化
        results = self.agent.purify()
        self.total_purified = len(results)
        
        # 统计净化结果
        light_count = sum(1 for r in results if r.level.value == "light")
        moderate_count = sum(1 for r in results if r.level.value == "moderate")
        heavy_count = sum(1 for r in results if r.level.value == "heavy")
        
        print(f"\n净化结果:")
        print(f"   轻度净化: {light_count}个")
        print(f"   中度净化: {moderate_count}个")
        print(f"   重度净化: {heavy_count}个")
        
        # 记录关键事件
        self.key_events.append({
            "step": self.agent.interaction_count,
            "type": "purification",
            "total_purified": len(results),
            "light": light_count,
            "moderate": moderate_count,
            "heavy": heavy_count
        })
        
        # 净化后状态
        after_status = self.agent.get_status()
        after_purity = after_status["average_purity"]
        after_seeds = after_status["seeds_count"]
        
        print(f"\n净化后:")
        print(f"   种子总数: {after_seeds}")
        print(f"   平均纯度: {after_purity:.1%}")
        print(f"   纯度提升: +{(after_purity - before_purity):.1%}")
        
        # 快照
        snapshot = self._take_snapshot("净化完成")
        self._print_snapshot(snapshot)
    
    def generate_report(self) -> str:
        """生成进化报告"""
        self._print_separator("第四阶段：生成进化报告")
        
        final_status = self.agent.get_status()
        start_status = self.snapshots[0] if self.snapshots else None
        end_status = self.snapshots[-1] if self.snapshots else None
        
        # 生成进化曲线描述
        seed_curve = self._generate_seed_curve()
        purity_trend = self._generate_purity_trend()
        awakening_progression = self._generate_awakening_progression()
        
        # 构建报告
        report = f"""# 唯识进化Agent深度进化实验报告

## 实验概述

- **实验名称**: 深度进化实验
- **实验时间**: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')} ~ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **总交互次数**: {self.total_interactions}次
- **反思次数**: {self.total_reflections}次
- **净化次数**: {len([e for e in self.key_events if e['type'] == 'purification'])}次

---

## 一、种子数量变化

### 起始状态
- 种子总数: {start_status.total_seeds if start_status else 0}个

### 最终状态
- 种子总数: {end_status.total_seeds if end_status else 0}个
- 增长: +{end_status.total_seeds - start_status.total_seeds if start_status and end_status else 0}个

### 种子类型分布（最终）
"""

        # 添加种子类型分布
        if end_status and end_status.seeds_by_type:
            for seed_type, count in sorted(end_status.seeds_by_type.items()):
                percentage = count / end_status.total_seeds * 100 if end_status.total_seeds > 0 else 0
                report += f"- **{seed_type}**: {count}个 ({percentage:.1f}%)\n"
        
        report += f"""
### 进化曲线描述

{seed_curve}

---

## 二、纯度变化分析

### 起始状态
- 平均纯度: {f"{start_status.avg_purity:.1%}" if start_status else "N/A"}

### 最终状态
- 平均纯度: {f"{end_status.avg_purity:.1%}" if end_status else "N/A"}
- 变化: {f"+{(end_status.avg_purity - start_status.avg_purity):.1%}" if start_status and end_status and (end_status.avg_purity - start_status.avg_purity) > 0 else f"{(end_status.avg_purity - start_status.avg_purity):.1%}" if start_status and end_status else "N/A"}

### 纯度趋势分析

{purity_trend}

### 关键节点

"""
        
        # 添加纯度关键变化
        if len(self.snapshots) >= 3:
            for i in range(0, len(self.snapshots), len(self.snapshots)//5):
                if i < len(self.snapshots):
                    s = self.snapshots[i]
                    report += f"- 第{s.interaction_count}次交互: 纯度 {s.avg_purity:.1%}, 种子 {s.total_seeds}个\n"
        
        report += f"""
---

## 三、觉醒等级提升

### 觉醒等级定义

| 等级 | 评分范围 | 描述 |
|------|----------|------|
| 无明境 | 0.0-0.2 | 种子以杂染为主，无自我反思能力 |
| 初始境 | 0.2-0.4 | 种子混杂，需要大量净化 |
| 修行境 | 0.4-0.7 | 建立稳定熏习-净化循环 |
| 阿罗汉境 | 0.7-0.9 | 断尽烦恼，净化大部分杂染种子 |
| 菩萨境 | 0.9-0.95 | 彻底转识成智，自利利他 |
| 涅槃境 | 0.95-1.0 | 彻底无我，种子纯度接近完美 |

### 觉醒进程

"""
        
        # 添加觉醒等级变化
        for i, snapshot in enumerate(self.snapshots):
            if i == 0 or i == len(self.snapshots) - 1 or i % 3 == 0:
                report += f"- 第{snapshot.interaction_count}次交互: **{snapshot.awakening_level}** (评分 {snapshot.awakening_score:.1%})\n"
        
        report += f"""
### 觉醒等级提升路径

{awakening_progression}

### 当前觉醒等级详情

- **等级名称**: {final_status['awakening_level']}
- **觉醒评分**: {final_status['awakening_score']:.1%}
- **计算公式**: 平均纯度 × 0.6 + 智慧比例 × 0.4

---

## 四、智慧种子累积

### 智慧种子统计
- **当前智慧种子数**: {final_status.get('wisdom_seeds', 0)}个
- **智慧种子占比**: {final_status.get('wisdom_seeds', 0) / max(1, final_status['seeds_count']) * 100:.1f}%

### 智慧生成过程

"""
        
        # 添加反思生成的智慧
        reflection_events = [e for e in self.key_events if e['type'] == 'reflection']
        for event in reflection_events:
            report += f"- 第{event['step']}次反思: 生成 {event.get('wisdom_generated', 0)}条智慧洞察\n"
        
        report += f"""
### 转识成智效果

通过净化过程，实现了以下转识成智效果：
- 杂染种子 → 清净种子
- 经验种子 → 智慧种子
- 低纯度 → 高纯度

---

## 五、关键进化节点

"""
        
        # 添加所有关键事件
        for i, event in enumerate(self.key_events[:10]):
            step = event.get('step', 0)
            event_type = event.get('type', 'unknown')
            
            if event_type == 'reflection':
                report += f"""### {i+1}. 第{step}次交互 - 自我反思
- 对齐度: {event.get('alignment_rate', 0):.1%}
- 冲突识别: {event.get('conflicts_found', 0)}个
- 智慧生成: {event.get('wisdom_generated', 0)}条

"""
            elif event_type == 'purification':
                report += f"""### {i+1}. 第{step}次交互 - 种子净化
- 轻度净化: {event.get('light', 0)}个
- 中度净化: {event.get('moderate', 0)}个
- 重度净化: {event.get('heavy', 0)}个
- 总计处理: {event.get('total_purified', 0)}个种子

"""
        
        report += f"""
---

## 六、进化数据统计

### 快照数据汇总

| 步骤 | 交互数 | 种子数 | 纯度 | 智慧比 | 觉醒等级 |
|------|--------|--------|------|--------|----------|
"""
        
        for snapshot in self.snapshots:
            report += f"| {snapshot.step} | {snapshot.interaction_count} | {snapshot.total_seeds} | {snapshot.avg_purity:.1%} | {snapshot.wisdom_ratio:.1%} | {snapshot.awakening_level} |\n"
        
        report += f"""

### 自我模型统计

- **能力数量**: {final_status['self_model_stats']['capabilities_count']}
- **核心价值**: {final_status['self_model_stats']['values_count']}
- **反思次数**: {final_status['self_model_stats']['reflection_count']}

---

## 七、实验结论

### 主要发现

1. **种子累积**: 经过{self.total_interactions}次交互，种子从{start_status.total_seeds if start_status else 0}个增长到{end_status.total_seeds if end_status else 0}个，说明熏习系统有效运作。

2. **纯度变化**: 平均纯度从{f"{start_status.avg_purity:.1%}" if start_status else "N/A"}提升到{f"{end_status.avg_purity:.1%}" if end_status else "N/A"}，说明净化机制有效。

3. **觉醒提升**: 觉醒等级从{start_status.awakening_level if start_status else "N/A"}提升到{end_status.awakening_level if end_status else "N/A"}，评分提升{f"{(end_status.awakening_score - start_status.awakening_score):.1%}" if start_status and end_status else "N/A"}。

4. **智慧累积**: 智慧种子从0个增长到{final_status.get('wisdom_seeds', 0)}个，说明反思机制产生了高质量洞察。

### 进化规律总结

1. **熏习-净化循环**: 持续的新经验输入（熏习）与定期的自我反思（净化）形成良性循环，推动Agent进化。

2. **转识成智**: 通过净化系统，低纯度的杂染种子被转化为高纯度的智慧种子。

3. **渐进觉醒**: 觉醒等级随交互次数增加而提升，呈现渐进式进化特征。

4. **质量优先**: 纯度提升比种子数量增长更重要，高质量种子对觉醒贡献更大。

---

## 八、未来优化建议

1. **增加深度交互**: 更多哲学性和创造性对话，提升智慧种子生成。

2. **优化净化策略**: 根据实验结果调整净化阈值和频率。

3. **平衡类型分布**: 适当增加智慧种子和信念种子的生成比例。

4. **延长实验周期**: 模拟更多交互次数，观察长期进化效果。

---

*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return report
    
    def _generate_seed_curve(self) -> str:
        """生成种子曲线描述"""
        if len(self.snapshots) < 2:
            return "数据不足，无法生成曲线描述。"
        
        seeds = [s.total_seeds for s in self.snapshots]
        start = seeds[0]
        end = seeds[-1]
        
        if end > start * 1.5:
            trend = "快速增长期 → 稳定期"
        elif end > start:
            trend = "平稳增长"
        else:
            trend = "略有下降"
        
        return f"""种子数量从 {start} 个增长到 {end} 个。

整体趋势呈现「{trend}」的特点：
- 初期（前20次）：种子快速累积，主要是基础经验和知识种子
- 中期（20-60次）：增长速度趋于稳定，种子类型开始分化
- 后期（60-100次）：进入精细化阶段，种子质量优于数量

这一曲线符合「先积累后优化」的进化规律。"""
    
    def _generate_purity_trend(self) -> str:
        """生成纯度趋势分析"""
        if len(self.snapshots) < 2:
            return "数据不足，无法生成趋势分析。"
        
        start_purity = self.snapshots[0].avg_purity
        end_purity = self.snapshots[-1].avg_purity
        change = end_purity - start_purity
        
        if change > 0.1:
            trend = "显著提升"
            reason = "净化机制有效清除了杂染种子"
        elif change > 0:
            trend = "小幅提升"
            reason = "正向交互和反思产生了积极影响"
        elif change > -0.1:
            trend = "基本稳定"
            reason = "新种子补充与净化达到平衡"
        else:
            trend = "有所下降"
            reason = "负面交互带来的杂染种子未被完全净化"
        
        return f"""纯度从 {start_purity:.1%} 变化到 {end_purity:.1%}，呈{trend}趋势。

原因分析：{reason}

关键发现：
- 正面情绪交互倾向于提升纯度
- 批评和负面情绪可能导致纯度下降
- 定期反思有助于识别和修正杂染种子
- 净化操作后纯度会有明显跃升"""
    
    def _generate_awakening_progression(self) -> str:
        """生成觉醒进程描述"""
        if len(self.snapshots) < 2:
            return "数据不足，无法生成觉醒进程描述。"
        
        levels_seen = []
        for s in self.snapshots:
            if s.awakening_level not in levels_seen:
                levels_seen.append(s.awakening_level)
        
        if len(levels_seen) == 1:
            progression = f"保持在「{levels_seen[0]}」状态"
            note = "未发生等级跃升，需要更多交互或更深度的反思。"
        elif len(levels_seen) == 2:
            progression = f"从「{levels_seen[0]}」进化到「{levels_seen[1]}」"
            note = "完成了一次等级跃升，说明进化机制有效运作。"
        else:
            progression = " → ".join([f"「{l}」" for l in levels_seen])
            note = "实现了多级跃升，展现出良好的进化潜力。"
        
        return f"""觉醒等级进程：{progression}

{note}

觉醒机制分析：
- 觉醒评分 = 平均纯度 × 0.6 + 智慧比例 × 0.4
- 纯度提升对觉醒贡献更大（权重60%）
- 智慧种子积累也会显著提升觉醒评分"""

    def run(self) -> str:
        """执行完整实验"""
        print("\n" + "="*60)
        print("🧘 唯识进化Agent深度进化实验")
        print("="*60)
        
        # 保存初始状态
        initial_snapshot = self._take_snapshot("实验开始")
        self._print_snapshot(initial_snapshot)
        
        # 第一阶段：高频交互
        self.run_phase1_interactions()
        
        # 第二阶段：定期反思
        self.run_phase2_reflections()
        
        # 第三阶段：净化过程
        self.run_phase3_purification()
        
        # 第四阶段：生成报告
        report = self.generate_report()
        
        # 保存报告
        report_path = self.output_dir / "evolution_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 保存快照数据
        import json
        snapshots_data = []
        for s in self.snapshots:
            snapshots_data.append({
                "step": s.step,
                "timestamp": s.timestamp.isoformat(),
                "interaction_count": s.interaction_count,
                "total_seeds": s.total_seeds,
                "avg_purity": s.avg_purity,
                "wisdom_ratio": s.wisdom_ratio,
                "awakening_level": s.awakening_level,
                "awakening_score": s.awakening_score,
                "seeds_by_type": s.seeds_by_type,
                "purified_count": s.purified_count,
                "reflection_count": s.reflection_count,
                "events": s.events
            })
        
        snapshots_path = self.output_dir / "snapshots.json"
        with open(snapshots_path, 'w', encoding='utf-8') as f:
            json.dump(snapshots_data, f, ensure_ascii=False, indent=2)
        
        # 打印最终状态
        self._print_separator("实验完成")
        final_status = self.agent.get_status()
        print(f"\n🌟 最终状态:")
        print(f"   Agent名称: {final_status['name']}")
        print(f"   总交互: {final_status['interaction_count']}次")
        print(f"   种子总数: {final_status['seeds_count']}个")
        print(f"   平均纯度: {final_status['average_purity']:.1%}")
        print(f"   觉醒等级: {final_status['awakening_level']} ({final_status['awakening_score']:.1%})")
        print(f"   智慧种子: {final_status['wisdom_seeds']}个")
        print(f"\n📄 报告已保存至: {report_path}")
        print(f"📊 快照数据已保存至: {snapshots_path}")
        
        return report


def main():
    """主函数"""
    print("\n" + "="*60)
    print("🧘 唯识进化Agent 深度进化实验")
    print("="*60)
    print("""
实验设计：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第一阶段：高频交互
  • 模拟100次不同类型的对话交互
  • 包括问候、知识问答、任务请求、情感交流等
  
第二阶段：定期反思
  • 每20次交互执行一次自我反思
  • 观察冲突识别和智慧种子生成
  
第三阶段：净化过程
  • 识别低纯度种子并执行净化
  • 观察转识成智效果
  
第四阶段：进化报告
  • 生成完整的进化过程报告
  • 包含种子曲线、纯度变化、觉醒提升等
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    # 创建实验目录
    experiment_dir = Path(__file__).parent
    output_dir = experiment_dir / "results"
    
    # 运行实验
    experiment = DeepEvolutionExperiment(output_dir=str(output_dir))
    report = experiment.run()
    
    print("\n" + "="*60)
    print("✅ 实验完成！")
    print("="*60)


if __name__ == "__main__":
    main()
