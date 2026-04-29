# -*- coding: utf-8 -*-
"""
智慧涌现扩展模块 - Wisdom Emergence Extension

为 NonlinearVasana 添加更完整的智慧涌现机制

核心功能：
1. 智慧种子相互吸引机制
2. 多类型涌现触发逻辑
3. 与 EmergenceObserver 的深度集成

Author: 唯识进化Agent团队
"""

from typing import Dict, List, Any, Optional, TYPE_CHECKING
from collections import defaultdict
import logging

if TYPE_CHECKING:
    from ..alaya_store import Seed, SeedType, SeedStatus, AlayaStore
    from .emergence_observer import EmergenceObserver, EmergenceType


class WisdomEmergenceExtension:
    """
    智慧涌现扩展
    
    为种子协同系统添加智慧涌现的高级功能
    """
    
    def __init__(self, vasana: 'NonlinearVasana'):
        """
        初始化扩展
        
        Args:
            vasana: NonlinearVasana 实例
        """
        self.vasana = vasana
        self.logger = logging.getLogger("WisdomEmergence")
        
        # 协同候选池
        self.synergy_candidates: List[str] = []
        
        # 涌现冷却期
        self.emergence_cooldown = 0
        self.cooldown_duration = 3  # 3次迭代冷却
    
    def calculate_wisdom_attraction(
        self,
        seed1: 'Seed',
        seed2: 'Seed'
    ) -> float:
        """
        计算智慧种子之间的相互吸引力
        
        Args:
            seed1: 种子1
            seed2: 种子2
        
        Returns:
            吸引力强度 (0-1)
        """
        # 1. 智慧权重因子
        wisdom_weight_factor = (seed1.weight + seed2.weight) / 2
        
        # 2. 类型匹配因子
        if seed1.seed_type == seed2.seed_type:
            type_match = 1.0
        elif self._are_complementary_types(seed1.seed_type, seed2.seed_type):
            type_match = 0.8
        else:
            type_match = 0.3
        
        # 3. 语义相关因子
        common_tags = set(seed1.tags) & set(seed2.tags)
        semantic_relevance = min(1.0, len(common_tags) / 3)
        
        # 4. 纯度因子
        purity_factor = (seed1.purity + seed2.purity) / 2
        
        # 综合吸引力
        attraction = (
            wisdom_weight_factor * 0.25 +
            type_match * 0.30 +
            semantic_relevance * 0.25 +
            purity_factor * 0.20
        )
        
        return min(1.0, max(0.0, attraction))
    
    def _are_complementary_types(
        self,
        type1: 'SeedType',
        type2: 'SeedType'
    ) -> bool:
        """判断两种子类型是否互补"""
        from ..alaya_store import SeedType
        complementary_pairs = [
            (SeedType.WISDOM, SeedType.KNOWLEDGE),
            (SeedType.WISDOM, SeedType.EXPERIENCE),
            (SeedType.KNOWLEDGE, SeedType.PATTERN),
            (SeedType.EXPERIENCE, SeedType.PATTERN),
            (SeedType.BELIEF, SeedType.SKILL),
        ]
        return (type1, type2) in complementary_pairs or (type2, type1) in complementary_pairs
    
    def find_synergy_opportunities(
        self,
        seeds: List['Seed'],
        min_attraction: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        寻找协同机会
        
        Args:
            seeds: 可参与协同的种子列表
            min_attraction: 最小吸引力阈值
        
        Returns:
            协同机会列表
        """
        opportunities = []
        
        for i, seed1 in enumerate(seeds):
            for seed2 in seeds[i+1:]:
                attraction = self.calculate_wisdom_attraction(seed1, seed2)
                if attraction >= min_attraction:
                    opportunities.append({
                        "seed1_id": seed1.seed_id,
                        "seed2_id": seed2.seed_id,
                        "attraction": attraction,
                        "seed1_type": seed1.seed_type.value,
                        "seed2_type": seed2.seed_type.value
                    })
        
        # 按吸引力排序
        opportunities.sort(key=lambda x: x["attraction"], reverse=True)
        return opportunities
    
    def trigger_emergence(
        self,
        seeds: List['Seed'],
        observer: Optional['EmergenceObserver'] = None
    ) -> Optional[Dict[str, Any]]:
        """
        触发智慧涌现
        
        Args:
            seeds: 参与涌现的种子列表
            observer: 可选的观测系统
        
        Returns:
            涌现结果
        """
        from ..alaya_store import SeedType, SeedStatus
        
        if len(seeds) < 2:
            return None
        
        # 检查冷却期
        if self.emergence_cooldown > 0:
            self.emergence_cooldown -= 1
            return None
        
        # 分类种子
        by_type: Dict[SeedType, List[Seed]] = defaultdict(list)
        for seed in seeds:
            by_type[seed.seed_type].append(seed)
        
        # 1. 洞察涌现（经验+知识）
        insight_seeds = by_type.get(SeedType.EXPERIENCE, []) + by_type.get(SeedType.KNOWLEDGE, [])
        if len(insight_seeds) >= 2:
            result = self._trigger_insight_emergence(insight_seeds, observer)
            if result:
                self.emergence_cooldown = self.cooldown_duration
                return result
        
        # 2. 模式涌现（模式+信念）
        pattern_seeds = by_type.get(SeedType.PATTERN, []) + by_type.get(SeedType.BELIEF, [])
        if len(pattern_seeds) >= 2:
            result = self._trigger_pattern_emergence(pattern_seeds, observer)
            if result:
                self.emergence_cooldown = self.cooldown_duration
                return result
        
        # 3. 智慧涌现（跨类型）
        wisdom_seeds = by_type.get(SeedType.WISDOM, [])
        if len(wisdom_seeds) >= 1 and len(seeds) >= 3:
            result = self._trigger_wisdom_emergence(seeds, wisdom_seeds, observer)
            if result:
                self.emergence_cooldown = self.cooldown_duration
                return result
        
        # 4. 整合涌现（多类型）
        if len(by_type) >= 3:
            result = self._trigger_integration_emergence(seeds, by_type, observer)
            if result:
                self.emergence_cooldown = self.cooldown_duration
                return result
        
        return None
    
    def _trigger_insight_emergence(
        self,
        seeds: List['Seed'],
        observer: Optional['EmergenceObserver'] = None
    ) -> Optional[Dict[str, Any]]:
        """触发洞察涌现"""
        from ..alaya_store import SeedType, SeedStatus, Seed
        from .emergence_observer import EmergenceType
        
        total_strength = sum(s.weight * s.purity for s in seeds) / len(seeds)
        
        if total_strength < self.vasana.emergence_threshold * 0.8:
            return None
        
        # 提取主题
        themes = []
        for seed in seeds[:3]:
            themes.extend(seed.tags[:2])
        theme_str = "、".join(themes[:4]) if themes else "生命智慧"
        
        content = f"洞察涌现：{theme_str}的深层联系被发现，多个经验相互印证形成新的理解框架"
        
        # 创建新种子
        new_seed = Seed.create(
            content=content,
            seed_type=SeedType.WISDOM,
            weight=total_strength * 1.2,
            purity=0.9,
            source="insight_emergence",
            tags=["洞察涌现", theme_str[:4] if theme_str else "智慧"],
            experience_context=f"由{len(seeds)}个经验/知识种子协同产生"
        )
        new_seed.status = SeedStatus.ENHANCED
        self.vasana.store.add(new_seed)
        
        # 强化参与种子
        for seed in seeds:
            seed.weight = min(1.0, seed.weight + 0.1)
            seed.purity = min(1.0, seed.purity + 0.05)
        
        result = {
            "type": "insight",
            "intensity": total_strength,
            "new_seed_id": new_seed.seed_id,
            "description": content,
            "participants": [s.seed_id for s in seeds]
        }
        
        if observer:
            observer.record_emergence(
                emergence_type=EmergenceType.INSIGHT,
                participant_seeds=[s.seed_id for s in seeds] + [new_seed.seed_id],
                participant_types=[s.seed_type.value for s in seeds] + ["wisdom"],
                intensity=total_strength,
                description=content
            )
        
        self.logger.info(f"洞察涌现: {content[:60]}...")
        return result
    
    def _trigger_pattern_emergence(
        self,
        seeds: List['Seed'],
        observer: Optional['EmergenceObserver'] = None
    ) -> Optional[Dict[str, Any]]:
        """触发模式涌现"""
        from ..alaya_store import SeedType, SeedStatus, Seed
        from .emergence_observer import EmergenceType
        
        total_strength = sum(s.weight for s in seeds) / len(seeds)
        
        if total_strength < self.vasana.emergence_threshold * 0.75:
            return None
        
        pattern_types = [s.tags[0] if s.tags else "行为" for s in seeds[:2]]
        content = f"模式涌现：发现'{pattern_types[0] if pattern_types else '行为'}'与'{pattern_types[1] if len(pattern_types)>1 else '思维'}'之间的深层关联"
        
        new_seed = Seed.create(
            content=content,
            seed_type=SeedType.WISDOM,
            weight=total_strength * 1.3,
            purity=0.92,
            source="pattern_emergence",
            tags=["模式涌现", "规律发现"],
            experience_context=f"由{len(seeds)}个模式/信念种子协同产生"
        )
        new_seed.status = SeedStatus.ENHANCED
        self.vasana.store.add(new_seed)
        
        result = {
            "type": "pattern",
            "intensity": total_strength,
            "new_seed_id": new_seed.seed_id,
            "description": content,
            "participants": [s.seed_id for s in seeds]
        }
        
        if observer:
            observer.record_emergence(
                emergence_type=EmergenceType.PATTERN,
                participant_seeds=[s.seed_id for s in seeds] + [new_seed.seed_id],
                participant_types=[s.seed_type.value for s in seeds] + ["wisdom"],
                intensity=total_strength,
                description=content
            )
        
        self.logger.info(f"模式涌现: {content[:60]}...")
        return result
    
    def _trigger_wisdom_emergence(
        self,
        all_seeds: List['Seed'],
        wisdom_seeds: List['Seed'],
        observer: Optional['EmergenceObserver'] = None
    ) -> Optional[Dict[str, Any]]:
        """触发智慧涌现"""
        from ..alaya_store import SeedType, SeedStatus, Seed
        from .emergence_observer import EmergenceType
        
        wisdom_strength = sum(s.weight for s in wisdom_seeds) / len(wisdom_seeds)
        context_strength = sum(s.weight for s in all_seeds if s not in wisdom_seeds) / max(1, len(all_seeds) - len(wisdom_seeds))
        combined_strength = wisdom_strength * 0.7 + context_strength * 0.3
        
        if combined_strength < self.vasana.emergence_threshold:
            return None
        
        wisdom_topics = []
        for seed in wisdom_seeds[:2]:
            if seed.tags:
                wisdom_topics.append(seed.tags[0])
            elif seed.content:
                wisdom_topics.append(seed.content[:5])
        
        topic_str = "、".join(wisdom_topics) if wisdom_topics else "存在本质"
        content = f"智慧涌现：'{topic_str}'的核心真谛被领悟，超越表象触及本质，获得清净无染的智慧"
        
        new_seed = Seed.create(
            content=content,
            seed_type=SeedType.WISDOM,
            weight=0.95,
            purity=0.98,
            source="wisdom_emergence",
            tags=["智慧涌现", topic_str[:4], "觉醒"],
            experience_context=f"由{len(wisdom_seeds)}个智慧种子与{len(all_seeds)-len(wisdom_seeds)}个辅助种子协同产生"
        )
        new_seed.status = SeedStatus.ENHANCED
        self.vasana.store.add(new_seed)
        
        result = {
            "type": "wisdom",
            "intensity": combined_strength,
            "new_seed_id": new_seed.seed_id,
            "description": content,
            "participants": [s.seed_id for s in all_seeds],
            "quality": "high"
        }
        
        if observer:
            observer.record_emergence(
                emergence_type=EmergenceType.WISDOM,
                participant_seeds=[s.seed_id for s in all_seeds] + [new_seed.seed_id],
                participant_types=[s.seed_type.value for s in all_seeds] + ["wisdom"],
                intensity=combined_strength,
                description=content,
                context={"quality": "high", "wisdom_count": len(wisdom_seeds)}
            )
        
        self.logger.info(f"智慧涌现: {content[:60]}...")
        return result
    
    def _trigger_integration_emergence(
        self,
        seeds: List['Seed'],
        by_type: Dict,
        observer: Optional['EmergenceObserver'] = None
    ) -> Optional[Dict[str, Any]]:
        """触发整合涌现"""
        from ..alaya_store import SeedType, SeedStatus, Seed
        from .emergence_observer import EmergenceType
        
        avg_strength = sum(s.weight for s in seeds) / len(seeds)
        
        if avg_strength < self.vasana.emergence_threshold * 0.6:
            return None
        
        type_diversity = len(by_type)
        types_str = "、".join([t.value for t in list(by_type.keys())[:3]])
        content = f"整合涌现：跨越{types_str}的多维认知整合，形成统一和谐的智慧体系"
        
        new_seed = Seed.create(
            content=content,
            seed_type=SeedType.WISDOM,
            weight=avg_strength * 1.1,
            purity=0.88,
            source="integration_emergence",
            tags=["整合涌现", "系统整合"],
            experience_context=f"整合{type_diversity}种类型共{len(seeds)}个种子"
        )
        new_seed.status = SeedStatus.ENHANCED
        self.vasana.store.add(new_seed)
        
        result = {
            "type": "integration",
            "intensity": avg_strength,
            "new_seed_id": new_seed.seed_id,
            "description": content,
            "participants": [s.seed_id for s in seeds],
            "type_diversity": type_diversity
        }
        
        if observer:
            observer.record_emergence(
                emergence_type=EmergenceType.INTEGRATION,
                participant_seeds=[s.seed_id for s in seeds] + [new_seed.seed_id],
                participant_types=[s.seed_type.value for s in seeds] + ["wisdom"],
                intensity=avg_strength,
                description=content
            )
        
        self.logger.info(f"整合涌现: {content[:60]}...")
        return result
