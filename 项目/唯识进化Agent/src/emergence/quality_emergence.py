# -*- coding: utf-8 -*-
"""
涌现质量评估系统 - Emergence Quality Assessment System

核心创新：
1. 多维度质量评估：原创性、深刻性、实用性、相关性、整合性
2. 种子生态关系网络：相生、相克、协同关系
3. 质量引导的涌现生成

涌现质量评估维度：
- 原创性(Novelty): 与现有种子的语义距离
- 深刻性(Depth): 对本质的洞察程度
- 实用性(Utility): 解决问题的实际价值
- 相关性(Relevance): 与当前情境的匹配度
- 整合性(Integration): 跨领域整合能力

Author: 唯识进化Agent团队
"""

import uuid
import math
import random
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from collections import defaultdict


class QualityDimension(Enum):
    """质量维度枚举"""
    NOVELTY = "novelty"           # 原创性
    DEPTH = "depth"               # 深刻性
    UTILITY = "utility"           # 实用性
    RELEVANCE = "relevance"       # 相关性
    INTEGRATION = "integration"   # 整合性


@dataclass
class QualityScore:
    """质量评分"""
    novelty: float = 0.5          # 原创性 0-1
    depth: float = 0.5            # 深刻性 0-1
    utility: float = 0.5          # 实用性 0-1
    relevance: float = 0.5        # 相关性 0-1
    integration: float = 0.5      # 整合性 0-1
    
    # 综合分数（加权平均）
    def weighted_score(self) -> float:
        """计算综合质量分数"""
        weights = {
            "novelty": 0.25,      # 原创性权重
            "depth": 0.25,        # 深刻性权重
            "utility": 0.20,      # 实用性权重
            "relevance": 0.15,    # 相关性权重
            "integration": 0.15   # 整合性权重
        }
        return (
            self.novelty * weights["novelty"] +
            self.depth * weights["depth"] +
            self.utility * weights["utility"] +
            self.relevance * weights["relevance"] +
            self.integration * weights["integration"]
        )
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "novelty": self.novelty,
            "depth": self.depth,
            "utility": self.utility,
            "relevance": self.relevance,
            "integration": self.integration,
            "weighted_score": self.weighted_score()
        }


@dataclass
class SeedRelationship:
    """种子关系"""
    seed1_id: str
    seed2_id: str
    relationship_type: str  # mutually_generating(相生), conflicting(相克), synergistic(协同), neutral
    strength: float = 0.5  # 关系强度 0-1
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "seed1_id": self.seed1_id,
            "seed2_id": self.seed2_id,
            "relationship_type": self.relationship_type,
            "strength": self.strength,
            "description": self.description
        }


@dataclass
class QualityEmergence:
    """高质量涌现"""
    emergence_id: str
    content: str
    quality_score: QualityScore
    participant_seeds: List[str]
    emergence_type: str
    timestamp: datetime
    insight_tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "emergence_id": self.emergence_id,
            "content": self.content,
            "quality_score": self.quality_score.to_dict(),
            "participant_seeds": self.participant_seeds,
            "emergence_type": self.emergence_type,
            "timestamp": self.timestamp.isoformat(),
            "insight_tags": self.insight_tags
        }


class SeedEcosystem:
    """
    种子生态系统 - 管理种子之间的关系网络
    
    核心功能：
    1. 种子关系建模：相生、相克、协同
    2. 关系强度动态调整
    3. 协同涌现检测
    4. 生态系统健康度评估
    """
    
    # 关系类型
    MUTUALLY_GENERATING = "mutually_generating"  # 相生
    CONFLICTING = "conflicting"                   # 相克
    SYNERGISTIC = "synergistic"                   # 协同
    NEUTRAL = "neutral"                           # 中性
    
    # 关键词匹配规则
    RELATIONSHIP_PATTERNS = {
        # 相生关系（真生善，善生美等）
        "mutually_generating": [
            ("truth", "goodness"), ("truth", "compassion"),
            ("goodness", "beauty"), ("compassion", "wisdom"),
            ("wisdom", "truth"), ("beauty", "goodness"),
        ],
        # 相克关系
        "conflicting": [
            ("wisdom", "trauma"), ("compassion", "fear"),
            ("truth", "delusion"), ("beauty", "greed"),
        ]
    }
    
    def __init__(self):
        """初始化种子生态系统"""
        self.relationships: List[SeedRelationship] = []
        self.seed_network: Dict[str, Set[str]] = defaultdict(set)  # seed_id -> related_seeds
        self.ecosystem_health = 1.0
        
        # 统计
        self.stats = {
            "total_relationships": 0,
            "mutually_generating_count": 0,
            "synergistic_count": 0,
            "conflicting_count": 0,
            "network_density": 0.0,
            "ecosystem_health": 1.0
        }
    
    def add_seed(self, seed_id: str, seed_type: str) -> None:
        """添加种子到生态系统"""
        if seed_id not in self.seed_network:
            self.seed_network[seed_id] = set()
    
    def create_relationship(
        self,
        seed1_id: str,
        seed2_id: str,
        relationship_type: str,
        strength: float = 0.5,
        description: str = ""
    ) -> SeedRelationship:
        """创建种子关系"""
        # 检查是否已存在关系
        existing = self._find_relationship(seed1_id, seed2_id)
        if existing:
            # 更新强度
            existing.strength = max(existing.strength, strength)
            return existing
        
        relationship = SeedRelationship(
            seed1_id=seed1_id,
            seed2_id=seed2_id,
            relationship_type=relationship_type,
            strength=strength,
            description=description
        )
        
        self.relationships.append(relationship)
        self.seed_network[seed1_id].add(seed2_id)
        self.seed_network[seed2_id].add(seed1_id)
        
        # 更新统计
        self.stats["total_relationships"] += 1
        if relationship_type == self.MUTUALLY_GENERATING:
            self.stats["mutually_generating_count"] += 1
        elif relationship_type == self.SYNERGISTIC:
            self.stats["synergistic_count"] += 1
        elif relationship_type == self.CONFLICTING:
            self.stats["conflicting_count"] += 1
        
        return relationship
    
    def _find_relationship(self, seed1_id: str, seed2_id: str) -> Optional[SeedRelationship]:
        """查找种子关系"""
        for rel in self.relationships:
            if (rel.seed1_id == seed1_id and rel.seed2_id == seed2_id) or \
               (rel.seed1_id == seed2_id and rel.seed2_id == seed1_id):
                return rel
        return None
    
    def get_synergistic_seeds(self, seed_id: str) -> List[Tuple[str, float]]:
        """获取协同种子"""
        synergistic = []
        for rel in self.relationships:
            if rel.relationship_type in [self.MUTUALLY_GENERATING, self.SYNERGISTIC]:
                if rel.seed1_id == seed_id:
                    synergistic.append((rel.seed2_id, rel.strength))
                elif rel.seed2_id == seed_id:
                    synergistic.append((rel.seed1_id, rel.strength))
        return synergistic
    
    def get_conflicting_seeds(self, seed_id: str) -> List[Tuple[str, float]]:
        """获取相克种子"""
        conflicting = []
        for rel in self.relationships:
            if rel.relationship_type == self.CONFLICTING:
                if rel.seed1_id == seed_id:
                    conflicting.append((rel.seed2_id, rel.strength))
                elif rel.seed2_id == seed_id:
                    conflicting.append((rel.seed1_id, rel.strength))
        return conflicting
    
    def calculate_synergy_strength(self, seed_ids: List[str]) -> float:
        """计算种子组合的协同强度"""
        if len(seed_ids) < 2:
            return 0.0
        
        total_synergy = 0.0
        pair_count = 0
        
        for i in range(len(seed_ids)):
            for j in range(i + 1, len(seed_ids)):
                rel = self._find_relationship(seed_ids[i], seed_ids[j])
                if rel and rel.relationship_type in [self.MUTUALLY_GENERATING, self.SYNERGISTIC]:
                    total_synergy += rel.strength
                    pair_count += 1
        
        return total_synergy / max(1, pair_count) if pair_count > 0 else 0.0
    
    def update_ecosystem_health(self) -> float:
        """更新生态系统健康度"""
        if not self.seed_network:
            self.ecosystem_health = 1.0
            return self.ecosystem_health
        
        # 健康度 = 相生/协同关系比例 - 相克关系惩罚
        positive = self.stats["mutually_generating_count"] + self.stats["synergistic_count"]
        negative = self.stats["conflicting_count"]
        total = max(1, self.stats["total_relationships"])
        
        health = (positive / total) - (negative / total) * 0.5
        self.ecosystem_health = max(0.0, min(1.0, health))
        self.stats["ecosystem_health"] = self.ecosystem_health
        
        return self.ecosystem_health
    
    def get_stats(self) -> Dict[str, Any]:
        """获取生态系统统计"""
        self.update_ecosystem_health()
        return self.stats.copy()


class EmergenceQualityAssessment:
    """
    涌现质量评估器
    
    核心功能：
    1. 多维度质量评估
    2. 质量引导的涌现生成
    3. 高质量涌现筛选
    """
    
    # 深刻性关键词（用于评估深度）
    DEPTH_KEYWORDS = [
        "本质", "核心", "根源", "究竟", "彻底",
        "真相", "实相", "第一义", "最深层", "终极",
        "缘起", "空性", "无常", "无我", "涅槃"
    ]
    
    # 实用性关键词
    UTILITY_KEYWORDS = [
        "方法", "实践", "应用", "解决", "步骤",
        "策略", "方案", "行动", "修行", "证得"
    ]
    
    # 整合性关键词
    INTEGRATION_KEYWORDS = [
        "融合", "统一", "整合", "贯通", "综合",
        "关联", "联系", "交织", "交织", "圆融"
    ]
    
    def __init__(self, alaya_store, ecosystem: Optional[SeedEcosystem] = None):
        """
        初始化质量评估器
        
        Args:
            alaya_store: 阿赖耶识存储
            ecosystem: 种子生态系统
        """
        self.alaya_store = alaya_store
        self.ecosystem = ecosystem or SeedEcosystem()
        
        # 质量历史
        self.quality_history: List[QualityScore] = []
        self.high_quality_emergences: List[QualityEmergence] = []
        
        # 质量阈值
        self.quality_threshold = 0.6  # 最低质量阈值
        self.high_quality_threshold = 0.75  # 高质量阈值
    
    def assess_quality(
        self,
        content: str,
        participant_seeds: List[Any],
        context: Optional[Dict[str, Any]] = None
    ) -> QualityScore:
        """
        评估涌现内容的质量
        
        Args:
            content: 涌现内容
            participant_seeds: 参与种子列表
            context: 上下文信息
        
        Returns:
            质量评分
        """
        score = QualityScore()
        context = context or {}
        
        # 1. 原创性评估：与现有种子的语义距离
        score.novelty = self._assess_novelty(content, participant_seeds)
        
        # 2. 深刻性评估：关键词匹配
        score.depth = self._assess_depth(content)
        
        # 3. 实用性评估：可操作性
        score.utility = self._assess_utility(content)
        
        # 4. 相关性评估：与情境匹配
        score.relevance = self._assess_relevance(content, context)
        
        # 5. 整合性评估：跨领域整合
        score.integration = self._assess_integration(content, participant_seeds)
        
        # 记录历史
        self.quality_history.append(score)
        
        return score
    
    def _assess_novelty(self, content: str, participant_seeds: List[Any]) -> float:
        """评估原创性"""
        if not participant_seeds:
            return 0.5
        
        # 检查与参与种子的相似度
        max_similarity = 0.0
        for seed in participant_seeds:
            if hasattr(seed, 'content'):
                similarity = self._calculate_text_similarity(content, seed.content)
                max_similarity = max(max_similarity, similarity)
        
        # 原创性 = 1 - 相似度
        novelty = 1.0 - max_similarity
        
        # 检查是否包含新关键词
        existing_keywords = set()
        for seed in participant_seeds:
            if hasattr(seed, 'tags'):
                existing_keywords.update(seed.tags)
        
        content_keywords = set(content.split())
        new_keywords_ratio = len(content_keywords - existing_keywords) / max(1, len(content_keywords))
        novelty = novelty * 0.7 + new_keywords_ratio * 0.3
        
        return max(0.0, min(1.0, novelty))
    
    def _assess_depth(self, content: str) -> float:
        """评估深刻性"""
        depth_score = 0.5
        
        # 关键词匹配
        matched_depth_keywords = sum(1 for kw in self.DEPTH_KEYWORDS if kw in content)
        depth_score += min(0.3, matched_depth_keywords * 0.05)
        
        # 长度惩罚（过短的内容可能不够深刻）
        if len(content) > 50:
            depth_score += 0.1
        
        # 反问句和思辨性语言
        if any(q in content for q in ["为什么", "如何", "什么", "何为"]):
            depth_score += 0.1
        
        return max(0.0, min(1.0, depth_score))
    
    def _assess_utility(self, content: str) -> float:
        """评估实用性"""
        utility_score = 0.5
        
        # 关键词匹配
        matched_utility_keywords = sum(1 for kw in self.UTILITY_KEYWORDS if kw in content)
        utility_score += min(0.3, matched_utility_keywords * 0.06)
        
        # 具体性（包含数字或具体名词）
        if any(c.isdigit() for c in content):
            utility_score += 0.1
        
        # 包含行动建议
        if any(action in content for action in ["应该", "可以", "需要", "必须", "应当"]):
            utility_score += 0.1
        
        return max(0.0, min(1.0, utility_score))
    
    def _assess_relevance(self, content: str, context: Dict[str, Any]) -> float:
        """评估相关性"""
        relevance_score = 0.5
        
        # 如果有上下文关键词，检查匹配度
        context_keywords = context.get("keywords", [])
        if context_keywords:
            matched = sum(1 for kw in context_keywords if kw in content)
            relevance_score += min(0.3, matched / max(1, len(context_keywords)))
        
        # 与用户问题的相关性（如果有）
        user_query = context.get("user_query", "")
        if user_query:
            # 简单关键词重叠
            query_words = set(user_query)
            content_words = set(content)
            overlap = len(query_words & content_words)
            relevance_score += min(0.2, overlap * 0.05)
        
        return max(0.0, min(1.0, relevance_score))
    
    def _assess_integration(self, content: str, participant_seeds: List[Any]) -> float:
        """评估整合性"""
        integration_score = 0.5
        
        # 关键词匹配
        matched_integration_keywords = sum(1 for kw in self.INTEGRATION_KEYWORDS if kw in content)
        integration_score += min(0.2, matched_integration_keywords * 0.05)
        
        # 参与种子的多样性
        seed_types = set()
        for seed in participant_seeds:
            if hasattr(seed, 'seed_type'):
                seed_types.add(str(seed.seed_type))
        
        if len(seed_types) >= 3:
            integration_score += 0.2
        elif len(seed_types) >= 2:
            integration_score += 0.1
        
        # 检查是否有多领域整合的迹象
        domains = ["智慧", "慈悲", "真理", "善", "美"]
        matched_domains = sum(1 for d in domains if d in content)
        if matched_domains >= 3:
            integration_score += 0.2
        
        return max(0.0, min(1.0, integration_score))
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度（简单词重叠）"""
        words1 = set(text1)
        words2 = set(text2)
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def is_high_quality(self, quality_score: QualityScore) -> bool:
        """判断是否为高质量涌现"""
        return quality_score.weighted_score() >= self.high_quality_threshold
    
    def meets_threshold(self, quality_score: QualityScore) -> bool:
        """判断是否满足最低质量阈值"""
        return quality_score.weighted_score() >= self.quality_threshold
    
    def create_quality_emergence(
        self,
        content: str,
        quality_score: QualityScore,
        participant_seeds: List[Any],
        emergence_type: str = "wisdom"
    ) -> Optional[QualityEmergence]:
        """创建高质量涌现记录"""
        if not self.meets_threshold(quality_score):
            return None
        
        emergence = QualityEmergence(
            emergence_id=str(uuid.uuid4()),
            content=content,
            quality_score=quality_score,
            participant_seeds=[s.seed_id if hasattr(s, 'seed_id') else str(s) for s in participant_seeds],
            emergence_type=emergence_type,
            timestamp=datetime.now(),
            insight_tags=self._extract_insight_tags(content)
        )
        
        # 保存高质量涌现
        if self.is_high_quality(quality_score):
            self.high_quality_emergences.append(emergence)
        
        return emergence
    
    def _extract_insight_tags(self, content: str) -> List[str]:
        """提取洞察标签"""
        tags = []
        
        # 提取匹配的关键字
        all_keywords = self.DEPTH_KEYWORDS + self.UTILITY_KEYWORDS + self.INTEGRATION_KEYWORDS
        for kw in all_keywords:
            if kw in content:
                tags.append(kw)
        
        # 限制标签数量
        return list(set(tags))[:5]
    
    def get_quality_report(self) -> Dict[str, Any]:
        """获取质量报告"""
        if not self.quality_history:
            return {
                "total_assessed": 0,
                "high_quality_count": 0,
                "avg_quality_score": 0.0,
                "avg_novelty": 0.0,
                "avg_depth": 0.0,
                "avg_utility": 0.0,
                "avg_relevance": 0.0,
                "avg_integration": 0.0
            }
        
        total = len(self.quality_history)
        return {
            "total_assessed": total,
            "high_quality_count": len(self.high_quality_emergences),
            "high_quality_ratio": len(self.high_quality_emergences) / total,
            "avg_quality_score": sum(q.weighted_score() for q in self.quality_history) / total,
            "avg_novelty": sum(q.novelty for q in self.quality_history) / total,
            "avg_depth": sum(q.depth for q in self.quality_history) / total,
            "avg_utility": sum(q.utility for q in self.quality_history) / total,
            "avg_relevance": sum(q.relevance for q in self.quality_history) / total,
            "avg_integration": sum(q.integration for q in self.quality_history) / total
        }


class QualityGuidedEmergenceGenerator:
    """
    质量引导的涌现生成器
    
    基于质量评估，智能生成高质量涌现内容
    """
    
    # 高质量涌现内容模板
    HIGH_QUALITY_TRUTH = [
        "真空妙有：一切法空无自性，却不妨碍宛然显现，此即中道实相",
        "缘起如幻：诸法因缘生，犹梦境泡影，虽幻而有序",
        "法尔如是：诸法本来如此，不假外求，当体即是",
        "圆满智慧：一切智智现前，照见诸法实相",
        "根本智慧：无分别智显现，直契真如本体"
    ]
    
    HIGH_QUALITY_COMPASSION = [
        "无缘大悲：不住相布施，度化一切众生而不以为度",
        "同体大悲：众生与我本无二别，感同身受即是",
        "慈悲喜舍：四无量心圆满，平等对待一切众生",
        "代众生苦：愿代一切众生受无量苦，不以为苦",
        "普皆度化：地狱不空誓不成佛，众生度尽方证菩提"
    ]
    
    HIGH_QUALITY_BEAUTY = [
        "圆满无碍：理事无碍，事事无碍，一真法界",
        "和谐统一：对立统一，矛盾调和，万物归一",
        "清净庄严：自性本净，功德庄严，净土成就",
        "相好光明：三十二相八十种好，光明普照",
        "微妙香洁：微妙不可思议，清净香洁第一"
    ]
    
    # 整合型高质量涌现
    HIGH_QUALITY_INTEGRATION = [
        "悲智双运：智慧照破迷暗，慈悲广度众生，二而不二",
        "空有不二：真空妙有，色即是空，空即是色",
        "理事圆融：理无碍，事无碍，理事无碍，事事无碍",
        "真善美一体：真为智慧，善为慈悲，美为和谐，三位一体",
        "自觉觉他：自己觉悟，觉悟他人，自度度人，直至圆满"
    ]
    
    def __init__(
        self,
        quality_assessor: EmergenceQualityAssessment,
        ecosystem: SeedEcosystem
    ):
        """
        初始化质量引导涌现生成器
        
        Args:
            quality_assessor: 质量评估器
            ecosystem: 种子生态系统
        """
        self.quality_assessor = quality_assessor
        self.ecosystem = ecosystem
        
        # 生成统计
        self.generation_stats = {
            "total_generated": 0,
            "high_quality_generated": 0,
            "type_breakdown": defaultdict(int)
        }
    
    def generate_quality_emergence(
        self,
        emergence_type: str,
        participant_seeds: List[Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[QualityEmergence]:
        """
        生成质量引导的涌现
        
        Args:
            emergence_type: 涌现类型
            participant_seeds: 参与种子
            context: 上下文
        
        Returns:
            高质量涌现（如果满足阈值）
        """
        # 选择内容池
        if emergence_type == "truth":
            content_pool = self.HIGH_QUALITY_TRUTH
        elif emergence_type == "compassion":
            content_pool = self.HIGH_QUALITY_COMPASSION
        elif emergence_type == "beauty":
            content_pool = self.HIGH_QUALITY_BEAUTY
        elif emergence_type == "integration":
            content_pool = self.HIGH_QUALITY_INTEGRATION
        else:
            content_pool = self.HIGH_QUALITY_TRUTH + self.HIGH_QUALITY_COMPASSION
        
        # 计算协同强度加成
        seed_ids = [s.seed_id if hasattr(s, 'seed_id') else str(s) for s in participant_seeds]
        synergy_bonus = self.ecosystem.calculate_synergy_strength(seed_ids)
        
        # 选择高质量内容
        base_content = random.choice(content_pool)
        
        # 如果协同强度高，添加额外洞察
        if synergy_bonus > 0.5:
            # 添加生态增强效果描述
            enhancement = f"，生态系统协同度{synergy_bonus:.0%}增强"
            content = base_content + enhancement
        else:
            content = base_content
        
        # 评估质量
        quality_score = self.quality_assessor.assess_quality(
            content=content,
            participant_seeds=participant_seeds,
            context=context
        )
        
        # 协同强度加成
        quality_score.depth = min(1.0, quality_score.depth + synergy_bonus * 0.1)
        quality_score.integration = min(1.0, quality_score.integration + synergy_bonus * 0.15)
        
        # 更新统计
        self.generation_stats["total_generated"] += 1
        self.generation_stats["type_breakdown"][emergence_type] += 1
        
        # 创建涌现
        emergence = self.quality_assessor.create_quality_emergence(
            content=content,
            quality_score=quality_score,
            participant_seeds=participant_seeds,
            emergence_type=emergence_type
        )
        
        if emergence and self.quality_assessor.is_high_quality(quality_score):
            self.generation_stats["high_quality_generated"] += 1
        
        return emergence
    
    def get_generation_report(self) -> Dict[str, Any]:
        """获取生成报告"""
        stats = self.generation_stats.copy()
        stats["type_breakdown"] = dict(stats["type_breakdown"])
        stats["high_quality_ratio"] = (
            stats["high_quality_generated"] / stats["total_generated"]
            if stats["total_generated"] > 0 else 0.0
        )
        return stats
