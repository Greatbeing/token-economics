# -*- coding: utf-8 -*-
"""
葫芦娃 Agent - 主入口模块

整合圣哲思维引擎、智慧孵化机制和唯识进化系统的核心Agent。
定位：思维健身房 + 智慧孵化器
"""

from typing import Dict, Optional
from sage_matcher import SageMatcher
from practice_generator import PracticeGenerator
from seed_tracker import SeedTracker
from awakening_display import AwakeningDisplay


class HuluwaAgent:
    """葫芦娃思维教练Agent（思维健身房 + 智慧孵化器）"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        
        # 初始化核心模块
        self.sage_matcher = SageMatcher()
        self.practice_generator = PracticeGenerator()
        self.tracker = SeedTracker(user_id)
        self.display = AwakeningDisplay(self.tracker)
        
        # 对话状态
        self.session_state = {
            "waiting_for_practice_answer": False,
            "current_practice": None,
            "current_answers": {},
            "last_insight": None  # 新增：记录最近一次洞察
        }
    
    def process(self, user_input: str) -> Dict:
        """
        处理用户输入，返回响应
        
        Args:
            user_input: 用户输入
            
        Returns:
            {
                "response": str,  # 回复文本
                "state_update": dict,  # 状态更新
                "actions": list  # 触发的事件
            }
        """
        response = ""
        state_update = {}
        actions = []
        
        # 0. 如果正在等待练习答案，先处理答案
        if self.session_state["waiting_for_practice_answer"]:
            result = self._handle_practice_answer(user_input)
            response = result["response"]
            actions.extend(result.get("actions", []))
            
            # 检查是否有洞察
            if result.get("insight"):
                self.session_state["last_insight"] = result["insight"]
                response += "\n\n" + self.display.display_insight_encouragement(result["insight"])
            
            return {
                "response": response,
                "state_update": state_update,
                "actions": actions
            }
        
        # 1. 识别意图
        intent = self.sage_matcher.analyze_intent(user_input)
        
        # 2. 根据意图处理
        if intent == "困惑":
            response = self._handle_confusion(user_input)
        elif intent == "学习":
            response = self._handle_learning(user_input)
        elif intent == "练习":
            response = self._handle_practice()
        elif intent == "成长":
            response = self._handle_growth()
        elif intent == "洞察":
            response = self._handle_insight(user_input)
        else:  # 闲聊
            response = self._handle_greeting(user_input)
        
        return {
            "response": response,
            "state_update": state_update,
            "actions": actions
        }
    
    def _handle_confusion(self, user_input: str) -> str:
        """处理困惑咨询"""
        # 匹配圣哲
        match_result = self.sage_matcher.match_thought(user_input)
        
        lines = [
            "嘿！让我看看..." + match_result["sage"] + "可能能帮你。",
            "",
            f"【{match_result['model']}】— {match_result['sage']}",
            f"核心：{match_result['core']}",
            "",
            match_result["suggestion"],
            ""
        ]
        
        # 生成练习
        practice = self.practice_generator.generate_practice(
            match_result["model"],
            {"scenario": user_input}
        )
        
        if practice:
            lines.extend([
                "🌿 来个练习：",
                "",
                f"[场景] {practice['scenario']}",
                ""
            ])
            
            for q in practice["questions"]:
                lines.append(f"问题：{q['text']}")
                lines.append(f"提示：{q['hint']}")
                lines.append("你的回答：__________")
                lines.append("")
            
            # 更新状态
            self.session_state["waiting_for_practice_answer"] = True
            self.session_state["current_practice"] = practice
            self.session_state["current_answers"] = {}
        
        return "\n".join(lines)
    
    def _handle_learning(self, user_input: str) -> str:
        """处理学习请求"""
        # 匹配圣哲
        match_result = self.sage_matcher.match_thought(user_input)
        
        # 展示思维模型介绍
        intro = self.sage_matcher.get_model_intro(match_result["model"])
        
        lines = [
            f"好！来学{match_result['model']}。",
            intro,
            "",
            "光知道不够，得练！"
        ]
        
        # 生成练习
        practice = self.practice_generator.generate_practice(
            match_result["model"],
            {"scenario": user_input}
        )
        
        if practice:
            lines.extend([
                "🌿 来个练习：",
                "",
                f"[场景] {practice['scenario']}",
                ""
            ])
            
            for q in practice["questions"]:
                lines.append(f"问题：{q['text']}")
                lines.append("你的回答：__________")
                lines.append("")
            
            self.session_state["waiting_for_practice_answer"] = True
            self.session_state["current_practice"] = practice
            self.session_state["current_answers"] = {}
        
        return "\n".join(lines)
    
    def _handle_practice(self) -> str:
        """处理练习请求"""
        if self.session_state["current_practice"]:
            practice = self.session_state["current_practice"]
        else:
            # 随机生成一个练习
            import random
            thought_types = list(SageMatcher.THOUGHT_MODELS.keys())
            thought_type = random.choice(thought_types)
            practice = self.practice_generator.generate_practice(thought_type)
        
        if practice:
            lines = [
                f"🌿 来做{practice['thought_type']}的练习：",
                "",
                f"[场景] {practice['scenario']}",
                ""
            ]
            
            for q in practice["questions"]:
                lines.append(f"问题：{q['text']}")
                lines.append("你的回答：__________")
                lines.append("")
            
            self.session_state["waiting_for_practice_answer"] = True
            self.session_state["current_practice"] = practice
            self.session_state["current_answers"] = {}
            
            return "\n".join(lines)
        
        return "来，做个练习巩固一下..."
    
    def _handle_practice_answer(self, user_input: str) -> Dict:
        """处理练习答案"""
        actions = []
        response = ""
        insight = None
        
        practice = self.session_state["current_practice"]
        if not practice:
            return {"response": "没有正在进行的练习。", "actions": [], "insight": None}
        
        # 记录答案
        self.session_state["current_answers"][len(self.session_state["current_answers"]) + 1] = user_input
        
        # 评估答案（简化版）
        scores = self._evaluate_answer(user_input, practice)
        
        # 计算总分
        total_score = sum(scores.values()) / len(scores) * 5 if scores else 0
        
        # 增加种子
        seed_added = int(total_score / 2)
        thought_type = practice.get("thought_type", "仁学思维")
        
        awakening_event = self.tracker.add_seed(thought_type, seed_added)
        
        # 检测洞察
        context = {
            "thought_type": thought_type,
            "practice_id": practice.get("id")
        }
        detected_insight = self.tracker.detect_insight(user_input, context)
        
        if detected_insight:
            insight = detected_insight
            # 记录洞察
            wisdom = self.tracker.record_insight(insight)
            actions.append({"type": "insight_recorded", "wisdom_id": wisdom["id"]})
        
        # 生成反馈
        lines = [
            "🌿 不错！来让我看看...",
            "",
            "问题1：",
            f"你的回答：{user_input[:50]}..." if len(user_input) > 50 else f"你的回答：{user_input}",
            f"得分：{'★' * int(scores.get(1, 0))}{'☆' * (5 - int(scores.get(1, 0)))} ({scores.get(1, 0):.1f}/5)",
            "",
            f"综合得分：{total_score:.1f}/5",
            f"🌱 种子 +{seed_added}",
            f"当前：{self.display.display_seeds()}",
        ]
        
        response = "\n".join(lines)
        
        # 如果触发了涌现
        if awakening_event:
            response += "\n\n" + self.display.display_emergence_event(awakening_event)
            actions.append({"type": "emergence", "event": awakening_event})
        
        # 更新状态
        self.session_state["waiting_for_practice_answer"] = False
        self.session_state["current_practice"] = None
        
        return {
            "response": response,
            "actions": actions,
            "insight": insight,
            "practice_result": {
                "thought_type": thought_type,
                "total_score": total_score,
                "seed_added": seed_added,
                "insight": insight
            }
        }
    
    def _evaluate_answer(self, answer: str, practice: Dict) -> Dict:
        """评估用户答案"""
        # 简化评估：基于答案长度和关键词
        score = 2.0
        
        if len(answer) > 20:
            score += 1
        if len(answer) > 50:
            score += 1
        
        # 检查洞察关键词
        insight_keywords = ["我觉得", "我发现", "但是", "可能", "也许"]
        for kw in insight_keywords:
            if kw in answer:
                score += 0.5
        
        return {1: min(score, 5.0)}
    
    def _handle_growth(self) -> str:
        """处理成长查询"""
        return self.display.display_full_report()
    
    def _handle_insight(self, user_input: str) -> str:
        """处理洞察相关请求"""
        # 用户主动记录洞察
        detected = self.tracker.detect_insight(user_input)
        
        if detected:
            wisdom = self.tracker.record_insight(detected)
            return self.display.display_insight_confirmed(wisdom)
        
        # 显示智慧库
        return self.display.display_wisdom_pool()
    
    def _handle_greeting(self, user_input: str) -> str:
        """处理闲聊/打招呼"""
        greetings = ["嘿！", "哟！", "来啦！"]
        
        lines = [
            f"{greetings[0]}有什么事吗？",
            "",
            "可以告诉我：",
            "• 你的困惑 - 我帮你分析",
            "• 想学什么思维 - 我教你",
            "• 想做练习 - 我出题",
            "• 看成长 - 我给你报告",
            "",
            "🌿 或者，有什么新想法也可以说！"
        ]
        
        return "\n".join(lines)
    
    def get_status(self) -> Dict:
        """获取当前状态"""
        return {
            "user_id": self.user_id,
            "tracker_status": self.tracker.get_status(),
            "session_state": {
                "waiting_for_practice": self.session_state["waiting_for_practice_answer"],
                "has_current_practice": self.session_state["current_practice"] is not None,
                "recent_insight": self.session_state["last_insight"] is not None
            }
        }
