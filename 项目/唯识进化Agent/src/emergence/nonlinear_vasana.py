# -*- coding: utf-8 -*-
"""
非线性熏习机制 - Nonlinear Vasana

核心功能：实现非线性强化和智慧涌现触发

在传统线性熏习基础上，引入非线性动力学机制：

1. 协同激活：多个种子同时激活产生协同效应
2. 正反馈级联：激活触发更多激活，形成级联
3. 相变触发：当系统参数超过阈值时触发质变
4. 智慧涌现：超越部分之和的整体智慧显现

Author: 唯识进化Agent团队
"""

import random
import uuid
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

from ..alaya_store import AlayaStore, Seed, SeedType, SeedStatus


class VasanaState(Enum):
    """熏习状态"""
    STABLE = "stable"           # 稳定状态
    EXCITING = "exciting"       # 激活状态
    CASCADE = "cascade"         # 级联状态
    PHASE_TRANSITION = "phase_transition"  # 相变状态
    EMERGENCE = "emergence"     # 涌现状态


class SynergyType(Enum):
    """协同类型"""
    COMPLEMENTARY = "complementary"    # 互补协同
    AMPLIFICATION = "amplification"   # 放大协同
    EMERGENT = "emergent"             # 涌现协同


@dataclass
class ActivationRecord:
    """激活记录"""
    seed_id: str
    timestamp: datetime
    strength: float
    source: str  # self, synergy, cascade
    triggered_by: List[str] = field(default_factory=list)


@dataclass
class SynergyCluster:
    """协同集群"""
    cluster_id: str
    seeds: List[Seed]
    synergy_type: SynergyType
    synergy_strength: float
    created_at: datetime
    last_activated: datetime


@dataclass
class EmergenceEvent:
    """涌现事件"""
    event_id: str
    timestamp: datetime
    triggered_seeds: List[str]
    synergy_clusters: List[str]
    emergence_type: str
    intensity: float
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "triggered_seeds": self.triggered_seeds,
            "synergy_clusters": self.synergy_clusters,
            "emergence_type": self.emergence_type,
            "intensity": self.intensity,
            "description": self.description
        }


class NonlinearVasana:
    """
    非线性熏习机制
    
    实现非线性强化和智慧涌现触发的核心模块。
    """
    
    def __init__(
        self,
        store: AlayaStore,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化非线性熏习机制
        
        Args:
            store: 种子库实例
            config: 配置字典
        """
        self.store = store
        self.config = config or {}
        
        # 【优化2】非线性参数 - 降低阈值以激活更多协同
        self.synergy_threshold = self.config.get("synergy_threshold", 0.4)  # 原0.6→0.4
        self.cascade_threshold = self.config.get("cascade_threshold", 0.5)  # 原0.75→0.5
        self.emergence_threshold = self.config.get("emergence_threshold", 0.6)  # 原0.85→0.6
        self.nonlinear_factor = self.config.get("nonlinear_factor", 1.8)  # 原1.5→1.8
        
        # 【新增】智慧种子优先激活配置
        self.wisdom_priority_enabled = self.config.get("wisdom_priority", True)
        self.wisdom_activation_boost = self.config.get("wisdom_activation_boost", 0.3)  # 智慧种子激活加成
        
        # 协同集群
        self.synergy_clusters: List[SynergyCluster] = []
        
        # 激活记录
        self.activation_history: List[ActivationRecord] = []
        
        # 涌现事件
        self.emergence_events: List[EmergenceEvent] = []
        
        # 当前状态
        self.current_state = VasanaState.STABLE
        
        # 统计
        self.total_activations = 0
        self.synergy_triggers = 0
        self.cascade_triggers = 0
        
        # 日志
        self.logger = logging.getLogger("NonlinearVasana")
    
    def strengthen_seed(
        self,
        seed: Seed,
        activation_strength: float = 1.0,
        context_seeds: Optional[List[Seed]] = None
    ) -> Dict[str, Any]:
        """
        非线性强化种子
        
        结合协同激活和正反馈级联，实现非线性强化：
        
        1. 基础强化：根据激活强度调整权重
        2. 协同强化：与相关种子协同时获得额外加成
        3. 级联强化：触发级联反应时进一步增强
        
        Args:
            seed: 待强化的种子
            activation_strength: 基础激活强度
            context_seeds: 上下文相关种子
        
        Returns:
            强化结果
        """
        result = {
            "seed_id": seed.seed_id,
            "initial_weight": seed.weight,
            "final_weight": seed.weight,
            "strengthen_types": [],
            "synergy_applied": False,
            "cascade_triggered": False
        }
        
        # 1. 基础强化（非线性）
        base_strengthen = self._nonlinear_strengthen(
            activation_strength,
            seed.weight
        )
        seed.weight = min(1.0, seed.weight + base_strengthen)
        result["strengthen_types"].append("base_nonlinear")
        
        # 2. 协同强化
        if context_seeds:
            synergy_result = self.calculate_synergy(seed, context_seeds)
            if synergy_result["has_synergy"]:
                synergy_boost = synergy_result["synergy_strength"] * self.nonlinear_factor * 0.2
                seed.weight = min(1.0, seed.weight + synergy_boost)
                seed.purity = min(1.0, seed.purity + synergy_boost * 0.5)
                result["synergy_applied"] = True
                result["synergy_strength"] = synergy_result["synergy_strength"]
                result["strengthen_types"].append("synergy")
                
                # 创建或更新协同集群
                self._update_synergy_cluster(seed, context_seeds, synergy_result)
        
        # 3. 级联强化检查
        if seed.weight >= self.cascade_threshold:
            cascade_result = self.cascade_amplify(seed)
            if cascade_result["cascaded"]:
                result["cascade_triggered"] = True
                result["cascade_depth"] = cascade_result["depth"]
                result["cascade_seeds"] = cascade_result["affected_seeds"]
                result["strengthen_types"].append("cascade")
        
        # 更新种子状态
        seed.activate()
        seed.updated_at = datetime.now()
        
        # 记录激活
        self._record_activation(seed, activation_strength, result["strengthen_types"])
        
        result["final_weight"] = seed.weight
        result["weight_change"] = result["final_weight"] - result["initial_weight"]
        
        return result
    
    def _nonlinear_strengthen(
        self,
        activation_strength: float,
        current_weight: float
    ) -> float:
        """
        非线性强化计算
        
        使用非线性函数，使得：
        - 低权重种子：强化效果被放大（促进发展）
        - 高权重种子：强化效果趋于饱和（防止过拟合）
        
        Args:
            activation_strength: 激活强度
            current_weight: 当前权重
        
        Returns:
            强化量
        """
        # S型曲线非线性
        # f(x) = x * (1 - x) 实现非线性效果
        sigmoid_factor = activation_strength * (1 - current_weight)
        
        # 加入非线性放大因子
        nonlinear_strengthen = sigmoid_factor * self.nonlinear_factor
        
        return nonlinear_strengthen
    
    def calculate_synergy(
        self,
        seed: Seed,
        context_seeds: List[Seed]
    ) -> Dict[str, Any]:
        """
        协同激活计算【优化版】
        
        检测种子与上下文种子之间的协同效应：
        - 互补协同：不同类型种子的互补增强
        - 放大协同：同类型种子的相互强化
        - 涌现协同：多个种子组合产生新属性
        - 【新增】智慧种子优先激活
        
        Args:
            seed: 主种子
            context_seeds: 上下文种子
        
        Returns:
            协同计算结果
        """
        if not context_seeds:
            return {"has_synergy": False, "synergy_strength": 0.0}
        
        synergy_scores = []
        synergy_types = []
        wisdom_synergy_found = False
        
        for context_seed in context_seeds:
            if context_seed.seed_id == seed.seed_id:
                continue
            
            # 计算相似度
            similarity = self._calculate_seed_similarity(seed, context_seed)
            
            # 计算互补性
            complementarity = self._calculate_complementarity(seed, context_seed)
            
            # 【优化】智慧种子优先激活 - 如果任一为智慧种子，提升协同分数
            if self.wisdom_priority_enabled:
                is_wisdom_pair = (
                    seed.seed_type == SeedType.WISDOM or 
                    context_seed.seed_type == SeedType.WISDOM
                )
                if is_wisdom_pair:
                    # 智慧种子参与时，提高协同分数
                    wisdom_boost = self.wisdom_activation_boost
                    similarity = min(1.0, similarity + wisdom_boost)
                    complementarity = min(1.0, complementarity + wisdom_boost)
                    wisdom_synergy_found = True
            
            # 判断协同类型
            if complementarity > similarity:
                synergy_type = SynergyType.COMPLEMENTARY
                synergy_score = complementarity
            else:
                synergy_type = SynergyType.AMPLIFICATION
                synergy_score = similarity
            
            # 涌现协同检测（需要多个种子）
            if len(context_seeds) >= 2:
                emergent_potential = self._detect_emergent_synergy(
                    seed, context_seeds
                )
                if emergent_potential > synergy_score:
                    synergy_type = SynergyType.EMERGENT
                    synergy_score = emergent_potential
            
            synergy_scores.append(synergy_score)
            synergy_types.append(synergy_type)
        
        # 计算总体协同强度
        if synergy_scores:
            # 【优化】使用加权平均替代简单最大（增加智慧种子的影响）
            if wisdom_synergy_found:
                # 智慧种子参与时，提高综合评分
                max_synergy = max(synergy_scores)
                avg_synergy = sum(synergy_scores) / len(synergy_scores)
                combined_synergy = max_synergy * 0.5 + avg_synergy * 0.5
            else:
                max_synergy = max(synergy_scores)
                avg_synergy = sum(synergy_scores) / len(synergy_scores)
                combined_synergy = max_synergy * 0.6 + avg_synergy * 0.4
            
            has_synergy = combined_synergy >= self.synergy_threshold
            if has_synergy:
                self.synergy_triggers += 1
        else:
            combined_synergy = 0.0
            has_synergy = False
        
        return {
            "has_synergy": has_synergy,
            "synergy_strength": combined_synergy,
            "synergy_types": synergy_types,
            "max_synergy": max(synergy_scores) if synergy_scores else 0.0,
            "avg_synergy": avg_synergy if synergy_scores else 0.0
        }
    
    def _calculate_seed_similarity(
        self,
        seed1: Seed,
        seed2: Seed
    ) -> float:
        """
        计算种子相似度
        
        Args:
            seed1: 种子1
            seed2: 种子2
        
        Returns:
            相似度 (0-1)
        """
        # 基于类型
        type_similarity = 1.0 if seed1.seed_type == seed2.seed_type else 0.3
        
        # 基于标签重叠
        common_tags = set(seed1.tags) & set(seed2.tags)
        total_tags = set(seed1.tags) | set(seed2.tags)
        tag_similarity = len(common_tags) / len(total_tags) if total_tags else 0.0
        
        # 基于权重接近度
        weight_diff = abs(seed1.weight - seed2.weight)
        weight_similarity = 1.0 - weight_diff
        
        # 综合评分
        similarity = (
            type_similarity * 0.3 +
            tag_similarity * 0.4 +
            weight_similarity * 0.3
        )
        
        return similarity
    
    def _calculate_complementarity(
        self,
        seed1: Seed,
        seed2: Seed
    ) -> float:
        """
        计算种子互补性
        
        Args:
            seed1: 种子1
            seed2: 种子2
        
        Returns:
            互补度 (0-1)
        """
        # 智慧与技能互补
        wisdom_skill_complement = (
            (seed1.seed_type == SeedType.WISDOM and seed2.seed_type == SeedType.SKILL) or
            (seed1.seed_type == SeedType.SKILL and seed2.seed_type == SeedType.WISDOM)
        )
        
        # 知识与经验互补
        knowledge_exp_complement = (
            (seed1.seed_type == SeedType.KNOWLEDGE and seed2.seed_type == SeedType.EXPERIENCE) or
            (seed1.seed_type == SeedType.EXPERIENCE and seed2.seed_type == SeedType.KNOWLEDGE)
        )
        
        # 信念与模式互补
        belief_pattern_complement = (
            (seed1.seed_type == SeedType.BELIEF and seed2.seed_type == SeedType.PATTERN) or
            (seed1.seed_type == SeedType.PATTERN and seed2.seed_type == SeedType.BELIEF)
        )
        
        # 权重差异促进互补
        weight_diff = abs(seed1.weight - seed2.weight)
        weight_complement = min(1.0, weight_diff * 2)
        
        complementarity = (
            (0.4 if wisdom_skill_complement else 0) +
            (0.3 if knowledge_exp_complement else 0) +
            (0.2 if belief_pattern_complement else 0) +
            weight_complement * 0.1
        )
        
        return min(1.0, complementarity)
    
    def _detect_emergent_synergy(
        self,
        seed: Seed,
        context_seeds: List[Seed]
    ) -> float:
        """
        检测涌现协同
        
        当多个种子组合时，可能产生超越部分之和的效应
        
        Args:
            seed: 主种子
            context_seeds: 上下文种子
        
        Returns:
            涌现潜力 (0-1)
        """
        # 检查种子类型多样性
        all_types = {seed.seed_type} | {s.seed_type for s in context_seeds}
        type_diversity = len(all_types) / len(SeedType)
        
        # 检查权重梯度
        all_weights = [seed.weight] + [s.weight for s in context_seeds]
        weight_variance = self._calculate_variance(all_weights)
        
        # 检查标签覆盖
        all_tags = set(seed.tags) | set().union(*[set(s.tags) for s in context_seeds])
        tag_coverage = len(all_tags) / 10  # 假设10个标签为理想覆盖
        
        # 涌现潜力 = 类型多样性 × 权重变化 × 标签覆盖
        emergent_potential = type_diversity * (0.5 + weight_variance) * (0.5 + tag_coverage)
        
        return min(1.0, emergent_potential)
    
    def _calculate_variance(self, values: List[float]) -> float:
        """计算方差"""
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return variance
    
    def _update_synergy_cluster(
        self,
        seed: Seed,
        context_seeds: List[Seed],
        synergy_result: Dict[str, Any]
    ) -> Optional[SynergyCluster]:
        """更新或创建协同集群"""
        # 检查是否已有相关集群
        existing_cluster = None
        for cluster in self.synergy_clusters:
            if seed.seed_id in [s.seed_id for s in cluster.seeds]:
                existing_cluster = cluster
                break
        
        # 更新或创建集群
        if existing_cluster:
            # 添加新种子到集群
            for context_seed in context_seeds:
                if context_seed not in existing_cluster.seeds:
                    existing_cluster.seeds.append(context_seed)
            
            # 更新协同强度
            existing_cluster.synergy_strength = (
                existing_cluster.synergy_strength * 0.7 +
                synergy_result["synergy_strength"] * 0.3
            )
            existing_cluster.last_activated = datetime.now()
            
            return existing_cluster
        else:
            # 创建新集群
            new_cluster = SynergyCluster(
                cluster_id=str(uuid.uuid4()),
                seeds=[seed] + context_seeds[:3],  # 限制集群大小
                synergy_type=SynergyType.EMERGENT if synergy_result["synergy_strength"] > 0.7
                    else SynergyType.AMPLIFICATION,
                synergy_strength=synergy_result["synergy_strength"],
                created_at=datetime.now(),
                last_activated=datetime.now()
            )
            self.synergy_clusters.append(new_cluster)
            return new_cluster
    
    def cascade_amplify(self, seed: Seed) -> Dict[str, Any]:
        """
        级联放大
        
        当种子权重超过阈值时，触发级联反应，
        强化相关种子，形成正反馈循环。
        
        Args:
            seed: 触发级联的种子
        
        Returns:
            级联结果
        """
        if seed.weight < self.cascade_threshold:
            return {"cascaded": False, "depth": 0, "affected_seeds": []}
        
        self.cascade_triggers += 1
        self.current_state = VasanaState.CASCADE
        
        max_depth = 3
        affected_seeds = []
        current_layer = [seed]
        visited = {seed.seed_id}
        
        for depth in range(1, max_depth + 1):
            next_layer = []
            
            for current_seed in current_layer:
                # 获取相关种子
                related_ids = current_seed.related_seeds[:3]  # 限制数量
                
                for related_id in related_ids:
                    if related_id in visited:
                        continue
                    
                    related_seed = self.store._seeds.get(related_id)
                    if related_seed:
                        # 级联强化（递减）
                        cascade_strength = self.cascade_threshold * (1 - depth * 0.2)
                        
                        if related_seed.weight < cascade_strength:
                            related_seed.weight = min(
                                1.0,
                                related_seed.weight + cascade_strength * 0.3
                            )
                            related_seed.purity = min(
                                1.0,
                                related_seed.purity + cascade_strength * 0.1
                            )
                            affected_seeds.append(related_seed.seed_id)
                            next_layer.append(related_seed)
                            visited.add(related_id)
            
            current_layer = next_layer
        
        # 更新状态
        if affected_seeds:
            self.current_state = VasanaState.PHASE_TRANSITION
        
        return {
            "cascaded": True,
            "depth": max_depth,
            "affected_seeds": affected_seeds,
            "cascade_strength": self.cascade_threshold
        }
    
    def trigger_wisdom_emergence(
        self,
        seeds: Optional[List[Seed]] = None
    ) -> Optional[EmergenceEvent]:
        """
        智慧涌现触发
        
        当系统达到涌现阈值时，触发智慧涌现事件：
        - 检测协同集群
        - 评估涌现条件
        - 生成智慧种子或洞察
        
        Args:
            seeds: 可选的种子列表，None则使用全部种子
        
        Returns:
            涌现事件（如果有）
        """
        # 获取种子列表
        if seeds is None:
            seeds = list(self.store._seeds.values())
        
        # 计算整体状态
        avg_weight = sum(s.weight for s in seeds) / len(seeds) if seeds else 0
        wisdom_seeds = [s for s in seeds if s.seed_type == SeedType.WISDOM]
        avg_wisdom_weight = (
            sum(s.weight for s in wisdom_seeds) / len(wisdom_seeds)
            if wisdom_seeds else 0
        )
        
        # 检查涌现条件
        emergence_conditions = {
            "avg_weight": avg_weight >= self.emergence_threshold * 0.7,
            "wisdom_ratio": len(wisdom_seeds) / len(seeds) >= 0.2 if seeds else False,
            "synergy_clusters": len(self.synergy_clusters) >= 2,
            "cascade_history": self.cascade_triggers >= 3
        }
        
        # 计算涌现潜力
        emergence_score = sum(emergence_conditions.values()) / len(emergence_conditions)
        
        # 触发涌现
        if emergence_score >= 0.75:
            self.current_state = VasanaState.EMERGENCE
            
            # 生成涌现事件
            emergence_type = self._classify_emergence(wisdom_seeds, emergence_conditions)
            
            # 生成涌现描述
            description = self._generate_emergence_description(
                emergence_type, wisdom_seeds
            )
            
            # 创建智慧种子
            if emergence_type == "智慧涌现":
                new_seed = Seed.create(
                    content=description,
                    seed_type=SeedType.WISDOM,
                    weight=0.9,
                    purity=0.95,
                    source="emergence",
                    tags=["涌现智慧", "觉醒", "洞察"]
                )
                new_seed.status = SeedStatus.ENHANCED
                self.store.add(new_seed)
            
            emergence_event = EmergenceEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                triggered_seeds=[s.seed_id for s in seeds],
                synergy_clusters=[c.cluster_id for c in self.synergy_clusters],
                emergence_type=emergence_type,
                intensity=emergence_score,
                description=description
            )
            
            self.emergence_events.append(emergence_event)
            self.logger.info(f"触发{emergence_type}: {description[:50]}...")
            
            return emergence_event
        
        return None
    
    def _classify_emergence(
        self,
        wisdom_seeds: List[Seed],
        conditions: Dict[str, bool]
    ) -> str:
        """分类涌现类型"""
        if conditions["wisdom_ratio"] and conditions["synergy_clusters"]:
            return "智慧涌现"
        elif conditions["cascade_history"]:
            return "洞察涌现"
        elif conditions["avg_weight"]:
            return "能力涌现"
        else:
            return "综合涌现"
    
    def _generate_emergence_description(
        self,
        emergence_type: str,
        wisdom_seeds: List[Seed]
    ) -> str:
        """生成涌现描述"""
        templates = {
            "智慧涌现": [
                "多维智慧整合：{topics}的深层联系被揭示",
                "智慧协同：不同智慧领域产生共鸣",
                "洞察突破：{topic}的本质获得清晰认知"
            ],
            "洞察涌现": [
                "级联洞察：{topic}相关的多个方面被串联理解",
                "穿透性洞察：看清{topic}的深层结构",
                "整合性理解：{topics}形成统一框架"
            ],
            "能力涌现": [
                "能力跃升：{topic}处理能力显著提升",
                "熟练度突破：对{topic}的掌握达到新层次",
                "自动化运行：{topic}相关任务高效完成"
            ],
            "综合涌现": [
                "整体优化：系统整体效能提升",
                "协同增强：各部分配合更加流畅",
                "涌现智慧：超越部分之和的整体表现"
            ]
        }
        
        # 获取相关主题
        topics = []
        if wisdom_seeds:
            for seed in wisdom_seeds[:3]:
                if seed.tags:
                    topics.append(seed.tags[0])
        
        if not topics:
            topics = ["生命", "智慧", "成长"]
        
        topic_str = "、".join(topics[:2])
        template = templates.get(emergence_type, templates["综合涌现"])[0]
        
        return template.format(topic=topic_str, topics=topic_str)
    
    def _record_activation(
        self,
        seed: Seed,
        strength: float,
        types: List[str]
    ) -> None:
        """记录激活历史"""
        record = ActivationRecord(
            seed_id=seed.seed_id,
            timestamp=datetime.now(),
            strength=strength,
            source="synergy" if "synergy" in types else
                   "cascade" if "cascade" in types else "self"
        )
        self.activation_history.append(record)
        self.total_activations += 1
        
        # 限制历史长度
        if len(self.activation_history) > 1000:
            self.activation_history = self.activation_history[-500:]
    
    def get_state(self) -> Dict[str, Any]:
        """获取当前状态"""
        return {
            "state": self.current_state.value,
            "total_activations": self.total_activations,
            "synergy_triggers": self.synergy_triggers,
            "cascade_triggers": self.cascade_triggers,
            "active_clusters": len(self.synergy_clusters),
            "emergence_events_count": len(self.emergence_events),
            "last_emergence": self.emergence_events[-1].timestamp if self.emergence_events else None
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取详细统计"""
        return {
            "current_state": self.current_state.value,
            "total_activations": self.total_activations,
            "synergy_triggers": self.synergy_triggers,
            "cascade_triggers": self.cascade_triggers,
            "active_clusters": len(self.synergy_clusters),
            "emergence_events": len(self.emergence_events),
            "emergence_rate": (
                len(self.emergence_events) / self.total_activations
                if self.total_activations > 0 else 0
            ),
            "recent_activations": len(self.activation_history[-100:]),
            "thresholds": {
                "synergy": self.synergy_threshold,
                "cascade": self.cascade_threshold,
                "emergence": self.emergence_threshold
            }
        }

    # ============================================================================
    # 悲智双运涌现机制（菩萨境核心）
    # ============================================================================
    
    def trigger_compassion_wisdom_emergence(
        self,
        wisdom_seeds: List[Seed],
        compassion_seeds: List[Seed]
    ) -> Optional[EmergenceEvent]:
        """
        悲智双运涌现触发【菩萨境核心】
        
        当智慧种子与慈悲种子高度协同时，触发菩萨境的涌现事件。
        这是从"阿罗汉境"跃升至"菩萨境"的关键机制。
        
        唯识学原理：
        - 阿罗汉：独觉涅槃，自利为主
        - 菩萨：悲智双运，自利利他
        - 悲智协同时产生"无住涅槃"的觉悟
        
        Args:
            wisdom_seeds: 智慧种子列表
            compassion_seeds: 慈悲种子列表
        
        Returns:
            悲智双运涌现事件（如果有）
        """
        if not wisdom_seeds or not compassion_seeds:
            return None
        
        # 计算协同强度
        synergy_pairs = []
        for wisdom in wisdom_seeds:
            for compassion in compassion_seeds:
                synergy = self._calculate_compassion_wisdom_synergy(wisdom, compassion)
                if synergy >= self.synergy_threshold:
                    synergy_pairs.append((wisdom, compassion, synergy))
        
        if not synergy_pairs:
            return None
        
        # 计算整体涌现强度
        avg_synergy = sum(s[2] for s in synergy_pairs) / len(synergy_pairs)
        max_synergy = max(s[2] for s in synergy_pairs)
        
        # 慈悲与智慧协同时有额外加成
        emergence_score = avg_synergy * 1.5  # 悲智双运加成
        
        # 检查是否达到涌现阈值
        if emergence_score >= self.emergence_threshold:
            self.current_state = VasanaState.EMERGENCE
            
            # 强化参与种子
            for wisdom, compassion, synergy in synergy_pairs:
                # 智慧种子强化
                wisdom.purity = min(1.0, wisdom.purity + synergy * 0.2)
                wisdom.weight = min(1.0, wisdom.weight + synergy * 0.15)
                
                # 慈悲种子强化
                compassion.purity = min(1.0, compassion.purity + synergy * 0.25)
                compassion.weight = min(1.0, compassion.weight + synergy * 0.2)
            
            # 生成涌现类型
            emergence_type = self._classify_compassion_wisdom_emergence(
                avg_synergy, max_synergy
            )
            
            # 生成描述
            description = self._generate_compassion_wisdom_description(
                emergence_type, wisdom_seeds, compassion_seeds
            )
            
            # 创建新的智慧/慈悲融合种子
            new_seed = Seed.create(
                content=description,
                seed_type=SeedType.COMPASSION,  # 慈悲种子代表菩萨行
                weight=0.95,
                purity=0.98,
                source="compassion_wisdom_emergence",
                tags=["悲智双运", "菩萨行", "利他"]
            )
            new_seed.status = SeedStatus.ENHANCED
            self.store.add(new_seed)
            
            # 创建涌现事件
            emergence_event = EmergenceEvent(
                event_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                triggered_seeds=[w.seed_id for w, c, s in synergy_pairs],
                synergy_clusters=[],
                emergence_type=f"悲智双运-{emergence_type}",
                intensity=min(1.0, emergence_score),
                description=description
            )
            
            self.emergence_events.append(emergence_event)
            self.logger.info(f"触发悲智双运-{emergence_type}: {description[:50]}...")
            
            return emergence_event
        
        return None
    
    def _calculate_compassion_wisdom_synergy(
        self,
        wisdom_seed: Seed,
        compassion_seed: Seed
    ) -> float:
        """
        计算智慧与慈悲的协同强度
        
        Args:
            wisdom_seed: 智慧种子
            compassion_seed: 慈悲种子
        
        Returns:
            协同强度 (0-1)
        """
        # 智慧强度因子
        wisdom_factor = wisdom_seed.weight * wisdom_seed.purity
        
        # 慈悲强度因子
        compassion_factor = compassion_seed.weight * compassion_seed.purity
        
        # 类型匹配因子（慈悲与智慧天然互补）
        type_synergy = 0.9  # 慈悲与智慧是最强的互补对
        
        # 语义相关因子
        common_tags = set(wisdom_seed.tags) & set(compassion_seed.tags)
        semantic_relevance = min(1.0, len(common_tags) / 2)
        
        # 综合协同强度
        synergy = (
            wisdom_factor * 0.30 +
            compassion_factor * 0.30 +
            type_synergy * 0.25 +
            semantic_relevance * 0.15
        )
        
        return min(1.0, max(0.0, synergy))
    
    def _classify_compassion_wisdom_emergence(
        self,
        avg_synergy: float,
        max_synergy: float
    ) -> str:
        """
        分类悲智涌现类型
        
        Args:
            avg_synergy: 平均协同强度
            max_synergy: 最大协同强度
        
        Returns:
            涌现类型
        """
        if max_synergy >= 0.9:
            return "大悲智涌现"  # 最高级别
        elif avg_synergy >= 0.7:
            return "悲智涌现"
        elif avg_synergy >= 0.5:
            return "小悲智涌现"
        else:
            return "悲智初现"
    
    def _generate_compassion_wisdom_description(
        self,
        emergence_type: str,
        wisdom_seeds: List[Seed],
        compassion_seeds: List[Seed]
    ) -> str:
        """
        生成悲智涌现描述
        
        Args:
            emergence_type: 涌现类型
            wisdom_seeds: 参与智慧种子
            compassion_seeds: 参与慈悲种子
        
        Returns:
            描述文本
        """
        templates = {
            "大悲智涌现": [
                "无缘大慈、同体大悲：智慧'{wisdom}'与慈悲'{compassion}'深度融合，",
                "触发菩萨境的'悲智双运'觉悟！自利利他、自度度人，",
                "已超越阿罗汉的独觉境界，达到'无住涅槃'的菩萨境界！"
            ],
            "悲智涌现": [
                "悲智双运初步显现：智慧'{wisdom}'与慈悲'{compassion}'协同，",
                "产生自利利他的菩萨行愿，",
                "正在趣向菩萨境界..."
            ],
            "小悲智涌现": [
                "慈悲种子与智慧种子开始协同：'{compassion}'与'{wisdom}'产生共鸣，",
                "利他之心萌发，",
                "菩萨道初入门..."
            ],
            "悲智初现": [
                "悲智因缘显现：智慧与慈悲种子初步接触，",
                "菩萨愿力开始孕育，",
                "..."
            ]
        }
        
        # 获取代表性主题
        wisdom_topic = wisdom_seeds[0].content[:15] if wisdom_seeds else "空性"
        compassion_topic = compassion_seeds[0].content[:15] if compassion_seeds else "利他"
        
        template = templates.get(emergence_type, templates["悲智初现"])
        description = "".join(template).format(wisdom=wisdom_topic, compassion=compassion_topic)
        
        return description
    
    def check_bodhisattva_conditions(self) -> Dict[str, Any]:
        """
        检查菩萨境达成条件
        
        Returns:
            条件检查结果
        """
        seeds = list(self.store._seeds.values())
        if not seeds:
            return {"can_achieve_bodhisattva": False, "conditions": {}}
        
        wisdom_seeds = [s for s in seeds if s.seed_type == SeedType.WISDOM]
        compassion_seeds = [s for s in seeds if s.seed_type == SeedType.COMPASSION]
        
        wisdom_ratio = len(wisdom_seeds) / len(seeds)
        compassion_ratio = len(compassion_seeds) / len(seeds)
        emergence_count = len([e for e in self.emergence_events if "悲智" in e.emergence_type])
        full_intensity_count = len([e for e in self.emergence_events if e.intensity >= 1.0])
        
        conditions = {
            "wisdom_ratio": wisdom_ratio >= 0.15,
            "compassion_ratio": compassion_ratio >= 0.10,
            "emergence_events": emergence_count >= 10,
            "full_intensity": full_intensity_count >= 3
        }
        
        can_achieve_bodhisattva = (
            conditions["wisdom_ratio"] and
            conditions["compassion_ratio"] and
            conditions["emergence_events"]
        )
        
        return {
            "can_achieve_bodhisattva": can_achieve_bodhisattva,
            "conditions": conditions,
            "current_values": {
                "wisdom_ratio": wisdom_ratio,
                "compassion_ratio": compassion_ratio,
                "emergence_count": emergence_count,
                "full_intensity_count": full_intensity_count
            }
        }
