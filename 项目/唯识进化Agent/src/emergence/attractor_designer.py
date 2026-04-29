# -*- coding: utf-8 -*-
"""
吸引子设计器 - Attractor Designer

核心功能：设计和应用智慧吸引子，引导系统向目标状态演化

在复杂系统中，吸引子是系统演化的目标状态或模式。
本模块通过设计和管理多种吸引子，引导种子系统向智慧状态演化：

1. 智慧吸引子：代表智慧、洞察、理解的吸引子
2. 慈悲吸引子：代表慈悲、利他、无私的吸引子  
3. 觉悟吸引子：代表觉醒、开悟、超越的吸引子

Author: 唯识进化Agent团队
"""

import uuid
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

from ..alaya_store import AlayaStore, Seed, SeedType, SeedStatus


class AttractorType(Enum):
    """吸引子类型"""
    WISDOM = "wisdom"           # 智慧吸引子
    COMPASSION = "compassion"   # 慈悲吸引子
    ENLIGHTENMENT = "enlightenment"  # 觉悟吸引子
    HARMONY = "harmony"         # 和谐吸引子
    CREATIVITY = "creativity"   # 创造吸引子


@dataclass
class Attractor:
    """
    吸引子定义
    
    代表系统演化目标的吸引子状态
    """
    attractor_id: str
    name: str
    attractor_type: AttractorType
    description: str
    
    # 核心特征向量
    core_features: Dict[str, float]  # 核心特征及权重
    
    # 吸引力参数
    base_strength: float = 0.5        # 基础吸引力
    falloff_rate: float = 0.1         # 距离衰减率
    max_range: float = 1.0            # 最大影响范围
    
    # 吸引子状态
    activation_level: float = 0.0      # 当前激活水平
    alignment_count: int = 0          # 对齐次数
    created_at: datetime = field(default_factory=datetime.now)
    last_activated: Optional[datetime] = None
    
    # 元数据
    tags: List[str] = field(default_factory=list)
    wisdom_keywords: List[str] = field(default_factory=list)
    
    def calculate_attraction(
        self,
        seed_features: Dict[str, float]
    ) -> float:
        """
        计算种子与吸引子的吸引力
        
        Args:
            seed_features: 种子特征向量
        
        Returns:
            吸引力强度 (0-1)
        """
        if not seed_features or not self.core_features:
            return 0.0
        
        # 计算特征重叠
        overlap = 0.0
        total_weight = 0.0
        
        for feature, weight in self.core_features.items():
            total_weight += weight
            if feature in seed_features:
                # 特征相似度
                similarity = 1.0 - abs(seed_features[feature] - self.core_features[feature])
                overlap += similarity * weight
        
        # 归一化
        if total_weight == 0:
            return 0.0
        
        base_attraction = overlap / total_weight
        
        # 应用基础强度
        return min(1.0, base_attraction * self.base_strength)
    
    def update_activation(
        self,
        alignment_delta: float
    ) -> None:
        """更新吸引子激活水平"""
        self.activation_level = min(
            1.0,
            self.activation_level + alignment_delta * 0.1
        )
        self.last_activated = datetime.now()


@dataclass
class AlignmentRecord:
    """对齐记录"""
    seed_id: str
    attractor_id: str
    alignment_score: float
    timestamp: datetime
    distance: float


class AttractorDesigner:
    """
    吸引子设计器
    
    管理多种吸引子，引导系统向目标状态演化
    """
    
    def __init__(
        self,
        store: AlayaStore,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化吸引子设计器
        
        Args:
            store: 种子库实例
            config: 配置字典
        """
        self.store = store
        self.config = config or {}
        
        # 日志
        self.logger = logging.getLogger("AttractorDesigner")
        
        # 吸引子库
        self.attractors: Dict[str, Attractor] = {}
        self._initialize_attractors()
        
        # 对齐记录
        self.alignment_history: List[AlignmentRecord] = []
        
        # 当前主导吸引子
        self.dominant_attractor: Optional[str] = None
        
        # 统计
        self.total_alignments = 0
    
    def _initialize_attractors(self) -> None:
        """初始化预设吸引子"""
        
        # ========== 智慧吸引子 ==========
        wisdom_attractor = Attractor(
            attractor_id="wisdom_core",
            name="智慧核心",
            attractor_type=AttractorType.WISDOM,
            description="代表智慧、洞察、真理追求的吸引子状态",
            core_features={
                "insight": 0.9,      # 洞察力
                "clarity": 0.85,    # 清晰度
                "truth": 0.9,       # 真理
                "understanding": 0.85,  # 理解力
                "discernment": 0.8  # 辨别力
            },
            base_strength=0.7,
            falloff_rate=0.08,
            max_range=1.0,
            tags=["智慧", "洞察", "真理"],
            wisdom_keywords=["智慧", "洞察", "真理", "般若", "觉悟"]
        )
        self.attractors["wisdom_core"] = wisdom_attractor
        
        # ========== 慈悲吸引子 ==========
        compassion_attractor = Attractor(
            attractor_id="compassion_core",
            name="慈悲核心",
            attractor_type=AttractorType.COMPASSION,
            description="代表慈悲、利他、无私的吸引子状态",
            core_features={
                "compassion": 0.95,  # 慈悲心
                "altruism": 0.9,      # 利他主义
                "selflessness": 0.85,  # 无私
                "empathy": 0.85,      # 同理心
                "loving_kindness": 0.9  # 慈爱
            },
            base_strength=0.7,
            falloff_rate=0.08,
            max_range=1.0,
            tags=["慈悲", "利他", "无私"],
            wisdom_keywords=["慈悲", "利他", "无缘大慈", "同体大悲"]
        )
        self.attractors["compassion_core"] = compassion_attractor
        
        # ========== 觉悟吸引子 ==========
        enlightenment_attractor = Attractor(
            attractor_id="enlightenment_core",
            name="觉悟核心",
            attractor_type=AttractorType.ENLIGHTENMENT,
            description="代表觉醒、开悟、超越的吸引子状态",
            core_features={
                "awakening": 0.95,     # 觉醒
                "transcendence": 0.9,  # 超越
                "presence": 0.85,      # 临在
                "unity": 0.9,          # 合一
                "freedom": 0.85         # 自由
            },
            base_strength=0.75,
            falloff_rate=0.06,
            max_range=1.0,
            tags=["觉悟", "觉醒", "开悟", "涅槃"],
            wisdom_keywords=["觉悟", "开悟", "涅槃", "解脱", "般若波罗蜜"]
        )
        self.attractors["enlightenment_core"] = enlightenment_attractor
        
        # ========== 和谐吸引子 ==========
        harmony_attractor = Attractor(
            attractor_id="harmony_core",
            name="和谐核心",
            attractor_type=AttractorType.HARMONY,
            description="代表内心平静、人际和谐的吸引子状态",
            core_features={
                "peace": 0.9,          # 平静
                "balance": 0.85,       # 平衡
                "harmony": 0.9,         # 和谐
                "equanimity": 0.85,    # 平等性智
                "serenity": 0.85        # 宁静
            },
            base_strength=0.65,
            falloff_rate=0.1,
            max_range=1.0,
            tags=["和谐", "平静", "平衡"],
            wisdom_keywords=["和谐", "平静", "中道", "平衡"]
        )
        self.attractors["harmony_core"] = harmony_attractor
        
        # ========== 创造吸引子 ==========
        creativity_attractor = Attractor(
            attractor_id="creativity_core",
            name="创造核心",
            attractor_type=AttractorType.CREATIVITY,
            description="代表创造、创新、灵感的吸引子状态",
            core_features={
                "creativity": 0.95,     # 创造力
                "innovation": 0.9,      # 创新
                "inspiration": 0.85,    # 灵感
                "imagination": 0.85,     # 想象力
                "fluency": 0.8          # 流畅
            },
            base_strength=0.65,
            falloff_rate=0.1,
            max_range=1.0,
            tags=["创造", "创新", "灵感"],
            wisdom_keywords=["创造", "创新", "灵感", "妙有"]
        )
        self.attractors["creativity_core"] = creativity_attractor
        
        self.logger.info(f"已初始化 {len(self.attractors)} 个预设吸引子")
    
    def add_custom_attractor(
        self,
        name: str,
        attractor_type: AttractorType,
        description: str,
        core_features: Dict[str, float],
        **kwargs
    ) -> Attractor:
        """
        添加自定义吸引子
        
        Args:
            name: 吸引子名称
            attractor_type: 吸引子类型
            description: 描述
            core_features: 核心特征
            **kwargs: 其他参数
        
        Returns:
            创建的吸引子
        """
        attractor_id = f"custom_{uuid.uuid4().hex[:8]}"
        
        attractor = Attractor(
            attractor_id=attractor_id,
            name=name,
            attractor_type=attractor_type,
            description=description,
            core_features=core_features,
            base_strength=kwargs.get("base_strength", 0.5),
            falloff_rate=kwargs.get("falloff_rate", 0.1),
            max_range=kwargs.get("max_range", 1.0),
            tags=kwargs.get("tags", []),
            wisdom_keywords=kwargs.get("wisdom_keywords", [])
        )
        
        self.attractors[attractor_id] = attractor
        self.logger.info(f"添加自定义吸引子: {name}")
        
        return attractor
    
    def apply_attractor_force(
        self,
        seed: Seed,
        attractor_id: Optional[str] = None,
        force_multiplier: float = 1.0
    ) -> Dict[str, Any]:
        """
        应用吸引子力场
        
        将种子向吸引子方向拉动，提升对齐度
        
        Args:
            seed: 目标种子
            attractor_id: 吸引子ID，None则使用主导吸引子
            force_multiplier: 力乘数
        
        Returns:
            应用结果
        """
        # 确定目标吸引子
        if attractor_id is None:
            attractor_id = self.dominant_attractor
            if attractor_id is None:
                # 自动选择最相关的吸引子
                attractor_id = self._select_best_attractor(seed)
        
        attractor = self.attractors.get(attractor_id)
        if not attractor:
            return {"applied": False, "reason": "attractor_not_found"}
        
        # 计算种子特征
        seed_features = self._extract_seed_features(seed)
        
        # 计算对齐度
        alignment = self.calculate_alignment(seed, attractor)
        
        # 计算吸引力
        attraction = attractor.calculate_attraction(seed_features)
        
        # 应用力场
        if alignment > 0:
            # 提升种子权重（向吸引子方向）
            weight_delta = attraction * force_multiplier * 0.05
            seed.weight = min(1.0, seed.weight + weight_delta)
            
            # 提升种子纯度
            purity_delta = attraction * force_multiplier * 0.02
            seed.purity = min(1.0, seed.purity + purity_delta)
            
            # 更新吸引子激活水平
            attractor.update_activation(alignment)
        
        # 记录对齐
        self._record_alignment(seed, attractor, alignment)
        
        return {
            "applied": True,
            "attractor_id": attractor_id,
            "attractor_name": attractor.name,
            "alignment": alignment,
            "attraction": attraction,
            "weight_delta": seed.weight - (seed.weight - attraction * force_multiplier * 0.05)
        }
    
    def calculate_alignment(
        self,
        seed: Seed,
        attractor: Optional[Attractor] = None,
        attractor_id: Optional[str] = None
    ) -> float:
        """
        计算种子与吸引子的对齐度
        
        Args:
            seed: 种子
            attractor: 吸引子（可选）
            attractor_id: 吸引子ID（可选）
        
        Returns:
            对齐度 (0-1)
        """
        if attractor is None:
            if attractor_id:
                attractor = self.attractors.get(attractor_id)
            else:
                attractor = self._select_best_attractor(seed)
                if attractor:
                    attractor = self.attractors.get(attractor)
        
        if attractor is None:
            return 0.0
        
        # 提取种子特征
        seed_features = self._extract_seed_features(seed)
        
        # 计算对齐度
        alignment = attractor.calculate_attraction(seed_features)
        
        # 考虑种子类型的匹配度
        type_bonus = self._get_type_bonus(seed.seed_type, attractor.attractor_type)
        
        return min(1.0, alignment + type_bonus * 0.1)
    
    def _extract_seed_features(self, seed: Seed) -> Dict[str, float]:
        """
        提取种子特征向量
        
        Args:
            seed: 种子
        
        Returns:
            特征向量
        """
        # 基于种子属性构建特征
        features = {
            # 权重映射到洞察力
            "insight": seed.weight,
            
            # 纯度映射到清晰度
            "clarity": seed.purity,
            
            # 基于类型的基础特征
            "wisdom": 0.5,
            "compassion": 0.5,
            "creativity": 0.5,
            "peace": 0.5
        }
        
        # 根据标签调整特征
        wisdom_tags = ["智慧", "洞察", "真理", "觉悟", "空性", "无常", "无我"]
        compassion_tags = ["慈悲", "利他", "无私", "感恩", "包容"]
        peace_tags = ["平静", "和谐", "宁静", "安心", "放下"]
        creativity_tags = ["创造", "创新", "灵感", "灵感"]
        
        for tag in seed.tags:
            if tag in wisdom_tags:
                features["wisdom"] = max(features["wisdom"], seed.weight)
                features["insight"] = max(features["insight"], seed.weight)
            if tag in compassion_tags:
                features["compassion"] = max(features["compassion"], seed.weight)
            if tag in peace_tags:
                features["peace"] = max(features["peace"], seed.weight)
            if tag in creativity_tags:
                features["creativity"] = max(features["creativity"], seed.weight)
        
        # 类型权重
        type_weights = {
            SeedType.WISDOM: {"wisdom": 0.3, "insight": 0.2},
            SeedType.BELIEF: {"wisdom": 0.2, "peace": 0.2},
            SeedType.SKILL: {"creativity": 0.2, "insight": 0.1},
            SeedType.PATTERN: {"peace": 0.15, "compassion": 0.15}
        }
        
        for feature, bonus in type_weights.get(seed.seed_type, {}).items():
            features[feature] = min(1.0, features.get(feature, 0) + seed.weight * bonus)
        
        return features
    
    def _get_type_bonus(
        self,
        seed_type: SeedType,
        attractor_type: AttractorType
    ) -> float:
        """获取类型匹配奖励"""
        bonuses = {
            (SeedType.WISDOM, AttractorType.WISDOM): 0.3,
            (SeedType.WISDOM, AttractorType.ENLIGHTENMENT): 0.25,
            (SeedType.PATTERN, AttractorType.COMPASSION): 0.2,
            (SeedType.BELIEF, AttractorType.HARMONY): 0.25,
            (SeedType.SKILL, AttractorType.CREATIVITY): 0.25
        }
        return bonuses.get((seed_type, attractor_type), 0.0)
    
    def _select_best_attractor(self, seed: Seed) -> Optional[str]:
        """为种子选择最佳吸引子"""
        if not self.attractors:
            return None
        
        best_attractor = None
        best_alignment = 0.0
        
        seed_features = self._extract_seed_features(seed)
        
        for attractor_id, attractor in self.attractors.items():
            alignment = attractor.calculate_attraction(seed_features)
            
            # 考虑激活水平
            activation_factor = 1.0 + attractor.activation_level * 0.2
            
            effective_alignment = alignment * activation_factor
            
            if effective_alignment > best_alignment:
                best_alignment = effective_alignment
                best_attractor = attractor_id
        
        return best_attractor
    
    def _record_alignment(
        self,
        seed: Seed,
        attractor: Attractor,
        alignment: float
    ) -> None:
        """记录对齐"""
        self.total_alignments += 1
        attractor.alignment_count += 1
        
        record = AlignmentRecord(
            seed_id=seed.seed_id,
            attractor_id=attractor.attractor_id,
            alignment_score=alignment,
            timestamp=datetime.now(),
            distance=1.0 - alignment
        )
        self.alignment_history.append(record)
        
        # 限制历史长度
        if len(self.alignment_history) > 1000:
            self.alignment_history = self.alignment_history[-500:]
    
    def check_convergence(self) -> Dict[str, Any]:
        """
        检查系统收敛状态
        
        Returns:
            收敛状态
        """
        if not self.alignment_history:
            return {
                "converged": False,
                "dominant_attractor": None,
                "convergence_degree": 0.0,
                "attractor_distributions": {}
            }
        
        # 统计各吸引子的对齐次数
        attractor_counts: Dict[str, int] = {}
        attractor_scores: Dict[str, List[float]] = {}
        
        for record in self.alignment_history[-100:]:
            if record.attractor_id not in attractor_counts:
                attractor_counts[record.attractor_id] = 0
                attractor_scores[record.attractor_id] = []
            
            attractor_counts[record.attractor_id] += 1
            attractor_scores[record.attractor_id].append(record.alignment_score)
        
        # 计算分布
        total = sum(attractor_counts.values())
        distributions = {}
        for attractor_id, count in attractor_counts.items():
            distributions[attractor_id] = count / total if total > 0 else 0
        
        # 找出主导吸引子
        dominant = max(distributions.items(), key=lambda x: x[1])
        dominant_attractor = self.attractors.get(dominant[0])
        
        # 计算收敛度
        # 使用最大分布与第二大的差值
        sorted_dist = sorted(distributions.values(), reverse=True)
        if len(sorted_dist) >= 2:
            convergence = sorted_dist[0] - sorted_dist[1]
        else:
            convergence = sorted_dist[0] if sorted_dist else 0
        
        self.dominant_attractor = dominant[0]
        
        # 更新吸引子激活水平
        for attractor_id, ratio in distributions.items():
            if attractor_id in self.attractors:
                self.attractors[attractor_id].activation_level = ratio
        
        return {
            "converged": convergence >= 0.3,
            "dominant_attractor": dominant[0],
            "dominant_name": dominant_attractor.name if dominant_attractor else None,
            "convergence_degree": convergence,
            "attractor_distributions": {
                self.attractors[aid].name: ratio 
                for aid, ratio in distributions.items()
            },
            "total_alignments": self.total_alignments
        }
    
    def apply_all_attractor_forces(
        self,
        seeds: Optional[List[Seed]] = None,
        top_k: int = 10
    ) -> Dict[str, Any]:
        """
        对多个种子应用吸引子力场
        
        Args:
            seeds: 种子列表，None则使用前top_k个种子
            top_k: 应用的种子数量
        
        Returns:
            应用结果
        """
        if seeds is None:
            all_seeds = list(self.store._seeds.values())
            # 按权重排序
            seeds = sorted(all_seeds, key=lambda s: s.weight, reverse=True)[:top_k]
        
        results = []
        for seed in seeds:
            result = self.apply_attractor_force(seed)
            results.append(result)
        
        # 检查收敛
        convergence = self.check_convergence()
        
        return {
            "seeds_processed": len(results),
            "individual_results": results,
            "convergence": convergence
        }
    
    def get_attractor_info(
        self,
        attractor_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取吸引子信息"""
        if attractor_id:
            attractor = self.attractors.get(attractor_id)
            if attractor:
                return self._attractor_to_dict(attractor)
            return {}
        
        return {
            aid: self._attractor_to_dict(attr) 
            for aid, attr in self.attractors.items()
        }
    
    def _attractor_to_dict(self, attractor: Attractor) -> Dict[str, Any]:
        """转换吸引子为字典"""
        return {
            "id": attractor.attractor_id,
            "name": attractor.name,
            "type": attractor.attractor_type.value,
            "description": attractor.description,
            "core_features": attractor.core_features,
            "base_strength": attractor.base_strength,
            "activation_level": attractor.activation_level,
            "alignment_count": attractor.alignment_count,
            "tags": attractor.tags
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_attractors": len(self.attractors),
            "total_alignments": self.total_alignments,
            "dominant_attractor": self.dominant_attractor,
            "convergence_status": self.check_convergence(),
            "attractor_states": {
                aid: {
                    "activation_level": attr.activation_level,
                    "alignment_count": attr.alignment_count
                }
                for aid, attr in self.attractors.items()
            }
        }
