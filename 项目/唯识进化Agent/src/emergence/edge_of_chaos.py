# -*- coding: utf-8 -*-
"""
混沌边缘管理器 - Edge of Chaos Manager

核心功能：维持系统在混沌边缘的最优状态

复杂性科学研究表明，最佳的创新和适应能力出现在"混沌边缘"——
既不是完全有序的稳定态，也不是完全随机的混沌态，
而是在秩序与混沌之间的临界状态。

本模块通过以下机制维持混沌边缘：

1. 秩序/混沌测量：实时评估系统状态
2. 动态平衡调节：通过扰动和稳定化维持边缘状态
3. 自组织临界性：系统在边缘自然产生涌现
4. 适应性调整：根据任务需求调整边缘位置

Author: 唯识进化Agent团队
"""

import uuid
import random
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

from ..alaya_store import AlayaStore, Seed, SeedType, SeedStatus


class SystemRegime(Enum):
    """系统状态区间"""
    ORDER = "order"           # 有序区域
    EDGE_OF_CHAOS = "edge_of_chaos"  # 混沌边缘
    CHAOS = "chaos"           # 混沌区域


@dataclass
class RegimeState:
    """状态区间"""
    regime: SystemRegime
    order_parameter: float
    chaos_parameter: float
    edge_distance: float  # 距离边缘的距离
    stability: float      # 稳定性指数
    timestamp: datetime


@dataclass
class Perturbation:
    """扰动记录"""
    perturbation_id: str
    perturbation_type: str  # chaos_inject, order_inject, random
    magnitude: float
    affected_seeds: List[str]
    timestamp: datetime
    effect: str


class EdgeOfChaos:
    """
    混沌边缘管理器
    
    维持系统在秩序与混沌之间的临界状态
    """
    
    def __init__(
        self,
        store: AlayaStore,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化混沌边缘管理器
        
        Args:
            store: 种子库实例
            config: 配置字典
        """
        self.store = store
        self.config = config or {}
        
        # 【优化3】边缘参数 - 调整边缘位置使其更易达到
        self.edge_center = self.config.get("edge_center", 0.45)    # 原0.5→0.45，更偏向混沌
        self.edge_width = self.config.get("edge_width", 0.25)       # 原0.15→0.25，扩大边缘范围
        self.order_threshold = self.config.get("order_threshold", 0.35)  # 原0.3→0.35
        self.chaos_threshold = self.config.get("chaos_threshold", 0.65)  # 原0.7→0.65
        
        # 调节参数
        self.adjustment_rate = self.config.get("adjustment_rate", 0.15)  # 原0.1→0.15，更积极调整
        self.max_perturbation = self.config.get("max_perturbation", 0.25)  # 原0.2→0.25
        
        # 【新增】主动扰动机制
        self.active_perturbation_enabled = self.config.get("active_perturbation", True)
        self.perturbation_interval = self.config.get("perturbation_interval", 20)  # 每20次检查扰动一次
        self.perturbation_counter = 0
        
        # 状态追踪
        self.current_regime = SystemRegime.EDGE_OF_CHAOS  # 默认从边缘开始
        self.regime_history: List[RegimeState] = []
        
        # 扰动记录
        self.perturbations: List[Perturbation] = []
        
        # 临界性指标
        self.criticality_index = 0.5
        self.power_law_exponent = -1.5
        
        # 日志
        self.logger = logging.getLogger("EdgeOfChaos")
    
    def measure_order(self) -> float:
        """
        测量系统秩序程度【优化版】
        
        Returns:
            秩序度 (0-1, 1=完全有序)
        """
        seeds = list(self.store._seeds.values())
        
        if not seeds:
            return 0.0
        
        # 【优化】调整权重：更重视纯度和智慧种子
        # 1. 基于纯度的秩序（降低权重）
        purities = [s.purity for s in seeds]
        avg_purity = sum(purities) / len(purities)
        purity_order = avg_purity
        
        # 2. 基于类型分布的秩序（降低权重）
        type_dist: Dict[str, int] = {}
        for seed in seeds:
            key = seed.seed_type.value
            type_dist[key] = type_dist.get(key, 0) + 1
        
        # 有序分布：少数类型占主导
        total = len(seeds)
        max_type_ratio = max(type_dist.values()) / total if type_dist else 0
        type_order = max_type_ratio
        
        # 3. 【优化】基于智慧种子比例的秩序（新增）
        wisdom_count = len([s for s in seeds if s.seed_type == SeedType.WISDOM])
        wisdom_order = wisdom_count / total if total > 0 else 0
        
        # 4. 基于激活模式的秩序
        # 稳定激活 = 高秩序
        activations = [s.activation_count for s in seeds]
        avg_activation = sum(activations) / len(activations) if activations else 0
        activation_order = min(1.0, avg_activation / 10)
        
        # 【优化】综合秩序 - 降低权重，提升智慧种子比例的影响
        order = (
            purity_order * 0.25 +      # 原0.4→0.25
            type_order * 0.20 +        # 原0.3→0.20
            wisdom_order * 0.35 +       # 新增权重
            activation_order * 0.20    # 原0.3→0.20
        )
        
        return min(1.0, max(0.0, order))
    
    def measure_chaos(self) -> float:
        """
        测量系统混沌程度【优化版】
        
        Returns:
            混沌度 (0-1, 1=完全混沌)
        """
        seeds = list(self.store._seeds.values())
        
        if not seeds:
            return 0.5  # 默认中间值
        
        # 【优化】调整权重：更重视染污种子的影响
        # 1. 基于权重差异的混沌
        # 高差异 = 高混沌
        weights = [s.weight for s in seeds]
        if len(weights) > 1:
            avg_weight = sum(weights) / len(weights)
            variance = sum((w - avg_weight) ** 2 for w in weights) / len(weights)
            weight_chaos = min(1.0, variance * 3)  # 降低权重
        else:
            weight_chaos = 0.3
        
        # 2. 基于染污种子比例的混沌【新增】
        contaminated_seeds = len([s for s in seeds if "染污" in s.tags or s.purity < 0.3])
        contaminated_ratio = contaminated_seeds / len(seeds)
        contamination_chaos = contaminated_ratio * 1.5  # 染污种子直接增加混沌
        
        # 3. 基于类型多样性的混沌
        type_dist: Dict[str, int] = {}
        for seed in seeds:
            key = seed.seed_type.value
            type_dist[key] = type_dist.get(key, 0) + 1
        
        # 多样 = 混沌
        num_types = len(type_dist)
        diversity_chaos = num_types / len(SeedType)
        
        # 4. 基于激活模式的混沌
        # 激活计数分布不均匀 = 混沌
        activations = [s.activation_count for s in seeds]
        if len(activations) > 1:
            avg_activation = sum(activations) / len(activations)
            variance = sum((a - avg_activation) ** 2 for a in activations)
            variance = variance / max(1, len(activations) - 1) if len(activations) > 1 else 0
            activation_chaos = min(1.0, math.sqrt(variance) / 8)  # 降低敏感度
        else:
            activation_chaos = 0.2
        
        # 【优化】综合混沌 - 添加染污种子权重
        chaos = (
            weight_chaos * 0.25 +         # 原0.35→0.25
            diversity_chaos * 0.25 +      # 原0.35→0.25
            activation_chaos * 0.20 +     # 原0.30→0.20
            contamination_chaos * 0.30     # 新增权重
        )
        
        return min(1.0, max(0.0, chaos))
    
    def maintain_edge(self) -> Dict[str, Any]:
        """
        维持混沌边缘【优化版】
        
        检查当前状态，如需要则进行调节
        添加主动扰动机制，定期引入随机性
        
        Returns:
            维持结果
        """
        # 测量秩序和混沌
        order = self.measure_order()
        chaos = self.measure_chaos()
        
        # 判断当前区间
        edge_start = self.edge_center - self.edge_width / 2
        edge_end = self.edge_center + self.edge_width / 2
        
        if chaos < edge_start:
            self.current_regime = SystemRegime.ORDER
        elif chaos > edge_end:
            self.current_regime = SystemRegime.CHAOS
        else:
            self.current_regime = SystemRegime.EDGE_OF_CHAOS
        
        # 计算距离边缘的距离
        edge_distance = min(abs(chaos - edge_start), abs(chaos - edge_end))
        
        # 记录状态
        regime_state = RegimeState(
            regime=self.current_regime,
            order_parameter=order,
            chaos_parameter=chaos,
            edge_distance=edge_distance,
            stability=1.0 - edge_distance,
            timestamp=datetime.now()
        )
        self.regime_history.append(regime_state)
        
        # 【新增】主动扰动机制
        adjustment = {"adjusted": False, "reason": "already_at_edge"}
        self.perturbation_counter += 1
        
        if self.active_perturbation_enabled:
            # 定期主动扰动
            if self.perturbation_counter >= self.perturbation_interval:
                self.perturbation_counter = 0
                # 主动注入混沌以维持边缘状态
                perturbation_result = self.inject_chaos(magnitude=0.15)
                adjustment = {
                    "adjusted": True,
                    "reason": "active_perturbation",
                    "perturbation": perturbation_result
                }
        
        # 如果不在边缘，进行调节
        if not adjustment["adjusted"] and self.current_regime != SystemRegime.EDGE_OF_CHAOS:
            adjustment = self._adjust_to_edge(chaos, order)
        
        # 限制历史长度
        if len(self.regime_history) > 500:
            self.regime_history = self.regime_history[-200:]
        
        return {
            "current_regime": self.current_regime.value,
            "order": order,
            "chaos": chaos,
            "edge_distance": edge_distance,
            "stability": regime_state.stability,
            "adjustment": adjustment
        }
    
    def _adjust_to_edge(
        self,
        chaos: float,
        order: float
    ) -> Dict[str, Any]:
        """调节到边缘"""
        if self.current_regime == SystemRegime.ORDER:
            # 需要注入混沌
            result = self.inject_chaos()
            result["action"] = "inject_chaos"
            return result
        elif self.current_regime == SystemRegime.CHAOS:
            # 需要注入秩序
            result = self.inject_order()
            result["action"] = "inject_order"
            return result
        
        return {"adjusted": False}
    
    def inject_chaos(
        self,
        magnitude: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        注入混沌
        
        增加系统的随机性和多样性，促进创新
        
        Args:
            magnitude: 扰动幅度，None则自动计算
        
        Returns:
            注入结果
        """
        if magnitude is None:
            # 自动计算：需要多少混沌才能到达边缘
            current_chaos = self.measure_chaos()
            edge_start = self.edge_center - self.edge_width / 2
            magnitude = min(self.max_perturbation, edge_start - current_chaos + 0.1)
        
        seeds = list(self.store._seeds.values())
        if not seeds:
            return {"injected": False, "reason": "no_seeds"}
        
        # 选择要扰动的种子
        num_to_perturb = max(1, len(seeds) // 5)  # 5%的种子
        selected_seeds = random.sample(seeds, min(num_to_perturb, len(seeds)))
        
        affected_seeds = []
        
        for seed in selected_seeds:
            # 注入混沌的方式
            chaos_type = random.choice(["weight_random", "type_mutate", "connection_shuffle"])
            
            original_weight = seed.weight
            
            if chaos_type == "weight_random":
                # 随机调整权重
                delta = random.uniform(-magnitude, magnitude) * 0.5
                seed.weight = max(0.0, min(1.0, seed.weight + delta))
            
            elif chaos_type == "type_mutate":
                # 随机改变类型（创造新类型种子）
                # 不改变原种子，但创建新种子
                new_seed = Seed.create(
                    content=f"混沌探索: {seed.content[:30]}...",
                    seed_type=random.choice(list(SeedType)),
                    weight=seed.weight * 0.5,
                    purity=seed.purity * 0.5,
                    source="chaos_injection",
                    tags=["混沌探索", "创新"]
                )
                self.store.add(new_seed)
                affected_seeds.append(new_seed.seed_id)
            
            elif chaos_type == "connection_shuffle":
                # 打乱连接
                if seed.related_seeds:
                    random.shuffle(seed.related_seeds)
            
            affected_seeds.append(seed.seed_id)
        
        # 记录扰动
        perturbation = Perturbation(
            perturbation_id=str(uuid.uuid4()),
            perturbation_type="chaos_inject",
            magnitude=magnitude,
            affected_seeds=affected_seeds,
            timestamp=datetime.now(),
            effect=f"注入了{magnitude:.2f}程度的混沌"
        )
        self.perturbations.append(perturbation)
        
        self.logger.info(f"注入混沌: magnitude={magnitude:.2f}, affected={len(affected_seeds)}")
        
        return {
            "injected": True,
            "perturbation_id": perturbation.perturbation_id,
            "magnitude": magnitude,
            "affected_seeds": len(affected_seeds),
            "chaos_type": chaos_type
        }
    
    def inject_order(
        self,
        magnitude: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        注入秩序
        
        增加系统的稳定性和一致性
        
        Args:
            magnitude: 扰动幅度，None则自动计算
        
        Returns:
            注入结果
        """
        if magnitude is None:
            current_chaos = self.measure_chaos()
            edge_end = self.edge_center + self.edge_width / 2
            magnitude = min(self.max_perturbation, current_chaos - edge_end + 0.1)
        
        seeds = list(self.store._seeds.values())
        if not seeds:
            return {"injected": False, "reason": "no_seeds"}
        
        # 选择要扰动的种子
        num_to_perturb = max(1, len(seeds) // 5)
        selected_seeds = random.sample(seeds, min(num_to_perturb, len(seeds)))
        
        affected_seeds = []
        
        for seed in selected_seeds:
            # 注入秩序的方式
            order_type = random.choice(["weight_normalize", "purity_enhance", "connection_strengthen"])
            
            if order_type == "weight_normalize":
                # 权重向均值收敛
                avg_weight = sum(s.weight for s in seeds) / len(seeds)
                delta = (avg_weight - seed.weight) * magnitude
                seed.weight = max(0.0, min(1.0, seed.weight + delta))
            
            elif order_type == "purity_enhance":
                # 提升纯度
                seed.purity = min(1.0, seed.purity + magnitude * 0.2)
            
            elif order_type == "connection_strengthen":
                # 强化连接
                # 选择部分种子增加连接
                if len(seeds) > 1:
                    targets = random.sample(
                        [s for s in seeds if s.seed_id != seed.seed_id],
                        min(2, len(seeds) - 1)
                    )
                    for target in targets:
                        if target.seed_id not in seed.related_seeds:
                            seed.related_seeds.append(target.seed_id)
            
            affected_seeds.append(seed.seed_id)
        
        # 记录扰动
        perturbation = Perturbation(
            perturbation_id=str(uuid.uuid4()),
            perturbation_type="order_inject",
            magnitude=magnitude,
            affected_seeds=affected_seeds,
            timestamp=datetime.now(),
            effect=f"注入了{magnitude:.2f}程度的秩序"
        )
        self.perturbations.append(perturbation)
        
        self.logger.info(f"注入秩序: magnitude={magnitude:.2f}, affected={len(affected_seeds)}")
        
        return {
            "injected": True,
            "perturbation_id": perturbation.perturbation_id,
            "magnitude": magnitude,
            "affected_seeds": len(affected_seeds),
            "order_type": order_type
        }
    
    def apply_random_perturbation(
        self,
        magnitude: float = 0.1
    ) -> Dict[str, Any]:
        """
        施加随机扰动
        
        在边缘维持中添加随机性，模拟自然临界性
        
        Args:
            magnitude: 扰动幅度
        
        Returns:
            扰动结果
        """
        seeds = list(self.store._seeds.values())
        if not seeds:
            return {"applied": False}
        
        # 随机选择种子
        num_to_perturb = max(1, len(seeds) // 10)
        selected_seeds = random.sample(seeds, min(num_to_perturb, len(seeds)))
        
        affected_seeds = []
        
        for seed in selected_seeds:
            # 随机扰动
            perturbation_type = random.choice([
                "weight_jitter",
                "add_connection",
                "remove_connection"
            ])
            
            if perturbation_type == "weight_jitter":
                seed.weight = max(0.0, min(1.0, seed.weight + random.uniform(-magnitude, magnitude)))
            elif perturbation_type == "add_connection":
                targets = [s for s in seeds if s.seed_id != seed.seed_id and s.seed_id not in seed.related_seeds]
                if targets:
                    seed.related_seeds.append(random.choice(targets).seed_id)
            elif perturbation_type == "remove_connection":
                if seed.related_seeds:
                    seed.related_seeds.pop()
            
            affected_seeds.append(seed.seed_id)
        
        # 记录扰动
        perturbation = Perturbation(
            perturbation_id=str(uuid.uuid4()),
            perturbation_type="random",
            magnitude=magnitude,
            affected_seeds=affected_seeds,
            timestamp=datetime.now(),
            effect="随机临界扰动"
        )
        self.perturbations.append(perturbation)
        
        # 更新临界性指标
        self._update_criticality()
        
        return {
            "applied": True,
            "perturbation_id": perturbation.perturbation_id,
            "affected_seeds": len(affected_seeds)
        }
    
    def _update_criticality(self) -> None:
        """更新临界性指标"""
        # 简化：基于扰动历史估计临界性
        recent_perturbations = self.perturbations[-20:]
        
        if not recent_perturbations:
            self.criticality_index = 0.5
            return
        
        # 计算近期的混沌/秩序注入比例
        chaos_count = sum(1 for p in recent_perturbations if p.perturbation_type == "chaos_inject")
        order_count = sum(1 for p in recent_perturbations if p.perturbation_type == "order_inject")
        
        if chaos_count + order_count > 0:
            chaos_ratio = chaos_count / (chaos_count + order_count)
            # 接近0.5表示在边缘
            self.criticality_index = 0.5 + (chaos_ratio - 0.5) * 0.2
        else:
            self.criticality_index = 0.5
    
    def get_current_state(self) -> Dict[str, Any]:
        """
        获取当前状态
        
        Returns:
            当前状态信息
        """
        order = self.measure_order()
        chaos = self.measure_chaos()
        
        edge_start = self.edge_center - self.edge_width / 2
        edge_end = self.edge_center + self.edge_width / 2
        
        if chaos < edge_start:
            regime = SystemRegime.ORDER
        elif chaos > edge_end:
            regime = SystemRegime.CHAOS
        else:
            regime = SystemRegime.EDGE_OF_CHAOS
        
        return {
            "regime": regime.value,
            "order": order,
            "chaos": chaos,
            "edge_center": self.edge_center,
            "edge_width": self.edge_width,
            "edge_range": (edge_start, edge_end),
            "distance_to_edge": min(abs(chaos - edge_start), abs(chaos - edge_end)),
            "criticality_index": self.criticality_index,
            "perturbations_count": len(self.perturbations),
            "regime_history_length": len(self.regime_history)
        }
    
    def is_at_edge(self) -> bool:
        """判断是否在边缘"""
        state = self.get_current_state()
        return state["regime"] == SystemRegime.EDGE_OF_CHAOS.value
    
    def get_regime_stability(self) -> float:
        """获取区间稳定性"""
        recent_states = self.regime_history[-10:]
        
        if len(recent_states) < 2:
            return 1.0
        
        # 计算区间切换频率
        regime_changes = sum(
            1 for i in range(1, len(recent_states))
            if recent_states[i].regime != recent_states[i-1].regime
        )
        
        # 频繁切换 = 低稳定性
        stability = 1.0 - (regime_changes / len(recent_states))
        
        return stability
    
    def apply_edge_force(
        self,
        target_chaos: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        应用边缘力
        
        将系统推向目标混沌度
        
        Args:
            target_chaos: 目标混沌度，None则保持在边缘
        
        Returns:
            应用结果
        """
        if target_chaos is None:
            target_chaos = self.edge_center
        
        current_chaos = self.measure_chaos()
        delta = target_chaos - current_chaos
        
        if abs(delta) < 0.05:
            return {"applied": False, "reason": "already_at_target"}
        
        if delta > 0:
            # 需要增加混沌
            result = self.inject_chaos(magnitude=abs(delta))
        else:
            # 需要增加秩序
            result = self.inject_order(magnitude=abs(delta))
        
        result["target_chaos"] = target_chaos
        result["current_chaos"] = current_chaos
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        state = self.get_current_state()
        
        recent_perturbations = self.perturbations[-20:]
        perturbation_types = {}
        for p in recent_perturbations:
            perturbation_types[p.perturbation_type] = perturbation_types.get(p.perturbation_type, 0) + 1
        
        return {
            "current_regime": state["regime"],
            "order_chaos_balance": {
                "order": state["order"],
                "chaos": state["chaos"]
            },
            "edge_parameters": {
                "center": self.edge_center,
                "width": self.edge_width
            },
            "criticality_index": self.criticality_index,
            "stability": self.get_regime_stability(),
            "recent_perturbations": len(recent_perturbations),
            "perturbation_types": perturbation_types,
            "total_regime_changes": sum(
                1 for i in range(1, len(self.regime_history))
                if self.regime_history[i].regime != self.regime_history[i-1].regime
            ) if len(self.regime_history) > 1 else 0
        }
