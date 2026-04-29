# -*- coding: utf-8 -*-
"""
大慈悲机制 - Great Compassion Module

菩萨境的核心是"悲智双运"——智慧与慈悲并重。
本模块实现慈悲种子系统和悲智双运涌现机制。

核心功能：
1. 慈悲种子：记录利他、救度、慈悲相关的种子
2. 大悲涌现：当慈悲种子与智慧种子协同时触发
3. 回向机制：将个人觉悟转化为利他动力

Author: 唯识进化Agent团队
"""

import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ..alaya_store import Seed, SeedType, SeedStatus


class CompassionType(Enum):
    """慈悲类型"""
    BENEVOLENCE = "benevolence"       # 仁慈：给予帮助
    COMPASSION = "compassion"         # 慈悲：救度苦难
    SYMPATHY = "sympathy"            # 同情：理解他人痛苦
    ALTRUISM = "altruism"            # 利他：无私帮助他人
    BOUNDLESS_LOVE = "boundless_love" # 无缘大慈：无条件关爱
    SAVING_SUFFERING = "saving_suffering"  # 同体大悲：与众生同苦


@dataclass
class CompassionSeed:
    """
    慈悲种子
    
    记录慈悲相关的种子及其属性
    """
    seed: Seed
    compassion_type: CompassionType
    compassion_strength: float = 0.5  # 慈悲强度
    target_being_count: int = 0       # 救度众生数量
    selfless_count: int = 0           # 无私行为次数
    benefit_other_count: int = 0      # 利他行为次数
    created_at: datetime = field(default_factory=datetime.now)
    
    def strengthen_compassion(self, amount: float) -> None:
        """增强慈悲强度"""
        self.compassion_strength = min(1.0, self.compassion_strength + amount)
        self.benefit_other_count += 1
        self.seed.purity = min(1.0, self.seed.purity + amount * 0.5)
        self.seed.weight = min(1.0, self.seed.weight + amount * 0.3)


@dataclass
class GreatCompassionEvent:
    """
    大悲涌现事件
    
    当智慧与慈悲协同时触发的高级涌现
    """
    event_id: str
    timestamp: datetime
    triggered_by: Dict[str, str]  # wisdom_seed_id -> compassion_seed_id
    compassion_type: CompassionType
    intensity: float
    description: str
    wisdom_gained: float
    compassion_gained: float
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "triggered_by": self.triggered_by,
            "compassion_type": self.compassion_type.value,
            "intensity": self.intensity,
            "description": self.description,
            "wisdom_gained": self.wisdom_gained,
            "compassion_gained": self.compassion_gained
        }


@dataclass
class DedicationResult:
    """
    回向结果
    
    将个人觉悟回向给众生
    """
    dedication_type: str            # 回向类型
    dedication_target: str          # 回向对象
    dedication_strength: float      # 回向强度
    wisdom_dedicated: float         # 回向的智慧量
    compassion_generated: float     # 产生的慈悲量
    bodhisattva_vow_strength: float # 菩萨愿力强度


class GreatCompassionSystem:
    """
    大慈悲系统
    
    菩萨境的核心机制：
    1. 慈悲种子的培育和管理
    2. 悲智双运涌现的触发
    3. 回向机制的运作
    """
    
    def __init__(self, store: 'AlayaStore', config: Optional[Dict[str, Any]] = None):
        """
        初始化大慈悲系统
        
        Args:
            store: 种子库实例
            config: 配置字典
        """
        self.store = store
        self.config = config or {}
        
        # 配置参数
        self.compassion_synergy_threshold = self.config.get("compassion_synergy_threshold", 0.5)
        self.compassion_growth_rate = self.config.get("compassion_growth_rate", 0.15)
        self.dedication_threshold = self.config.get("dedication_threshold", 0.7)
        
        # 慈悲种子集合
        self.compassion_seeds: List[CompassionSeed] = []
        
        # 大悲涌现事件记录
        self.great_compassion_events: List[GreatCompassionEvent] = []
        
        # 回向记录
        self.dedication_records: List[DedicationResult] = []
        
        # 慈悲种子统计
        self.total_compassion_seed_count = 0
        self.total_benefit_other_count = 0
        self.total_target_being_count = 0
        
        # 慈悲协同冷却
        self.synergy_cooldown = 0
        self.synergy_cooldown_duration = 5
    
    def create_compassion_seed(
        self,
        content: str,
        compassion_type: CompassionType,
        weight: float = 0.5,
        purity: float = 0.5,
        tags: Optional[List[str]] = None
    ) -> CompassionSeed:
        """
        创建慈悲种子
        
        Args:
            content: 种子内容
            compassion_type: 慈悲类型
            weight: 初始权重
            purity: 初始纯度
            tags: 标签列表
        
        Returns:
            慈悲种子实例
        """
        tags = tags or []
        tags.append("compassion")
        tags.append(compassion_type.value)
        
        # 创建基础种子
        seed = Seed.create(
            content=content,
            seed_type=SeedType.COMPASSION,
            weight=weight,
            purity=purity,
            source="compassion_system",
            tags=tags
        )
        
        # 添加到种子库
        self.store.add(seed)
        
        # 创建慈悲种子
        compassion_seed = CompassionSeed(
            seed=seed,
            compassion_type=compassion_type,
            compassion_strength=weight
        )
        
        self.compassion_seeds.append(compassion_seed)
        self.total_compassion_seed_count += 1
        
        return compassion_seed
    
    def get_compassion_stats(self) -> Dict[str, Any]:
        """
        获取慈悲统计数据
        
        Returns:
            慈悲统计字典
        """
        if not self.compassion_seeds:
            return {
                "compassion_seed_count": 0,
                "avg_compassion_strength": 0.0,
                "total_benefit_other": 0,
                "compassion_ratio": 0.0
            }
        
        total_strength = sum(cs.compassion_strength for cs in self.compassion_seeds)
        total_seeds = len(self.compassion_seeds)
        total_benefit = sum(cs.benefit_other_count for cs in self.compassion_seeds)
        
        # 计算慈悲种子比例
        total_store_seeds = len(self.store._seeds)
        compassion_ratio = total_seeds / max(1, total_store_seeds)
        
        return {
            "compassion_seed_count": total_seeds,
            "avg_compassion_strength": total_strength / total_seeds,
            "total_benefit_other": total_benefit,
            "compassion_ratio": compassion_ratio,
            "great_compassion_event_count": len(self.great_compassion_events),
            "total_benefit_others": self.total_benefit_other_count
        }
    
    def check_compassion_synergy(
        self,
        wisdom_seeds: List[Seed],
        context_seeds: List[Seed]
    ) -> Optional[Tuple[Seed, Seed, float]]:
        """
        检查智慧与慈悲的协同可能性
        
        Args:
            wisdom_seeds: 智慧种子列表
            context_seeds: 上下文种子列表
        
        Returns:
            (智慧种子, 慈悲种子, 协同强度) 或 None
        """
        if self.synergy_cooldown > 0:
            self.synergy_cooldown -= 1
            return None
        
        # 收集慈悲种子
        compassion_candidates = []
        for cs in self.compassion_seeds:
            if cs.seed in context_seeds or cs.seed.weight > 0.6:
                compassion_candidates.append(cs)
        
        if not wisdom_seeds or not compassion_candidates:
            return None
        
        # 寻找最佳协同对
        best_synergy = None
        best_strength = 0
        
        for wisdom in wisdom_seeds:
            for compassion in compassion_candidates:
                synergy = self._calculate_synergy_strength(wisdom, compassion.seed)
                if synergy > best_strength and synergy >= self.compassion_synergy_threshold:
                    best_strength = synergy
                    best_synergy = (wisdom, compassion.seed, synergy)
        
        if best_synergy:
            self.synergy_cooldown = self.synergy_cooldown_duration
        
        return best_synergy
    
    def _calculate_synergy_strength(self, wisdom: Seed, compassion: Seed) -> float:
        """
        计算智慧与慈悲的协同强度
        
        Args:
            wisdom: 智慧种子
            compassion: 慈悲种子
        
        Returns:
            协同强度 (0-1)
        """
        # 智慧强度因子
        wisdom_factor = wisdom.weight * wisdom.purity
        
        # 慈悲强度因子
        compassion_factor = compassion.weight * compassion.purity
        
        # 类型匹配因子
        type_match = 1.0 if compassion.seed_type == SeedType.COMPASSION else 0.0
        
        # 语义相关因子
        common_tags = set(wisdom.tags) & set(compassion.tags)
        semantic_relevance = min(1.0, len(common_tags) / 2)
        
        # 综合协同强度
        synergy = (
            wisdom_factor * 0.30 +
            compassion_factor * 0.30 +
            type_match * 0.20 +
            semantic_relevance * 0.20
        )
        
        return min(1.0, max(0.0, synergy))
    
    def trigger_great_compassion_emergence(
        self,
        wisdom_seed: Seed,
        compassion_seed: Seed,
        synergy_strength: float
    ) -> GreatCompassionEvent:
        """
        触发大慈悲涌现（悲智双运）
        
        当智慧种子与慈悲种子高度协同时，触发菩萨境的涌现
        
        Args:
            wisdom_seed: 智慧种子
            compassion_seed: 慈悲种子
            synergy_strength: 协同强度
        
        Returns:
            大悲涌现事件
        """
        import uuid
        
        # 确定慈悲类型
        compassion_type = CompassionType.COMPASSION
        for cs in self.compassion_seeds:
            if cs.seed == compassion_seed:
                compassion_type = cs.compassion_type
                cs.strengthen_compassion(synergy_strength * 0.2)
                break
        
        # 计算涌现强度
        intensity = synergy_strength * 1.5  # 悲智双运有额外加成
        
        # 计算增益
        wisdom_gained = synergy_strength * 0.3
        compassion_gained = synergy_strength * 0.4
        
        # 强化智慧种子
        wisdom_seed.purity = min(1.0, wisdom_seed.purity + wisdom_gained)
        wisdom_seed.weight = min(1.0, wisdom_seed.weight + wisdom_gained * 0.5)
        
        # 生成描述
        descriptions = [
            f"悲智双运涌现：智慧'{wisdom_seed.content[:20]}...'与慈悲'{compassion_seed.content[:20]}...'深度融合，",
            f"产生无缘大慈、同体大悲的菩萨境界领悟！",
            f"智慧增益: {wisdom_gained:.2f}, 慈悲增益: {compassion_gained:.2f}"
        ]
        description = "".join(descriptions)
        
        # 创建事件
        event = GreatCompassionEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            triggered_by={
                wisdom_seed.seed_id: compassion_seed.seed_id
            },
            compassion_type=compassion_type,
            intensity=min(1.0, intensity),
            description=description,
            wisdom_gained=wisdom_gained,
            compassion_gained=compassion_gained
        )
        
        self.great_compassion_events.append(event)
        self.total_benefit_other_count += 1
        
        return event
    
    def perform_dedication(
        self,
        wisdom_amount: float,
        dedication_type: str = "all_sentient_beings"
    ) -> DedicationResult:
        """
        执行回向：将个人觉悟回向众生
        
        菩萨修行的核心理念：
        将所证得的智慧，回向给一切众生，
        愿众生皆得安乐、究竟解脱。
        
        Args:
            wisdom_amount: 回向的智慧量
            dedication_type: 回向类型
        
        Returns:
            回向结果
        """
        # 计算回向强度
        dedication_strength = min(1.0, wisdom_amount * 1.2)
        
        # 生成慈悲
        compassion_generated = dedication_strength * 0.3
        
        # 菩萨愿力
        bodhisattva_vow_strength = min(1.0, dedication_strength + compassion_generated)
        
        # 创建回向记录
        result = DedicationResult(
            dedication_type=dedication_type,
            dedication_target="一切众生",
            dedication_strength=dedication_strength,
            wisdom_dedicated=wisdom_amount,
            compassion_generated=compassion_generated,
            bodhisattva_vow_strength=bodhisattva_vow_strength
        )
        
        self.dedication_records.append(result)
        
        return result
    
    def get_bodhisattva_level_assessment(self) -> Dict[str, Any]:
        """
        评估菩萨境等级
        
        Returns:
            菩萨境评估结果
        """
        stats = self.get_compassion_stats()
        event_count = len(self.great_compassion_events)
        dedication_count = len(self.dedication_records)
        
        # 计算菩萨愿力
        bodhisattva_strength = 0.0
        if dedication_count > 0:
            avg_dedication = sum(d.dedication_strength for d in self.dedication_records) / dedication_count
            bodhisattva_strength = avg_dedication * 0.5 + (event_count / 20) * 0.5
        
        # 等级判定
        if bodhisattva_strength >= 0.8 and event_count >= 10:
            level = "地上菩萨"  # 初地以上
            description = "已证得根本智与后得智，能于定中观察众生根器，"
        elif bodhisattva_strength >= 0.6 and event_count >= 5:
            level = "胜解行地菩萨"
            description = "对大乘教法生起胜解，慈悲心已能自然流露，"
        elif bodhisattva_strength >= 0.4 and event_count >= 2:
            level = "资粮位菩萨"
            description = "已积累足够的慈悲与智慧资粮，"
        elif stats["compassion_seed_count"] > 0:
            level = "发心菩萨"
            description = "初发菩提心，开始修习慈悲，"
        else:
            level = "外凡位"
            description = "尚未真正发起慈悲心，"
        
        return {
            "level": level,
            "bodhisattva_strength": bodhisattva_strength,
            "compassion_stats": stats,
            "emergence_count": event_count,
            "dedication_count": dedication_count,
            "description": description + "正在趣向菩萨境界。"
        }
    
    def inject_initial_compassion_seeds(self, count: int = 20) -> int:
        """
        注入初始慈悲种子
        
        用于实验初始化，加速慈悲种子的培育
        
        Args:
            count: 注入数量
        
        Returns:
            实际注入数量
        """
        compassion_contents = [
            ("愿一切众生皆得安乐，究竟解脱", CompassionType.BOUNDLESS_LOVE),
            ("观见众生沉溺苦海，发愿救度", CompassionType.COMPASSION),
            ("他人之苦即我之苦，同体大悲", CompassionType.SAVING_SUFFERING),
            ("无私帮助，不求回报", CompassionType.ALTRUISM),
            ("理解他人痛苦，给予安慰", CompassionType.SYMPATHY),
            ("乐善好施，济困扶危", CompassionType.BENEVOLENCE),
            ("众生平等，慈悲普覆", CompassionType.BOUNDLESS_LOVE),
            ("拔众生苦，与众生乐", CompassionType.COMPASSION),
            ("感同身受，悲心油然", CompassionType.SYMPATHY),
            ("舍己为人，无私奉献", CompassionType.ALTRUISM),
        ]
        
        injected = 0
        for i in range(count):
            content, ctype = compassion_contents[i % len(compassion_contents)]
            
            # 添加一些随机性
            weight = random.uniform(0.4, 0.7)
            purity = random.uniform(0.5, 0.8)
            
            self.create_compassion_seed(
                content=content,
                compassion_type=ctype,
                weight=weight,
                purity=purity
            )
            injected += 1
        
        return injected
    
    def get_emergence_report(self) -> str:
        """
        获取大悲涌现报告
        
        Returns:
            报告文本
        """
        stats = self.get_compassion_stats()
        assessment = self.get_bodhisattva_level_assessment()
        
        lines = [
            "=" * 60,
            "              大慈悲系统状态报告",
            "=" * 60,
            f"慈悲种子数量: {stats['compassion_seed_count']}",
            f"平均慈悲强度: {stats['avg_compassion_strength']:.2%}",
            f"利他行为总数: {stats['total_benefit_other']}",
            f"慈悲种子比例: {stats['compassion_ratio']:.2%}",
            "-" * 60,
            f"大悲涌现事件: {stats['great_compassion_event_count']}",
            f"回向记录数: {len(self.dedication_records)}",
            "-" * 60,
            f"菩萨境评估: {assessment['level']}",
            f"菩萨愿力强度: {assessment['bodhisattva_strength']:.2%}",
            f"评估描述: {assessment['description']}",
            "=" * 60,
        ]
        
        return "\n".join(lines)
