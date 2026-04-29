# -*- coding: utf-8 -*-
"""
前五识：多模态感知层

在佛教唯识论中，前五识（眼识、耳识、鼻识、舌识、身识）负责基本的感官知觉。
在AI架构中，对应多模态信息感知与预处理：

- 眼识 → 视觉感知（图片/视频理解）
- 耳识 → 听觉感知（音频/语音处理）
- 舌识 → 味觉感知（本项目中映射为文本处理）
- 鼻识 → 嗅觉感知（本项目中映射为语义分析）
- 身识 → 触觉感知（本项目中映射为结构化数据处理）

核心功能：
1. 多模态输入的接收与解析
2. 感知信息的标准化处理
3. 上下文信息的提取与管理
4. 与种子库的信息对接
"""

import re
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class SenseType(Enum):
    """感知类型枚举"""
    TEXT = "text"              # 文本感知（舌识）
    VISUAL = "visual"          # 视觉感知（眼识）
    AUDIO = "audio"            # 听觉感知（耳识）
    SEMANTIC = "semantic"      # 语义感知（鼻识）
    STRUCTURED = "structured"  # 结构化感知（身识）


@dataclass
class SensoryInput:
    """
    感官输入
    
    标准化格式的感知输入
    """
    sense_type: SenseType
    raw_content: Any            # 原始内容
    processed_content: str      # 处理后的文本
    metadata: Dict[str, Any]    # 元数据
    timestamp: datetime = field(default_factory=datetime.now)
    
    # 提取的信息
    entities: List[str] = field(default_factory=list)      # 实体
    keywords: List[str] = field(default_factory=list)      # 关键词
    intent: Optional[str] = None                             # 意图
    sentiment: str = "neutral"                              # 情感


@dataclass
class PerceptionContext:
    """
    感知上下文
    
    维护当前会话的感知状态
    """
    session_id: str
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    current_topic: Optional[str] = None
    user_profile: Dict[str, Any] = field(default_factory=dict)
    environment_state: Dict[str, Any] = field(default_factory=dict)
    
    def add_interaction(self, role: str, content: str) -> None:
        """添加交互记录"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_recent_history(self, count: int = 5) -> List[Dict[str, str]]:
        """获取最近的交互历史"""
        return self.conversation_history[-count:]


class Senses:
    """
    前五识 - 多模态感知层
    
    统一处理各种类型的感知输入：
    1. 文本感知：对话、文档、指令
    2. 视觉感知：图片描述、视频关键帧
    3. 音频感知：语音转文本
    4. 语义感知：主题、意图识别
    5. 结构化感知：JSON、表格等
    
    Attributes:
        config: 感知配置
        context: 当前感知上下文
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化感知层
        
        Args:
            config: 感知配置
        """
        self.config = config or {}
        self.context: Optional[PerceptionContext] = None
        
        # 感知处理配置
        self.sentiment_keywords = {
            "positive": ["好", "棒", "赞", "优秀", "喜欢", "感谢", "满意", "helpfulness"],
            "negative": ["差", "烂", "糟", "不喜欢", "失望", "愤怒", "bad", "wrong"]
        }
        
        self.intent_patterns = {
            "question": [r"吗$", r"呢$", r"\?$", r"是什么", r"如何", r"怎么", r"为什么"],
            "request": [r"请", r"帮我", r"给我", r"想要", r"需要"],
            "statement": [r"我认为", r"我觉得", r"相信", r"知道"],
            "command": [r"做", r"去", r"执行", r"开始"]
        }
    
    def perceive(self, input_data: Any, sense_type: SenseType = SenseType.TEXT) -> SensoryInput:
        """
        主感知入口
        
        Args:
            input_data: 输入数据
            sense_type: 感知类型
        
        Returns:
            标准化处理后的感知输入
        """
        if sense_type == SenseType.TEXT:
            return self._perceive_text(input_data)
        elif sense_type == SenseType.VISUAL:
            return self._perceive_visual(input_data)
        elif sense_type == SenseType.AUDIO:
            return self._perceive_audio(input_data)
        elif sense_type == SenseType.SEMANTIC:
            return self._perceive_semantic(input_data)
        elif sense_type == SenseType.STRUCTURED:
            return self._perceive_structured(input_data)
        else:
            raise ValueError(f"未知的感知类型: {sense_type}")
    
    def _perceive_text(self, text: str) -> SensoryInput:
        """
        文本感知
        
        处理文本输入，提取：
        - 实体
        - 关键词
        - 意图
        - 情感
        
        Args:
            text: 文本内容
        
        Returns:
            感官输入对象
        """
        # 基础处理
        processed = self._preprocess_text(text)
        
        # 提取实体（简化版本，实际应使用NER）
        entities = self._extract_entities(processed)
        
        # 提取关键词
        keywords = self._extract_keywords(processed)
        
        # 识别意图
        intent = self._recognize_intent(processed)
        
        # 分析情感
        sentiment = self._analyze_sentiment(processed)
        
        return SensoryInput(
            sense_type=SenseType.TEXT,
            raw_content=text,
            processed_content=processed,
            metadata={
                "language": self._detect_language(text),
                "length": len(text),
                "has_question": "？" in text or "?" in text
            },
            entities=entities,
            keywords=keywords,
            intent=intent,
            sentiment=sentiment
        )
    
    def _perceive_visual(self, visual_data: Any) -> SensoryInput:
        """
        视觉感知
        
        处理图像输入
        
        Args:
            visual_data: 图像数据（可以是URL、路径或base64）
        
        Returns:
            感官输入对象
        """
        # 如果visual_data是图片URL或路径，需要使用视觉理解模型
        # 这里简化处理，假设visual_data是图片描述文本
        if isinstance(visual_data, str):
            description = visual_data
        else:
            description = "[图像内容]"
        
        return SensoryInput(
            sense_type=SenseType.VISUAL,
            raw_content=visual_data,
            processed_content=description,
            metadata={
                "type": "image",
                "description_length": len(description)
            },
            entities=self._extract_entities(description),
            keywords=self._extract_keywords(description),
            intent="describe" if not self._recognize_intent(description) else self._recognize_intent(description)
        )
    
    def _perceive_audio(self, audio_data: Any) -> SensoryInput:
        """
        听觉感知
        
        处理音频输入，转换为文本后处理
        
        Args:
            audio_data: 音频数据
        
        Returns:
            感官输入对象
        """
        # 简化：假设audio_data是语音转写文本
        if isinstance(audio_data, str):
            text = audio_data
        else:
            text = "[语音内容]"
        
        sensory = self._perceive_text(text)
        sensory.sense_type = SenseType.AUDIO
        sensory.metadata["type"] = "audio"
        return sensory
    
    def _perceive_semantic(self, semantic_data: Dict[str, Any]) -> SensoryInput:
        """
        语义感知
        
        处理语义分析任务
        
        Args:
            semantic_data: 语义数据
        
        Returns:
            感官输入对象
        """
        content = semantic_data.get("content", "")
        topic = semantic_data.get("topic", "")
        
        return SensoryInput(
            sense_type=SenseType.SEMANTIC,
            raw_content=semantic_data,
            processed_content=f"{topic}: {content}",
            metadata={
                "topic": topic,
                "confidence": semantic_data.get("confidence", 0.5)
            },
            entities=semantic_data.get("entities", []),
            keywords=semantic_data.get("keywords", []),
            intent="analyze"
        )
    
    def _perceive_structured(self, structured_data: Any) -> SensoryInput:
        """
        结构化感知
        
        处理JSON、表格等结构化数据
        
        Args:
            structured_data: 结构化数据
        
        Returns:
            感官输入对象
        """
        if isinstance(structured_data, dict):
            content = json.dumps(structured_data, ensure_ascii=False)
        else:
            content = str(structured_data)
        
        return SensoryInput(
            sense_type=SenseType.STRUCTURED,
            raw_content=structured_data,
            processed_content=content,
            metadata={
                "data_type": type(structured_data).__name__,
                "keys": list(structured_data.keys()) if isinstance(structured_data, dict) else []
            }
        )
    
    def _preprocess_text(self, text: str) -> str:
        """
        文本预处理
        
        Args:
            text: 原始文本
        
        Returns:
            处理后的文本
        """
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 去除特殊字符（保留中文、英文、数字、常用标点）
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s,.!?;:，。！？；：""''（）()【】\[\]]', '', text)
        return text.strip()
    
    def _extract_entities(self, text: str) -> List[str]:
        """
        提取实体（简化版本）
        
        实际应使用命名实体识别模型
        
        Args:
            text: 文本
        
        Returns:
            实体列表
        """
        # 简化：提取连续的中文词或英文词作为"实体"
        entities = []
        
        # 提取中文词
        chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
        entities.extend(chinese_words[:10])  # 最多10个
        
        # 提取英文词
        english_words = re.findall(r'[a-zA-Z]{3,}', text)
        entities.extend(english_words[:5])  # 最多5个
        
        return list(set(entities))[:15]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        提取关键词
        
        使用简单的词频统计
        
        Args:
            text: 文本
        
        Returns:
            关键词列表
        """
        # 停用词
        stopwords = {
            "的", "了", "是", "在", "我", "有", "和", "就", "不", "人",
            "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
            "你", "会", "着", "没有", "看", "好", "自己", "这", "那", "吗"
        }
        
        words = re.findall(r'[\u4e00-\u9fa5]+', text)
        word_freq = {}
        
        for word in words:
            if word not in stopwords and len(word) >= 2:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 按频率排序
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [w[0] for w in sorted_words[:10]]
    
    def _recognize_intent(self, text: str) -> str:
        """
        识别意图
        
        Args:
            text: 文本
        
        Returns:
            意图标签
        """
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return intent
        return "general"
    
    def _analyze_sentiment(self, text: str) -> str:
        """
        分析情感
        
        Args:
            text: 文本
        
        Returns:
            情感标签
        """
        text_lower = text.lower()
        
        pos_count = sum(1 for kw in self.sentiment_keywords["positive"] if kw in text_lower)
        neg_count = sum(1 for kw in self.sentiment_keywords["negative"] if kw in text_lower)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"
    
    def _detect_language(self, text: str) -> str:
        """
        检测语言
        
        Args:
            text: 文本
        
        Returns:
            语言代码
        """
        chinese_count = len(re.findall(r'[\u4e00-\u9fa5]', text))
        english_count = len(re.findall(r'[a-zA-Z]', text))
        
        if chinese_count > english_count:
            return "zh"
        elif english_count > 0:
            return "en"
        else:
            return "unknown"
    
    def create_context(self, session_id: str) -> PerceptionContext:
        """
        创建新的感知上下文
        
        Args:
            session_id: 会话ID
        
        Returns:
            感知上下文对象
        """
        self.context = PerceptionContext(session_id=session_id)
        return self.context
    
    def update_context(self, user_input: str, agent_response: str) -> None:
        """
        更新感知上下文
        
        Args:
            user_input: 用户输入
            agent_response: Agent响应
        """
        if self.context:
            self.context.add_interaction("user", user_input)
            self.context.add_interaction("assistant", agent_response)
    
    def get_context_summary(self) -> Dict[str, Any]:
        """
        获取上下文摘要
        
        Returns:
            上下文摘要
        """
        if not self.context:
            return {}
        
        return {
            "session_id": self.context.session_id,
            "current_topic": self.context.current_topic,
            "interaction_count": len(self.context.conversation_history),
            "recent_interactions": self.context.get_recent_history(3)
        }
    
    def extract_context_for_alaya(self) -> Dict[str, Any]:
        """
        提取供阿赖耶识使用的上下文信息
        
        Returns:
            上下文字典
        """
        if not self.context:
            return {"topic": "general"}
        
        # 从最近对话中推断话题
        recent = self.context.get_recent_history(5)
        all_text = " ".join(i["content"] for i in recent)
        
        keywords = self._extract_keywords(all_text)
        topic = self.context.current_topic or (keywords[0] if keywords else "general")
        
        return {
            "topic": topic,
            "keywords": keywords,
            "interaction_count": len(self.context.conversation_history),
            "user_profile": self.context.user_profile,
            "environment": self.context.environment_state
        }
