# -*- coding: utf-8 -*-
"""
熏习系统 - Vasana

熏习（vāsanā）是唯识论的核心机制，描述现行与种子之间的相互转化：
1. 现行熏种子：当前经验影响种子库，形成新的记忆痕迹
2. 种子生现行：种子库中的种子被激活，影响当前认知与行为

在AI架构中，实现双向的信息流动：
- 向下：交互经验 → 提取模式 → 编码存储
- 向上：检索相关种子 → 激活 → 影响决策
"""

import re
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Callable
from dataclasses import dataclass

from .alaya_store import AlayaStore, Seed, SeedType, SeedStatus


@dataclass
class ExperienceRecord:
    """
    经验记录 - 熏习的输入数据
    
    Attributes:
        timestamp: 时间戳
        user_input: 用户输入
        agent_response: Agent响应
        context: 上下文信息
        outcome: 结果评价
        emotional_tone: 情感色调
    """
    timestamp: datetime
    user_input: str
    agent_response: str
    context: Dict[str, Any]
    outcome: float = 0.5  # 0-1, 0差1好
    emotional_tone: str = "neutral"  # positive/negative/neutral


class PatternExtractor:
    """
    模式提取器
    
    从交互经验中提取可存储的模式：
    - 对话模式（问答结构）
    - 行为模式（决策倾向）
    - 情感模式（情绪反应）
    """
    
    def __init__(self):
        # 模式权重配置
        self.pattern_weights = {
            "question_pattern": 0.3,
            "response_style": 0.3,
            "emotional_tone": 0.2,
            "topic_transition": 0.2
        }
    
    def extract(self, experience: ExperienceRecord) -> Dict[str, Any]:
        """
        从经验中提取模式
        
        Args:
            experience: 经验记录
        
        Returns:
            提取的模式字典
        """
        patterns = {}
        
        # 1. 提取问答模式
        patterns["question_pattern"] = self._extract_question_pattern(experience.user_input)
        
        # 2. 提取响应风格
        patterns["response_style"] = self._extract_response_style(experience.agent_response)
        
        # 3. 提取情感模式
        patterns["emotional_tone"] = experience.emotional_tone
        
        # 4. 提取话题转换
        patterns["topic_transition"] = self._extract_topic_context(experience.context)
        
        # 5. 计算整体模式强度
        patterns["intensity"] = self._calculate_intensity(patterns, experience.outcome)
        
        # 6. 生成模式摘要
        patterns["summary"] = self._generate_summary(patterns)
        
        return patterns
    
    def _extract_question_pattern(self, text: str) -> str:
        """提取问题模式"""
        if "为什么" in text or "为何" in text:
            return "causal_query"
        elif "如何" in text or "怎么" in text:
            return "method_query"
        elif "什么" in text:
            return "definition_query"
        elif "是否" in text or "能不能" in text:
            return "binary_query"
        elif text.endswith("？") or text.endswith("?"):
            return "general_query"
        return "statement"
    
    def _extract_response_style(self, text: str) -> str:
        """提取响应风格"""
        if len(text) < 50:
            return "concise"
        elif len(text) > 500:
            return "detailed"
        else:
            return "moderate"
    
    def _extract_topic_context(self, context: Dict[str, Any]) -> str:
        """提取话题上下文"""
        return context.get("topic", "general")
    
    def _calculate_intensity(self, patterns: Dict[str, Any], outcome: float) -> float:
        """计算模式强度"""
        # 正面结果加强模式，负面结果减弱
        # 基于模式存在性计算基础分数
        base_intensity = 0.3  # 基础分数
        
        # 根据各模式类型加分
        if patterns.get("question_pattern"):
            base_intensity += 0.2
        if patterns.get("response_style"):
            base_intensity += 0.2
        if patterns.get("emotional_tone"):
            base_intensity += 0.15
        if patterns.get("topic_transition"):
            base_intensity += 0.15
        
        # 根据结果调整
        outcome_factor = 0.5 + (outcome - 0.5) * 0.5
        return min(1.0, base_intensity * outcome_factor)
    
    def _generate_summary(self, patterns: Dict[str, Any]) -> str:
        """生成模式摘要"""
        parts = [
            patterns.get("question_pattern", "unknown"),
            patterns.get("response_style", "moderate"),
            patterns.get("emotional_tone", "neutral")
        ]
        return " | ".join(parts)


class Vasana:
    """
    熏习系统
    
    实现现行与种子的双向转化：
    - 熏习过程（record_interaction）：经验 → 种子
    - 激活过程（activate_seeds）：种子 → 影响
    
    Attributes:
        store: 种子存储
        extractor: 模式提取器
        embed_func: 向量嵌入函数
    """
    
    # 【优化1】种子质量门控配置
    PURITY_THRESHOLD = 0.4           # 新种子入库纯度阈值（原0.3→0.4）
    CONTAMINATED_SEED_TAG = "染污"   # 低纯度种子标记
    AUTO_PURIFY_INTERVAL = 50        # 自动净化检查间隔（交互次数）
    
    def __init__(
        self,
        store: AlayaStore,
        embed_func: Optional[Callable[[str], List[float]]] = None,
        purity_threshold: float = 0.3
    ):
        """
        初始化熏习系统
        
        Args:
            store: 阿赖耶识种子库
            embed_func: 向量嵌入函数（接受文本返回向量列表）
            purity_threshold: 种子入库纯度阈值
        """
        self.store = store
        self.extractor = PatternExtractor()
        self.purity_threshold = purity_threshold
        
        # 默认嵌入函数（使用简单的词频向量）
        self.embed_func = embed_func or self._simple_embed
        
        # 质量追踪
        self.total_seeds_created = 0
        self.rejected_seeds_count = 0
        self.total_activations = 0  # 种子激活计数
    
    def _simple_embed(self, text: str, dim: int = 384) -> List[float]:
        """
        简单的文本嵌入函数
        
        实际使用时建议替换为OpenAI/Cohere等高质量嵌入
        
        Args:
            text: 文本
            dim: 向量维度
        
        Returns:
            向量列表
        """
        # 简单的基于词汇的嵌入
        words = re.findall(r'\w+', text.lower())
        vector = [0.0] * dim
        
        for i, word in enumerate(words[:dim]):
            # 使用词的hash分布
            word_hash = int(hashlib.md5(word.encode()).hexdigest(), 16)
            vector[i % dim] = (word_hash % 1000) / 1000.0
        
        # 归一化
        magnitude = sum(v * v for v in vector) ** 0.5
        if magnitude > 0:
            vector = [v / magnitude for v in vector]
        
        return vector
    
    def record_interaction(
        self,
        user_input: str,
        agent_response: str,
        context: Optional[Dict[str, Any]] = None,
        outcome: float = 0.5,
        emotional_tone: str = "neutral",
        embed_func: Optional[Callable[[str], List[float]]] = None
    ) -> List[str]:
        """
        记录交互经验并熏习为种子
        
        这是"现行熏种子"的过程：
        1. 创建经验记录
        2. 提取模式
        3. 创建种子
        4. 存入种子库
        
        Args:
            user_input: 用户输入
            agent_response: Agent响应
            context: 上下文信息
            outcome: 结果评价 (0-1)
            emotional_tone: 情感色调
            embed_func: 自定义嵌入函数
        
        Returns:
            创建的种子ID列表
        """
        context = context or {}
        embed_func = embed_func or self.embed_func
        
        # 创建经验记录
        experience = ExperienceRecord(
            timestamp=datetime.now(),
            user_input=user_input,
            agent_response=agent_response,
            context=context,
            outcome=outcome,
            emotional_tone=emotional_tone
        )
        
        # 提取模式
        patterns = self.extractor.extract(experience)
        
        # 生成种子ID列表
        seed_ids = []
        
        # 【优化1-2】先估算纯度并进行质量检查
        estimated_purity = self._estimate_purity(outcome, emotional_tone)
        
        # 1. 创建经验种子（入库前进行质量检查）
        experience_content = self._serialize_experience(experience)
        experience_embedding = embed_func(experience_content)
        
        # 【核心优化】经验种子质量检查
        exp_quality = self._check_seed_quality(estimated_purity, SeedType.EXPERIENCE)
        self.total_seeds_created += 1
        
        if exp_quality["accepted"]:
            experience_seed = Seed.create(
                content=experience_content,
                seed_type=SeedType.EXPERIENCE,
                embedding=experience_embedding,
                weight=patterns["intensity"] * outcome,
                purity=estimated_purity,
                source="interaction",
                experience_context=context.get("topic", "general"),
                tags=[patterns["question_pattern"], patterns["response_style"]] + 
                     ([exp_quality["tag"]] if exp_quality["tagged"] else [])
            )
            self.store.add(experience_seed)
            seed_ids.append(experience_seed.seed_id)
        else:
            # 拒绝入库
            self.rejected_seeds_count += 1
            self.store.add(Seed.create(
                content=f"[已拒绝] {experience_content[:100]}",
                seed_type=SeedType.EXPERIENCE,
                embedding=experience_embedding,
                weight=0,
                purity=estimated_purity,
                source="rejected",
                tags=["rejected", exp_quality["tag"]]
            ))
        
        # 2. 创建模式种子（如果模式强度足够）
        if patterns["intensity"] > 0.3:
            pattern_content = f"模式: {patterns['summary']}"
            pattern_embedding = embed_func(pattern_content)
            
            # 【优化】模式种子也进行质量检查
            pattern_purity = estimated_purity * 0.9  # 模式种子略低于经验种子
            pattern_quality = self._check_seed_quality(pattern_purity, SeedType.PATTERN)
            self.total_seeds_created += 1
            
            if pattern_quality["accepted"]:
                pattern_seed = Seed.create(
                    content=pattern_content,
                    seed_type=SeedType.PATTERN,
                    embedding=pattern_embedding,
                    weight=patterns["intensity"] * 0.8,
                    purity=pattern_purity,
                    source="interaction",
                    experience_context=f"问题类型={patterns['question_pattern']}",
                    tags=[patterns["question_pattern"]] + ([pattern_quality["tag"]] if pattern_quality["tagged"] else [])
                )
                self.store.add(pattern_seed)
                seed_ids.append(pattern_seed.seed_id)
        
        # 3. 根据情感色调创建情感种子
        if emotional_tone != "neutral" and outcome < 0.3:
            emotion_content = f"负面反应: {agent_response[:200]}..."
            emotion_embedding = embed_func(emotion_content)
            
            emotion_seed = Seed.create(
                content=emotion_content,
                seed_type=SeedType.TRAUMA,
                embedding=emotion_embedding,
                weight=0.3,
                purity=0.2,  # 负面种子初始纯度低
                source="interaction",
                tags=["negative", emotional_tone]
            )
            self.store.add(emotion_seed)
            seed_ids.append(emotion_seed.seed_id)
        
        return seed_ids
    
    def record_knowledge(
        self,
        content: str,
        knowledge_type: str = "general",
        importance: float = 0.5,
        embed_func: Optional[Callable[[str], List[float]]] = None
    ) -> str:
        """
        记录知识为种子
        
        Args:
            content: 知识内容
            knowledge_type: 知识类型
            importance: 重要性 (0-1)
            embed_func: 嵌入函数
        
        Returns:
            种子ID
        """
        embed_func = embed_func or self.embed_func
        
        seed = Seed.create(
            content=content,
            seed_type=SeedType.KNOWLEDGE,
            embedding=embed_func(content),
            weight=importance,
            purity=0.7,  # 知识种子默认较高纯度
            source="knowledge_implant"
        )
        self.store.add(seed)
        return seed.seed_id
    
    def record_reflection(
        self,
        reflection_content: str,
        wisdom_level: float = 0.5,
        embed_func: Optional[Callable[[str], List[float]]] = None
    ) -> str:
        """
        记录反思产生的智慧种子
        
        Args:
            reflection_content: 反思内容
            wisdom_level: 智慧程度 (0-1)
            embed_func: 嵌入函数
        
        Returns:
            种子ID
        """
        embed_func = embed_func or self.embed_func
        
        seed = Seed.create(
            content=reflection_content,
            seed_type=SeedType.WISDOM,
            embedding=embed_func(reflection_content),
            weight=wisdom_level,
            purity=0.8,  # 智慧种子高纯度
            source="reflection"
        )
        self.store.add(seed)
        return seed.seed_id
    
    def activate_seeds(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        top_k: int = 5,
        activation_threshold: float = 0.3,
        embed_func: Optional[Callable[[str], List[float]]] = None
    ) -> List[Tuple[Seed, float]]:
        """
        激活相关种子（种子生现行）
        
        【优化版】添加关键词匹配机制，解决嵌入函数无法计算语义相似度的问题
        
        1. 先尝试向量相似度搜索
        2. 如果激活不足，使用关键词匹配补充
        3. 根据权重和纯度计算影响力
        4. 返回激活的种子
        
        Args:
            query: 查询文本
            context: 上下文信息
            top_k: 返回数量
            activation_threshold: 激活阈值
            embed_func: 嵌入函数
        
        Returns:
            (种子, 影响力分数) 列表
        """
        context = context or {}
        embed_func = embed_func or self.embed_func
        
        # 【第一步】向量相似度搜索
        query_embedding = embed_func(query)
        seeds = self.store.search(
            query_embedding=query_embedding,
            top_k=top_k * 2,
            min_weight=0.1,
            exclude_status=[SeedStatus.PURIFYING, SeedStatus.DELETED]
        )
        
        # 计算影响力
        activated = []
        activated_ids = set()
        
        for seed, similarity in seeds:
            # 影响力 = 相似度 * 权重 * 纯度
            influence = similarity * seed.weight * seed.purity
            
            # 根据上下文调整
            if context.get("topic") and context["topic"] == seed.experience_context:
                influence *= 1.2
            
            if influence >= activation_threshold:
                seed.activate()
                self.store.update(seed)
                activated.append((seed, influence))
                activated_ids.add(seed.seed_id)
        
        # 【第二步】关键词匹配补充（如果向量激活不足）
        if len(activated) < top_k:
            keyword_activated = self._activate_by_keywords(
                query=query,
                exclude_ids=activated_ids,
                top_k=top_k - len(activated),
                activation_threshold=activation_threshold,
                context=context
            )
            activated.extend(keyword_activated)
        
        # 按影响力排序
        activated.sort(key=lambda x: x[1], reverse=True)
        return activated[:top_k]
    
    def _activate_by_keywords(
        self,
        query: str,
        exclude_ids: set,
        top_k: int,
        activation_threshold: float,
        context: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Seed, float]]:
        """
        【新增】基于关键词匹配激活种子
        
        Args:
            query: 查询文本
            exclude_ids: 已激活的种子ID集合
            top_k: 返回数量
            activation_threshold: 激活阈值
            context: 上下文信息
        
        Returns:
            (种子, 影响力分数) 列表
        """
        context = context or {}
        query_lower = query.lower()
        
        # 定义关键词权重映射（根据种子内容提取）
        keyword_weights = {
            # 唯识相关
            "唯识": 0.9, "阿赖耶": 0.95, "种子": 0.85, "末那": 0.85, "意识": 0.8,
            "熏习": 0.85, "因缘": 0.85, "缘起": 0.85, "业力": 0.85,
            # 觉醒相关
            "觉醒": 0.9, "修行": 0.85, "菩萨": 0.9, "智慧": 0.85, "慈悲": 0.9,
            "佛": 0.9, "觉悟": 0.9, "涅槃": 0.85, "解脱": 0.85,
            # AI/进化相关
            "AI": 0.85, "Agent": 0.85, "进化": 0.85, "成长": 0.8, "学习": 0.75,
            "智能": 0.8, "涌现": 0.9, "意识": 0.85,
            # 儿童教育相关
            "儿童": 0.85, "哲学": 0.85, "播客": 0.8, "教育": 0.8, "思考": 0.75,
            "孩子": 0.8, "小星": 0.85, "小宇": 0.85,
            # 工作相关
            "文档": 0.75, "任务": 0.7, "计划": 0.7, "迭代": 0.75, "优化": 0.7,
            "质量": 0.7, "深度": 0.75, "反思": 0.8,
            # 核心价值观
            "利他": 0.9, "服务": 0.8, "用户": 0.75, "核心": 0.7, "价值": 0.75
        }
        
        # 遍历所有种子进行关键词匹配
        candidates = []
        
        for seed_id, seed in self.store._seeds.items():
            # 跳过已激活和排除状态的种子
            if seed_id in exclude_ids:
                continue
            if seed.status in [SeedStatus.PURIFYING, SeedStatus.DELETED]:
                continue
            
            # 计算关键词匹配分数
            match_score = 0.0
            matched_keywords = []
            
            for keyword, weight in keyword_weights.items():
                if keyword.lower() in query_lower:
                    # 检查种子内容是否包含该关键词
                    if keyword in seed.content or keyword.lower() in seed.content.lower():
                        match_score += weight
                        matched_keywords.append(keyword)
            
            # 也检查种子内容中的关键词是否在query中
            seed_keywords = self._extract_keywords_from_seed(seed.content)
            for kw in seed_keywords:
                if kw.lower() in query_lower:
                    match_score += 0.5  # 较低的权重，避免过度激活
                    matched_keywords.append(kw)
            
            # 计算最终影响力
            if match_score > 0:
                # 归一化匹配分数（0-1范围）
                normalized_score = min(1.0, match_score / 3.0)  # 假设3个关键词满匹配
                
                # 影响力 = 匹配分数 * 权重 * 纯度
                influence = normalized_score * seed.weight * seed.purity
                
                # 上下文增强
                if context.get("topic") and context["topic"] == seed.experience_context:
                    influence *= 1.2
                
                if influence >= activation_threshold:
                    candidates.append((seed, influence, matched_keywords))
        
        # 按影响力排序，取top_k
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # 激活并返回
        result = []
        for seed, influence, matched_kw in candidates[:top_k]:
            seed.activate()
            self.store.update(seed)
            result.append((seed, influence))
            self.total_activations += 1  # 更新激活计数
        
        return result
    
    def _extract_keywords_from_seed(self, content: str) -> List[str]:
        """
        【新增】从种子内容中提取关键词
        
        Args:
            content: 种子内容
        
        Returns:
            关键词列表
        """
        # 定义关键词提取规则
        important_terms = [
            "唯识", "阿赖耶识", "末那识", "种子", "熏习", "因缘", "缘起",
            "觉醒", "修行", "菩萨", "智慧", "慈悲", "佛", "觉悟",
            "AI", "Agent", "进化", "涌现", "意识",
            "儿童哲学", "播客", "教育", "思考",
            "利他", "服务", "反思", "迭代", "优化"
        ]
        
        keywords = []
        content_lower = content.lower()
        
        for term in important_terms:
            if term.lower() in content_lower:
                keywords.append(term)
        
        return keywords
    
    def get_activation_context(
        self,
        activated_seeds: List[Tuple[Seed, float]]
    ) -> Dict[str, Any]:
        """
        从激活的种子生成决策上下文
        
        Args:
            activated_seeds: 激活的种子列表
        
        Returns:
            包含决策提示的上下文
        """
        if not activated_seeds:
            return {}
        
        # 收集相关信息
        patterns = []
        wisdoms = []
        experiences = []
        
        for seed, influence in activated_seeds:
            if seed.seed_type == SeedType.PATTERN:
                patterns.append(seed.content)
            elif seed.seed_type == SeedType.WISDOM:
                wisdoms.append(seed.content)
            elif seed.seed_type == SeedType.EXPERIENCE:
                experiences.append(seed.content)
        
        return {
            "activated_patterns": patterns,
            "activated_wisdom": wisdoms,
            "relevant_experiences": experiences[:3],  # 最多3个
            "total_influence": sum(i for _, i in activated_seeds)
        }
    
    def _serialize_experience(self, experience: ExperienceRecord) -> str:
        """序列化经验为文本"""
        return (
            f"[交互记录]\n"
            f"用户: {experience.user_input}\n"
            f"回应: {experience.agent_response}\n"
            f"话题: {experience.context.get('topic', 'general')}\n"
            f"结果: {experience.outcome:.2f}"
        )
    
    def _estimate_purity(self, outcome: float, emotional_tone: str) -> float:
        """
        估计种子纯度【优化版】
        
        正面结果产生高纯度种子，负面结果产生低纯度种子
        调整参数使中性结果产生中等偏上纯度
        """
        # 【优化】基于outcome的计算，基准提高
        # outcome=0.6 → base_purity=0.7
        # outcome=0.8 → base_purity=0.8
        # outcome=0.4 → base_purity=0.55
        base_purity = 0.3 + outcome * 0.5  # 0.3-0.8范围
        
        if emotional_tone == "negative":
            base_purity *= 0.6  # 负面情感降低纯度
        elif emotional_tone == "positive":
            base_purity = min(1.0, base_purity * 1.15)  # 正面情感提升
        
        return min(1.0, max(0.0, base_purity))
    
    def _check_seed_quality(self, purity: float, seed_type: SeedType) -> Dict[str, Any]:
        """
        【新增】检查种子质量
        
        种子入库前的质量检查，决定是否允许入库或标记
        
        Args:
            purity: 种子纯度
            seed_type: 种子类型
        
        Returns:
            质量检查结果字典
        """
        # TRAUMA类型特殊处理 - 允许低纯度但需标记
        if seed_type == SeedType.TRAUMA:
            return {
                "accepted": True,
                "tagged": True,
                "tag": self.CONTAMINATED_SEED_TAG,
                "participates_awakening": False,  # 创伤种子不参与觉醒评分
                "reason": "创伤种子已标记为染污"
            }
        
        # 【核心优化】纯度低于阈值直接拒绝入库
        if purity < self.purity_threshold:
            return {
                "accepted": False,
                "tagged": True,
                "tag": self.CONTAMINATED_SEED_TAG,
                "participates_awakening": False,
                "reason": f"纯度 {purity:.2f} 低于阈值 {self.purity_threshold}"
            }
        
        # 边缘纯度 - 允许入库但标记
        if purity < 0.5:
            return {
                "accepted": True,
                "tagged": True,
                "tag": self.CONTAMINATED_SEED_TAG,
                "participates_awakening": True,  # 参与但影响力降低
                "reason": "低纯度种子已标记"
            }
        
        # 高纯度种子
        return {
            "accepted": True,
            "tagged": False,
            "participates_awakening": True,
            "reason": "高质量种子"
        }
    
    def get_quality_stats(self) -> Dict[str, Any]:
        """
        【新增】获取种子质量统计
        
        Returns:
            质量统计字典
        """
        seeds = list(self.store._seeds.values())
        total = len(seeds)
        if total == 0:
            return {"total": 0, "high_quality_ratio": 0, "wisdom_ratio": 0}
        
        high_quality = len([s for s in seeds if s.purity >= 0.5 and s.purity < self.CONTAMINATED_SEED_TAG])
        contaminated = len([s for s in seeds if self.CONTAMINATED_SEED_TAG in s.tags])
        wisdom = len([s for s in seeds if s.seed_type == SeedType.WISDOM and s.purity >= 0.6])
        
        # 智慧种子比例（只计算高质量种子）
        effective_seeds = total - contaminated
        wisdom_ratio = wisdom / effective_seeds if effective_seeds > 0 else 0
        
        return {
            "total": total,
            "high_quality": high_quality,
            "contaminated": contaminated,
            "wisdom": wisdom,
            "high_quality_ratio": high_quality / total if total > 0 else 0,
            "wisdom_ratio": wisdom_ratio,
            "rejected_count": self.rejected_seeds_count,
            "acceptance_rate": (self.total_seeds_created - self.rejected_seeds_count) / max(1, self.total_seeds_created)
        }
    
    def record_batch_interactions(self, interactions: List[Dict[str, Any]]) -> int:
        """
        批量熏习交互历史
        
        Args:
            interactions: 交互历史列表
        
        Returns:
            创建的种子数量
        """
        count = 0
        for interaction in interactions:
            seed_ids = self.record_interaction(
                user_input=interaction.get("user_input", ""),
                agent_response=interaction.get("agent_response", ""),
                context=interaction.get("context", {}),
                outcome=interaction.get("outcome", 0.5),
                emotional_tone=interaction.get("emotional_tone", "neutral")
            )
            count += len(seed_ids)
        return count
