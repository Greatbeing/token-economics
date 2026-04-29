# -*- coding: utf-8 -*-
"""
觉醒展示器 - AwakeningDisplay

生成用户成长报告、可视化展示、激励内容、智慧孵化展示。
新增智慧库展示功能：展示用户产生的原创洞察。
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from seed_tracker import SeedTracker


class AwakeningDisplay:
    """觉醒展示器 + 智慧孵化展示器"""
    
    # 等级描述
    LEVEL_DESCRIPTIONS = {
        1: "遇到问题习惯焦虑，需要引导",
        2: "开始有圣哲思维的意识",
        3: "能主动运用多种思维框架",
        4: "思维灵活，能快速匹配情境",
        5: "内化为本能，智慧涌现"
    }
    
    # 等级徽章
    LEVEL_BADGES = {
        1: "🌱",
        2: "🌿",
        3: "🌳",
        4: "🍃",
        5: "✨"
    }
    
    # 思维类型图标
    THOUGHT_ICONS = {
        "仁学思维": "🤝",
        "逍遥思维": "🦋",
        "无为思维": "☯️",
        "四谛思维": "🪷",
        "心性思维": "💎",
        "心学思维": "⚡",
        "产婆术": "🔮",
        "实践智慧": "⚖️",
        "权衡思维": "🎭"
    }
    
    # 升级激励语
    LEVEL_UP_MESSAGES = {
        2: "🌿 你开始觉醒！开始用圣哲的智慧思考问题了。",
        3: "🌳 恭喜晋升修行者！你已经能运用多种思维框架了。",
        4: "🍃 你成为明智者了！思维灵活，快速匹配各种情境。",
        5: "✨ 你达到了圣哲境！智慧内化为本能，炉火纯青！"
    }
    
    # 洞察类型图标
    INSIGHT_ICONS = {
        "质疑类": "🤔",
        "联想类": "🔗",
        "归纳类": "📊",
        "应用类": "🚀",
        "边界类": "⚠️",
        "综合洞察": "💡"
    }
    
    def __init__(self, tracker: SeedTracker):
        self.tracker = tracker
    
    def display_level(self) -> str:
        """显示当前等级"""
        level = self.tracker.awakening_level
        name = self.tracker.AWAKENING_LEVELS[level]["name"]
        badge = self.LEVEL_BADGES.get(level, "🌱")
        desc = self.LEVEL_DESCRIPTIONS[level]
        
        return f"""
{badge} 觉醒等级：L{level} {name}
   {desc}
"""
    
    def display_seeds(self, filter_active: bool = True) -> str:
        """显示种子状态"""
        lines = ["🌱 思维种子库："]
        
        active_seeds = [(t, c) for t, c in self.tracker.seeds.items() if c > 0]
        
        if not active_seeds:
            return lines[0] + "\n   还没有种子，继续练习吧！"
        
        for i, (thought_type, count) in enumerate(active_seeds):
            icon = self.THOUGHT_ICONS.get(thought_type, "")
            bar = "▓" * count + "░" * (5 - count)
            
            if i == len(active_seeds) - 1:
                prefix = "└─"
            else:
                prefix = "├─"
            
            lines.append(f"   {prefix} {icon} {thought_type}：{count}/5 {bar}")
        
        # 补充未激活的种子
        inactive = sum(1 for c in self.tracker.seeds.values() if c == 0)
        if inactive > 0 and filter_active:
            lines.append(f"   └─ ...还有{inactive}种思维待解锁")
        
        return "\n".join(lines)
    
    # ========== 智慧孵化展示（新增）==========
    
    def display_wisdom_pool(self, limit: int = 5) -> str:
        """显示智慧库"""
        if not self.tracker.wisdom_pool:
            return "✨ 智慧库：还没有洞察，继续练习，孵化物将破壳而出！"
        
        lines = ["✨ 智慧库："]
        
        # 显示最近的洞察
        recent_wisdoms = self.tracker.wisdom_pool[-limit:]
        for i, wisdom in enumerate(recent_wisdoms):
            icon = self.INSIGHT_ICONS.get(wisdom.get("type", ""), "💡")
            
            if i == len(recent_wisdoms) - 1:
                prefix = "└─"
            else:
                prefix = "├─"
            
            # 截取洞察内容的前30个字符
            content = wisdom.get("content", "")[:30]
            if len(wisdom.get("content", "")) > 30:
                content += "..."
            
            lines.append(f"   {prefix} {icon} {content}")
        
        if len(self.tracker.wisdom_pool) > limit:
            lines.append(f"   └─ ...还有{len(self.tracker.wisdom_pool) - limit}条")
        
        lines.append(f"   共 {self.tracker.insights_count} 条洞察")
        
        return "\n".join(lines)
    
    def display_wisdom_detail(self, wisdom_id: int = None) -> str:
        """显示某条洞察的详情"""
        if wisdom_id:
            wisdom = next((w for w in self.tracker.wisdom_pool if w["id"] == wisdom_id), None)
        else:
            wisdom = self.tracker.wisdom_pool[-1] if self.tracker.wisdom_pool else None
        
        if not wisdom:
            return "✨ 智慧库：还没有洞察记录"
        
        icon = self.INSIGHT_ICONS.get(wisdom.get("type", ""), "💡")
        date = datetime.fromisoformat(wisdom["date"]).strftime("%Y-%m-%d")
        
        lines = [
            f"✨ 💡 洞察 #{wisdom['id']}",
            f"   📅 {date}",
            f"   🏷️ 类型：{wisdom.get('type', '综合洞察')}",
            f"   📝 内容：",
        ]
        
        # 分行显示内容
        content = wisdom.get("content", "")
        for i in range(0, len(content), 50):
            lines.append(f"      {content[i:i+50]}")
        
        if wisdom.get("tags"):
            lines.append(f"   🏷️ 标签：{' / '.join(wisdom['tags'])}")
        
        return "\n".join(lines)
    
    def display_insight_encouragement(self, insight: Dict) -> str:
        """显示洞察鼓励"""
        content = insight.get("content", "")[:50]
        if len(insight.get("content", "")) > 50:
            content += "..."
        
        lines = [
            "✨ 有意思！",
            "",
            f"你刚才说的\"{content}\"",
            "让我想到了一些东西...",
            "",
            "🌿 你能把这个想法再明确地说一遍吗？"
        ]
        
        return "\n".join(lines)
    
    def display_insight_confirmed(self, wisdom: Dict) -> str:
        """显示洞察确认"""
        lines = [
            "✨ 你说得对！",
            "",
            "┌─────────────────────────────────┐",
            f"│ 💡 {wisdom.get('content', '')[:30]}",  # 标题（简化）
            "│                                 │",
            f"│ 来源：练习反馈                  │",
            "│                                 │",
            "│ 🌱 已记录到智慧库！              │",
            "└─────────────────────────────────┘",
            "",
            "🌿 试试把这个洞察用到其他地方？"
        ]
        
        return "\n".join(lines)
    
    # ========== 原有功能 ==========
    
    def display_progress(self, thought_type: str) -> str:
        """显示某个思维类型的进度"""
        if thought_type not in self.tracker.seeds:
            return ""
        
        count = self.tracker.seeds[thought_type]
        icon = self.THOUGHT_ICONS.get(thought_type, "")
        
        # 计算到下一级还需多少
        next_level = count + 1
        remaining = max(0, 5 - count)
        
        if count == 0:
            status = "还没开始"
            bar = "░░░░░"
        elif count < 3:
            status = "初学者"
            bar = "▓" * count + "░" * (5 - count)
        elif count < 5:
            status = "进阶中"
            bar = "▓" * count + "░" * (5 - count)
        else:
            status = "已圆满！"
            bar = "▓▓▓▓▓"
        
        return f"""
{icon} {thought_type}
   进度：{bar} ({count}/5) {status}
   {f"再练习{remaining}次可触发智慧涌现！" if remaining > 0 else "✨ 智慧涌现已触发！"}
"""
    
    def display_achievements(self) -> str:
        """显示成就里程碑"""
        if not self.tracker.milestones:
            return ""
        
        lines = ["🏆 成就里程碑："]
        for m in self.tracker.milestones[-5:]:  # 只显示最近5个
            date = datetime.fromisoformat(m["date"]).strftime("%m/%d")
            thought = m.get("thought_type", "")
            lines.append(f"   🎉 {date} {m['type']} - {thought}")
        
        return "\n".join(lines)
    
    def display_full_report(self, period_days: int = 30) -> str:
        """显示完整成长报告"""
        report = self.tracker.generate_report(period_days)
        
        lines = [
            "=" * 45,
            "🌿 葫芦娃成长报告",
            f"   生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "=" * 45,
            "",
            self.display_level().strip(),
            "",
            self.display_seeds(),
            "",
            self.display_wisdom_pool(limit=3),
            ""
        ]
        
        # 本期数据
        lines.extend([
            "📊 本期数据：",
            f"   ├─ 练习次数：{report['practice_count']}次",
            f"   ├─ 涌现次数：{report['emergence_count']}次",
            f"   ├─ 新增洞察：{report['insight_count']}条"
        ])
        
        if report.get("most_used_thought"):
            lines.append(f"   ├─ 最常用：{report['most_used_thought']}")
        
        if report.get("most_grown_thought"):
            lines.append(f"   └─ 进步最大：{report['most_grown_thought']}")
        
        # 成就
        achievements = self.display_achievements()
        if achievements:
            lines.extend(["", achievements])
        
        # 建议
        lines.extend([
            "",
            "💡 下一步建议：",
            self._generate_suggestion()
        ])
        
        return "\n".join(lines)
    
    def display_emergence_event(self, event: Dict) -> str:
        """显示智慧涌现事件"""
        old_level = event.get("old_level", 1)
        new_level = event.get("new_level", 1)
        thought_type = event.get("thought_type", "")
        
        lines = [
            "✨✨✨ 智慧涌现！",
            "",
            "🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉",
            "",
            f"你的「{thought_type}」种子集齐了5颗星！",
            "触发了一次觉醒事件！",
            "",
            f"等级提升：L{old_level} → L{new_level}",
            f"{self.LEVEL_BADGES.get(new_level, '✨')} {self.tracker.AWAKENING_LEVELS[new_level]['name']}",
            "",
            "🌿 你已经能运用多种思维框架了！",
            "去试试新的思维方式吧！",
            "",
            "🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉"
        ]
        
        return "\n".join(lines)
    
    def display_practice_feedback(self, practice_result: Dict) -> str:
        """显示练习反馈"""
        lines = [
            "🌿 " + practice_result.get("thought_type", "") + "练习完成！",
            "",
            f"问题1得分：{practice_result.get('q1_score', 'N/A')}",
            f"问题2得分：{practice_result.get('q2_score', 'N/A')}",
            f"问题3得分：{practice_result.get('q3_score', 'N/A')}",
            f"综合得分：{practice_result.get('total_score', 0)}/5",
            "",
            f"🌱 种子 +{practice_result.get('seed_added', 1)}"
        ]
        
        # 添加涌现提示
        if practice_result.get("insight"):
            lines.extend([
                "",
                "✨ " + practice_result["insight"]
            ])
        
        return "\n".join(lines)
    
    def _generate_suggestion(self) -> str:
        """生成成长建议"""
        seeds = self.tracker.seeds
        
        # 找出需要加强的
        zero_seeds = [t for t, c in seeds.items() if c == 0]
        low_seeds = [t for t, c in seeds.items() if 0 < c < 3]
        high_seeds = [t for t, c in seeds.items() if c >= 4]
        complete_seeds = [t for t, c in seeds.items() if c >= 5]
        
        suggestions = []
        
        if high_seeds:
            suggestions.append(f"✨ 你的{high_seeds[0]}已经很成熟了，可以挑战其他领域！")
        elif low_seeds:
            suggestions.append(f"🌿 建议继续练习{low_seeds[0]}，再努力一下就能触发智慧涌现了！")
        elif zero_seeds:
            suggestions.append(f"🌱 试试解锁{zero_seeds[0]}？不同场景需要不同思维方式。")
        
        # 添加智慧孵化建议
        if complete_seeds and self.tracker.insights_count < complete_seeds[0]:
            suggestions.append("💡 尝试在练习中产生自己的洞察，可能会有意外收获！")
        
        if not suggestions:
            suggestions.append("🌿 继续练习，保持好奇，智慧会自然涌现！")
        
        return suggestions[0] if suggestions else "🌿 继续加油！"
