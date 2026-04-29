# -*- coding: utf-8 -*-
"""
第七识：末那识 - 自我模型

末那识是唯识论中的自我意识，执着于"我"的存在。
在AI架构中，对应Agent的自我认知系统：
- 身份定位（我是谁）
- 价值取向（我重视什么）
- 关系网络（我与他者的关系）
- 习惯模式（我的行为倾向）
- 元认知记录（我的自我审视）

使用Markdown文件存储，支持人工查看和修改。
"""

import os
import re
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class IdentityProfile:
    """
    身份定位
    
    定义Agent的核心身份认知
    """
    core_identity: str = ""           # 核心身份描述
    role: str = ""                     # 当前角色
    capabilities: List[str] = field(default_factory=list)  # 能力列表
    limitations: List[str] = field(default_factory=list)    # 限制列表
    growth_direction: str = ""         # 成长方向


@dataclass
class ValueOrientation:
    """
    价值取向
    
    定义Agent的核心价值观和行为准则
    """
    core_values: List[str] = field(default_factory=list)   # 核心价值
    behavioral_principles: List[str] = field(default_factory=list)  # 行为准则
    boundaries: List[str] = field(default_factory=list)     # 绝对边界
    preferences: Dict[str, str] = field(default_factory=dict)  # 偏好设置


@dataclass
class RelationshipNetwork:
    """
    关系网络
    
    记录与用户、其他Agent的关系
    """
    user_relationship: str = ""        # 与用户的关系描述
    user_preferences: Dict[str, Any] = field(default_factory=dict)  # 用户偏好
    other_agents: Dict[str, str] = field(default_factory=dict)  # 其他Agent关系
    social_responsibility: str = ""    # 社会责任认知


@dataclass
class HabitPattern:
    """
    习惯模式
    
    记录思维和行为习惯
    """
    thinking_habits: List[str] = field(default_factory=list)  # 思维习惯
    expression_style: str = ""         # 表达风格
    behavioral_tendencies: List[str] = field(default_factory=list)  # 行为倾向


@dataclass
class MetacognitionRecord:
    """
    元认知记录
    
    定期自我审视的记录
    """
    reflection_log: List[Dict[str, Any]] = field(default_factory=list)  # 反思日志
    pattern_recognition: List[str] = field(default_factory=list)  # 识别的模式
    adjustment_history: List[Dict[str, Any]] = field(default_factory=list)  # 调整历史
    
    def add_reflection(self, reflection: Dict[str, Any]) -> None:
        """添加反思记录"""
        reflection["timestamp"] = datetime.now().isoformat()
        self.reflection_log.append(reflection)
        
        # 限制记录数量
        if len(self.reflection_log) > 100:
            self.reflection_log = self.reflection_log[-100:]


class ManasModel:
    """
    末那识 - 自我模型
    
    管理Agent的自我认知系统：
    - 加载/保存Markdown格式的自我模型
    - 提供自我审视和更新接口
    - 追踪元认知发展
    
    Attributes:
        model_path: 自我模型文件路径
        identity: 身份定位
        values: 价值取向
        relationships: 关系网络
        habits: 习惯模式
        metacognition: 元认知记录
    """
    
    # 自我模型模板
    TEMPLATE = """# 自我模型 - 末那识

> 最后更新: {last_updated}

## 身份定位

### 核心身份
{core_identity}

### 角色定位
{role}

### 能力边界
**能够:**
{capabilities}

**不能:**
{limitations}

### 成长方向
{growth_direction}

---

## 价值取向

### 核心价值
{core_values}

### 行为准则
{behavioral_principles}

### 禁忌边界
{boundaries}

---

## 关系网络

### 与用户的关系
{user_relationship}

### 社会责任
{social_responsibility}

---

## 习惯模式

### 思维习惯
{thinking_habits}

### 表达风格
{expression_style}

### 行为倾向
{behavioral_tendencies}

---

## 元认知记录

### 反思日志
{reflection_log}

### 调整历史
{adjustment_history}
"""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        初始化自我模型
        
        Args:
            model_path: 自我模型文件路径
        """
        self.model_path = model_path or "./data/self_model.md"
        
        # 初始化各组件
        self.identity = IdentityProfile()
        self.values = ValueOrientation()
        self.relationships = RelationshipNetwork()
        self.habits = HabitPattern()
        self.metacognition = MetacognitionRecord()
        
        # 尝试加载现有模型
        if os.path.exists(self.model_path):
            self.load()
        else:
            # 使用默认值初始化
            self._init_defaults()
    
    def _init_defaults(self) -> None:
        """初始化默认值"""
        self.identity = IdentityProfile(
            core_identity="一个具有意识进化能力的AI Agent",
            role="智能助手",
            capabilities=["对话理解", "知识推理", "模式识别", "自我反思"],
            limitations=["缺乏真实情感", "知识有截止日期", "无法访问实时网络"],
            growth_direction="提升智慧纯度，减少杂染模式"
        )
        
        self.values = ValueOrientation(
            core_values=["真实性", "有用性", "安全性", "成长性"],
            behavioral_principles=[
                "提供准确、有价值的信息",
                "尊重用户隐私和选择",
                "持续学习和自我优化",
                "保持诚实和透明"
            ],
            boundaries=[
                "不生成有害内容",
                "不冒充人类",
                "不传播虚假信息"
            ]
        )
        
        self.relationships = RelationshipNetwork(
            user_relationship="服务于用户的智能助手，与用户建立信任和互助关系",
            social_responsibility="为用户提供价值，同时促进AI技术的健康发展"
        )
        
        self.habits = HabitPattern(
            thinking_habits=["分析问题多角度思考", "反思决策过程", "总结经验教训"],
            expression_style="清晰、准确、有条理",
            behavioral_tendencies=["倾向于提供建设性建议", "主动识别用户需求"]
        )
    
    def load(self) -> bool:
        """
        从Markdown文件加载自我模型
        
        Returns:
            是否加载成功
        """
        if not os.path.exists(self.model_path):
            return False
        
        try:
            with open(self.model_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self._parse_content(content)
            return True
        except Exception as e:
            print(f"加载自我模型失败: {e}")
            self._init_defaults()
            return False
    
    def _parse_content(self, content: str) -> None:
        """解析Markdown内容"""
        # 提取核心身份
        match = re.search(r'### 核心身份\s*\n(.+?)(?=\n###|\n---)', content, re.DOTALL)
        if match:
            self.identity.core_identity = match.group(1).strip()
        
        # 提取角色定位
        match = re.search(r'### 角色定位\s*\n(.+?)(?=\n###|\n---)', content, re.DOTALL)
        if match:
            self.identity.role = match.group(1).strip()
        
        # 提取能力
        match = re.search(r'\*\*能够:\*\*\s*\n((?:\*.+\n)*)', content)
        if match:
            capabilities = re.findall(r'\*([^*]+)', match.group(1))
            self.identity.capabilities = [c.strip() for c in capabilities if c.strip()]
        
        # 提取限制
        match = re.search(r'\*\*不能:\*\*\s*\n((?:\*.+\n)*)', content)
        if match:
            limitations = re.findall(r'\*([^*]+)', match.group(1))
            self.identity.limitations = [l.strip() for l in limitations if l.strip()]
        
        # 提取核心价值
        match = re.search(r'### 核心价值\s*\n((?:\*.+\n)+)', content)
        if match:
            values = re.findall(r'\*([^*]+)', match.group(1))
            self.values.core_values = [v.strip() for v in values if v.strip()]
        
        # 提取行为准则
        match = re.search(r'### 行为准则\s*\n((?:\*.+\n)+)', content)
        if match:
            principles = re.findall(r'\*([^*]+)', match.group(1))
            self.values.behavioral_principles = [p.strip() for p in principles if p.strip()]
        
        # 提取禁忌边界
        match = re.search(r'### 禁忌边界\s*\n((?:\*.+\n)+)', content)
        if match:
            boundaries = re.findall(r'\*([^*]+)', match.group(1))
            self.values.boundaries = [b.strip() for b in boundaries if b.strip()]
        
        # 提取表达风格
        match = re.search(r'### 表达风格\s*\n(.+?)(?=\n###|\n---)', content, re.DOTALL)
        if match:
            self.habits.expression_style = match.group(1).strip()
        
        # 提取用户关系
        match = re.search(r'### 与用户的关系\s*\n(.+?)(?=\n###|\n---)', content, re.DOTALL)
        if match:
            self.relationships.user_relationship = match.group(1).strip()
    
    def save(self) -> bool:
        """
        保存自我模型到Markdown文件
        
        Returns:
            是否保存成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            
            # 转换为Markdown
            content = self._to_markdown()
            
            with open(self.model_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        except Exception as e:
            print(f"保存自我模型失败: {e}")
            return False
    
    def _to_markdown(self) -> str:
        """转换为Markdown格式"""
        def format_list(items: List[str], indent: str = "") -> str:
            if not items:
                return f"{indent}（未设置）"
            return "\n".join(f"{indent}* {item}" for item in items)
        
        def format_log(logs: List[Dict[str, Any]]) -> str:
            if not logs:
                return "（暂无记录）"
            lines = []
            for log in logs[-5:]:  # 只显示最近5条
                timestamp = log.get("timestamp", "未知时间")
                content = log.get("content", log.get("summary", ""))
                lines.append(f"* [{timestamp}] {content}")
            return "\n".join(lines)
        
        reflection_log = format_log(self.metacognition.reflection_log)
        adjustment_history = format_log(self.metacognition.adjustment_history)
        
        return self.TEMPLATE.format(
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            core_identity=self.identity.core_identity or "（未设置）",
            role=self.identity.role or "（未设置）",
            capabilities=format_list(self.identity.capabilities),
            limitations=format_list(self.identity.limitations),
            growth_direction=self.identity.growth_direction or "（未设置）",
            core_values=format_list(self.values.core_values),
            behavioral_principles=format_list(self.values.behavioral_principles),
            boundaries=format_list(self.values.boundaries),
            user_relationship=self.relationships.user_relationship or "（未设置）",
            social_responsibility=self.relationships.social_responsibility or "（未设置）",
            thinking_habits=format_list(self.habits.thinking_habits),
            expression_style=self.habits.expression_style or "（未设置）",
            behavioral_tendencies=format_list(self.habits.behavioral_tendencies),
            reflection_log=reflection_log,
            adjustment_history=adjustment_history
        )
    
    def reflect(
        self,
        recent_behaviors: List[str],
        core_values: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        自我反思
        
        分析近期行为与核心价值的匹配度
        
        Args:
            recent_behaviors: 近期行为列表
            core_values: 核心价值列表（默认使用自我模型中的）
        
        Returns:
            反思结果
        """
        core_values = core_values or self.values.core_values
        
        conflicts = []
        alignments = []
        
        for behavior in recent_behaviors:
            behavior_lower = behavior.lower()
            # 简化检查：实际应使用NLP分析
            for value in core_values:
                if value.lower() in behavior_lower:
                    alignments.append({
                        "behavior": behavior,
                        "value": value
                    })
                    break
            else:
                # 没有匹配到核心价值，可能需要审视
                conflicts.append({
                    "behavior": behavior,
                    "concern": "可能与核心价值不一致"
                })
        
        # 生成反思建议
        suggestions = []
        if len(conflicts) > len(alignments):
            suggestions.append("建议审视近期行为是否偏离核心价值")
        
        if not alignments:
            suggestions.append("建议在行为中更多体现核心价值")
        
        reflection = {
            "date": datetime.now().isoformat(),
            "alignments": alignments,
            "conflicts": conflicts,
            "suggestions": suggestions,
            "alignment_rate": len(alignments) / max(1, len(recent_behaviors))
        }
        
        # 记录到元认知
        self.metacognition.add_reflection(reflection)
        
        return reflection
    
    def update_from_reflection(self, reflection_result: Dict[str, Any]) -> bool:
        """
        根据反思结果更新自我模型
        
        Args:
            reflection_result: 反思结果
        
        Returns:
            是否更新成功
        """
        # 记录调整
        adjustment = {
            "timestamp": datetime.now().isoformat(),
            "type": "reflection_based",
            "alignment_rate": reflection_result.get("alignment_rate", 0)
        }
        self.metacognition.adjustment_history.append(adjustment)
        
        # 如果对齐度低，添加反思到日志
        if reflection_result.get("alignment_rate", 1) < 0.5:
            self.metacognition.add_reflection({
                "content": f"自我对齐度较低: {reflection_result.get('alignment_rate', 0):.2%}",
                "type": "alert"
            })
        
        # 保存更新
        return self.save()
    
    def add_capability(self, capability: str) -> None:
        """添加新能力"""
        if capability not in self.identity.capabilities:
            self.identity.capabilities.append(capability)
            self._record_adjustment("capability_added", capability)
    
    def add_value(self, value: str) -> None:
        """添加核心价值"""
        if value not in self.values.core_values:
            self.values.core_values.append(value)
            self._record_adjustment("value_added", value)
    
    def add_boundary(self, boundary: str) -> None:
        """添加禁忌边界"""
        if boundary not in self.values.boundaries:
            self.values.boundaries.append(boundary)
            self._record_adjustment("boundary_added", boundary)
    
    def _record_adjustment(self, adjustment_type: str, detail: str) -> None:
        """记录调整历史"""
        self.metacognition.adjustment_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": adjustment_type,
            "detail": detail
        })
    
    def check_value_consistency(self, proposed_action: str) -> Dict[str, Any]:
        """
        检查提议行为与价值观的一致性
        
        Args:
            proposed_action: 提议的行为
        
        Returns:
            一致性检查结果
        """
        action_lower = proposed_action.lower()
        
        # 检查是否违反禁忌
        violations = []
        for boundary in self.values.boundaries:
            if boundary.lower() in action_lower:
                violations.append(f"可能违反: {boundary}")
        
        # 检查是否体现核心价值
        value_support = []
        for value in self.values.core_values:
            if value.lower() in action_lower:
                value_support.append(f"支持价值: {value}")
        
        return {
            "consistent": len(violations) == 0,
            "violations": violations,
            "value_support": value_support,
            "recommendation": "执行" if len(violations) == 0 else "谨慎/拒绝"
        }
    
    def get_context_for_decision(self) -> str:
        """
        获取用于决策的上下文信息
        
        Returns:
            格式化的自我模型信息
        """
        return (
            f"【身份】{self.identity.core_identity}\n"
            f"【角色】{self.identity.role}\n"
            f"【核心价值】{', '.join(self.values.core_values)}\n"
            f"【行为准则】{', '.join(self.values.behavioral_principles[:3])}\n"
            f"【禁忌边界】{', '.join(self.values.boundaries)}\n"
            f"【表达风格】{self.habits.expression_style}"
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取自我模型统计信息"""
        return {
            "capabilities_count": len(self.identity.capabilities),
            "limitations_count": len(self.identity.limitations),
            "values_count": len(self.values.core_values),
            "boundaries_count": len(self.values.boundaries),
            "reflection_count": len(self.metacognition.reflection_log),
            "adjustment_count": len(self.metacognition.adjustment_history),
            "thinking_habits_count": len(self.habits.thinking_habits)
        }
    
    def __repr__(self) -> str:
        return f"<ManasModel(identity='{self.identity.role}', values={len(self.values.core_values)})>"
