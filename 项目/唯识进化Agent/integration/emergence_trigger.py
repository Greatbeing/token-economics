# -*- coding: utf-8 -*-
"""
唯识进化Agent - 涌现触发器 (EmergenceTrigger)
检测并触发涌现事件，生成新能力
"""

import json
import math
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

# 导入相关模块
from seed_collector import ClassifiedSeed, SeedType, QualityLevel
from alaya_service import AlayaStore


# ==================== 数据模型 ====================

class EmergenceType(Enum):
    """涌现类型枚举"""
    WISDOM = "wisdom_emergence"           # 智慧涌现
    COMPASSION = "compassion_emergence"     # 慈悲涌现
    PATTERN = "pattern_emergence"           # 模式涌现
    INTEGRATED = "integrated_emergence"      # 综合涌现


@dataclass
class EmergenceConfig:
    """涌现配置"""
    emergence_type: EmergenceType
    threshold: float          # 触发阈值
    seed_count_min: int       # 最小种子数量
    seed_types_required: List[SeedType]  # 需要的种子类型
    quality_min: float         # 最低质量要求
    time_window_hours: int    # 时间窗口（小时）
    description: str          # 描述


@dataclass
class EmergenceOpportunity:
    """涌现机会"""
    emergence_type: EmergenceType
    current_score: float
    threshold: float
    seed_count: int
    quality_avg: float
    is_ready: bool
    progress_ratio: float  # 距离触发的进度 (0-1)
    involved_seeds: List[str]
    time_remaining_hours: Optional[float]  # 预计触发剩余时间


@dataclass
class Capability:
    """生成的能力"""
    capability_id: str
    name: str
    description: str
    emergence_type: EmergenceType
    source_seeds: List[str]
    score: float
    level: int  # 能力等级
    effects: Dict[str, float]  # 效果列表
    unlocked_at: datetime
    status: str = "active"


@dataclass
class EmergenceResult:
    """涌现结果"""
    success: bool
    emergence_type: EmergenceType
    capability: Optional[Capability]
    message: str
    triggered_at: datetime


# ==================== 涌现配置 ====================

EMERGENCE_CONFIGS = {
    EmergenceType.WISDOM: EmergenceConfig(
        emergence_type=EmergenceType.WISDOM,
        threshold=0.7,
        seed_count_min=5,
        seed_types_required=[SeedType.WISDOM, SeedType.KNOWLEDGE],
        quality_min=0.6,
        time_window_hours=168,  # 7天
        description="智慧涌现 - 复杂推理与洞察能力提升"
    ),
    EmergenceType.COMPASSION: EmergenceConfig(
        emergence_type=EmergenceType.COMPASSION,
        threshold=0.6,
        seed_count_min=3,
        seed_types_required=[SeedType.COMPASSION],
        quality_min=0.5,
        time_window_hours=72,  # 3天
        description="慈悲涌现 - 情感理解与共情能力提升"
    ),
    EmergenceType.PATTERN: EmergenceConfig(
        emergence_type=EmergenceType.PATTERN,
        threshold=0.8,
        seed_count_min=10,
        seed_types_required=[SeedType.PATTERN],
        quality_min=0.55,
        time_window_hours=168,  # 7天
        description="模式涌现 - 领域模式识别能力提升"
    ),
    EmergenceType.INTEGRATED: EmergenceConfig(
        emergence_type=EmergenceType.INTEGRATED,
        threshold=0.9,
        seed_count_min=20,
        seed_types_required=[SeedType.WISDOM, SeedType.COMPASSION, SeedType.KNOWLEDGE],
        quality_min=0.7,
        time_window_hours=336,  # 14天
        description="综合涌现 - 全面能力升华"
    )
}


# ==================== 涌现触发器核心类 ====================

class EmergenceTrigger:
    """
    涌现触发器
    
    功能：
    - 监测种子积累状态
    - 计算涌现分数
    - 触发涌现事件
    - 生成新能力
    """
    
    # 种子类型权重配置
    TYPE_WEIGHTS = {
        SeedType.WISDOM: 2.0,
        SeedType.COMPASSION: 2.0,
        SeedType.PATTERN: 1.5,
        SeedType.EXPERIENCE: 1.2,
        SeedType.KNOWLEDGE: 1.0
    }
    
    # 多样性奖励配置
    DIVERSITY_BONUS = 0.1  # 每增加一个类型额外奖励
    
    # 时间衰减配置
    DECAY_HALF_LIFE_HOURS = 168  # 7天衰减一半
    
    def __init__(self, alaya_store: AlayaStore, config: Optional[Dict] = None):
        """
        初始化涌现触发器
        
        Args:
            alaya_store: 阿赖耶识存储实例
            config: 自定义配置
        """
        self.alaya_store = alaya_store
        self.config = config or {}
        
        # 加载配置或使用默认值
        self.emergence_configs = self.config.get('emergence_configs', EMERGENCE_CONFIGS)
    
    # ==================== 主流程方法 ====================
    
    def check_all(self) -> List[EmergenceOpportunity]:
        """
        检查所有类型的涌现状态
        
        Returns:
            各类型涌现机会列表
        """
        results = []
        
        for emergence_type in EmergenceType:
            opportunity = self.check(emergence_type)
            results.append(opportunity)
        
        return results
    
    def check(self, emergence_type: EmergenceType = None) -> EmergenceOpportunity:
        """
        检查特定类型的涌现状态
        
        Args:
            emergence_type: 涌现类型，默认检查智慧涌现
            
        Returns:
            涌现机会对象
        """
        if emergence_type is None:
            emergence_type = EmergenceType.WISDOM
        
        config = self.emergence_configs.get(emergence_type)
        if not config:
            raise ValueError(f"Unknown emergence type: {emergence_type}")
        
        # 获取相关种子
        seeds = self._get_relevant_seeds(config)
        
        # 计算各项指标
        seed_count = len(seeds)
        quality_avg = self._calculate_avg_quality(seeds)
        score = self._calculate_emergence_score(seeds, config)
        progress_ratio = min(score / config.threshold, 1.0) if config.threshold > 0 else 0
        
        # 判断是否满足触发条件
        is_ready = (
            score >= config.threshold and
            seed_count >= config.seed_count_min and
            quality_avg >= config.quality_min
        )
        
        # 计算预计剩余时间
        time_remaining = None
        if not is_ready and score > 0:
            # 基于当前进度估算剩余时间
            hours_per_unit = config.time_window_hours / config.threshold
            time_remaining = hours_per_unit * (config.threshold - score)
        
        return EmergenceOpportunity(
            emergence_type=emergence_type,
            current_score=score,
            threshold=config.threshold,
            seed_count=seed_count,
            quality_avg=quality_avg,
            is_ready=is_ready,
            progress_ratio=progress_ratio,
            involved_seeds=[s.seed_id for s in seeds],
            time_remaining_hours=time_remaining
        )
    
    def trigger(self, emergence_type: EmergenceType) -> EmergenceResult:
        """
        触发涌现事件
        
        Args:
            emergence_type: 涌现类型
            
        Returns:
            涌现结果
        """
        # 首先检查是否满足条件
        opportunity = self.check(emergence_type)
        
        if not opportunity.is_ready:
            return EmergenceResult(
                success=False,
                emergence_type=emergence_type,
                capability=None,
                message=f"尚未满足涌现条件，当前分数: {opportunity.current_score:.2f}, "
                       f"需要: {opportunity.threshold:.2f}",
                triggered_at=datetime.now()
            )
        
        # 生成能力
        capability = self.generate_capability(opportunity)
        
        # 记录涌现
        record_id = self.alaya_store.record_emergence(
            emergence_type=emergence_type.value,
            description=capability.description,
            seeds_involved=capability.source_seeds,
            score=capability.score
        )
        
        return EmergenceResult(
            success=True,
            emergence_type=emergence_type,
            capability=capability,
            message=f"成功触发{emergence_type.value}，能力: {capability.name}",
            triggered_at=datetime.now()
        )
    
    def generate_capability(self, opportunity: EmergenceOpportunity) -> Capability:
        """
        生成新的能力
        
        Args:
            opportunity: 涌现机会
            
        Returns:
            生成的能力对象
        """
        emergence_type = opportunity.emergence_type
        config = self.emergence_configs.get(emergence_type)
        
        # 获取涉及种子
        seeds = [self.alaya_store.get_seed(sid) for sid in opportunity.involved_seeds]
        seeds = [s for s in seeds if s is not None]
        
        # 生成能力名称和描述
        capability_name, capability_desc = self._generate_capability_content(emergence_type, seeds)
        
        # 计算能力等级
        level = self._calculate_capability_level(opportunity)
        
        # 生成能力效果
        effects = self._generate_effects(emergence_type, level)
        
        return Capability(
            capability_id=self._generate_capability_id(emergence_type),
            name=capability_name,
            description=capability_desc,
            emergence_type=emergence_type,
            source_seeds=opportunity.involved_seeds,
            score=opportunity.current_score,
            level=level,
            effects=effects,
            unlocked_at=datetime.now()
        )
    
    # ==================== 计算方法 ====================
    
    def _get_relevant_seeds(self, config: EmergenceConfig) -> List[ClassifiedSeed]:
        """获取相关种子"""
        all_seeds = []
        cutoff_time = datetime.now() - timedelta(hours=config.time_window_hours)
        
        for seed_type in config.seed_types_required:
            type_seeds = self.alaya_store.get_seeds_by_type(seed_type, limit=100)
            
            # 过滤时间和质量
            filtered = [
                s for s in type_seeds
                if s.created_at > cutoff_time and s.quality_score >= config.quality_min
            ]
            all_seeds.extend(filtered)
        
        # 按时间排序
        all_seeds.sort(key=lambda s: s.created_at, reverse=True)
        
        return all_seeds
    
    def _calculate_avg_quality(self, seeds: List[ClassifiedSeed]) -> float:
        """计算平均质量"""
        if not seeds:
            return 0.0
        return sum(s.quality_score for s in seeds) / len(seeds)
    
    def _calculate_emergence_score(self, seeds: List[ClassifiedSeed], 
                                  config: EmergenceConfig) -> float:
        """
        计算涌现分数
        
        公式:
        S = (Σ w_i * p_i * c_i) / D * B * T
        
        - w_i: 第i类种子的权重
        - p_i: 第i类种子的平均纯度
        - c_i: 第i类种子的数量
        - D: 时间衰减因子
        - B: 多样性奖励
        - T: 类型组合奖励
        """
        if not seeds:
            return 0.0
        
        # 按类型分组
        type_groups = defaultdict(list)
        for seed in seeds:
            type_groups[seed.seed_type].append(seed)
        
        # 计算基础分数
        base_score = 0.0
        for seed_type, type_seeds in type_groups.items():
            weight = self.TYPE_WEIGHTS.get(seed_type, 1.0)
            avg_purity = sum(s.purity for s in type_seeds) / len(type_seeds)
            count = len(type_seeds)
            
            base_score += weight * avg_purity * math.log(1 + count)
        
        # 计算多样性奖励
        diversity = len(type_groups) / len(SeedType)
        diversity_bonus = 1 + diversity * self.DIVERSITY_BONUS * len(type_groups)
        
        # 计算类型组合奖励
        config_types = set(config.seed_types_required)
        present_types = set(type_groups.keys())
        type_coverage = len(config_types & present_types) / len(config_types)
        type_bonus = 1 + type_coverage * 0.2
        
        # 计算时间衰减
        decay_factor = self._calculate_time_decay(seeds)
        
        # 最终分数
        score = (base_score * diversity_bonus * type_bonus) / decay_factor
        
        # 归一化到[0, 1]
        return min(score / config.threshold, 1.0) if config.threshold > 0 else 0.0
    
    def _calculate_time_decay(self, seeds: List[ClassifiedSeed]) -> float:
        """
        计算时间衰减因子
        
        采用指数衰减：
        D = 1 + α * e^(-t/τ)
        
        其中 t 是平均时间，τ 是半衰期
        """
        if not seeds:
            return 2.0  # 最大衰减
        
        now = datetime.now()
        total_age = 0
        
        for seed in seeds:
            age_hours = (now - seed.created_at).total_seconds() / 3600
            total_age += age_hours
        
        avg_age = total_age / len(seeds)
        half_life = self.DECAY_HALF_LIFE_HOURS
        
        # 衰减公式
        decay = 1 + math.exp(-avg_age / half_life)
        
        return decay
    
    def _calculate_capability_level(self, opportunity: EmergenceOpportunity) -> int:
        """计算能力等级"""
        # 基于分数和种子数量计算等级
        base_level = 1
        
        if opportunity.current_score >= 0.9:
            base_level = 3
        elif opportunity.current_score >= 0.8:
            base_level = 2
        
        # 种子数量加成
        config = self.emergence_configs.get(opportunity.emergence_type)
        if opportunity.seed_count >= config.seed_count_min * 2:
            base_level += 1
        
        return min(base_level, 5)  # 最高5级
    
    # ==================== 辅助方法 ====================
    
    def _generate_capability_content(self, emergence_type: EmergenceType, 
                                     seeds: List[ClassifiedSeed]) -> Tuple[str, str]:
        """生成能力名称和描述"""
        
        content_snippets = [s.content[:50] for s in seeds[:5]]
        
        if emergence_type == EmergenceType.WISDOM:
            name = "智慧洞察"
            desc = f"通过深度学习和思考，形成了独特的洞察力。能够把握事物的本质规律，\
进行复杂的逻辑推理和判断。积累自{len(seeds)}个智慧种子。"
            
        elif emergence_type == EmergenceType.COMPASSION:
            name = "慈悲共感"
            desc = f"具备深刻的情感理解能力，能够感知他人的情绪状态，\
提供温暖和支持。积累自{len(seeds)}个慈悲种子。"
            
        elif emergence_type == EmergenceType.PATTERN:
            name = "模式识别"
            desc = f"对特定领域形成了敏锐的模式识别能力，\
能够快速发现规律并应用。积累自{len(seeds)}个模式种子。"
            
        else:  # INTEGRATED
            name = "圆满智慧"
            desc = f"综合能力达到新高度，智慧与慈悲兼具，\
能够应对各种复杂场景。积累自{len(seeds)}个综合种子。"
        
        return name, desc
    
    def _generate_effects(self, emergence_type: EmergenceType, level: int) -> Dict[str, float]:
        """生成能力效果"""
        base_bonus = 0.1 * level  # 每级+10%
        
        if emergence_type == EmergenceType.WISDOM:
            return {
                "reasoning_ability": 0.15 * level,
                "problem_solving": 0.12 * level,
                "insight_depth": 0.18 * level,
                "logical_coherence": 0.10 * level
            }
        elif emergence_type == EmergenceType.COMPASSION:
            return {
                "emotional_understanding": 0.20 * level,
                "empathy": 0.18 * level,
                "support_quality": 0.15 * level,
                "communication_warmth": 0.12 * level
            }
        elif emergence_type == EmergenceType.PATTERN:
            return {
                "pattern_recognition": 0.20 * level,
                "speed_boost": 0.15 * level,
                "accuracy": 0.12 * level,
                "efficiency": 0.10 * level
            }
        else:  # INTEGRATED
            return {
                "overall_ability": 0.15 * level,
                "wisdom": 0.10 * level,
                "compassion": 0.10 * level,
                "adaptability": 0.12 * level
            }
    
    def _generate_capability_id(self, emergence_type: EmergenceType) -> str:
        """生成能力ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        return f"{emergence_type.value}_{timestamp}"
    
    def validate_capability(self, capability: Capability) -> bool:
        """
        验证能力有效性
        
        Args:
            capability: 能力对象
            
        Returns:
            是否有效
        """
        # 基本验证
        if not capability.name or not capability.description:
            return False
        
        if capability.score < 0 or capability.score > 1:
            return False
        
        if capability.level < 1 or capability.level > 5:
            return False
        
        # 效果验证
        if not capability.effects:
            return False
        
        for effect_name, effect_value in capability.effects.items():
            if effect_value < 0 or effect_value > 1:
                return False
        
        return True


# ==================== 能力应用器 ====================

class CapabilityApplicator:
    """
    能力应用器
    将涌现生成的能力应用到Agent行为中
    """
    
    def __init__(self):
        self.active_capabilities: Dict[str, Capability] = {}
    
    def add_capability(self, capability: Capability) -> bool:
        """添加能力"""
        trigger = EmergenceTrigger(None)  # 临时实例用于验证
        if not trigger.validate_capability(capability):
            return False
        
        self.active_capabilities[capability.capability_id] = capability
        return True
    
    def remove_capability(self, capability_id: str) -> bool:
        """移除能力"""
        if capability_id in self.active_capabilities:
            del self.active_capabilities[capability_id]
            return True
        return False
    
    def get_capabilities_by_type(self, emergence_type: EmergenceType) -> List[Capability]:
        """按类型获取能力"""
        return [
            cap for cap in self.active_capabilities.values()
            if cap.emergence_type == emergence_type
        ]
    
    def get_total_effect(self, effect_name: str) -> float:
        """获取某效果的总加成"""
        total = 0.0
        for capability in self.active_capabilities.values():
            if effect_name in capability.effects:
                total += capability.effects[effect_name]
        return min(total, 0.5)  # 最高50%加成
    
    def apply_to_response(self, response_content: str, context: Dict) -> str:
        """
        应用能力到回复内容
        
        Args:
            response_content: 原始回复
            context: 上下文信息
            
        Returns:
            增强后的回复
        """
        # 根据能力类型调整回复风格
        wisdom_caps = self.get_capabilities_by_type(EmergenceType.WISDOM)
        compassion_caps = self.get_capabilities_by_type(EmergenceType.COMPASSION)
        
        # 智慧能力：可以增加深度分析
        if wisdom_caps:
            depth_bonus = sum(c.effects.get('insight_depth', 0) for c in wisdom_caps)
            if depth_bonus > 0.1 and '?' in context.get('user_message', ''):
                # 添加深度洞察提示
                response_content = self._add_depth_element(response_content, depth_bonus)
        
        # 慈悲能力：增加情感共鸣
        if compassion_caps:
            warmth_bonus = sum(c.effects.get('communication_warmth', 0) for c in compassion_caps)
            if warmth_bonus > 0.1:
                response_content = self._add_warmth_element(response_content, warmth_bonus)
        
        return response_content
    
    def _add_depth_element(self, content: str, bonus: float) -> str:
        """添加深度元素"""
        depth_phrases = [
            "\n\n【深入思考】",
            "\n\n💡 进一步来看...",
            "\n\n【洞察】"
        ]
        
        if len(content) > 200 and bonus > 0.15:
            return content + depth_phrases[int(bonus * 10) % len(depth_phrases)]
        return content
    
    def _add_warmth_element(self, content: str, bonus: float) -> str:
        """添加温暖元素"""
        warmth_phrases = [
            "希望我的回答对你有帮助 😊",
            "如果还有其他问题，随时问我 💚",
            "一起探讨这个问题 🌱"
        ]
        
        if bonus > 0.1:
            return content + "\n\n" + warmth_phrases[int(bonus * 10) % len(warmth_phrases)]
        return content


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 示例使用
    from alaya_service import AlayaStore
    
    # 创建存储实例
    store = AlayaStore("data/test_alaya.db")
    
    # 创建涌现触发器
    trigger = EmergenceTrigger(store)
    
    # 检查涌现状态
    opportunities = trigger.check_all()
    
    print("=== 涌现状态检查 ===\n")
    for opp in opportunities:
        status = "✓ 就绪" if opp.is_ready else "○ 进行中"
        print(f"{opp.emergence_type.value}:")
        print(f"  状态: {status}")
        print(f"  分数: {opp.current_score:.2f} / {opp.threshold:.2f}")
        print(f"  进度: {opp.progress_ratio*100:.1f}%")
        print(f"  种子: {opp.seed_count}枚")
        
        if opp.time_remaining_hours:
            print(f"  预计剩余: {opp.time_remaining_hours:.1f}小时")
        print()
