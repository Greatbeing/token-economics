# -*- coding: utf-8 -*-
"""
圣哲思维匹配器 - SageMatcher

根据用户问题，智能匹配最适合的圣哲思维视角。
"""

from typing import Dict, List, Optional
import re


class SageMatcher:
    """圣哲思维匹配器"""
    
    # 圣哲思维模型库
    THOUGHT_MODELS = {
        "仁学思维": {
            "sage": "孔子",
            "core": "推己及人",
            "keywords": ["人际", "朋友", "关系", "冲突", "沟通", "室友", "同事", "家人", 
                        "生气", "矛盾", "原谅", "道德", "仁义", "君子"],
            "methods": ["己所不欲勿施于人", "己欲立而立人", "忠恕之道", "换位思考"],
            "scenario": ["人际冲突", "沟通问题", "关系处理", "道德困境"],
            "contra_keywords": []
        },
        "逍遥思维": {
            "sage": "庄子",
            "core": "顺其自然",
            "keywords": ["焦虑", "压力", "担心", "害怕", "恐惧", "得失", "名利", 
                        "控制", "执念", "烦恼", "纠结", "患得患失"],
            "methods": ["逍遥游", "齐物论", "无用之用", "天人合一"],
            "scenario": ["焦虑压力", "得失心重", "控制欲强", "患得患失"],
            "contra_keywords": []
        },
        "无为思维": {
            "sage": "老子",
            "core": "无为而治",
            "keywords": ["选择", "纠结", "决定", "策略", "权衡", "取舍", "迷茫",
                        "方向", "计划", "有为", "强求", "刻意"],
            "methods": ["无为而无不为", "柔弱胜刚强", "道法自然", "知其不可奈何而安之若命"],
            "scenario": ["选择困难", "决策纠结", "方向迷茫", "策略制定"],
            "contra_keywords": []
        },
        "四谛思维": {
            "sage": "佛陀",
            "core": "苦集灭道",
            "keywords": ["痛苦", "意义", "迷茫", "空虚", "无聊", "人生", "活着",
                        "欲望", "执念", "烦恼", "生死", "解脱", "智慧"],
            "methods": ["四圣谛", "八正道", "止观", "缘起性空"],
            "scenario": ["意义迷茫", "存在困惑", "欲望困扰", "生死恐惧"],
            "contra_keywords": []
        },
        "心性思维": {
            "sage": "孟子",
            "core": "求诸于心",
            "keywords": ["自信", "自卑", "心虚", "良心", "善恶", "本性", "勇气",
                        "怯懦", "志向", "格局", "气节", "浩然之气"],
            "methods": ["性善论", "养浩然气", "求放心", "不动心"],
            "scenario": ["自信问题", "怯懦自卑", "良心困惑", "志向迷茫"],
            "contra_keywords": []
        },
        "心学思维": {
            "sage": "王阳明",
            "core": "知行合一",
            "keywords": ["行动", "拖延", "执行力", "知道", "做到", "实践", "事上磨练",
                        "良知", "意念", "致良知", "知行"],
            "methods": ["知行合一", "事上磨练", "致良知", "心即理"],
            "scenario": ["行动困难", "拖延症", "知行不一", "执行力弱"],
            "contra_keywords": []
        },
        "产婆术": {
            "sage": "苏格拉底",
            "core": "追问反思",
            "keywords": ["困惑", "问题", "定义", "思考", "辩论", "追问", "审视",
                        "什么是", "为什么", "真的吗", "你怎么看", "我想知道"],
            "methods": ["产婆术", "助产术", "认识你自己", "未经审视的人生不值得过"],
            "scenario": ["困惑咨询", "概念不清", "观点探讨", "自我认知"],
            "contra_keywords": []
        },
        "实践智慧": {
            "sage": "亚里士多德",
            "core": "中道选择",
            "keywords": ["判断", "决策", "选择", "道德", "伦理", "两难", "应该",
                        "适度", "中庸", "平衡", "美德", "德性"],
            "methods": ["中道", "实践智慧", "德性伦理", "目的论"],
            "scenario": ["决策判断", "道德两难", "价值选择", "伦理困惑"],
            "contra_keywords": []
        },
        "权衡思维": {
            "sage": "鬼谷子",
            "core": "捭阖飞钳",
            "keywords": ["博弈", "谈判", "谋略", "人心", "说服", "权谋", "纵横",
                        "策略", "对手", "利益", "强弱", "进退"],
            "methods": ["捭阖", "反应", "内揵", "飞钳", "忤合"],
            "scenario": ["博弈情境", "谈判沟通", "人际博弈", "策略制定"],
            "contra_keywords": []
        }
    }
    
    # 意图关键词
    INTENT_KEYWORDS = {
        "困惑": ["怎么办", "不知道", "纠结", "迷茫", "焦虑", "烦恼", "难受"],
        "学习": ["学", "了解", "想知道", "什么是", "道理", "思想"],
        "练习": ["练习", "实践", "做", "试试", "训练"],
        "成长": ["成长", "进步", "等级", "种子", "报告"]
    }
    
    def __init__(self):
        self.models = self.THOUGHT_MODELS
        self.intent_keywords = self.INTENT_KEYWORDS
    
    def analyze_intent(self, user_input: str) -> str:
        """识别用户意图"""
        user_input_lower = user_input.lower()
        
        scores = {}
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for kw in keywords if kw in user_input_lower)
            scores[intent] = score
        
        if max(scores.values()) == 0:
            return "闲聊"
        
        return max(scores, key=scores.get)
    
    def match_thought(self, user_input: str, context: Optional[Dict] = None) -> Dict:
        """
        根据用户输入匹配最适合的圣哲思维
        
        Args:
            user_input: 用户输入文本
            context: 上下文信息（可选）
            
        Returns:
            {
                "model": "仁学思维",
                "sage": "孔子",
                "confidence": 0.85,
                "reason": "匹配理由",
                "suggestion": "使用建议"
            }
        """
        user_input_lower = user_input.lower()
        
        # 计算各思维模型的匹配分数
        scores = {}
        for model_name, model in self.models.items():
            score = 0
            matched_keywords = []
            
            # 关键词匹配
            for keyword in model["keywords"]:
                if keyword in user_input_lower:
                    score += 2
                    matched_keywords.append(keyword)
            
            # 圣哲名字匹配（加分）
            if model["sage"] in user_input:
                score += 5
            
            # 方法名匹配（加分）
            for method in model["methods"]:
                if method[:2] in user_input:  # 取前两字
                    score += 3
            
            scores[model_name] = {
                "score": score,
                "matched_keywords": matched_keywords
            }
        
        # 获取最高分
        best_model = max(scores, key=lambda x: scores[x]["score"])
        best_score = scores[best_model]["score"]
        
        # 计算置信度（归一化）
        if best_score == 0:
            confidence = 0.3
            best_model = "产婆术"  # 默认使用产婆术追问
        else:
            confidence = min(0.5 + best_score * 0.1, 0.95)
        
        model_info = self.models[best_model]
        
        return {
            "model": best_model,
            "sage": model_info["sage"],
            "core": model_info["core"],
            "confidence": confidence,
            "matched_keywords": scores[best_model]["matched_keywords"],
            "reason": self._generate_reason(best_model, scores[best_model]),
            "suggestion": self._generate_suggestion(best_model),
            "methods": model_info["methods"],
            "scenario": model_info["scenario"]
        }
    
    def _generate_reason(self, model: str, score_info: Dict) -> str:
        """生成匹配理由"""
        if score_info["score"] == 0:
            return "通过追问帮你理清问题"
        
        keywords = score_info["matched_keywords"]
        if keywords:
            return f"匹配到关键词：{', '.join(keywords[:3])}"
        return "根据问题特征匹配"
    
    def _generate_suggestion(self, model: str) -> str:
        """生成使用建议"""
        suggestions = {
            "仁学思维": "遇到人际冲突时，先理解对方处境，再换位思考，最后寻求双赢",
            "逍遥思维": "焦虑时，试着接受不确定性，专注自己能控制的部分",
            "无为思维": "纠结选择时，顺其自然，看清什么是真正重要的",
            "四谛思维": "迷茫时，认清痛苦的本质，找到解脱之道",
            "心性思维": "不自信时，向内求，问问自己的良知和本心",
            "心学思维": "想行动但拖延时，在事上磨练，边做边想",
            "产婆术": "困惑时，通过追问澄清概念，逐步逼近真相",
            "实践智慧": "两难决策时，找到两个极端之间的平衡点",
            "权衡思维": "博弈情境时，观察对方心理，灵活运用捭阖"
        }
        return suggestions.get(model, "来，咱们一起想想")
    
    def get_model_intro(self, model: str) -> str:
        """获取思维模型简介"""
        if model not in self.models:
            return ""
        
        info = self.models[model]
        return f"""
【{model}】— {info['sage']}

核心：{info['core']}

方法：
{chr(10).join(f'• {m}' for m in info['methods'])}

适用：{', '.join(info['scenario'])}
"""
    
    def suggest_multiple(self, user_input: str, top_n: int = 3) -> List[Dict]:
        """获取多个可能的匹配结果"""
        user_input_lower = user_input.lower()
        
        results = []
        for model_name, model in self.models.items():
            score = 0
            for keyword in model["keywords"]:
                if keyword in user_input_lower:
                    score += 2
            
            if model["sage"] in user_input:
                score += 5
            
            results.append({
                "model": model_name,
                "sage": model["sage"],
                "score": score
            })
        
        # 排序并返回前N个
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_n]


# 便捷函数
def match_sage(user_input: str, context: Optional[Dict] = None) -> Dict:
    """快速匹配函数"""
    matcher = SageMatcher()
    return matcher.match_thought(user_input, context)


def get_intent(user_input: str) -> str:
    """快速识别意图"""
    matcher = SageMatcher()
    return matcher.analyze_intent(user_input)


if __name__ == "__main__":
    # 测试
    matcher = SageMatcher()
    
    test_inputs = [
        "室友每天熬夜影响我休息，我很生气",
        "最近很焦虑，不知道要不要换工作",
        "我想学孔子的思维",
        "很迷茫，不知道人生有什么意义"
    ]
    
    for inp in test_inputs:
        print(f"\n{'='*50}")
        print(f"输入: {inp}")
        print(f"意图: {matcher.analyze_intent(inp)}")
        result = matcher.match_thought(inp)
        print(f"匹配: {result['model']} ({result['sage']})")
        print(f"置信度: {result['confidence']:.2f}")
        print(f"理由: {result['reason']}")
