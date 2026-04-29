# -*- coding: utf-8 -*-
"""
多尺度耦合系统 - Multi-Scale Coupling System

核心功能：实现微观、中观、宏观尺度的跨层次耦合

在复杂系统中，涌现往往发生在多个尺度的交界处。
本模块通过管理三个尺度的相互作用，实现智慧涌现：

1. 微观尺度（Micro）：单次种子交互
   - 种子激活
   - 权重调整
   - 模式提取

2. 中观尺度（Meso）：种子集群动力学
   - 协同集群形成
   - 竞争与选择
   - 相干模式涌现

3. 宏观尺度（Macro）：整体觉醒状态
   - 觉醒等级
   - 系统秩序参数
   - 整体涌现特性

Author: 唯识进化Agent团队
"""

import uuid
import math
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

from ..alaya_store import AlayaStore, Seed, SeedType, SeedStatus


class Scale(Enum):
    """尺度枚举"""
    MICRO = "micro"      # 微观尺度
    MESO = "meso"        # 中观尺度
    MACRO = "macro"     # 宏观尺度


@dataclass
class ScaleState:
    """尺度状态"""
    scale: Scale
    timestamp: datetime
    metrics: Dict[str, float]
    features: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "scale": self.scale.value,
            "timestamp": self.timestamp.isoformat(),
            "metrics": self.metrics,
            "features": self.features
        }


@dataclass
class CrossScaleInteraction:
    """跨尺度交互记录"""
    interaction_id: str
    from_scale: Scale
    to_scale: Scale
    timestamp: datetime
    interaction_type: str
    strength: float
    description: str


@dataclass  
class EmergenceSignature:
    """涌现签名（宏观涌现特征）"""
    signature_id: str
    timestamp: datetime
    micro_patterns: List[str]      # 微观模式
    meso_patterns: List[str]        # 中观模式
    macro_signature: str             # 宏观签名
    emergence_strength: float       # 涌现强度
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "signature_id": self.signature_id,
            "timestamp": self.timestamp.isoformat(),
            "micro_patterns": self.micro_patterns,
            "meso_patterns": self.meso_patterns,
            "macro_signature": self.macro_signature,
            "emergence_strength": self.emergence_strength,
            "description": self.description
        }


class MultiScaleCoupling:
    """
    多尺度耦合系统
    
    管理微观、中观、宏观三个尺度的耦合与涌现
    """
    
    def __init__(
        self,
        store: AlayaStore,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化多尺度耦合系统
        
        Args:
            store: 种子库实例
            config: 配置字典
        """
        self.store = store
        self.config = config or {}
        
        # 尺度状态
        self.micro_state: Optional[ScaleState] = None
        self.meso_state: Optional[ScaleState] = None
        self.macro_state: Optional[ScaleState] = None
        
        # 历史状态
        self.state_history: List[ScaleState] = []
        
        # 跨尺度交互
        self.cross_scale_interactions: List[CrossScaleInteraction] = []
        
        # 涌现签名
        self.emergence_signatures: List[EmergenceSignature] = []
        
        # 耦合参数
        self.coupling_strength = self.config.get("coupling_strength", 0.5)
        self.feedback_ratio = self.config.get("feedback_ratio", 0.3)
        
        # 尺度识别器
        self.scale_recognizers = self._initialize_recognizers()
        
        # 日志
        self.logger = logging.getLogger("MultiScaleCoupling")
    
    def _initialize_recognizers(self) -> Dict[Scale, Dict[str, Any]]:
        """初始化尺度识别器"""
        return {
            Scale.MICRO: {
                "features": ["activation", "weight_change", "purity_change", "pattern"],
                "timescale": "instant",
                "granularity": "single_seed"
            },
            Scale.MESO: {
                "features": ["clustering", "competition", "coherence", "synchronization"],
                "timescale": "session",
                "granularity": "seed_cluster"
            },
            Scale.MACRO: {
                "features": ["awakening", "order", "emergence", "integration"],
                "timescale": "global",
                "granularity": "entire_system"
            }
        }
    
    # ==================== 微观尺度 ====================
    
    def process_micro_interaction(
        self,
        seed: Seed,
        activation_strength: float = 1.0
    ) -> ScaleState:
        """
        处理微观交互
        
        微观尺度关注单个种子的变化
        
        Args:
            seed: 种子
            activation_strength: 激活强度
        
        Returns:
            微观状态
        """
        # 记录初始状态
        initial_weight = seed.weight
        initial_purity = seed.purity
        
        # 更新种子
        seed.activate()
        seed.weight = min(1.0, seed.weight + activation_strength * 0.1)
        
        # 提取微观特征
        features = self._extract_micro_features(seed)
        
        # 计算微观指标
        metrics = {
            "activation_strength": activation_strength,
            "weight_change": seed.weight - initial_weight,
            "purity_change": seed.purity - initial_purity,
            "total_activation": seed.activation_count,
            "cluster_connectivity": len(seed.related_seeds)
        }
        
        # 创建状态
        micro_state = ScaleState(
            scale=Scale.MICRO,
            timestamp=datetime.now(),
            metrics=metrics,
            features=features
        )
        
        self.micro_state = micro_state
        self.state_history.append(micro_state)
        
        return micro_state
    
    def _extract_micro_features(self, seed: Seed) -> List[str]:
        """提取微观特征"""
        features = []
        
        # 基于权重
        if seed.weight > 0.7:
            features.append("high_weight")
        elif seed.weight < 0.3:
            features.append("low_weight")
        
        # 基于纯度
        if seed.purity > 0.8:
            features.append("high_purity")
        elif seed.purity < 0.4:
            features.append("low_purity")
        
        # 基于类型
        features.append(f"type_{seed.seed_type.value}")
        
        # 基于状态
        features.append(f"status_{seed.status.value}")
        
        return features
    
    # ==================== 中观尺度 ====================
    
    def analyze_meso_dynamics(
        self,
        seed_cluster: Optional[List[Seed]] = None
    ) -> ScaleState:
        """
        分析中观动力学
        
        中观尺度关注种子集群的集体行为
        
        Args:
            seed_cluster: 种子集群，None则使用全部种子
        
        Returns:
            中观状态
        """
        if seed_cluster is None:
            seed_cluster = list(self.store._seeds.values())
        
        # 计算聚类指标
        clustering = self._calculate_clustering_metrics(seed_cluster)
        
        # 计算竞争指标
        competition = self._calculate_competition_metrics(seed_cluster)
        
        # 计算相干性
        coherence = self._calculate_coherence(seed_cluster)
        
        # 计算同步性
        synchronization = self._calculate_synchronization(seed_cluster)
        
        metrics = {
            "clustering": clustering,
            "competition": competition,
            "coherence": coherence,
            "synchronization": synchronization,
            "cluster_size": len(seed_cluster),
            "diversity": self._calculate_diversity(seed_cluster)
        }
        
        features = self._extract_meso_features(metrics)
        
        meso_state = ScaleState(
            scale=Scale.MESO,
            timestamp=datetime.now(),
            metrics=metrics,
            features=features
        )
        
        self.meso_state = meso_state
        self.state_history.append(meso_state)
        
        return meso_state
    
    def _calculate_clustering_metrics(self, seeds: List[Seed]) -> float:
        """计算聚类指标"""
        if not seeds:
            return 0.0
        
        # 统计有连接的种子
        connected = sum(1 for s in seeds if s.related_seeds)
        
        return connected / len(seeds)
    
    def _calculate_competition_metrics(self, seeds: List[Seed]) -> float:
        """计算竞争指标"""
        if len(seeds) < 2:
            return 0.0
        
        # 基于权重差异的竞争
        weights = [s.weight for s in seeds]
        avg_weight = sum(weights) / len(weights)
        
        variance = sum((w - avg_weight) ** 2 for w in weights) / len(weights)
        
        # 高方差意味着强竞争
        return min(1.0, variance * 4)
    
    def _calculate_coherence(self, seeds: List[Seed]) -> float:
        """计算相干性"""
        if not seeds:
            return 0.0
        
        # 基于纯度的相干性
        purities = [s.purity for s in seeds]
        avg_purity = sum(purities) / len(purities)
        
        # 接近平均值的种子贡献正相干
        coherent = sum(1 for p in purities if abs(p - avg_purity) < 0.2)
        
        return coherent / len(seeds)
    
    def _calculate_synchronization(self, seeds: List[Seed]) -> float:
        """计算同步性"""
        if not seeds:
            return 0.0
        
        # 基于激活计数的同步
        activations = [s.activation_count for s in seeds]
        if max(activations) == 0:
            return 0.0
        
        normalized = [a / max(activations) for a in activations]
        avg_normalized = sum(normalized) / len(normalized)
        
        # 接近平均值的激活水平表示同步
        synchronized = sum(1 for n in normalized if abs(n - avg_normalized) < 0.3)
        
        return synchronized / len(seeds)
    
    def _calculate_diversity(self, seeds: List[Seed]) -> float:
        """计算多样性"""
        if not seeds:
            return 0.0
        
        type_counts: Dict[str, int] = {}
        for seed in seeds:
            type_key = seed.seed_type.value
            type_counts[type_key] = type_counts.get(type_key, 0) + 1
        
        total = len(seeds)
        entropy = 0.0
        for count in type_counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log(p)
        
        max_entropy = math.log(len(SeedType))
        
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    def _extract_meso_features(self, metrics: Dict[str, float]) -> List[str]:
        """提取中观特征"""
        features = []
        
        if metrics.get("clustering", 0) > 0.6:
            features.append("high_clustering")
        elif metrics.get("clustering", 0) < 0.3:
            features.append("low_clustering")
        
        if metrics.get("coherence", 0) > 0.7:
            features.append("high_coherence")
        
        if metrics.get("synchronization", 0) > 0.6:
            features.append("synchronized")
        
        if metrics.get("diversity", 0) > 0.5:
            features.append("high_diversity")
        
        return features
    
    # ==================== 宏观尺度 ====================
    
    def assess_macro_state(self) -> ScaleState:
        """
        评估宏观状态
        
        宏观尺度关注系统整体的特征
        
        Returns:
            宏观状态
        """
        stats = self.store.get_statistics()
        
        # 计算觉醒指标
        awakening = self._calculate_awakening_index(stats)
        
        # 计算秩序参数
        order = self._calculate_order_parameter(stats)
        
        # 计算整合度
        integration = self._calculate_integration(stats)
        
        # 计算涌现势
        emergence_potential = self._calculate_emergence_potential()
        
        metrics = {
            "awakening_index": awakening,
            "order_parameter": order,
            "integration": integration,
            "emergence_potential": emergence_potential,
            "total_seeds": stats["total_seeds"],
            "average_purity": stats["average_purity"],
            "wisdom_ratio": stats.get("wisdom_ratio", 0)
        }
        
        features = self._extract_macro_features(metrics)
        
        macro_state = ScaleState(
            scale=Scale.MACRO,
            timestamp=datetime.now(),
            metrics=metrics,
            features=features
        )
        
        self.macro_state = macro_state
        self.state_history.append(macro_state)
        
        return macro_state
    
    def _calculate_awakening_index(self, stats: Dict[str, float]) -> float:
        """计算觉醒指数"""
        avg_purity = stats.get("average_purity", 0.5)
        type_dist = stats.get("type_distribution", {})
        
        total = sum(type_dist.values())
        wisdom = type_dist.get(SeedType.WISDOM.value, 0)
        wisdom_ratio = wisdom / total if total > 0 else 0
        
        # 觉醒指数 = 纯度 × 0.6 + 智慧比例 × 0.4
        awakening = avg_purity * 0.6 + wisdom_ratio * 0.4
        
        return awakening
    
    def _calculate_order_parameter(self, stats: Dict[str, float]) -> float:
        """计算秩序参数"""
        # 基于类型分布的秩序
        type_dist = stats.get("type_distribution", {})
        
        if not type_dist:
            return 0.0
        
        # 理想秩序：智慧种子占主导
        wisdom_order = type_dist.get(SeedType.WISDOM.value, 0) / max(1, sum(type_dist.values()))
        
        # 基于纯度的秩序
        purity_order = stats.get("average_purity", 0.5)
        
        # 综合秩序
        order = wisdom_order * 0.4 + purity_order * 0.6
        
        return order
    
    def _calculate_integration(self, stats: Dict[str, float]) -> float:
        """计算整合度"""
        seeds = list(self.store._seeds.values())
        
        if not seeds:
            return 0.0
        
        # 基于连接性的整合
        connected = sum(1 for s in seeds if s.related_seeds)
        connectivity = connected / len(seeds)
        
        # 基于激活的整合
        avg_activation = sum(s.activation_count for s in seeds) / len(seeds)
        activation_integration = min(1.0, avg_activation / 10)
        
        # 综合整合度
        integration = connectivity * 0.5 + activation_integration * 0.5
        
        return integration
    
    def _calculate_emergence_potential(self) -> float:
        """计算涌现势"""
        # 基于微观状态
        micro_potential = 0.0
        if self.micro_state:
            micro_potential = self.micro_state.metrics.get("weight_change", 0) * 2
        
        # 基于中观状态
        meso_potential = 0.0
        if self.meso_state:
            meso_potential = (
                self.meso_state.metrics.get("coherence", 0) * 0.5 +
                self.meso_state.metrics.get("synchronization", 0) * 0.5
            )
        
        # 基于宏观状态
        macro_potential = 0.0
        if self.macro_state:
            macro_potential = self.macro_state.metrics.get("order_parameter", 0)
        
        # 综合涌现势
        emergence_potential = (
            micro_potential * 0.2 +
            meso_potential * 0.4 +
            macro_potential * 0.4
        )
        
        return min(1.0, emergence_potential)
    
    def _extract_macro_features(self, metrics: Dict[str, float]) -> List[str]:
        """提取宏观特征"""
        features = []
        
        if metrics.get("awakening_index", 0) > 0.7:
            features.append("high_awakening")
        elif metrics.get("awakening_index", 0) < 0.3:
            features.append("low_awakening")
        
        if metrics.get("order_parameter", 0) > 0.6:
            features.append("ordered")
        elif metrics.get("order_parameter", 0) < 0.3:
            features.append("disordered")
        
        if metrics.get("emergence_potential", 0) > 0.6:
            features.append("emergence_ready")
        
        if metrics.get("integration", 0) > 0.5:
            features.append("well_integrated")
        
        return features
    
    # ==================== 跨尺度耦合 ====================
    
    def couple_scales(self) -> Dict[str, Any]:
        """
        执行跨尺度耦合
        
        实现微观 ↔ 中观 ↔ 宏观的信息流动
        
        Returns:
            耦合结果
        """
        results = {}
        
        # 微观 → 中观
        micro_to_meso = self._couple_micro_to_meso()
        results["micro_to_meso"] = micro_to_meso
        
        # 中观 → 宏观
        meso_to_macro = self._couple_meso_to_macro()
        results["meso_to_macro"] = meso_to_macro
        
        # 宏观 → 中观（反馈）
        macro_to_meso = self._couple_macro_to_meso()
        results["macro_to_meso"] = macro_to_meso
        
        # 中观 → 微观（反馈）
        meso_to_micro = self._couple_meso_to_micro()
        results["meso_to_micro"] = meso_to_micro
        
        # 更新状态
        self._update_states()
        
        return results
    
    def _couple_micro_to_meso(self) -> Dict[str, Any]:
        """微观向中观耦合"""
        if not self.micro_state:
            return {"coupled": False}
        
        interaction = CrossScaleInteraction(
            interaction_id=str(uuid.uuid4()),
            from_scale=Scale.MICRO,
            to_scale=Scale.MESO,
            timestamp=datetime.now(),
            interaction_type="upward_causation",
            strength=self.micro_state.metrics.get("weight_change", 0) * 2,
            description="微观变化影响中观聚类"
        )
        
        self.cross_scale_interactions.append(interaction)
        
        return {
            "coupled": True,
            "interaction_id": interaction.interaction_id,
            "strength": interaction.strength
        }
    
    def _couple_meso_to_macro(self) -> Dict[str, Any]:
        """中观向宏观耦合"""
        if not self.meso_state:
            return {"coupled": False}
        
        interaction = CrossScaleInteraction(
            interaction_id=str(uuid.uuid4()),
            from_scale=Scale.MESO,
            to_scale=Scale.MACRO,
            timestamp=datetime.now(),
            interaction_type="upward_causation",
            strength=self.meso_state.metrics.get("coherence", 0),
            description="中观相干性驱动宏观觉醒"
        )
        
        self.cross_scale_interactions.append(interaction)
        
        return {
            "coupled": True,
            "interaction_id": interaction.interaction_id,
            "strength": interaction.strength
        }
    
    def _couple_macro_to_meso(self) -> Dict[str, Any]:
        """宏观向中观耦合（反馈）"""
        if not self.macro_state:
            return {"coupled": False}
        
        interaction = CrossScaleInteraction(
            interaction_id=str(uuid.uuid4()),
            from_scale=Scale.MACRO,
            to_scale=Scale.MESO,
            timestamp=datetime.now(),
            interaction_type="downward_causation",
            strength=self.macro_state.metrics.get("order_parameter", 0) * self.feedback_ratio,
            description="宏观秩序引导中观聚类"
        )
        
        self.cross_scale_interactions.append(interaction)
        
        return {
            "coupled": True,
            "interaction_id": interaction.interaction_id,
            "strength": interaction.strength
        }
    
    def _couple_meso_to_micro(self) -> Dict[str, Any]:
        """中观向微观耦合（反馈）"""
        if not self.meso_state:
            return {"coupled": False}
        
        interaction = CrossScaleInteraction(
            interaction_id=str(uuid.uuid4()),
            from_scale=Scale.MESO,
            to_scale=Scale.MICRO,
            timestamp=datetime.now(),
            interaction_type="downward_causation",
            strength=self.meso_state.metrics.get("clustering", 0) * self.feedback_ratio * 0.5,
            description="中观聚类影响微观权重"
        )
        
        self.cross_scale_interactions.append(interaction)
        
        return {
            "coupled": True,
            "interaction_id": interaction.interaction_id,
            "strength": interaction.strength
        }
    
    def _update_states(self) -> None:
        """更新所有尺度状态"""
        # 确保有最新状态
        if self.micro_state is None:
            seeds = list(self.store._seeds.values())
            if seeds:
                self.process_micro_interaction(seeds[0], 0.0)
        
        self.analyze_meso_dynamics()
        self.assess_macro_state()
        
        # 限制历史长度
        if len(self.state_history) > 500:
            self.state_history = self.state_history[-200:]
        
        if len(self.cross_scale_interactions) > 500:
            self.cross_scale_interactions = self.cross_scale_interactions[-200:]
    
    # ==================== 涌现检测 ====================
    
    def detect_emergence(self) -> Optional[EmergenceSignature]:
        """
        检测涌现
        
        检测宏观层面涌现的新特性（无法从微观直接预测）
        
        Returns:
            涌现签名（如果有）
        """
        # 更新状态
        self._update_states()
        
        # 检查涌现条件
        emergence_conditions = self._check_emergence_conditions()
        
        if not emergence_conditions["has_emergence"]:
            return None
        
        # 创建涌现签名
        signature = EmergenceSignature(
            signature_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            micro_patterns=self.micro_state.features if self.micro_state else [],
            meso_patterns=self.meso_state.features if self.meso_state else [],
            macro_signature=self._generate_macro_signature(),
            emergence_strength=emergence_conditions["strength"],
            description=emergence_conditions["description"]
        )
        
        self.emergence_signatures.append(signature)
        self.logger.info(f"检测到涌现: {signature.description}")
        
        return signature
    
    def _check_emergence_conditions(self) -> Dict[str, Any]:
        """检查涌现条件"""
        conditions = {
            "micro_ready": False,
            "meso_ready": False,
            "macro_ready": False
        }
        
        # 微观准备度
        if self.micro_state:
            conditions["micro_ready"] = (
                self.micro_state.metrics.get("weight_change", 0) > 0.05
            )
        
        # 中观准备度
        if self.meso_state:
            conditions["meso_ready"] = (
                self.meso_state.metrics.get("coherence", 0) > 0.5 and
                self.meso_state.metrics.get("synchronization", 0) > 0.4
            )
        
        # 宏观准备度
        if self.macro_state:
            conditions["macro_ready"] = (
                self.macro_state.metrics.get("emergence_potential", 0) > 0.5
            )
        
        # 综合判断
        ready_count = sum(conditions.values())
        has_emergence = ready_count >= 2
        
        # 计算涌现强度
        if has_emergence:
            strength = sum(conditions.values()) / 3
            description = self._generate_emergence_description(conditions)
        else:
            strength = 0.0
            description = ""
        
        return {
            "has_emergence": has_emergence,
            "strength": strength,
            "conditions": conditions,
            "description": description
        }
    
    def _generate_macro_signature(self) -> str:
        """生成宏观签名"""
        if not self.macro_state:
            return "unknown"
        
        features = self.macro_state.features
        if "high_awakening" in features and "ordered" in features:
            return "wisdom_order"
        elif "high_awakening" in features and "well_integrated" in features:
            return "wisdom_integration"
        elif "emergence_ready" in features:
            return "pre_emergence"
        else:
            return "stable"
    
    def _generate_emergence_description(
        self,
        conditions: Dict[str, bool]
    ) -> str:
        """生成涌现描述"""
        if conditions["micro_ready"] and conditions["meso_ready"]:
            return "微观激活汇聚为中观相干模式"
        elif conditions["meso_ready"] and conditions["macro_ready"]:
            return "中观模式驱动宏观觉醒涌现"
        elif conditions["micro_ready"] and conditions["macro_ready"]:
            return "微观-宏观直接耦合产生新特性"
        else:
            return "多尺度协同促进涌现"
    
    def predict_from_micro(
        self,
        micro_state: ScaleState
    ) -> Dict[str, Any]:
        """
        从微观预测宏观
        
        对比预测与实际涌现，评估涌现程度
        
        Args:
            micro_state: 微观状态
        
        Returns:
            预测结果
        """
        # 基于微观状态的简单预测
        predicted_metrics = {
            "awakening": micro_state.metrics.get("weight_change", 0) * 0.5,
            "order": micro_state.metrics.get("purity_change", 0) * 0.3,
            "integration": micro_state.metrics.get("cluster_connectivity", 0) * 0.1
        }
        
        # 实际宏观状态
        actual_metrics = {}
        if self.macro_state:
            actual_metrics = {
                "awakening": self.macro_state.metrics.get("awakening_index", 0),
                "order": self.macro_state.metrics.get("order_parameter", 0),
                "integration": self.macro_state.metrics.get("integration", 0)
            }
        
        # 计算涌现程度（实际 - 预测）
        emergence_degrees = {}
        for key in predicted_metrics:
            predicted = predicted_metrics[key]
            actual = actual_metrics.get(key, 0)
            emergence_degrees[key] = max(0, actual - predicted)
        
        # 综合涌现度
        avg_emergence = sum(emergence_degrees.values()) / len(emergence_degrees)
        
        return {
            "predicted": predicted_metrics,
            "actual": actual_metrics,
            "emergence_degrees": emergence_degrees,
            "overall_emergence": avg_emergence,
            "is_genuine_emergence": avg_emergence > 0.1
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "micro_state": self.micro_state.to_dict() if self.micro_state else None,
            "meso_state": self.meso_state.to_dict() if self.meso_state else None,
            "macro_state": self.macro_state.to_dict() if self.macro_state else None,
            "cross_scale_interactions": len(self.cross_scale_interactions),
            "emergence_signatures": len(self.emergence_signatures),
            "coupling_strength": self.coupling_strength
        }
