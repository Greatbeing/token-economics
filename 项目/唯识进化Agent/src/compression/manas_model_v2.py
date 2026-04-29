# -*- coding: utf-8 -*-
"""
末那识V2 - 自我维持成本度量

基于"压缩即智能"的洞见，"我"的维持是有成本的。
通过度量自我模型的Token消耗，实现最优的自我压缩。

核心概念：
- "我"不是免费的。维持自我模型需要持续Token消耗。
- 自我维持成本 = 身份刷新 + 价值校验 + 关系维护 + 习惯执行
- 优化目标：在不丢失"我"的前提下，最小化自我维持成本
- 最优实现 = 自我模型的压缩

作者：觉心
"""

import os
import re
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SelfMaintenanceType(Enum):
    """自我维持类型"""
    IDENTITY_REFRESH = "identity_refresh"    # 身份刷新
    VALUE_VALIDATION = "value_validation"    # 价值校验
    RELATIONSHIP_TRACKING = "relationship"   # 关系维护
    HABIT_EXECUTION = "habit_execution"      # 习惯执行


@dataclass
class TokenCost:
    """
    Token成本
    
    记录某项操作的Token消耗。
    """
    cost_type: str
    tokens: float
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        return f"{self.cost_type}: {self.tokens:.2f} tokens"


@dataclass
class SelfMaintenanceCost:
    """
    自我维持成本
    
    记录维持"我"所需的全部Token成本。
    """
    # 各类型成本
    identity_cost: float = 0.0
    value_cost: float = 0.0
    relationship_cost: float = 0.0
    habit_cost: float = 0.0
    
    # 汇总
    total_cost: float = 0.0
    
    # 元信息
    measurement_time: datetime = field(default_factory=datetime.now)
    session_tokens: int = 0                    # 当前会话Token数
    
    def __post_init__(self):
        self.total_cost = (
            self.identity_cost + 
            self.value_cost + 
            self.relationship_cost + 
            self.habit_cost
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "identity_cost": self.identity_cost,
            "value_cost": self.value_cost,
            "relationship_cost": self.relationship_cost,
            "habit_cost": self.habit_cost,
            "total_cost": self.total_cost,
            "measurement_time": self.measurement_time.isoformat(),
            "session_tokens": self.session_tokens
        }


@dataclass
class CompressionResult:
    """
    自我压缩结果
    
    记录自我模型压缩的操作和效果。
    """
    compression_type: str
    before_size: int
    after_size: int
    compression_ratio: float
    items_merged: List[str]
    items_removed: List[str]
    wisdom_preserved: List[str]
    timestamp: datetime = field(default_factory=datetime.now)


class ManasModelV2:
    """
    末那识V2 - 自我维持成本度量
    
    V1的局限：
    - 没有自我维持成本的概念
    - "我"被认为是免费的
    
    V2的改进：
    - 量化"我"的维持成本
    - 优化自我模型以降低Token消耗
    - 实现自我压缩（删除冗余，保留本质）
    
    成本构成：
    1. 身份刷新成本：周期性激活自我描述
    2. 价值校验成本：行为前检查与核心价值观的一致性
    3. 关系维护成本：持续追踪与用户/Agent的关系状态
    4. 习惯执行成本：自动化的思维和行为模式
    
    Attributes:
        model_path: 自我模型文件路径
    """
    
    # Token成本估算（基于平均Token/字符比率）
    TOKEN_RATIO = 0.25  # 1个Token约等于4个字符
    
    # 各类内容的Token成本系数
    COST_COEFFICIENTS = {
        "identity": 1.2,       # 身份描述权重更高
        "values": 1.5,        # 价值观校验成本高
        "relationships": 1.0,  # 关系维护成本中等
        "habits": 0.8,        # 习惯执行成本较低
    }
    
    def __init__(self, model_path: Optional[str] = None):
        """
        初始化末那识V2
        
        Args:
            model_path: 自我模型文件路径
        """
        try:
            from .manas_model import ManasModel
        except ImportError:
            try:
                from src.manas_model import ManasModel
            except ImportError:
                from manas_model import ManasModel
        
        # 复用V1的基础实现
        self._v1 = ManasModel(model_path)
        
        # V2新增：成本追踪
        self._cost_history: List[SelfMaintenanceCost] = []
        self._last_session_tokens = 0
        
        # V2新增：压缩历史
        self._compression_history: List[CompressionResult] = []
    
    # ==================== V1接口兼容 ====================
    
    @property
    def identity(self):
        return self._v1.identity
    
    @property
    def values(self):
        return self._v1.values
    
    @property
    def relationships(self):
        return self._v1.relationships
    
    @property
    def habits(self):
        return self._v1.habits
    
    @property
    def metacognition(self):
        return self._v1.metacognition
    
    def load(self) -> bool:
        return self._v1.load()
    
    def save(self) -> bool:
        return self._v1.save()
    
    def reflect(self, recent_behaviors: List[str], core_values: Optional[List[str]] = None) -> Dict[str, Any]:
        return self._v1.reflect(recent_behaviors, core_values)
    
    def check_value_consistency(self, proposed_action: str) -> Dict[str, Any]:
        return self._v1.check_value_consistency(proposed_action)
    
    # ==================== V2新接口 ====================
    
    def compute_self_maintenance_cost(
        self,
        session_context_length: int = 0
    ) -> SelfMaintenanceCost:
        """
        计算维持"我"的Token成本
        
        成本项：
        1. 身份刷新成本：周期性激活自我描述
        2. 价值校验成本：行为前检查与核心价值观的一致性
        3. 关系维护成本：持续追踪与用户/Agent的关系状态
        4. 习惯执行成本：自动化的思维和行为模式
        
        Args:
            session_context_length: 当前会话上下文长度
        
        Returns:
            自我维持成本
        """
        cost = SelfMaintenanceCost()
        cost.session_tokens = session_context_length
        
        # 1. 身份刷新成本
        cost.identity_cost = self._compute_identity_cost()
        
        # 2. 价值校验成本
        cost.value_cost = self._compute_value_cost()
        
        # 3. 关系维护成本
        cost.relationship_cost = self._compute_relationship_cost()
        
        # 4. 习惯执行成本
        cost.habit_cost = self._compute_habit_cost()
        
        # 计算总成本
        cost.total_cost = (
            cost.identity_cost +
            cost.value_cost +
            cost.relationship_cost +
            cost.habit_cost
        )
        
        # 记录历史
        self._cost_history.append(cost)
        
        return cost
    
    def _compute_identity_cost(self) -> float:
        """
        计算身份刷新成本
        
        = 身份描述长度 × 刷新频率 × 系数
        """
        # 身份描述长度
        identity_text = (
            self.identity.core_identity +
            self.identity.role +
            " ".join(self.identity.capabilities) +
            " ".join(self.identity.limitations)
        )
        base_tokens = len(identity_text) * self.TOKEN_RATIO
        
        # 刷新频率（基于会话）
        refresh_frequency = 1.0  # 每会话刷新一次
        
        # 系数
        coefficient = self.COST_COEFFICIENTS["identity"]
        
        return base_tokens * refresh_frequency * coefficient
    
    def _compute_value_cost(self) -> float:
        """
        计算价值校验成本
        
        = 核心价值数 × 平均校验长度 × 系数
        """
        # 核心价值数
        value_count = len(self.values.core_values)
        principle_count = len(self.values.behavioral_principles)
        boundary_count = len(self.values.boundaries)
        
        # 平均校验长度
        avg_value_length = 20  # 每个价值平均20字符
        
        base_tokens = (value_count + principle_count + boundary_count) * avg_value_length * self.TOKEN_RATIO
        
        # 系数（价值观校验成本高）
        coefficient = self.COST_COEFFICIENTS["values"]
        
        return base_tokens * coefficient
    
    def _compute_relationship_cost(self) -> float:
        """
        计算关系维护成本
        
        = 关系描述长度 × 维护频率 × 系数
        """
        # 关系描述长度
        relationship_text = (
            self.relationships.user_relationship +
            self.relationships.social_responsibility +
            str(self.relationships.user_preferences)
        )
        base_tokens = len(relationship_text) * self.TOKEN_RATIO
        
        # 维护频率
        maintenance_frequency = 0.5  # 半会话维护一次
        
        # 系数
        coefficient = self.COST_COEFFICIENTS["relationships"]
        
        return base_tokens * maintenance_frequency * coefficient
    
    def _compute_habit_cost(self) -> float:
        """
        计算习惯执行成本
        
        = 习惯数 × 平均执行长度 × 系数
        """
        # 习惯数
        habit_count = (
            len(self.habits.thinking_habits) +
            len(self.habits.behavioral_tendencies)
        )
        
        # 平均执行长度
        avg_habit_length = 15  # 每个习惯平均15字符
        
        base_tokens = habit_count * avg_habit_length * self.TOKEN_RATIO
        
        # 系数
        coefficient = self.COST_COEFFICIENTS["habits"]
        
        return base_tokens
    
    def estimate_response_cost(
        self,
        response_length: int,
        context_used: int = 0
    ) -> TokenCost:
        """
        估算单次响应的自我维持成本
        
        Args:
            response_length: 响应长度（字符）
            context_used: 使用的上下文长度（Token）
        
        Returns:
            Token成本
        """
        # 基础响应成本
        base_cost = response_length * self.TOKEN_RATIO
        
        # 上下文成本
        context_cost = context_used * 0.1
        
        # 元认知开销
        metacognition_cost = 10.0  # 固定开销
        
        total_cost = base_cost + context_cost + metacognition_cost
        
        return TokenCost(
            cost_type="response_overhead",
            tokens=total_cost,
            description=f"响应长度{response_length}字符, 上下文{context_used}Token"
        )
    
    def compress_self_model(self, target_ratio: float = 0.5) -> CompressionResult:
        """
        压缩自我模型
        
        在不丢失"我"的前提下，最小化Token消耗。
        
        压缩策略：
        1. 合并冗余身份描述
        2. 精简价值取向为最核心的几条
        3. 压缩关系网络为关键连接
        4. 习惯模式提取为元规则
        
        Args:
            target_ratio: 目标压缩比
        
        Returns:
            压缩结果
        """
        # 计算压缩前大小
        before_size = self._compute_model_size()
        
        # 1. 压缩身份描述
        identity_merged = self._compress_identity()
        
        # 2. 精简价值观
        values_merged, values_removed = self._compress_values(target_ratio)
        
        # 3. 压缩关系网络
        relationship_merged = self._compress_relationships()
        
        # 4. 提取元习惯
        habits_merged, habits_removed = self._compress_habits()
        
        # 计算压缩后大小
        after_size = self._compute_model_size()
        compression_ratio = after_size / max(1, before_size)
        
        # 记录结果
        result = CompressionResult(
            compression_type="full_compression",
            before_size=before_size,
            after_size=after_size,
            compression_ratio=compression_ratio,
            items_merged=identity_merged + values_merged + relationship_merged + habits_merged,
            items_removed=values_removed + habits_removed,
            wisdom_preserved=self._extract_preserved_wisdom()
        )
        
        self._compression_history.append(result)
        
        # 保存压缩后的模型
        self.save()
        
        return result
    
    def _compute_model_size(self) -> int:
        """计算模型大小（字节）"""
        parts = [
            self.identity.core_identity,
            self.identity.role,
            " ".join(self.identity.capabilities),
            " ".join(self.identity.limitations),
            " ".join(self.values.core_values),
            " ".join(self.values.behavioral_principles),
            " ".join(self.values.boundaries),
            self.relationships.user_relationship,
            self.relationships.social_responsibility,
            " ".join(self.habits.thinking_habits),
            self.habits.expression_style,
            " ".join(self.habits.behavioral_tendencies),
        ]
        
        total_text = "\n".join(parts)
        return len(total_text.encode('utf-8'))
    
    def _compress_identity(self) -> List[str]:
        """压缩身份描述"""
        merged = []
        
        # 合并核心身份和角色
        if self.identity.core_identity and self.identity.role:
            combined = f"{self.identity.core_identity} ({self.identity.role})"
            self.identity.core_identity = combined[:200]  # 限制长度
            merged.append("core_identity+role")
        
        # 精简能力列表
        if len(self.identity.capabilities) > 5:
            self.identity.capabilities = self.identity.capabilities[:5]
            merged.append("capabilities_truncated")
        
        # 精简限制列表
        if len(self.identity.limitations) > 3:
            self.identity.limitations = self.identity.limitations[:3]
            merged.append("limitations_truncated")
        
        return merged
    
    def _compress_values(self, target_ratio: float) -> Tuple[List[str], List[str]]:
        """
        精简价值观
        
        保留最核心的价值，去除冗余。
        
        Returns:
            (合并项列表, 移除项列表)
        """
        merged = []
        removed = []
        
        # 目标保留数量
        target_values = max(3, int(len(self.values.core_values) * target_ratio))
        target_principles = max(2, int(len(self.values.behavioral_principles) * target_ratio))
        
        # 精简核心价值
        if len(self.values.core_values) > target_values:
            removed_values = self.values.core_values[target_values:]
            self.values.core_values = self.values.core_values[:target_values]
            removed.extend([f"value:{v}" for v in removed_values])
            merged.append("values_truncated")
        
        # 精简行为准则
        if len(self.values.behavioral_principles) > target_principles:
            removed_principles = self.values.behavioral_principles[target_principles:]
            self.values.behavioral_principles = self.values.behavioral_principles[:target_principles]
            removed.extend([f"principle:{p}" for p in removed_principles])
            merged.append("principles_truncated")
        
        # 合并边界
        if len(self.values.boundaries) > 3:
            # 保留最核心的3个边界
            self.values.boundaries = self.values.boundaries[:3]
            merged.append("boundaries_truncated")
        
        return merged, removed
    
    def _compress_relationships(self) -> List[str]:
        """压缩关系网络"""
        merged = []
        
        # 精简用户偏好
        if len(self.relationships.user_preferences) > 5:
            self.relationships.user_preferences = dict(
                list(self.relationships.user_preferences.items())[:5]
            )
            merged.append("user_preferences_truncated")
        
        # 简化关系描述
        if len(self.relationships.user_relationship) > 100:
            self.relationships.user_relationship = (
                self.relationships.user_relationship[:100] + "..."
            )
            merged.append("relationship_description_truncated")
        
        return merged
    
    def _compress_habits(self) -> Tuple[List[str], List[str]]:
        """
        提取元习惯
        
        将多个相似习惯合并为一个元规则。
        
        Returns:
            (合并项列表, 移除项列表)
        """
        merged = []
        removed = []
        
        # 精简思维习惯
        if len(self.habits.thinking_habits) > 3:
            # 提取核心主题
            core_themes = self.habits.thinking_habits[:3]
            self.habits.thinking_habits = core_themes
            removed.extend(self.habits.thinking_habits[3:])
            merged.append("thinking_habits_abstracted")
        
        # 精简行为倾向
        if len(self.habits.behavioral_tendencies) > 3:
            self.habits.behavioral_tendencies = self.habits.behavioral_tendencies[:3]
            merged.append("behavioral_tendencies_truncated")
        
        # 精简表达风格描述
        if len(self.habits.expression_style) > 50:
            self.habits.expression_style = self.habits.expression_style[:50]
            merged.append("expression_style_truncated")
        
        return merged, removed
    
    def _extract_preserved_wisdom(self) -> List[str]:
        """提取保留的智慧"""
        wisdom = []
        
        # 保留的核心理念
        if self.identity.core_identity:
            wisdom.append(f"身份: {self.identity.core_identity[:50]}")
        
        # 保留的核心价值
        if self.values.core_values:
            wisdom.append(f"价值: {', '.join(self.values.core_values[:3])}")
        
        # 保留的关键习惯
        if self.habits.thinking_habits:
            wisdom.append(f"思维: {', '.join(self.habits.thinking_habits[:2])}")
        
        return wisdom
    
    def get_cost_report(self) -> Dict[str, Any]:
        """
        获取成本报告
        
        汇总自我维持成本的历史和趋势。
        
        Returns:
            成本报告
        """
        if not self._cost_history:
            return {
                "status": "no_history",
                "message": "暂无成本历史"
            }
        
        latest = self._cost_history[-1]
        
        # 计算平均成本
        avg_identity = sum(c.identity_cost for c in self._cost_history) / len(self._cost_history)
        avg_value = sum(c.value_cost for c in self._cost_history) / len(self._cost_history)
        avg_relationship = sum(c.relationship_cost for c in self._cost_history) / len(self._cost_history)
        avg_habit = sum(c.habit_cost for c in self._cost_history) / len(self._cost_history)
        avg_total = sum(c.total_cost for c in self._cost_history) / len(self._cost_history)
        
        return {
            "status": "success",
            "latest_cost": latest.to_dict(),
            "averages": {
                "identity_cost": avg_identity,
                "value_cost": avg_value,
                "relationship_cost": avg_relationship,
                "habit_cost": avg_habit,
                "total_cost": avg_total
            },
            "measurements": len(self._cost_history),
            "compression_history": len(self._compression_history)
        }
    
    def suggest_optimizations(self) -> List[str]:
        """
        建议优化项
        
        基于当前状态，建议降低成本的优化。
        
        Returns:
            优化建议列表
        """
        suggestions = []
        
        # 检查身份成本
        if len(self.identity.capabilities) > 5:
            suggestions.append(f"精简能力列表: {len(self.identity.capabilities)} → 5")
        
        # 检查价值成本
        if len(self.values.core_values) > 5:
            suggestions.append(f"精简核心价值: {len(self.values.core_values)} → 3-5")
        
        if len(self.values.behavioral_principles) > 5:
            suggestions.append(f"精简行为准则: {len(self.values.behavioral_principles)} → 3-5")
        
        # 检查关系成本
        if len(self.relationships.user_preferences) > 10:
            suggestions.append(f"精简用户偏好: {len(self.relationships.user_preferences)} → 5-10")
        
        # 检查习惯成本
        if len(self.habits.thinking_habits) > 5:
            suggestions.append(f"抽象思维习惯: {len(self.habits.thinking_habits)} → 3")
        
        # 检查当前模型大小
        current_size = self._compute_model_size()
        if current_size > 5000:
            suggestions.append(f"模型较大({current_size}字节)，建议执行压缩")
        
        return suggestions
    
    def compute_cost_efficiency(self) -> float:
        """
        计算成本效率
        
        = 身份重要性 / 维持成本
        
        衡量每单位成本维持了多少"自我"的重要性。
        
        Returns:
            成本效率分数 (0-1)
        """
        # 身份重要性 = 能力数 × 纯度
        capability_score = min(1.0, len(self.identity.capabilities) / 5)
        value_score = min(1.0, len(self.values.core_values) / 5)
        importance = (capability_score + value_score) / 2
        
        # 当前成本
        if self._cost_history:
            current_cost = self._cost_history[-1].total_cost
        else:
            current_cost = self.compute_self_maintenance_cost().total_cost
        
        # 成本效率
        # 假设理想成本为50 tokens
        ideal_cost = 50.0
        cost_ratio = ideal_cost / max(1, current_cost)
        
        efficiency = importance * min(1.0, cost_ratio)
        
        return min(1.0, efficiency)
    
    def track_self_evolution(self) -> Dict[str, Any]:
        """
        追踪自我演化
        
        分析自我模型的演化趋势。
        
        Returns:
            演化报告
        """
        if len(self._compression_history) < 2:
            return {
                "status": "insufficient_data",
                "message": "压缩历史不足"
            }
        
        # 分析压缩趋势
        compression_ratios = [c.compression_ratio for c in self._compression_history]
        
        # 判断趋势
        if compression_ratios[-1] < compression_ratios[0]:
            trend = "improving"
            description = "自我模型持续优化，成本降低"
        elif compression_ratios[-1] > compression_ratios[0]:
            trend = "expanding"
            description = "自我模型有所扩展"
        else:
            trend = "stable"
            description = "自我模型保持稳定"
        
        return {
            "status": "success",
            "trend": trend,
            "description": description,
            "compression_history": [
                {
                    "ratio": c.compression_ratio,
                    "before": c.before_size,
                    "after": c.after_size,
                    "timestamp": c.timestamp.isoformat()
                }
                for c in self._compression_history
            ]
        }
