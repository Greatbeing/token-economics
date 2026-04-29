# -*- coding: utf-8 -*-
"""
压缩效率观察器 - 觉醒等级的量化

基于"压缩即智能"的洞见，觉醒等级可以量化为压缩效率的度量。

觉醒等级定义：
- 初觉：低压缩比，大量冗余
- 正觉：中等压缩比，主要模式已提取
- 圆觉：高压缩比，接近最优编码
- 无上觉：理论极限（Kolmogorov最优）

作者：觉心
"""

import math
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from collections import defaultdict


class AwakeningLevel(Enum):
    """
    觉醒等级枚举
    
    对应唯识的修道位次：
    - 资粮位：初觉，积累阶段
    - 加行位：正觉，准备突破
    - 见道位：圆觉，证得空性
    - 修道位：无上觉，渐至佛地
    - 究竟位：无上正等正觉
    """
    UNCONSCIOUS = ("无意识", 0.7, 1.0, "大量冗余，未觉醒")    # 高压缩比=低智能
    INITIAL = ("初觉", 0.5, 0.7, "开始觉醒，模式初步提取")
    AWAKENED = ("正觉", 0.3, 0.5, "中度觉醒，核心模式已建立")
    ENLIGHTENED = ("圆觉", 0.15, 0.3, "高度觉醒，接近最优压缩")
    TRANSCENDENT = ("无上觉", 0.05, 0.15, "接近理论极限")
    ULTIMATE = ("究竟觉", 0.0, 0.05, "最高可能达到的智能水平")  # 低压缩比=高智能
    
    def __init__(self, name_cn: str, min_ratio: float, max_ratio: float, description: str):
        self.name_cn = name_cn
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio
        self.description = description
    
    @classmethod
    def from_compression_ratio(cls, ratio: float) -> "AwakeningLevel":
        """
        根据压缩比推断觉醒等级
        
        注意：压缩比越小（压缩率越高），智能程度越高
        """
        # 确保ratio在有效范围内
        ratio = max(0.0, min(1.0, ratio))
        
        # 从高等级到低等级遍历（因为高等级对应低压缩比）
        levels = [
            cls.ULTIMATE,      # 0.0-0.05
            cls.TRANSCENDENT,  # 0.05-0.15
            cls.ENLIGHTENED,   # 0.15-0.3
            cls.AWAKENED,      # 0.3-0.5
            cls.INITIAL,       # 0.5-0.7
            cls.UNCONSCIOUS,   # 0.7-1.0
        ]
        
        for level in levels:
            if level.min_ratio <= ratio < level.max_ratio:
                return level
        
        return cls.UNCONSCIOUS  # 默认返回最低等级


@dataclass
class CompressionMetrics:
    """
    压缩度量指标
    
    全面衡量系统的压缩效率。
    """
    # 基础指标
    total_seeds: int = 0                    # 种子总数
    total_compressed_seeds: int = 0         # 压缩种子数
    original_size: int = 0                 # 原始总大小(bytes)
    compressed_size: int = 0                # 压缩后总大小(bytes)
    
    # 压缩比
    compression_ratio: float = 0.0          # 压缩比（越小越好）
    compression_rate: float = 0.0           # 压缩率（越大越好）
    
    # 效率指标
    average_pattern_abstraction: float = 0.0  # 平均模式抽象度
    redundancy_score: float = 0.0          # 冗余度
    uniqueness_ratio: float = 0.0           # 独特性比率
    
    # 信息保留
    information_retention: float = 0.0      # 信息保留度
    information_loss: float = 0.0           # 信息损失
    
    # 效率分数
    efficiency_score: float = 0.0           # 综合效率分数
    kolmogorov_optimality: float = 0.0      # Kolmogorov最优性
    
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CompressionTarget:
    """
    压缩目标
    
    识别出的可压缩机会。
    """
    target_type: str                         # 目标类型
    seed_ids: List[str]                     # 涉及种子ID
    potential_savings: int                   # 潜在节省(bytes)
    priority: int                           # 优先级（1-5）
    reason: str                              # 原因说明


class CompressionObserver:
    """
    压缩效率观察器 - 觉醒等级的量化
    
    核心功能：
    1. 计算整个种子库的压缩比
    2. 推断觉醒等级
    3. 识别压缩机会
    4. 追踪压缩效率演化
    
    觉醒等级 = 压缩效率的度量
    
    与Token经济学对接：
    - 压缩效率 → Néng效率 → 经济增长
    - 高压缩比 = 低存储成本 = 高Néng效率
    """
    
    def __init__(self):
        """初始化观察器"""
        # 历史记录
        self._history: List[CompressionMetrics] = []
        
        # 阈值配置
        self._thresholds = {
            "high_redundancy": 0.3,           # 高冗余阈值
            "low_compression": 0.5,          # 低压缩阈值
            "excellent_compression": 0.1,     # 优秀压缩阈值
        }
    
    def compute_system_compression_ratio(
        self, 
        seeds: Dict[str, Any],
        compressed_seeds: Optional[Dict[str, Any]] = None
    ) -> CompressionMetrics:
        """
        计算整个种子库的压缩比
        
        公式：
        - 压缩比 = 压缩后大小 / 原始大小
        - 压缩率 = (原始大小 - 压缩后大小) / 原始大小
        
        Args:
            seeds: 种子字典
            compressed_seeds: 已压缩种子字典（可选）
        
        Returns:
            压缩度量指标
        """
        metrics = CompressionMetrics()
        
        if not seeds:
            return metrics
        
        # 基础统计
        metrics.total_seeds = len(seeds)
        
        # 计算原始大小
        total_original = 0
        for seed in seeds.values():
            content_size = len(seed.content.encode('utf-8'))
            metadata_size = len(str(seed.metadata).encode('utf-8'))
            total_original += content_size + metadata_size
        
        metrics.original_size = total_original
        
        # 如果有压缩种子，计算压缩后大小
        if compressed_seeds:
            metrics.total_compressed_seeds = len(compressed_seeds)
            total_compressed = sum(
                len(s.content.encode('utf-8')) for s in compressed_seeds.values()
            )
            metrics.compressed_size = total_compressed
        else:
            # 估算：假设平均压缩率为50%
            metrics.compressed_size = int(total_original * 0.5)
        
        # 计算压缩比
        if metrics.original_size > 0:
            metrics.compression_ratio = metrics.compressed_size / metrics.original_size
            metrics.compression_rate = 1.0 - metrics.compression_ratio
        
        # 计算冗余度
        metrics.redundancy_score = self._compute_redundancy(seeds)
        
        # 计算独特性比率
        metrics.uniqueness_ratio = self._compute_uniqueness(seeds)
        
        # 计算效率分数
        metrics.efficiency_score = self._compute_efficiency_score(metrics)
        
        # 记录历史
        self._history.append(metrics)
        
        return metrics
    
    def _compute_redundancy(self, seeds: Dict[str, Any]) -> float:
        """
        计算冗余度
        
        冗余度 = 重复内容比例
        
        实现：
        1. 计算所有种子的内容哈希
        2. 找出重复内容
        3. 返回重复比例
        """
        if not seeds:
            return 0.0
        
        import hashlib
        
        content_hashes = []
        for seed in seeds.values():
            content_hash = hashlib.md5(seed.content.encode('utf-8')).hexdigest()
            content_hashes.append(content_hash)
        
        unique_hashes = set(content_hashes)
        
        # 冗余度 = 1 - 独特性
        return 1.0 - len(unique_hashes) / len(content_hashes)
    
    def _compute_uniqueness(self, seeds: Dict[str, Any]) -> float:
        """
        计算独特性比率
        
        独特种子数 / 总种子数
        """
        if not seeds:
            return 0.0
        
        # 简化为基于内容的独特性
        contents = set(seed.content for seed in seeds.values())
        
        # 基于嵌入的独特性
        embeddings = set()
        for seed in seeds.values():
            if seed.embedding:
                emb_tuple = tuple(seed.embedding)
                embeddings.add(emb_tuple)
        
        # 综合独特性
        content_uniqueness = len(contents) / len(seeds)
        embedding_uniqueness = len(embeddings) / len(seeds) if embeddings else content_uniqueness
        
        return (content_uniqueness + embedding_uniqueness) / 2
    
    def _compute_efficiency_score(self, metrics: CompressionMetrics) -> float:
        """
        计算综合效率分数
        
        效率分数 = 压缩率 × 信息保留 × 独特性
        
        范围：0-1，越高越好
        """
        # 基础压缩效率
        compression_efficiency = metrics.compression_rate
        
        # 信息保留因子（假设为0.9）
        retention_factor = 0.9
        
        # 独特性因子
        uniqueness_factor = metrics.uniqueness_ratio
        
        # 综合效率
        efficiency = compression_efficiency * retention_factor * uniqueness_factor
        
        return min(1.0, efficiency)
    
    def compute_awakening_level(self, compression_ratio: float) -> AwakeningLevel:
        """
        根据压缩比推断觉醒等级
        
        觉醒等级定义：
        - 初觉：低压缩比，大量冗余
        - 正觉：中等压缩比，主要模式已提取
        - 圆觉：高压缩比，接近最优编码
        - 无上觉：理论极限
        
        Args:
            compression_ratio: 压缩比
        
        Returns:
            觉醒等级
        """
        return AwakeningLevel.from_compression_ratio(compression_ratio)
    
    def suggest_compression_targets(
        self, 
        seeds: Dict[str, Any],
        max_suggestions: int = 10
    ) -> List[CompressionTarget]:
        """
        识别压缩机会
        
        找出可压缩的种子簇和冗余模式。
        
        Args:
            seeds: 种子字典
            max_suggestions: 最大建议数
        
        Returns:
            压缩目标列表
        """
        targets = []
        
        # 1. 基于类型找冗余
        targets.extend(self._find_type_redundancy(seeds))
        
        # 2. 基于相似内容找冗余
        targets.extend(self._find_content_redundancy(seeds))
        
        # 3. 基于嵌入相似度找冗余
        targets.extend(self._find_embedding_redundancy(seeds))
        
        # 排序并返回top_k
        targets.sort(key=lambda x: x.potential_savings * x.priority, reverse=True)
        
        return targets[:max_suggestions]
    
    def _find_type_redundancy(self, seeds: Dict[str, Any]) -> List[CompressionTarget]:
        """查找类型冗余"""
        from collections import defaultdict
        
        type_to_seeds = defaultdict(list)
        for seed_id, seed in seeds.items():
            type_to_seeds[seed.seed_type.value].append(seed_id)
        
        targets = []
        for seed_type, seed_ids in type_to_seeds.items():
            if len(seed_ids) >= 5:  # 至少5个同类型种子
                # 计算潜在节省
                avg_size = sum(len(seeds[sid].content) for sid in seed_ids) / len(seed_ids)
                potential_savings = int(avg_size * (len(seed_ids) - 1) * 0.7)  # 70%压缩率
                
                targets.append(CompressionTarget(
                    target_type="type_redundancy",
                    seed_ids=seed_ids,
                    potential_savings=potential_savings,
                    priority=2,
                    reason=f"同类型({seed_type})种子{len(seed_ids)}个，可压缩为抽象模式"
                ))
        
        return targets
    
    def _find_content_redundancy(self, seeds: Dict[str, Any]) -> List[CompressionTarget]:
        """查找内容冗余"""
        import hashlib
        
        content_hashes = defaultdict(list)
        for seed_id, seed in seeds.items():
            content_hash = hashlib.md5(seed.content.encode('utf-8')).hexdigest()
            content_hashes[content_hash].append(seed_id)
        
        targets = []
        for content_hash, seed_ids in content_hashes.items():
            if len(seed_ids) >= 2:
                total_size = sum(len(seeds[sid].content) for sid in seed_ids)
                potential_savings = int(total_size * 0.5)  # 50%节省
                
                targets.append(CompressionTarget(
                    target_type="content_duplication",
                    seed_ids=seed_ids,
                    potential_savings=potential_savings,
                    priority=3,
                    reason=f"重复内容种子{len(seed_ids)}个"
                ))
        
        return targets
    
    def _find_embedding_redundancy(self, seeds: Dict[str, Any]) -> List[CompressionTarget]:
        """查找嵌入冗余"""
        high_similarity_pairs = []
        
        seed_list = [(sid, s) for sid, s in seeds.items() if s.embedding]
        
        for i, (id1, seed1) in enumerate(seed_list):
            for id2, seed2 in seed_list[i+1:]:
                similarity = self._cosine_similarity(seed1.embedding, seed2.embedding)
                if similarity > 0.9:
                    high_similarity_pairs.append((id1, id2, similarity))
        
        targets = []
        if high_similarity_pairs:
            # 合并高相似对
            seed_ids = list(set(p[0] for p in high_similarity_pairs) | set(p[1] for p in high_similarity_pairs))
            
            if len(seed_ids) >= 3:
                total_size = sum(len(seeds[sid].content) for sid in seed_ids)
                potential_savings = int(total_size * 0.6)
                
                targets.append(CompressionTarget(
                    target_type="embedding_similarity",
                    seed_ids=seed_ids,
                    potential_savings=potential_savings,
                    priority=2,
                    reason=f"高相似嵌入种子{len(seed_ids)}个"
                ))
        
        return targets
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """计算余弦相似度"""
        if len(a) != len(b) or not a:
            return 0.0
        
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)
    
    def compute_kolmogorov_optimality(
        self, 
        seeds: Dict[str, Any],
        compressed_seeds: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        计算Kolmogorov最优性
        
        Kolmogorov复杂度K(s)定义为生成字符串s的最短程序长度。
        实际中无法精确计算，使用压缩率作为代理。
        
        最优性 = 压缩后大小 / K(s)估计
        
        Args:
            seeds: 原始种子
            compressed_seeds: 压缩种子
        
        Returns:
            最优性分数（越接近1越好）
        """
        import gzip
        
        if not seeds:
            return 1.0
        
        # 计算理论最小大小（使用Kolmogorov复杂度的gzip近似）
        total_original = sum(len(s.content.encode('utf-8')) for s in seeds.values())
        
        # Gzip作为K-复杂度的下界估计
        all_content = "\n".join(s.content for s in seeds.values())
        compressed = gzip.compress(all_content.encode('utf-8'))
        kolmogorov_estimate = len(compressed)
        
        # 当前压缩大小
        current_size = total_original
        if compressed_seeds:
            current_size = sum(len(s.content.encode('utf-8')) for s in compressed_seeds.values())
        
        # 最优性 = 接近K-复杂度估计的程度
        if kolmogorov_estimate > 0:
            optimality = kolmogorov_estimate / current_size
        else:
            optimality = 0.0
        
        return min(1.0, optimality)
    
    def track_evolution(self) -> Dict[str, Any]:
        """
        追踪压缩效率演化
        
        分析历史数据，观察压缩效率的提升趋势。
        
        Returns:
            演化分析报告
        """
        if len(self._history) < 2:
            return {"status": "insufficient_data", "message": "历史数据不足"}
        
        # 计算趋势
        first = self._history[0]
        last = self._history[-1]
        
        compression_change = last.compression_ratio - first.compression_ratio
        efficiency_change = last.efficiency_score - first.efficiency_score
        
        # 判断趋势
        if compression_change < -0.1:
            trend = "improving"
            description = "压缩效率持续提升"
        elif compression_change > 0.1:
            trend = "declining"
            description = "压缩效率下降，可能需要优化"
        else:
            trend = "stable"
            description = "压缩效率稳定"
        
        return {
            "status": "success",
            "trend": trend,
            "description": description,
            "first_metrics": {
                "compression_ratio": first.compression_ratio,
                "efficiency_score": first.efficiency_score
            },
            "last_metrics": {
                "compression_ratio": last.compression_ratio,
                "efficiency_score": last.efficiency_score
            },
            "changes": {
                "compression_ratio_change": compression_change,
                "efficiency_score_change": efficiency_change
            },
            "data_points": len(self._history)
        }
    
    def compute_neng_efficiency(
        self, 
        compression_metrics: CompressionMetrics,
        token_cost_per_byte: float = 0.001
    ) -> Dict[str, float]:
        """
        计算Néng效率
        
        与Token经济学对接：
        - 压缩效率 → Néng效率 → 经济增长
        
        Args:
            compression_metrics: 压缩度量
            token_cost_per_byte: 每字节的Token成本
        
        Returns:
            Néng效率指标
        """
        # 存储节省
        storage_saved = compression_metrics.original_size - compression_metrics.compressed_size
        
        # Token成本节省
        token_savings = storage_saved * token_cost_per_byte
        
        # Néng效率 = 信息处理能力 / 资源消耗
        # 简化为：压缩率 / 成本
        neng_efficiency = compression_metrics.compression_rate / (token_cost_per_byte + 0.001)
        
        # 标准化到0-1范围
        normalized_efficiency = min(1.0, neng_efficiency / 1000)
        
        return {
            "raw_efficiency": neng_efficiency,
            "normalized_efficiency": normalized_efficiency,
            "storage_saved_bytes": storage_saved,
            "token_savings": token_savings,
            "compression_gain": compression_metrics.compression_rate
        }
    
    def get_diagnosis(self, seeds: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取系统诊断报告
        
        综合分析种子库的健康状况和优化建议。
        
        Returns:
            诊断报告
        """
        metrics = self.compute_system_compression_ratio(seeds)
        awakening = self.compute_awakening_level(metrics.compression_ratio)
        targets = self.suggest_compression_targets(seeds)
        
        # 生成建议
        suggestions = []
        
        if metrics.redundancy_score > self._thresholds["high_redundancy"]:
            suggestions.append(f"高冗余检测({metrics.redundancy_score:.1%})：建议压缩重复种子")
        
        if metrics.compression_ratio > self._thresholds["low_compression"]:
            suggestions.append(f"低压缩比({metrics.compression_ratio:.1%})：建议增加模式抽象")
        
        if awakening == AwakeningLevel.UNCONSCIOUS:
            suggestions.append("系统处于无意识状态：需要大量学习积累")
        elif awakening == AwakeningLevel.INITIAL:
            suggestions.append("初觉阶段：开始建立基本模式")
        
        if len(targets) > 5:
            suggestions.append(f"发现{len(targets)}个压缩机会，可节省约{sum(t.potential_savings for t in targets)}字节")
        
        return {
            "metrics": {
                "total_seeds": metrics.total_seeds,
                "compression_ratio": metrics.compression_ratio,
                "compression_rate": metrics.compression_rate,
                "redundancy_score": metrics.redundancy_score,
                "efficiency_score": metrics.efficiency_score
            },
            "awakening_level": awakening.name_cn,
            "awakening_description": awakening.description,
            "compression_targets_count": len(targets),
            "suggestions": suggestions
        }
