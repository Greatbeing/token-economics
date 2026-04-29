# -*- coding: utf-8 -*-
"""
练习题生成器 - PracticeGenerator

根据圣哲思维类型和用户场景，生成思维练习题。
"""

from typing import Dict, List, Optional
import random


class PracticeGenerator:
    """练习题生成器"""
    
    # 练习模板库
    PRACTICE_TEMPLATES = {
        "仁学思维": [
            {
                "id": "ren_001",
                "title": "室友的噪音",
                "scenario": "室友每天熬夜打游戏，声音很大，影响你休息。你很生气。",
                "questions": [
                    {
                        "id": "q1",
                        "text": "他为什么这样？尝试理解他的处境",
                        "hint": "他在面对什么压力？或者他可能没意识到影响？",
                        "type": "understanding",
                        "scoring_keywords": ["可能", "也许", "理解", "体谅"]
                    },
                    {
                        "id": "q2", 
                        "text": "如果是你熬夜，你会希望室友怎么说？",
                        "hint": "想想你最希望听到什么样的表达",
                        "type": "empathy",
                        "scoring_keywords": ["希望", "愿意", "期待"]
                    },
                    {
                        "id": "q3",
                        "text": "你会怎么和他沟通，既表达不满又不伤感情？",
                        "hint": "选个合适的时机，用'我觉得'开头",
                        "type": "action",
                        "scoring_keywords": ["沟通", "表达", "合适"]
                    }
                ],
                "difficulty": 2
            },
            {
                "id": "ren_002",
                "title": "朋友的请求",
                "scenario": "朋友找你帮忙，但你手头事情很多，而且这不是第一次了。",
                "questions": [
                    {
                        "id": "q1",
                        "text": "他为什么总是找你帮忙？",
                        "hint": "他在信任你？还是觉得你好说话？",
                        "type": "understanding",
                        "scoring_keywords": ["信任", "依赖", "觉得"]
                    },
                    {
                        "id": "q2",
                        "text": "如果你拒绝，他会有什么感受？你能接受吗？",
                        "hint": "考虑对方反应，也考虑自己的边界",
                        "type": "empathy",
                        "scoring_keywords": ["感受", "接受", "理解"]
                    },
                    {
                        "id": "q3",
                        "text": "你会怎么回应，既不伤感情又守住边界？",
                        "hint": "可以说不，但不是简单拒绝",
                        "type": "action",
                        "scoring_keywords": ["但是", "同时", "建议"]
                    }
                ],
                "difficulty": 3
            },
            {
                "id": "ren_003",
                "title": "同事的功劳",
                "scenario": "你和同事合作完成了一个项目，但他在领导面前把功劳全归自己。",
                "questions": [
                    {
                        "id": "q1",
                        "text": "他为什么要这么做？背后可能有什么原因？",
                        "hint": "他在担心什么？或者性格使然？",
                        "type": "understanding",
                        "scoring_keywords": ["可能", "担心", "性格", "无意识"]
                    },
                    {
                        "id": "q2",
                        "text": "如果你当众揭穿，结果会怎样？你希望怎样？",
                        "hint": "想想短期和长期的不同结果",
                        "type": "empathy",
                        "scoring_keywords": ["揭穿", "短期", "长期", "关系"]
                    },
                    {
                        "id": "q3",
                        "text": "你会怎么处理这件事？",
                        "hint": "可以私下沟通，也可以选择放下",
                        "type": "action",
                        "scoring_keywords": ["私下", "沟通", "领导", "放下"]
                    }
                ],
                "difficulty": 3
            }
        ],
        "逍遥思维": [
            {
                "id": "xiaoyao_001",
                "title": "工作的焦虑",
                "scenario": "你很焦虑，不知道这次项目会不会出问题，担心老板的评价。",
                "questions": [
                    {
                        "id": "q1",
                        "text": "你最担心的结果是什么？试着说出来",
                        "hint": "最坏能坏到哪里去？真的会发生吗？",
                        "type": "acceptance",
                        "scoring_keywords": ["担心", "最坏"]
                    },
                    {
                        "id": "q2",
                        "text": "如果那个结果真的发生了，你会怎么应对？",
                        "hint": "应对方案比担心本身更有用",
                        "type": "resilience",
                        "scoring_keywords": ["应对", "办法", "接受"]
                    },
                    {
                        "id": "q3",
                        "text": "现在你能控制的是什么？什么是你控制不了的？",
                        "hint": "区分可控和不可控，专注能做的",
                        "type": "focus",
                        "scoring_keywords": ["控制", "专注", "能做"]
                    }
                ],
                "difficulty": 2
            },
            {
                "id": "xiaoyao_002",
                "title": "别人的评价",
                "scenario": "你精心准备了一份方案，但同事说了一些负面评价，你很在意。",
                "questions": [
                    {
                        "id": "q1",
                        "text": "那些评价是事实，还是只是他的观点？",
                        "hint": "区分客观事实和主观看法",
                        "type": "acceptance",
                        "scoring_keywords": ["事实", "观点", "主观", "客观"]
                    },
                    {
                        "id": "q2",
                        "text": "如果抛开他的评价，你的方案真的不好吗？",
                        "hint": "你内心的标准是什么？",
                        "type": "resilience",
                        "scoring_keywords": ["其实", "真正", "标准"]
                    },
                    {
                        "id": "q3",
                        "text": "你能从评价中提取有用的信息，忽略无用的部分吗？",
                        "hint": "去其糟粕，取其精华",
                        "type": "focus",
                        "scoring_keywords": ["有用", "采纳", "忽略"]
                    }
                ],
                "difficulty": 2
            }
        ],
        "无为思维": [
            {
                "id": "wuwei_001",
                "title": "职业的选择",
                "scenario": "有两个工作机会摆在你面前：一个钱多但压力大，一个稳定但发展有限。你纠结了很久。",
                "questions": [
                    {
                        "id": "q1",
                        "text": "如果你不选择，结果会怎样？试着放下'必须选一个'的执念",
                        "hint": "有时候不选择也是一种选择",
                        "type": "letting_go",
                        "scoring_keywords": ["不选", "也可以", "顺其自然"]
                    },
                    {
                        "id": "q2",
                        "text": "三年后回头看，你会觉得哪个选择更重要？",
                        "hint": "长期视角往往更清晰",
                        "type": "perspective",
                        "scoring_keywords": ["三年", "长期", "重要"]
                    },
                    {
                        "id": "q3",
                        "text": "哪个选择让你更想做自己？",
                        "hint": "违背内心的选择往往后悔",
                        "type": "essence",
                        "scoring_keywords": ["自己", "内心", "想做"]
                    }
                ],
                "difficulty": 3
            },
            {
                "id": "wuwei_002",
                "title": "计划的纠结",
                "scenario": "你本来计划周末学习，但朋友约你出去玩。你想去又觉得该学习。",
                "questions": [
                    {
                        "id": "q1",
                        "text": "为什么你觉得'应该'学习？是真的需要，还是习惯了逼自己？",
                        "hint": "区分真正的需要和习惯性的自我强迫",
                        "type": "letting_go",
                        "scoring_keywords": ["应该", "真的", "习惯"]
                    },
                    {
                        "id": "q2",
                        "text": "如果顺其自然，你内心真正想做什么？",
                        "hint": "放下评判，听听内心的声音",
                        "type": "essence",
                        "scoring_keywords": ["其实", "内心", "想"]
                    },
                    {
                        "id": "q3",
                        "text": "能不能找到一个'不去想该做什么'的答案？",
                        "hint": "有时候不思考的选择最真实",
                        "type": "spontaneity",
                        "scoring_keywords": ["不管", "就是", "想"]
                    }
                ],
                "difficulty": 2
            }
        ],
        "四谛思维": [
            {
                "id": "sidi_001",
                "title": "人生的意义",
                "scenario": "最近觉得做什么都没意思，工作是为了赚钱，赚钱是为了生活，生活又是为了什么？",
                "questions": [
                    {
                        "id": "q1",
                        "text": "这种'没意思'的感觉，具体是什么样的？",
                        "hint": "给苦一个具体的形状，它就没那么可怕了",
                        "type": "suffering",
                        "scoring_keywords": ["感觉", "具体", "空虚", "无聊"]
                    },
                    {
                        "id": "q2",
                        "text": "这种感受是从什么时候开始的？是什么'集'起了它？",
                        "hint": "追根溯源，找到问题的源头",
                        "type": "origin",
                        "scoring_keywords": ["开始", "因为", "源头"]
                    },
                    {
                        "id": "q3",
                        "text": "如果这种苦消失了，你的生活会是什么样的？",
                        "hint": "找到'灭'的状态，就是找到方向",
                        "type": "cessation",
                        "scoring_keywords": ["如果", "会", "希望"]
                    }
                ],
                "difficulty": 3
            }
        ],
        "心性思维": [
            {
                "id": "xinxing_001",
                "title": "不自信的我",
                "scenario": "开会时你有个好想法，但犹豫了一下没说出来，被别人说了类似的。你很后悔。",
                "questions": [
                    {
                        "id": "q1",
                        "text": "你当时在'心虚'什么？内心在怕什么？",
                        "hint": "向内看，找到那个胆怯的声音",
                        "type": "inner",
                        "scoring_keywords": ["怕", "担心", "害怕", "心虚"]
                    },
                    {
                        "id": "q2",
                        "text": "那个怕是真的吗？还是你的念头在夸大它？",
                        "hint": "区分真实和想象的恐惧",
                        "type": "clarity",
                        "scoring_keywords": ["真的", "想象", "念头"]
                    },
                    {
                        "id": "q3",
                        "text": "下次开会，你会怎么做？想象一下",
                        "hint": "在想象中先'行'一次",
                        "type": "action",
                        "scoring_keywords": ["下次", "会", "想说"]
                    }
                ],
                "difficulty": 2
            }
        ],
        "心学思维": [
            {
                "id": "xinxue_001",
                "title": "拖延的我",
                "scenario": "你知道该学习了，但就是不想动。心里想着'再玩会儿'，一天就过去了。",
                "questions": [
                    {
                        "id": "q1",
                        "text": "当你拖延时，脑子里在想什么？",
                        "hint": "捕捉那个导致拖延的念头",
                        "type": "mind",
                        "scoring_keywords": ["想着", "觉得", "念头"]
                    },
                    {
                        "id": "q2",
                        "text": "那个念头是真的吗？还是借口？",
                        "hint": "良知知道答案，直面它",
                        "type": "conscience",
                        "scoring_keywords": ["真的", "借口", "知道"]
                    },
                    {
                        "id": "q3",
                        "text": "别想那么多，现在立刻能做什么？只做第一步",
                        "hint": "知行合一，行比知更重要",
                        "type": "action",
                        "scoring_keywords": ["现在", "先", "第一步"]
                    }
                ],
                "difficulty": 2
            }
        ],
        "产婆术": [
            {
                "id": "socratic_001",
                "title": "什么是勇敢",
                "scenario": "你觉得某个人很勇敢，你很羡慕他。但你说不清什么是勇敢。",
                "questions": [
                    {
                        "id": "q1",
                        "text": "你觉得那个人做了什么让你觉得勇敢？具体行为",
                        "hint": "先描述具体现象，再抽象概念",
                        "type": "definition",
                        "scoring_keywords": ["做了", "行为", "具体"]
                    },
                    {
                        "id": "q2",
                        "text": "一个为了正义冲上前的人，和一个为了义气打架的人，都叫勇敢吗？",
                        "hint": "通过比较，澄清概念边界",
                        "type": "comparison",
                        "scoring_keywords": ["都", "同样", "区别"]
                    },
                    {
                        "id": "q3",
                        "text": "那你觉得，勇敢的本质是什么？",
                        "hint": "经过前面的追问，你有什么新的理解？",
                        "type": "essence",
                        "scoring_keywords": ["本质", "其实", "是"]
                    }
                ],
                "difficulty": 3
            }
        ],
        "实践智慧": [
            {
                "id": "phronesis_001",
                "title": "两难的选择",
                "scenario": "朋友找你借钱，但你手头也紧，而且上次借的还没还。你该怎么办？",
                "questions": [
                    {
                        "id": "q1",
                        "text": "如果借，适度是多少？不能影响自己的生活",
                        "hint": "找平衡点，不是全有或全无",
                        "type": "balance",
                        "scoring_keywords": ["适度", "部分", "多少"]
                    },
                    {
                        "id": "q2",
                        "text": "如果直接拒绝，会伤害友情吗？有没有更好的方式？",
                        "hint": "考虑行为的后果和替代方案",
                        "type": "consequence",
                        "scoring_keywords": ["伤害", "方式", "替代"]
                    },
                    {
                        "id": "q3",
                        "text": "综合考虑，你会怎么处理？",
                        "hint": "中道不是折中，是最适合的选择",
                        "type": "decision",
                        "scoring_keywords": ["综合", "最终", "决定"]
                    }
                ],
                "difficulty": 3
            }
        ],
        "权衡思维": [
            {
                "id": "guigu_001",
                "title": "说服的艺术",
                "scenario": "你想让室友收拾房间，但他总是拖着。你怎么说他会更愿意动？",
                "questions": [
                    {
                        "id": "q1",
                        "text": "他现在是什么状态？可能为什么不收拾？",
                        "hint": "知己知彼，先了解对方",
                        "type": "reading",
                        "scoring_keywords": ["状态", "为什么", "可能"]
                    },
                    {
                        "id": "q2",
                        "text": "直接要求和给他选择，哪个效果更好？为什么？",
                        "hint": "人不喜欢被命令，喜欢自主",
                        "type": "strategy",
                        "scoring_keywords": ["选择", "自主", "命令"]
                    },
                    {
                        "id": "q3",
                        "text": "设计一段话，让他主动想收拾",
                        "hint": "用'捭阖'之道，先让他说yes",
                        "type": "action",
                        "scoring_keywords": ["设计", "让他", "主动"]
                    }
                ],
                "difficulty": 3
            }
        ]
    }
    
    def __init__(self):
        self.templates = self.PRACTICE_TEMPLATES
    
    def generate_practice(self, thought_type: str, user_context: Optional[Dict] = None) -> Optional[Dict]:
        """
        生成练习
        
        Args:
            thought_type: 思维类型
            user_context: 用户上下文（可选）
            
        Returns:
            练习题字典，包含场景和问题
        """
        templates = self.templates.get(thought_type, [])
        
        if not templates:
            return None
        
        # 选择模板：优先匹配用户场景，否则随机
        selected = None
        if user_context and "scenario" in user_context:
            scenario = user_context["scenario"]
            for t in templates:
                if any(kw in scenario for kw in t.get("scenario", "").split()):
                    selected = t
                    break
        
        if not selected:
            selected = random.choice(templates)
        
        return {
            "title": selected["title"],
            "scenario": selected["scenario"],
            "questions": selected["questions"],
            "thought_type": thought_type,
            "difficulty": selected.get("difficulty", 2)
        }
    
    def evaluate_answer(self, thought_type: str, question_id: str, answer: str) -> Dict:
        """
        评估用户答案
        
        Args:
            thought_type: 思维类型
            question_id: 问题ID
            answer: 用户答案
            
        Returns:
            评分结果，包含分数和反馈
        """
        templates = self.templates.get(thought_type, [])
        
        # 找到问题
        question = None
        scoring_keywords = []
        for t in templates:
            for q in t.get("questions", []):
                if q["id"] == question_id:
                    question = q
                    scoring_keywords = q.get("scoring_keywords", [])
                    break
        
        if not question:
            return {"score": 3, "feedback": "答案已记录"}
        
        # 简单评分：关键词匹配
        answer_lower = answer.lower()
        matched = sum(1 for kw in scoring_keywords if kw in answer_lower)
        
        # 计算分数
        if matched >= 3:
            score = 5
            feedback = "🌟 非常好！"
        elif matched >= 2:
            score = 4
            feedback = "✓ 不错！"
        elif matched >= 1:
            score = 3
            feedback = "💪 有这个意识了，继续加油！"
        else:
            # 基础分，看回答是否有实质内容
            if len(answer) > 10:
                score = 3
                feedback = "💭 好的，你在思考了。"
            else:
                score = 2
                feedback = "🤔 再想想？提示：" + question.get("hint", "")
        
        return {
            "score": score,
            "feedback": feedback,
            "matched_keywords": matched,
            "hint": question.get("hint", "")
        }
    
    def evaluate_practice(self, thought_type: str, answers: Dict[str, str]) -> Dict:
        """
        评估完整练习
        
        Args:
            thought_type: 思维类型
            answers: 问题ID到答案的映射
            
        Returns:
            综合评分结果
        """
        results = []
        total_score = 0
        
        for q_id, answer in answers.items():
            result = self.evaluate_answer(thought_type, q_id, answer)
            results.append({
                "question_id": q_id,
                "score": result["score"],
                "feedback": result["feedback"]
            })
            total_score += result["score"]
        
        avg_score = total_score / len(results) if results else 0
        
        # 计算种子奖励
        seed_points = 0
        if avg_score >= 4:
            seed_points = 2
        elif avg_score >= 3:
            seed_points = 1
        
        return {
            "question_results": results,
            "avg_score": round(avg_score, 1),
            "total_score": round(avg_score, 1),  # 满分5分
            "seed_points": seed_points,
            "encouragement": self._get_encouragement(avg_score)
        }
    
    def _get_encouragement(self, avg_score: float) -> str:
        """获取鼓励语"""
        if avg_score >= 4.5:
            return "🌿 太棒了！你对这个思维已经很有感觉了！"
        elif avg_score >= 4:
            return "🌿 很好！继续保持这个势头！"
        elif avg_score >= 3:
            return "🌿 不错，有进步！继续加油！"
        elif avg_score >= 2:
            return "🌿 别急，慢慢来，多练习几次就熟练了。"
        else:
            return "🌿 没关系，思维成长需要时间，我们再来一次？"


# 便捷函数
def generate_practice(thought_type: str, user_context: Optional[Dict] = None) -> Optional[Dict]:
    """快速生成练习"""
    generator = PracticeGenerator()
    return generator.generate_practice(thought_type, user_context)


def evaluate_practice(thought_type: str, answers: Dict[str, str]) -> Dict:
    """快速评估练习"""
    generator = PracticeGenerator()
    return generator.evaluate_practice(thought_type, answers)


if __name__ == "__main__":
    # 测试
    generator = PracticeGenerator()
    
    # 测试生成
    practice = generator.generate_practice("仁学思维")
    print("练习题：")
    print(f"标题: {practice['title']}")
    print(f"场景: {practice['scenario']}")
    for q in practice["questions"]:
        print(f"\n问题: {q['text']}")
        print(f"提示: {q['hint']}")
    
    # 测试评估
    print("\n" + "="*50)
    print("评估测试：")
    answers = {
        "q1": "他可能最近压力大，用游戏放松",
        "q2": "我希望他直接说，别阴阳怪气",
        "q3": "我会在他清醒的时候说，我觉得有点影响我休息"
    }
    result = generator.evaluate_practice("仁学思维", answers)
    print(f"平均分: {result['avg_score']}")
    print(f"种子奖励: {result['seed_points']}")
    print(f"鼓励: {result['encouragement']}")
