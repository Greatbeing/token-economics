# -*- coding: utf-8 -*-
"""
第六识：意识 - 推理决策层

第六识是唯识论中的意识，负责思维、推理、决策等功能。
在AI架构中，对应Agent的核心决策系统：

核心功能：
1. 上下文理解与意图识别
2. 基于种子激活的策略规划
3. 响应生成与行为决策
4. 结果评估与反思

与八识的协作：
- 接收前五识的感知信息
- 参考末那识的自我模型
- 从阿赖耶识获取经验知识
- 通过熏习系统更新种子库
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from .alaya_store import Seed, SeedType
from .manas_model import ManasModel
from .vasana import Vasana, ExperienceRecord
from .senses import Senses, SensoryInput


@dataclass
class DecisionContext:
    """
    决策上下文
    
    封装决策所需的所有信息
    """
    sensory_input: SensoryInput      # 感知输入
    activated_seeds: List[Tuple[Seed, float]]  # 激活的种子
    self_model_context: str         # 自我模型上下文
    available_actions: List[str]     # 可用行动
    constraints: List[str]           # 约束条件
    goal: Optional[str] = None       # 目标（如果有）


@dataclass
class Decision:
    """
    决策结果
    
    包含决策的完整信息
    """
    action: str                      # 选定的行动
    reasoning: str                  # 推理过程
    confidence: float               # 置信度
    seed_influence: List[str]       # 影响的种子ID
    alternative_actions: List[str]  # 备选行动
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Evaluation:
    """
    结果评估
    
    对决策执行结果的事后评估
    """
    decision: Decision              # 被评估的决策
    outcome: float                  # 结果评分 (0-1)
    feedback: str                   # 反馈信息
    improvement_suggestions: List[str]  # 改进建议
    timestamp: datetime = field(default_factory=datetime.now)


class Consciousness:
    """
    第六识 - 意识（推理决策层）
    
    核心决策系统，整合各层信息进行推理和决策：
    1. 理解阶段：解析感知输入，理解意图
    2. 检索阶段：从种子库激活相关经验
    3. 决策阶段：结合自我模型做出决策
    4. 评估阶段：评估结果并反思
    
    Attributes:
        vasana: 熏习系统（用于种子检索和记录）
        manas: 自我模型
        senses: 感知层
        config: 配置参数
    """
    
    def __init__(
        self,
        vasana: Vasana,
        manas: ManasModel,
        senses: Senses,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化意识层
        
        Args:
            vasana: 熏习系统
            manas: 自我模型
            senses: 感知层
            config: 配置参数
        """
        self.vasana = vasana
        self.manas = manas
        self.senses = senses
        self.config = config or {}
        
        # 决策配置
        self.max_activated_seeds = self.config.get("max_activated_seeds", 5)
        self.confidence_threshold = self.config.get("confidence_threshold", 0.5)
        self.consider_wisdom_seeds = self.config.get("consider_wisdom_seeds", True)
    
    def understand(self, input_data: Any) -> SensoryInput:
        """
        理解阶段：处理感知输入
        
        Args:
            input_data: 输入数据
        
        Returns:
            处理后的感知输入
        """
        return self.senses.perceive(input_data)
    
    def retrieve_experience(self, query: str, context: Optional[Dict[str, Any]] = None) -> List[Tuple[Seed, float]]:
        """
        检索阶段：从种子库激活相关经验
        
        Args:
            query: 查询文本
            context: 上下文信息
        
        Returns:
            激活的种子列表
        """
        return self.vasana.activate_seeds(
            query=query,
            context=context,
            top_k=self.max_activated_seeds
        )
    
    def decide(
        self,
        sensory_input: SensoryInput,
        activated_seeds: List[Tuple[Seed, float]],
        available_actions: Optional[List[str]] = None
    ) -> Decision:
        """
        决策阶段：基于所有信息做出决策
        
        Args:
            sensory_input: 感知输入
            activated_seeds: 激活的种子
            available_actions: 可用行动列表
        
        Returns:
            决策结果
        """
        # 获取自我模型上下文
        self_context = self.manas.get_context_for_decision()
        
        # 生成可用行动（如果未提供）
        if available_actions is None:
            available_actions = self._generate_actions(sensory_input, activated_seeds)
        
        # 基于种子和自我模型评估每个行动
        action_scores = {}
        for action in available_actions:
            score = self._evaluate_action(action, sensory_input, activated_seeds)
            action_scores[action] = score
        
        # 选择最佳行动
        if action_scores:
            best_action = max(action_scores.items(), key=lambda x: x[1])
            action = best_action[0]
            confidence = best_action[1]
        else:
            action = "提供一般性回应"
            confidence = 0.5
        
        # 生成推理过程
        reasoning = self._generate_reasoning(action, sensory_input, activated_seeds)
        
        return Decision(
            action=action,
            reasoning=reasoning,
            confidence=confidence,
            seed_influence=[s[0].seed_id for s in activated_seeds[:3]],
            alternative_actions=[a for a in available_actions if a != action][:2]
        )
    
    def _generate_actions(
        self,
        sensory_input: SensoryInput,
        activated_seeds: List[Tuple[Seed, float]]
    ) -> List[str]:
        """
        生成可能的行动选项
        
        Args:
            sensory_input: 感知输入
            activated_seeds: 激活的种子
        
        Returns:
            行动列表
        """
        actions = []
        
        # 基于意图生成行动
        intent = sensory_input.intent
        if intent == "question":
            actions.append("提供直接回答")
            actions.append("询问更多信息后回答")
        elif intent == "request":
            actions.append("执行请求")
            actions.append("确认理解后执行")
        elif intent == "statement":
            actions.append("认可并适当回应")
            actions.append("提供相关建议")
        elif intent == "command":
            actions.append("立即执行")
            actions.append("规划后执行")
        else:
            actions.append("友好对话")
        
        # 基于激活的智慧种子添加选项
        for seed, influence in activated_seeds:
            if seed.seed_type == SeedType.WISDOM and influence > 0.3:
                actions.append(f"运用智慧: {seed.content[:50]}")
        
        # 添加审慎选项
        actions.append("谨慎评估后回应")
        
        return list(set(actions))[:5]  # 去重，最多5个
    
    def _evaluate_action(
        self,
        action: str,
        sensory_input: SensoryInput,
        activated_seeds: List[Tuple[Seed, float]]
    ) -> float:
        """
        评估行动得分
        
        Args:
            action: 行动
            sensory_input: 感知输入
            activated_seeds: 激活的种子
        
        Returns:
            得分 (0-1)
        """
        score = 0.5  # 基础分
        
        # 检查与价值观的一致性
        consistency = self.manas.check_value_consistency(action)
        if consistency["consistent"]:
            score += 0.2
        else:
            score -= 0.3
        
        # 基于经验调整
        for seed, influence in activated_seeds:
            # 正面经验支持
            if seed.purity > 0.6 and seed.weight > 0.3:
                score += influence * 0.1
            # 负面经验警告
            elif seed.seed_type == SeedType.TRAUMA and seed.purity < 0.3:
                score -= influence * 0.2
        
        # 基于意图匹配
        if sensory_input.intent == "question" and "回答" in action:
            score += 0.1
        elif sensory_input.intent == "request" and "执行" in action:
            score += 0.1
        
        # 情感匹配
        if sensory_input.sentiment == "negative" and "谨慎" in action:
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _generate_reasoning(
        self,
        action: str,
        sensory_input: SensoryInput,
        activated_seeds: List[Tuple[Seed, float]]
    ) -> str:
        """
        生成推理过程描述
        
        Args:
            action: 选定的行动
            sensory_input: 感知输入
            activated_seeds: 激活的种子
        
        Returns:
            推理过程文本
        """
        parts = []
        
        # 意图理解
        parts.append(f"理解用户意图: {sensory_input.intent}")
        
        # 经验激活
        if activated_seeds:
            seed_types = [s[0].seed_type.value for s in activated_seeds]
            parts.append(f"激活相关经验: {', '.join(set(seed_types))}")
        
        # 价值观考量
        consistency = self.manas.check_value_consistency(action)
        if consistency["value_support"]:
            parts.append(f"符合价值观: {', '.join(consistency['value_support'])}")
        
        # 最终决策
        parts.append(f"决定: {action}")
        
        return " | ".join(parts)
    
    def evaluate(
        self,
        decision: Decision,
        actual_response: str,
        user_feedback: Optional[str] = None
    ) -> Evaluation:
        """
        评估阶段：评估决策结果
        
        Args:
            decision: 决策
            actual_response: 实际响应
            user_feedback: 用户反馈
        
        Returns:
            评估结果
        """
        # 基础评估
        outcome = decision.confidence
        
        # 根据种子结果调整
        for seed_id in decision.seed_influence:
            seed = self.vasana.store.get(seed_id)
            if seed and seed.activation_count > 0:
                outcome = outcome * 0.7 + seed.purity * 0.3
        
        # 生成改进建议
        suggestions = []
        if outcome < 0.5:
            suggestions.append("建议更多参考智慧种子")
        if len(decision.seed_influence) < 2:
            suggestions.append("可检索更多相关经验")
        if decision.confidence < 0.6:
            suggestions.append("决策置信度较低，可考虑询问更多")
        
        return Evaluation(
            decision=decision,
            outcome=outcome,
            feedback=user_feedback or "基于种子激活和自我模型评估",
            improvement_suggestions=suggestions
        )
    
    def think(
        self,
        input_data: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[SensoryInput, List[Tuple[Seed, float]], Decision]:
        """
        完整的思考过程
        
        整合理解、检索、决策三个阶段
        
        Args:
            input_data: 输入数据
            context: 上下文
        
        Returns:
            (感知输入, 激活种子, 决策) 元组
        """
        # 理解阶段
        sensory = self.understand(input_data)
        
        # 检索阶段
        query = sensory.processed_content
        seeds = self.retrieve_experience(query, context)
        
        # 决策阶段
        decision = self.decide(sensory, seeds)
        
        return sensory, seeds, decision
    
    def reflect(
        self,
        interaction: Dict[str, Any],
        outcome: float
    ) -> str:
        """
        反思：产生智慧种子
        
        根据交互结果产生新的智慧
        
        Args:
            interaction: 交互记录
            outcome: 结果评分
        
        Returns:
            生成的智慧种子ID
        """
        if outcome < 0.7:
            # 结果不佳，生成反思
            reflection = (
                f"反思这次交互："
                f"输入={interaction.get('user_input', '')[:50]}..., "
                f"结果评分={outcome:.2f}"
            )
            
            seed_id = self.vasana.record_reflection(
                reflection_content=reflection,
                wisdom_level=outcome
            )
            return seed_id
        
        return ""
    
    def process(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None,
        generate_response: bool = True
    ) -> Dict[str, Any]:
        """
        完整处理流程
        
        执行从输入到输出的完整处理
        
        Args:
            user_input: 用户输入
            context: 上下文
            generate_response: 是否生成响应
        
        Returns:
            处理结果字典
        """
        context = context or {}
        
        # 1. 感知
        sensory = self.understand(user_input)
        
        # 2. 检索
        seeds = self.retrieve_experience(user_input, context)
        
        # 3. 决策
        decision = self.decide(sensory, seeds)
        
        # 4. 生成响应（如果需要）
        response = ""
        if generate_response:
            response = self._generate_text_response(user_input, sensory, decision, seeds)
        
        # 5. 评估
        evaluation = self.evaluate(decision, response)
        
        return {
            "user_input": user_input,
            "sensory_analysis": {
                "intent": sensory.intent,
                "sentiment": sensory.sentiment,
                "entities": sensory.entities,
                "keywords": sensory.keywords
            },
            "activated_seeds": [
                {"id": s[0].seed_id, "type": s[0].seed_type.value, "influence": s[1]}
                for s in seeds
            ],
            "decision": {
                "action": decision.action,
                "reasoning": decision.reasoning,
                "confidence": decision.confidence
            },
            "response": response,
            "evaluation": {
                "outcome": evaluation.outcome,
                "suggestions": evaluation.improvement_suggestions
            }
        }
    
    def _generate_text_response(
        self,
        user_input: str,
        sensory: SensoryInput,
        decision: Decision,
        seeds: List[Tuple[Seed, float]]
    ) -> str:
        """
        生成文本响应
        
        Args:
            user_input: 用户输入
            sensory: 感知分析
            decision: 决策
            seeds: 激活的种子
        
        Returns:
            响应文本
        """
        # 简单的响应生成逻辑
        intent = sensory.intent
        
        if intent == "question":
            # 检查是否有相关知识种子
            knowledge_seeds = [s for s, _ in seeds if s.seed_type == SeedType.KNOWLEDGE]
            if knowledge_seeds:
                return f"根据我的理解：{knowledge_seeds[0].content[:100]}..."
            else:
                return "这是一个好问题。让我基于一般知识来回答。"
        
        elif intent == "request":
            return f"好的，我会帮你处理这个请求。"
        
        elif intent == "statement":
            return "感谢分享你的想法。"
        
        else:
            return "我理解你的意思了。有什么我可以帮助你的吗？"
