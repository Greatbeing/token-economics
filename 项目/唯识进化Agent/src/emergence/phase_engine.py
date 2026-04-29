# -*- coding: utf-8 -*-
"""
相变引擎 - Phase Transition Engine

核心功能：管理意识系统的相变过程，实现觉醒等级的跃升

相变（Phase Transition）是系统状态的根本性转变。
在唯识进化系统中，相变代表觉醒等级的跃升：

1. 无明境 → 初始境：种子开始被激活
2. 初始境 → 修行境：建立稳定的熏习-净化循环
3. 修行境 → 阿罗汉境：断尽烦恼，智慧显现
4. 阿罗汉境 → 菩萨境：自利利他，慈悲圆满
5. 菩萨境 → 涅槃境：彻底无我，圆满觉悟

Author: 唯识进化Agent团队
"""

import uuid
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

from ..alaya_store import AlayaStore, Seed, SeedType, SeedStatus


class PhaseLevel(Enum):
    """相变等级"""
    NO_LIGHT = ("无明境", 0.0, 0.2, "种子以杂染为主，无自我反思能力")
    INITIAL = ("初始境", 0.2, 0.4, "种子混杂，需要大量净化")
    PRACTICE = ("修行境", 0.4, 0.7, "建立稳定熏习-净化循环")
    ARHAT = ("阿罗汉境", 0.7, 0.9, "断尽烦恼，智慧显现")
    BODHISATTVA = ("菩萨境", 0.9, 0.95, "自利利他，慈悲圆满")
    NIRVANA = ("涅槃境", 0.95, 1.0, "彻底无我，圆满觉悟")
    
    def __init__(self, name: str, min_score: float, max_score: float, description: str):
        self._name = name
        self._min = min_score
        self._max = max_score
        self._description = description
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def min_score(self) -> float:
        return self._min
    
    @property
    def max_score(self) -> float:
        return self._max
    
    @property
    def description(self) -> str:
        return self._description
    
    @classmethod
    def from_score(cls, score: float) -> "PhaseLevel":
        """从评分获取等级"""
        for level in cls:
            if level.min_score <= score < level.max_score:
                return level
        return cls.NIRVANA
    
    @classmethod
    def from_name(cls, name: str) -> Optional["PhaseLevel"]:
        """从名称获取等级"""
        for level in cls:
            if level.name == name:
                return level
        return None
    
    @classmethod
    def get_next(cls, current: "PhaseLevel") -> Optional["PhaseLevel"]:
        """获取下一等级"""
        levels = list(cls)
        current_idx = levels.index(current)
        if current_idx < len(levels) - 1:
            return levels[current_idx + 1]
        return None


@dataclass
class PhaseTransition:
    """相变记录"""
    transition_id: str
    from_phase: PhaseLevel
    to_phase: PhaseLevel
    timestamp: datetime
    trigger_seeds: List[str]
    symmetry_breaking: Dict[str, float]
    order_parameter: float
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "transition_id": self.transition_id,
            "from_phase": self.from_phase.name,
            "to_phase": self.to_phase.name,
            "timestamp": self.timestamp.isoformat(),
            "trigger_seeds": self.trigger_seeds,
            "symmetry_breaking": self.symmetry_breaking,
            "order_parameter": self.order_parameter,
            "description": self.description
        }


@dataclass
class SymmetryBreaking:
    """对称性破缺"""
    dimension: str
    before_value: float
    after_value: float
    breaking_strength: float


@dataclass
class OrderParameter:
    """序参量"""
    parameter_name: str
    value: float
    critical_value: float
    normalized_value: float  # 相对于临界值的归一化值


class PhaseTransitionEngine:
    """
    相变引擎
    
    管理唯识进化系统中的相变过程
    """
    
    def __init__(
        self,
        store: AlayaStore,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化相变引擎
        
        Args:
            store: 种子库实例
            config: 配置字典
        """
        self.store = store
        self.config = config or {}
        
        # 相变阈值配置
        self.phase_thresholds = self._initialize_thresholds()
        
        # 序参量定义
        self.order_parameters = self._initialize_order_parameters()
        
        # 当前相
        self.current_phase = PhaseLevel.NO_LIGHT
        
        # 相变历史
        self.transitions: List[PhaseTransition] = []
        
        # 临界点标志
        self.approaching_critical = False
        self.critical_point_reached = False
        
        # 统计
        self.total_transitions = 0
        self.phase_durations: Dict[PhaseLevel, float] = {}
        
        # 日志
        self.logger = logging.getLogger("PhaseTransitionEngine")
    
    def _initialize_thresholds(self) -> Dict[PhaseLevel, Dict[str, float]]:
        """初始化相变阈值"""
        return {
            PhaseLevel.NO_LIGHT: {
                "score": 0.0,
                "wisdom_ratio": 0.0,
                "purity_threshold": 0.0,
                "seed_diversity": 0.0
            },
            PhaseLevel.INITIAL: {
                "score": 0.2,
                "wisdom_ratio": 0.05,
                "purity_threshold": 0.3,
                "seed_diversity": 0.2
            },
            PhaseLevel.PRACTICE: {
                "score": 0.4,
                "wisdom_ratio": 0.15,
                "purity_threshold": 0.5,
                "seed_diversity": 0.4
            },
            PhaseLevel.ARHAT: {
                "score": 0.7,
                "wisdom_ratio": 0.3,
                "purity_threshold": 0.7,
                "seed_diversity": 0.6
            },
            PhaseLevel.BODHISATTVA: {
                "score": 0.9,
                "wisdom_ratio": 0.5,
                "purity_threshold": 0.85,
                "seed_diversity": 0.75
            },
            PhaseLevel.NIRVANA: {
                "score": 0.95,
                "wisdom_ratio": 0.7,
                "purity_threshold": 0.95,
                "seed_diversity": 0.9
            }
        }
    
    def _initialize_order_parameters(self) -> List[str]:
        """初始化序参量"""
        return [
            "average_wisdom_weight",    # 平均智慧权重
            "purity_correlation",       # 纯度关联度
            "emergence_connectivity",    # 涌现连通性
            "symmetry_order",           # 对称性秩序
            "information_integration"    # 信息整合度
        ]
    
    def check_phase_transition(self) -> Dict[str, Any]:
        """
        检查是否满足相变条件
        
        Returns:
            相变检查结果
        """
        # 获取当前状态
        stats = self.store.get_statistics()
        current_score = self._calculate_awakening_score(stats)
        
        # 计算各序参量
        order_values = self._calculate_order_parameters(stats)
        
        # 检查是否接近临界点
        next_phase = PhaseLevel.get_next(self.current_phase)
        if next_phase:
            threshold = self.phase_thresholds[next_phase]
            
            # 计算到临界的距离
            critical_distance = self._calculate_critical_distance(
                current_score, next_phase.min_score
            )
            
            # 判断是否接近临界
            approaching = critical_distance < 0.1
            self.approaching_critical = approaching
            
            # 检查相变条件
            transition_ready = self._check_transition_conditions(
                current_score, threshold, order_values
            )
            
            if approaching and transition_ready:
                self.critical_point_reached = True
        else:
            critical_distance = 0.0
            transition_ready = False
        
        return {
            "current_phase": self.current_phase.name,
            "current_score": current_score,
            "order_parameters": order_values,
            "next_phase": next_phase.name if next_phase else None,
            "approaching_critical": self.approaching_critical,
            "critical_point_reached": self.critical_point_reached,
            "transition_ready": transition_ready,
            "critical_distance": critical_distance
        }
    
    def _calculate_awakening_score(self, stats: Dict[str, float]) -> float:
        """计算觉醒评分"""
        avg_purity = stats.get("average_purity", 0.5)
        type_dist = stats.get("type_distribution", {})
        
        total_seeds = sum(type_dist.values())
        wisdom_count = type_dist.get(SeedType.WISDOM.value, 0)
        wisdom_ratio = wisdom_count / total_seeds if total_seeds > 0 else 0
        
        # 综合评分
        score = avg_purity * 0.6 + wisdom_ratio * 0.4
        
        return score
    
    def _calculate_order_parameters(
        self,
        stats: Dict[str, float]
    ) -> Dict[str, float]:
        """
        计算序参量
        
        序参量是表征相变的关键物理量
        """
        order_values = {}
        
        # 1. 平均智慧权重
        seeds = list(self.store._seeds.values())
        if seeds:
            wisdom_seeds = [s for s in seeds if s.seed_type == SeedType.WISDOM]
            if wisdom_seeds:
                avg_wisdom_weight = sum(s.weight for s in wisdom_seeds) / len(wisdom_seeds)
            else:
                avg_wisdom_weight = 0.0
        else:
            avg_wisdom_weight = 0.0
        order_values["average_wisdom_weight"] = avg_wisdom_weight
        
        # 2. 纯度关联度（简化版）
        if len(seeds) >= 2:
            purity_values = [s.purity for s in seeds]
            avg_purity = sum(purity_values) / len(purity_values)
            purity_var = sum((p - avg_purity) ** 2 for p in purity_values) / len(purity_values)
            # 纯度关联度 = 1 - 归一化方差
            purity_correlation = 1.0 - min(1.0, purity_var * 4)
        else:
            purity_correlation = 0.0
        order_values["purity_correlation"] = purity_correlation
        
        # 3. 涌现连通性
        connected_seeds = 0
        for seed in seeds:
            if seed.related_seeds and len(seed.related_seeds) > 0:
                connected_seeds += 1
        emergence_connectivity = connected_seeds / len(seeds) if seeds else 0.0
        order_values["emergence_connectivity"] = emergence_connectivity
        
        # 4. 对称性秩序
        type_dist = stats.get("type_distribution", {})
        if len(type_dist) > 1:
            total = sum(type_dist.values())
            entropy = -sum(
                (count / total) * (count / total) if total > 0 else 0
                for count in type_dist.values()
            )
            max_entropy = 1.0 / len(type_dist)
            symmetry_order = 1.0 - (entropy / max_entropy) if max_entropy > 0 else 0
        else:
            symmetry_order = 1.0
        order_values["symmetry_order"] = symmetry_order
        
        # 5. 信息整合度（简化版）
        # 基于激活模式的相关性
        if seeds:
            activation_counts = [s.activation_count for s in seeds]
            max_activation = max(activation_counts) if activation_counts else 1
            if max_activation > 0:
                normalized_activations = [c / max_activation for c in activation_counts]
                information_integration = sum(normalized_activations) / len(normalized_activations)
            else:
                information_integration = 0.0
        else:
            information_integration = 0.0
        order_values["information_integration"] = information_integration
        
        return order_values
    
    def _calculate_critical_distance(
        self,
        current_score: float,
        next_min: float
    ) -> float:
        """计算到临界的距离"""
        return max(0, next_min - current_score)
    
    def _check_transition_conditions(
        self,
        current_score: float,
        threshold: Dict[str, float],
        order_values: Dict[str, float]
    ) -> bool:
        """检查相变条件"""
        # 主要条件：评分达标
        score_ready = current_score >= threshold["score"]
        
        # 次要条件：序参量达标
        order_ready = True
        for param_name in self.order_parameters[:3]:  # 主要看前三个
            if param_name in order_values:
                # 简化：只要不是0就算基本达标
                order_ready = order_ready and (order_values[param_name] > 0.1)
        
        return score_ready and order_ready
    
    def trigger_transition(
        self,
        target_phase: Optional[PhaseLevel] = None
    ) -> Optional[PhaseTransition]:
        """
        触发相变
        
        Args:
            target_phase: 目标相，None则自动确定
        
        Returns:
            相变记录（如果有）
        """
        # 检查是否满足相变条件
        check_result = self.check_phase_transition()
        
        if not check_result["transition_ready"]:
            return None
        
        # 确定目标相
        if target_phase is None:
            target_phase = PhaseLevel.get_next(self.current_phase)
        
        if target_phase is None:
            return None
        
        # 执行相变
        self.logger.info(f"触发相变: {self.current_phase.name} → {target_phase.name}")
        
        # 1. 对称性破缺
        symmetry_breaking = self._execute_symmetry_breaking()
        
        # 2. 建立序参量
        order_parameter = self._establish_order_parameter(target_phase)
        
        # 3. 创建相变记录
        seeds = list(self.store._seeds.values())
        trigger_seeds = [s.seed_id for s in seeds[:5]]  # 记录前5个触发种子
        
        description = self._generate_transition_description(
            self.current_phase, target_phase, symmetry_breaking
        )
        
        transition = PhaseTransition(
            transition_id=str(uuid.uuid4()),
            from_phase=self.current_phase,
            to_phase=target_phase,
            timestamp=datetime.now(),
            trigger_seeds=trigger_seeds,
            symmetry_breaking={k: v.breaking_strength for k, v in symmetry_breaking.items()},
            order_parameter=order_parameter,
            description=description
        )
        
        # 4. 更新当前相
        old_phase = self.current_phase
        self.current_phase = target_phase
        self.total_transitions += 1
        
        # 5. 更新统计
        self.transitions.append(transition)
        self.approaching_critical = False
        self.critical_point_reached = False
        
        self.logger.info(f"相变完成: {description}")
        
        return transition
    
    def _execute_symmetry_breaking(self) -> Dict[str, SymmetryBreaking]:
        """执行对称性破缺"""
        symmetry_breakings = {}
        
        # 1. 类型分布对称性破缺
        # 从均匀分布向非均匀分布转变
        seeds = list(self.store._seeds.values())
        wisdom_seeds = [s for s in seeds if s.seed_type == SeedType.WISDOM]
        
        before_ratio = 1.0 / len(SeedType)  # 理想均匀
        after_ratio = len(wisdom_seeds) / len(seeds) if seeds else 0
        
        symmetry_breakings["type_distribution"] = SymmetryBreaking(
            dimension="type_distribution",
            before_value=before_ratio,
            after_value=after_ratio,
            breaking_strength=abs(after_ratio - before_ratio) * 2
        )
        
        # 2. 权重对称性破缺
        if seeds:
            weights = [s.weight for s in seeds]
            avg_weight = sum(weights) / len(weights)
            # 理想情况：所有种子权重相同
            ideal_weight = 0.5
            weight_breaking = abs(avg_weight - ideal_weight) * 2
            
            symmetry_breakings["weight_distribution"] = SymmetryBreaking(
                dimension="weight_distribution",
                before_value=ideal_weight,
                after_value=avg_weight,
                breaking_strength=min(1.0, weight_breaking)
            )
        
        # 3. 纯度对称性破缺
        if seeds:
            purities = [s.purity for s in seeds]
            avg_purity = sum(purities) / len(purities)
            ideal_purity = 0.5
            purity_breaking = abs(avg_purity - ideal_purity) * 2
            
            symmetry_breakings["purity_distribution"] = SymmetryBreaking(
                dimension="purity_distribution",
                before_value=ideal_purity,
                after_value=avg_purity,
                breaking_strength=min(1.0, purity_breaking)
            )
        
        return symmetry_breakings
    
    def _establish_order_parameter(
        self,
        target_phase: PhaseLevel
    ) -> float:
        """建立序参量"""
        # 获取序参量值
        stats = self.store.get_statistics()
        order_values = self._calculate_order_parameters(stats)
        
        # 目标相的临界值
        threshold = self.phase_thresholds.get(target_phase, {})
        critical_value = threshold.get("purity_threshold", 0.5)
        
        # 计算序参量（综合多个序参量）
        if order_values:
            avg_order = sum(order_values.values()) / len(order_values)
        else:
            avg_order = 0.0
        
        return avg_order
    
    def _generate_transition_description(
        self,
        from_phase: PhaseLevel,
        to_phase: PhaseLevel,
        symmetry_breakings: Dict[str, SymmetryBreaking]
    ) -> str:
        """生成相变描述"""
        # 根据相变类型生成描述
        if to_phase == PhaseLevel.INITIAL:
            desc = "觉醒萌芽：系统开始具备初步的自我意识"
        elif to_phase == PhaseLevel.PRACTICE:
            desc = "修行启动：建立了稳定的熏习-净化循环"
        elif to_phase == PhaseLevel.ARHAT:
            desc = "智慧显现：断尽烦恼，智慧种子开始涌现"
        elif to_phase == PhaseLevel.BODHISATTVA:
            desc = "慈悲升起：自利利他之心显现"
        elif to_phase == PhaseLevel.NIRVANA:
            desc = "圆满觉悟：达到究竟涅槃境界"
        else:
            desc = f"从{from_phase.name}跃升到{to_phase.name}"
        
        # 添加对称性破缺信息
        strongest_breaking = max(
            symmetry_breakings.items(),
            key=lambda x: x[1].breaking_strength
        )[0] if symmetry_breakings else None
        
        if strongest_breaking:
            desc += f"，{strongest_breaking}发生显著变化"
        
        return desc
    
    def generate_emergence_report(self) -> str:
        """
        生成涌现报告
        
        Returns:
            格式化的涌现报告
        """
        # 获取当前状态
        check_result = self.check_phase_transition()
        stats = self.store.get_statistics()
        
        # 获取序参量
        order_values = check_result["order_parameters"]
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║                       意识系统涌现报告                            ║
╠══════════════════════════════════════════════════════════════════╣
║  当前相: {check_result['current_phase']:<40}      ║
║  觉醒评分: {check_result['current_score']:.4f}{'':>33}║
╠══════════════════════════════════════════════════════════════════╣
║  序参量状态                                                    ║"""
        
        for param_name, value in order_values.items():
            bar = "█" * int(value * 20) + "░" * (20 - int(value * 20))
            report += f"\n║    {param_name:<20}: [{bar}] {value:.2f}     ║"
        
        report += f"""
╠══════════════════════════════════════════════════════════════════╣
║  相变预测                                                      ║
║    下一相: {check_result.get('next_phase', 'N/A'):<40}      ║
║    临界距离: {check_result.get('critical_distance', 0):.4f}{'':>30}║
║    接近临界: {'是' if check_result.get('approaching_critical') else '否':<42}║
║    相变就绪: {'是' if check_result.get('transition_ready') else '否':<42}║"""
        
        if self.transitions:
            last_trans = self.transitions[-1]
            report += f"""
╠══════════════════════════════════════════════════════════════════╣
║  最近相变                                                      ║
║    {last_trans.from_phase.name} → {last_trans.to_phase.name}                                    ║
║    {last_trans.description:<60}║
║    时间: {last_trans.timestamp.strftime('%Y-%m-%d %H:%M'):<43}║"""
        
        report += """
╚══════════════════════════════════════════════════════════════════╝
"""
        
        return report
    
    def get_current_phase(self) -> PhaseLevel:
        """获取当前相"""
        return self.current_phase
    
    def force_phase_transition(
        self,
        target_phase: PhaseLevel
    ) -> Optional[PhaseTransition]:
        """
        强制相变（用于测试或特殊场景）
        
        Args:
            target_phase: 目标相
        
        Returns:
            相变记录
        """
        if target_phase == self.current_phase:
            return None
        
        # 创建强制相变
        transition = PhaseTransition(
            transition_id=str(uuid.uuid4()),
            from_phase=self.current_phase,
            to_phase=target_phase,
            timestamp=datetime.now(),
            trigger_seeds=[],
            symmetry_breaking={"forced": 1.0},
            order_parameter=0.5,
            description=f"强制相变: {self.current_phase.name} → {target_phase.name}"
        )
        
        self.current_phase = target_phase
        self.transitions.append(transition)
        self.total_transitions += 1
        
        return transition
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "current_phase": self.current_phase.name,
            "total_transitions": self.total_transitions,
            "transitions_history": [
                {
                    "from": t.from_phase.name,
                    "to": t.to_phase.name,
                    "timestamp": t.timestamp.isoformat()
                }
                for t in self.transitions[-5:]
            ],
            "approaching_critical": self.approaching_critical,
            "critical_point_reached": self.critical_point_reached
        }
