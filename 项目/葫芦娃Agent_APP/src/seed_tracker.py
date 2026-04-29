# -*- coding: utf-8 -*-
"""
种子追踪器 - SeedTracker

追踪用户的思维种子积累、智慧孵化进程和觉醒等级进化。
新增智慧孵化功能：检测、记录用户产生的原创洞察。
"""

from typing import Dict, List, Optional
from datetime import datetime
import json
import re


class SeedTracker:
    """思维种子追踪器 + 智慧孵化器"""
    
    # 觉醒等级定义
    AWAKENING_LEVELS = {
        1: {"name": "迷途者", "description": "遇到问题习惯性焦虑", "requirements": "注册即得"},
        2: {"name": "觉醒者", "description": "开始用圣哲思维思考", "requirements": "任意种子达2颗"},
        3: {"name": "修行者", "description": "能主动运用多种思维框架", "requirements": "任意种子达5颗"},
        4: {"name": "明智者", "description": "思维灵活，快速匹配情境", "requirements": "3种以上种子达3颗"},
        5: {"name": "圣哲境", "description": "内化为本能，智慧涌现", "requirements": "5种以上种子达4颗"}
    }
    
    # 思维类型定义
    THOUGHT_TYPES = [
        "仁学思维", "逍遥思维", "无为思维", "四谛思维",
        "心性思维", "心学思维", "产婆术", "实践智慧", "权衡思维"
    ]
    
    # 涌现触发关键词
    EMERGENCE_KEYWORDS = {
        "质疑类": ["但是", "我觉得不对", "好像有问题", "这不对"],
        "联想类": ["这让我想到", "类似于", "和...一样", "就像"],
        "归纳类": ["所以规律是", "我发现", "总的来说", "结论是"],
        "应用类": ["如果用在", "可以应用于", "是不是也能"],
        "边界类": ["但是如果", "那如果", "例外是", "特殊情况"]
    }
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.seeds: Dict[str, int] = {t: 0 for t in self.THOUGHT_TYPES}
        self.awakening_level = 1
        self.history: List[Dict] = []
        self.milestones: List[Dict] = []
        
        # 智慧孵化相关（新增）
        self.wisdom_pool: List[Dict] = []  # 用户产生的原创洞察
        self.insights_count = 0  # 洞察总数
        self.emergence_count = 0  # 涌现次数
        
        self.created_at = datetime.now().isoformat()
        self.last_active = datetime.now().isoformat()
    
    def add_seed(self, thought_type: str, points: int = 1) -> Optional[Dict]:
        """
        增加思维种子
        
        Args:
            thought_type: 思维类型
            points: 增加的种子数量
            
        Returns:
            如果触发智慧涌现，返回事件信息；否则返回None
        """
        if thought_type not in self.seeds:
            return None
        
        old_level = self.awakening_level
        old_seeds = self.seeds.copy()
        
        # 增加种子
        self.seeds[thought_type] += points
        self.last_active = datetime.now().isoformat()
        
        # 记录历史
        self.history.append({
            "date": datetime.now().isoformat(),
            "action": "add_seed",
            "thought_type": thought_type,
            "points": points,
            "new_value": self.seeds[thought_type]
        })
        
        # 检查智慧涌现
        awakening_event = None
        if self.seeds[thought_type] == 5 and old_seeds[thought_type] < 5:
            awakening_event = self._trigger_awakening(thought_type)
        
        # 重新计算等级
        self._recalculate_level()
        
        return awakening_event
    
    def _trigger_awakening(self, thought_type: str) -> Dict:
        """触发智慧涌现事件"""
        old_level = self.awakening_level
        
        # 升级
        if self.awakening_level < 5:
            self.awakening_level += 1
        
        self.emergence_count += 1
        
        event = {
            "date": datetime.now().isoformat(),
            "type": "智慧涌现",
            "thought_type": thought_type,
            "old_level": old_level,
            "new_level": self.awakening_level,
            "message": f"你的\"{thought_type}\"种子集齐了5颗星，触发智慧涌现！"
        }
        
        self.milestones.append(event)
        self.history.append({
            "date": datetime.now().isoformat(),
            "action": "awakening",
            "thought_type": thought_type
        })
        
        return event
    
    def _recalculate_level(self) -> None:
        """重新计算觉醒等级"""
        # 统计各水平种子数
        strong_seeds = sum(1 for v in self.seeds.values() if v >= 4)  # 4星以上
        medium_seeds = sum(1 for v in self.seeds.values() if v >= 3)  # 3星以上
        any_seeds = sum(1 for v in self.seeds.values() if v >= 2)     # 2星以上
        max_seed = max(self.seeds.values()) if self.seeds else 0
        
        new_level = 1
        
        # L2: 任意种子达2颗
        if any_seeds >= 1:
            new_level = 2
        
        # L3: 任意种子达5颗
        if max_seed >= 5:
            new_level = 3
            
        # L4: 3种以上种子达3颗
        if medium_seeds >= 3:
            new_level = 4
            
        # L5: 5种以上种子达4颗
        if strong_seeds >= 5:
            new_level = 5
        
        self.awakening_level = new_level
    
    # ========== 智慧孵化功能（新增）==========
    
    def detect_insight(self, user_input: str, context: Dict = None) -> Optional[Dict]:
        """
        检测用户输入中是否包含洞察
        
        Args:
            user_input: 用户输入
            context: 上下文信息（可选）
            
        Returns:
            如果检测到洞察，返回洞察信息；否则返回None
        """
        if not user_input:
            return None
        
        insight_type = None
        insight_score = 0
        
        # 检查关键词类型
        for kw_type, keywords in self.EMERGENCE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in user_input:
                    insight_type = kw_type
                    insight_score += 2
                    break
        
        # 检查洞察特征
        insight_features = [
            (r"我[的发]现.*?[是规律结论]", 3),  # 发现规律
            (r"[如果那].*?呢\?", 2),  # 提出假设
            (r"但是.*?[是|在|有].*?", 2),  # 发现边界
            (r"类似于.*?但.*?", 2),  # 类比差异
            (r"不只是.*?而是.*?", 3),  # 超越原意
        ]
        
        for pattern, score in insight_features:
            if re.search(pattern, user_input):
                insight_score += score
        
        # 超过阈值认为是洞察
        if insight_score >= 4:
            return {
                "type": insight_type or "综合洞察",
                "score": insight_score,
                "content": user_input,
                "context": context,
                "date": datetime.now().isoformat()
            }
        
        return None
    
    def record_insight(self, insight: Dict) -> Dict:
        """
        记录用户的洞察到智慧库
        
        Args:
            insight: 洞察信息
            
        Returns:
            记录结果
        """
        wisdom = {
            "id": len(self.wisdom_pool) + 1,
            "content": insight.get("content", ""),
            "type": insight.get("type", "综合洞察"),
            "score": insight.get("score", 1),
            "source_thought": insight.get("context", {}).get("thought_type"),
            "date": insight.get("date", datetime.now().isoformat()),
            "tags": self._extract_tags(insight.get("content", ""))
        }
        
        self.wisdom_pool.append(wisdom)
        self.insights_count += 1
        
        # 记录历史
        self.history.append({
            "date": datetime.now().isoformat(),
            "action": "record_insight",
            "insight_id": wisdom["id"]
        })
        
        return wisdom
    
    def _extract_tags(self, content: str) -> List[str]:
        """从洞察内容中提取标签"""
        tags = []
        
        # 思维类型标签
        for thought in self.THOUGHT_TYPES:
            if thought in content:
                tags.append(thought)
        
        # 通用概念标签
        concepts = ["人际关系", "自我认知", "压力", "选择", "意义", "行动"]
        for concept in concepts:
            if concept in content:
                tags.append(concept)
        
        return tags[:5]  # 最多5个标签
    
    def get_insight_suggestions(self, user_input: str) -> List[str]:
        """
        根据用户输入生成引导涌现的建议
        
        Args:
            user_input: 用户输入
            
        Returns:
            引导建议列表
        """
        suggestions = []
        
        # 基于关键词生成建议
        if "但是" in user_input or "不对" in user_input:
            suggestions.append("你发现了什么问题？能详细说说吗？")
        
        if "好像" in user_input:
            suggestions.append("你的直觉是什么？")
        
        if len(user_input) > 50:
            suggestions.append("你能不能把这个想法再明确地说一遍？")
        
        # 默认建议
        if not suggestions:
            suggestions.append("你觉得这个发现可以用到别的地方吗？")
            suggestions.append("如果换一种情况，这个规律还成立吗？")
        
        return suggestions
    
    # ========== 原有功能 ==========
    
    def get_status(self) -> Dict:
        """获取当前状态"""
        return {
            "user_id": self.user_id,
            "level": self.awakening_level,
            "level_name": self.AWAKENING_LEVELS[self.awakening_level]["name"],
            "seeds": self.seeds.copy(),
            "seed_count": sum(self.seeds.values()),
            "insights_count": self.insights_count,
            "emergence_count": self.emergence_count,
            "wisdom_pool_size": len(self.wisdom_pool),
            "created_at": self.created_at,
            "last_active": self.last_active
        }
    
    def get_seed_display(self, thought_type: str) -> str:
        """获取种子的可视化显示"""
        if thought_type not in self.seeds:
            return ""
        
        count = self.seeds[thought_type]
        full = "★" * count
        empty = "☆" * (5 - count)
        return f"[{full}{empty}] ({count}/5)"
    
    def get_all_seeds_display(self) -> str:
        """获取所有种子的可视化显示"""
        lines = []
        for t in self.THOUGHT_TYPES:
            if self.seeds[t] > 0:
                lines.append(f"{t}：{self.get_seed_display(t)}")
        
        if not lines:
            return "还没有种子，继续练习吧！"
        
        return "\n".join(lines)
    
    def generate_report(self, days: int = 30) -> Dict:
        """
        生成成长报告
        
        Args:
            days: 报告周期（天数）
            
        Returns:
            成长报告字典
        """
        now = datetime.now()
        
        # 筛选近期历史
        recent_history = []
        for item in self.history:
            item_date = datetime.fromisoformat(item["date"])
            if (now - item_date).days <= days:
                recent_history.append(item)
        
        # 统计
        practice_count = sum(1 for h in recent_history if h.get("action") == "add_seed")
        insight_count = sum(1 for h in recent_history if h.get("action") == "record_insight")
        
        # 使用最多的思维
        usage = {}
        for h in recent_history:
            if h.get("action") == "add_seed":
                tt = h.get("thought_type", "")
                usage[tt] = usage.get(tt, 0) + 1
        
        most_used = max(usage, key=usage.get) if usage else None
        
        # 最有进步的思维
        # 简化：取种子最多的
        active_thoughts = [(t, c) for t, c in self.seeds.items() if c > 0]
        most_grown = max(active_thoughts, key=lambda x: x[1])[0] if active_thoughts else None
        
        # 获取近期洞察
        recent_insights = [w for w in self.wisdom_pool 
                          if (now - datetime.fromisoformat(w["date"])).days <= days]
        
        return {
            "user_id": self.user_id,
            "level": self.awakening_level,
            "level_name": self.AWAKENING_LEVELS[self.awakening_level]["name"],
            "practice_count": practice_count,
            "insight_count": insight_count,
            "most_used_thought": most_used,
            "most_grown_thought": most_grown,
            "recent_insights": recent_insights[-3:] if recent_insights else [],
            "total_insights": self.insights_count,
            "emergence_count": self.emergence_count
        }
    
    def to_dict(self) -> Dict:
        """导出完整数据"""
        return {
            "user_id": self.user_id,
            "seeds": self.seeds,
            "awakening_level": self.awakening_level,
            "history": self.history,
            "milestones": self.milestones,
            "wisdom_pool": self.wisdom_pool,
            "insights_count": self.insights_count,
            "emergence_count": self.emergence_count,
            "created_at": self.created_at,
            "last_active": self.last_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "SeedTracker":
        """从数据恢复"""
        tracker = cls(data.get("user_id", ""))
        tracker.seeds = data.get("seeds", {t: 0 for t in cls.THOUGHT_TYPES})
        tracker.awakening_level = data.get("awakening_level", 1)
        tracker.history = data.get("history", [])
        tracker.milestones = data.get("milestones", [])
        tracker.wisdom_pool = data.get("wisdom_pool", [])
        tracker.insights_count = data.get("insights_count", 0)
        tracker.emergence_count = data.get("emergence_count", 0)
        tracker.created_at = data.get("created_at", datetime.now().isoformat())
        tracker.last_active = data.get("last_active", datetime.now().isoformat())
        return tracker
