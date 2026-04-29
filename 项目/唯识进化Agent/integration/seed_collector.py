# -*- coding: utf-8 -*-
"""
唯识进化Agent - 种子收集器 (SeedCollector)
从对话中自动提取、管理种子
"""

import json
import re
import hashlib
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from enum import Enum
from collections import Counter


# ==================== 数据模型 ====================

class SeedType(Enum):
    """种子类型枚举"""
    KNOWLEDGE = "knowledge"      # 知识种子
    EXPERIENCE = "experience"    # 经验种子
    PATTERN = "pattern"          # 模式种子
    WISDOM = "wisdom"            # 智慧种子
    COMPASSION = "compassion"    # 慈悲种子


class QualityLevel(Enum):
    """质量等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXCELLENT = "excellent"


@dataclass
class Conversation:
    """对话数据结构"""
    user_id: str
    user_message: str
    agent_response: str
    session_id: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RawSeed:
    """原始种子"""
    content: str
    source: str  # "user" or "agent"
    conversation_id: str
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AssessedSeed:
    """评估后的种子"""
    seed_id: str
    content: str
    quality_score: float
    quality_dimensions: Dict[str, float]  # 各个维度的分数
    quality_level: QualityLevel


@dataclass
class ClassifiedSeed:
    """分类后的种子（最终存储格式）"""
    seed_id: str
    content: str
    seed_type: SeedType
    quality_score: float
    quality_level: QualityLevel
    weight: float  # 基于类型的权重
    purity: float  # 纯度
    embedding: List[float] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    conversation_id: str = ""
    user_id: str = ""
    tags: List[str] = field(default_factory=list)
    usage_count: int = 0
    last_used_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SeedBatch:
    """种子批次"""
    seeds: List[ClassifiedSeed]
    batch_id: str
    created_at: datetime = field(default_factory=datetime.now)
    total_weight: float = 0.0
    
    def __post_init__(self):
        self.total_weight = sum(s.weight * s.quality_score for s in self.seeds)


# ==================== 种子收集器核心类 ====================

class SeedCollector:
    """
    种子收集器
    从对话中提取有价值的内容作为种子
    """
    
    # 种子类型配置
    SEED_CONFIG = {
        SeedType.KNOWLEDGE: {
            'weight': 1.0,
            'keywords': ['知识', '概念', '定义', '原理', '事实', '信息'],
            'indicators': ['准确', '正确', '详细', '全面']
        },
        SeedType.EXPERIENCE: {
            'weight': 1.2,
            'keywords': ['经验', '经历', '案例', '实践', '应用'],
            'indicators': ['成功', '有效', '验证', '可行']
        },
        SeedType.PATTERN: {
            'weight': 1.5,
            'keywords': ['模式', '规律', '方法', '步骤', '流程'],
            'indicators': ['重复', '常见', '通常', '一般']
        },
        SeedType.WISDOM: {
            'weight': 2.0,
            'keywords': ['智慧', '洞察', '哲理', '思考', '领悟'],
            'indicators': ['深刻', '独到', '本质', '核心']
        },
        SeedType.COMPASSION: {
            'weight': 2.0,
            'keywords': ['理解', '关怀', '支持', '陪伴', '温暖'],
            'indicators': ['共情', '善意', '体贴', '用心']
        }
    }
    
    # 质量评估权重
    QUALITY_WEIGHTS = {
        'originality': 0.2,
        'depth': 0.3,
        'utility': 0.3,
        'uniqueness': 0.2
    }
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.history_hashes = set()  # 用于去重
        
    # ==================== 主流程方法 ====================
    
    def extract(self, conversation: Conversation) -> List[RawSeed]:
        """
        从对话中提取原始种子
        
        Args:
            conversation: 对话数据
            
        Returns:
            原始种子列表
        """
        seeds = []
        
        # 从用户消息提取
        user_seeds = self._extract_from_message(
            conversation.user_message, 
            "user",
            conversation.session_id
        )
        seeds.extend(user_seeds)
        
        # 从Agent回复提取
        agent_seeds = self._extract_from_message(
            conversation.agent_response,
            "agent",
            conversation.session_id
        )
        seeds.extend(agent_seeds)
        
        return seeds
    
    def assess(self, seed: RawSeed) -> AssessedSeed:
        """
        评估种子质量
        
        Args:
            seed: 原始种子
            
        Returns:
            评估后的种子
        """
        # 计算各个维度
        dimensions = {
            'originality': self._calculate_originality(seed),
            'depth': self._calculate_depth(seed),
            'utility': self._calculate_utility(seed),
            'uniqueness': self._calculate_uniqueness(seed)
        }
        
        # 加权计算总分
        total_score = sum(
            dimensions[k] * self.QUALITY_WEIGHTS[k]
            for k in dimensions
        )
        
        # 确定质量等级
        if total_score >= 0.85:
            level = QualityLevel.EXCELLENT
        elif total_score >= 0.7:
            level = QualityLevel.HIGH
        elif total_score >= 0.4:
            level = QualityLevel.MEDIUM
        else:
            level = QualityLevel.LOW
        
        return AssessedSeed(
            seed_id=self._generate_seed_id(seed.content),
            content=seed.content,
            quality_score=total_score,
            quality_dimensions=dimensions,
            quality_level=level
        )
    
    def classify(self, seed: AssessedSeed) -> ClassifiedSeed:
        """
        分类种子
        
        Args:
            seed: 评估后的种子
            
        Returns:
            分类后的种子
        """
        # 确定种子类型
        seed_type = self._classify_type(seed)
        
        # 获取类型配置
        type_config = self.SEED_CONFIG.get(seed_type, {'weight': 1.0})
        
        # 计算纯度
        purity = self._calculate_purity(seed)
        
        return ClassifiedSeed(
            seed_id=seed.seed_id,
            content=seed.content,
            seed_type=seed_type,
            quality_score=seed.quality_score,
            quality_level=seed.quality_level,
            weight=type_config['weight'],
            purity=purity
        )
    
    def process(self, conversation: Conversation) -> List[ClassifiedSeed]:
        """
        完整处理流程：提取 -> 评估 -> 分类
        
        Args:
            conversation: 对话数据
            
        Returns:
            分类后的种子列表
        """
        raw_seeds = self.extract(conversation)
        results = []
        
        for raw in raw_seeds:
            assessed = self.assess(raw)
            # 只保留中等质量以上的种子
            if assessed.quality_level in [QualityLevel.HIGH, QualityLevel.EXCELLENT]:
                classified = self.classify(assessed)
                results.append(classified)
        
        return results
    
    def aggregate(self, seeds: List[ClassifiedSeed], group_by: str = "type") -> SeedBatch:
        """
        聚合种子
        
        Args:
            seeds: 种子列表
            group_by: 分组方式 ("type", "user", "session")
            
        Returns:
            种子批次
        """
        batch_id = hashlib.md5(
            f"{len(seeds)}_{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        
        return SeedBatch(
            seeds=seeds,
            batch_id=batch_id
        )
    
    # ==================== 提取方法 ====================
    
    def _extract_from_message(self, message: str, source: str, session_id: str) -> List[RawSeed]:
        """从消息中提取种子"""
        seeds = []
        
        # 清理消息
        message = message.strip()
        if not message or len(message) < 10:
            return seeds
        
        # 分割成句子
        sentences = self._split_sentences(message)
        
        for sentence in sentences:
            # 跳过太短或太长的句子
            if len(sentence) < 20 or len(sentence) > 500:
                continue
            
            # 生成内容哈希
            content_hash = self._generate_seed_id(sentence)
            
            # 去重
            if content_hash in self.history_hashes:
                continue
            
            seeds.append(RawSeed(
                content=sentence,
                source=source,
                conversation_id=session_id,
                context={'extracted_at': datetime.now().isoformat()}
            ))
            
            self.history_hashes.add(content_hash)
        
        return seeds
    
    def _split_sentences(self, text: str) -> List[str]:
        """将文本分割成句子"""
        # 使用常见分隔符分割
        separators = r'[。！？；\n]+'
        sentences = re.split(separators, text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _generate_seed_id(self, content: str) -> str:
        """生成种子ID"""
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    # ==================== 评估方法 ====================
    
    def _calculate_originality(self, seed: RawSeed) -> float:
        """
        计算原创性
        评估内容是否重复/常见
        """
        # 检查是否包含常见模板词
        template_patterns = [
            r'根据.*?规定',
            r'按照.*?要求',
            r'一般来说',
            r'通常情况下'
        ]
        
        for pattern in template_patterns:
            if re.search(pattern, seed.content):
                return 0.6
        
        # 检查是否与历史内容重复
        content_hash = self._generate_seed_id(seed.content)
        if content_hash in self.history_hashes:
            return 0.3
        
        # 原创内容基础分
        return 0.7 + (0.3 * min(len(seed.content) / 200, 1.0))
    
    def _calculate_depth(self, seed: RawSeed) -> float:
        """
        计算深度
        评估内容的复杂度和洞察力
        """
        score = 0.5
        
        # 长度贡献
        length_factor = min(len(seed.content) / 300, 1.0)
        score += 0.2 * length_factor
        
        # 包含因果关系的加分
        if any(kw in seed.content for kw in ['因为', '所以', '因此', '导致']):
            score += 0.1
        
        # 包含对比分析的加分
        if any(kw in seed.content for kw in ['然而', '但是', '相比', '然而']):
            score += 0.1
        
        # 包含举例说明的加分
        if any(kw in seed.content for kw in ['例如', '比如', '比如', '以']):
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_utility(self, seed: RawSeed) -> float:
        """
        计算实用性
        评估内容的可复用性
        """
        score = 0.5
        
        # 包含可操作步骤的加分
        if re.search(r'第一.{0,10}第二|步骤|流程|方法', seed.content):
            score += 0.2
        
        # 包含具体建议的加分
        if any(kw in seed.content for kw in ['建议', '推荐', '可以', '应该']):
            score += 0.15
        
        # 包含数字/量化的加分
        if re.search(r'\d+', seed.content):
            score += 0.1
        
        # 包含专业术语的加分（表示有具体领域知识）
        if len(re.findall(r'[\u4e00-\u9fff]{2,}', seed.content)) > 3:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_uniqueness(self, seed: RawSeed) -> float:
        """
        计算独特性
        评估内容的新颖程度
        """
        # 基础分
        score = 0.6
        
        # 检查是否包含独特的表达
        unique_indicators = [
            '创新', '独特', '首创', '突破', '原创',
            '深刻', '独到', '新颖', '别具一格'
        ]
        
        if any(indicator in seed.content for indicator in unique_indicators):
            score += 0.2
        
        # 检查语义独特性（通过哈希）
        content_hash = self._generate_seed_id(seed.content)
        # 如果在近期历史中没有见过，加分
        if content_hash not in self.history_hashes:
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_purity(self, seed: AssessedSeed) -> float:
        """
        计算种子纯度
        纯度 = 质量分数 * 类型匹配度
        """
        # 基础纯度等于质量分
        base_purity = seed.quality_score
        
        # 类型关键词匹配加成
        type_keywords = self._get_type_keywords(seed.content)
        if type_keywords > 0:
            purity = base_purity * (1 + 0.1 * type_keywords)
        else:
            purity = base_purity * 0.9
        
        return min(purity, 1.0)
    
    def _get_type_keywords(self, content: str) -> int:
        """计算内容匹配的类型关键词数量"""
        count = 0
        for seed_type, config in self.SEED_CONFIG.items():
            for keyword in config.get('keywords', []):
                if keyword in content:
                    count += 1
        return count
    
    # ==================== 分类方法 ====================
    
    def _classify_type(self, seed: AssessedSeed) -> SeedType:
        """
        确定种子类型
        
        分类策略:
        1. 智慧种子优先（高质量深度内容）
        2. 慈悲种子次之（情感支持内容）
        3. 知识种子（事实性信息）
        4. 经验种子（实践案例）
        5. 模式种子（方法论）
        """
        content = seed.content
        
        # 深度内容 -> 智慧种子
        if seed.quality_dimensions.get('depth', 0) > 0.7:
            if any(kw in content for kw in ['智慧', '洞察', '哲理', '本质', '核心']):
                return SeedType.WISDOM
        
        # 情感支持内容 -> 慈悲种子
        if any(kw in content for kw in ['理解', '关怀', '支持', '陪伴', '共情']):
            if seed.quality_dimensions.get('utility', 0) > 0.5:
                return SeedType.COMPASSION
        
        # 步骤/方法论内容 -> 模式种子
        if re.search(r'第一.{0,10}第二|步骤|流程|方法|技巧', content):
            return SeedType.PATTERN
        
        # 案例/实践内容 -> 经验种子
        if any(kw in content for kw in ['经验', '案例', '实践', '经历', '故事']):
            return SeedType.EXPERIENCE
        
        # 事实性信息 -> 知识种子
        if any(kw in content for kw in ['知识', '概念', '定义', '原理', '信息']):
            return SeedType.KNOWLEDGE
        
        # 默认：根据质量分配
        if seed.quality_dimensions.get('depth', 0) > 0.6:
            return SeedType.WISDOM
        elif seed.quality_dimensions.get('utility', 0) > 0.6:
            return SeedType.EXPERIENCE
        else:
            return SeedType.KNOWLEDGE


# ==================== 辅助工具 ====================

def load_conversation_from_json(json_str: str) -> Conversation:
    """从JSON加载对话数据"""
    data = json.loads(json_str)
    return Conversation(
        user_id=data['user_id'],
        user_message=data['user_message'],
        agent_response=data['agent_response'],
        session_id=data['session_id'],
        timestamp=datetime.fromisoformat(data['timestamp']),
        metadata=data.get('metadata', {})
    )


def seed_to_dict(seed: ClassifiedSeed) -> Dict:
    """将种子转换为字典"""
    return {
        'seed_id': seed.seed_id,
        'content': seed.content,
        'seed_type': seed.seed_type.value,
        'quality_score': seed.quality_score,
        'quality_level': seed.quality_level.value,
        'weight': seed.weight,
        'purity': seed.purity,
        'created_at': seed.created_at.isoformat(),
        'conversation_id': seed.conversation_id,
        'user_id': seed.user_id,
        'tags': seed.tags,
        'usage_count': seed.usage_count,
        'metadata': seed.metadata
    }


def dict_to_seed(data: Dict) -> ClassifiedSeed:
    """从字典恢复种子"""
    return ClassifiedSeed(
        seed_id=data['seed_id'],
        content=data['content'],
        seed_type=SeedType(data['seed_type']),
        quality_score=data['quality_score'],
        quality_level=QualityLevel(data['quality_level']),
        weight=data['weight'],
        purity=data['purity'],
        created_at=datetime.fromisoformat(data['created_at']),
        conversation_id=data.get('conversation_id', ''),
        user_id=data.get('user_id', ''),
        tags=data.get('tags', []),
        usage_count=data.get('usage_count', 0),
        metadata=data.get('metadata', {})
    )


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 示例对话
    conversation = Conversation(
        user_id="user_001",
        user_message="我最近在思考人生的意义是什么？",
        agent_response="这是一个深刻的哲学问题。从佛学的角度看，\
            人生的意义在于觉醒——认识到自心的本真面目。通过修行，\
            我们可以从无明中解脱，获得智慧与慈悲。具体来说，\
            这需要三个步骤：第一，觉察当下的心念；第二，\
            理解诸法无我的道理；第三，在生活中实践般若智慧。",
        session_id="session_001",
        timestamp=datetime.now()
    )
    
    # 创建收集器
    collector = SeedCollector()
    
    # 处理对话
    seeds = collector.process(conversation)
    
    # 打印结果
    print(f"从对话中提取了 {len(seeds)} 个种子：\n")
    for seed in seeds:
        print(f"类型: {seed.seed_type.value}")
        print(f"内容: {seed.content[:80]}...")
        print(f"质量: {seed.quality_score:.2f} ({seed.quality_level.value})")
        print(f"权重: {seed.weight}")
        print("-" * 50)
