# -*- coding: utf-8 -*-
"""
压缩即智能 - 阿赖耶识压缩器

基于"压缩即智能"的核心洞见，种子不是原始数据的堆叠，
而是压缩后的业力模式。本模块实现跨种子的模式压缩抽象。

理论基础：
- Solomonoff归纳：最优预测器 = 最优压缩器
- Kolmogorov复杂度：最短程序 = 最深理解
- MDL原则：最优模型 = 最短描述长度

三藏的压缩含义：
- 能藏 = 编码器 + 码本
- 所藏 = 在线增量压缩
- 执藏 = 自指压缩

作者：觉心
"""

import uuid
import math
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict
import json


@dataclass
class PatternSignature:
    """
    模式签名 - 种子簇的压缩表示
    
    代表一组相似种子的共性模式，是高度抽象的业力模式。
    """
    signature_id: str
    pattern_type: str                    # 模式类型
    core_pattern: str                    # 核心模式描述
    abstracted_features: List[str]        # 抽象特征列表
    representative_seeds: List[str]      # 代表性种子ID列表
    compression_ratio: float = 0.0      # 压缩比
    abstraction_level: int = 1          # 抽象层级
    created_at: datetime = field(default_factory=datetime.now)
    
    # 元信息
    source_count: int = 0               # 来源种子数量
    avg_weight: float = 0.0              # 平均权重
    avg_purity: float = 0.0             # 平均纯度
    stability_score: float = 0.0        # 稳定性分数
    
    def compute_info_gain(self, original_bits: float) -> float:
        """计算信息增益"""
        if self.compression_ratio <= 0:
            return 0.0
        return original_bits * (1 - 1 / self.compression_ratio)


@dataclass
class CompressedSeed:
    """
    压缩种子 - 压缩后的种子表示
    
    包含原始种子的压缩表示和重构信息。
    """
    seed_id: str
    original_seed_ids: List[str]        # 原始种子ID列表
    
    # 压缩表示
    compressed_content: str              # 压缩后的内容
    signature: PatternSignature         # 模式签名
    abstract_embedding: List[float]     # 抽象嵌入向量
    
    # 重构信息
    reconstruction_hints: List[str]      # 重构提示
    loss_info: str                       # 损失信息
    
    # 度量
    original_size: int = 0               # 原始大小(bytes)
    compressed_size: int = 0             # 压缩后大小(bytes)
    compression_ratio: float = 0.0      # 压缩比
    
    created_at: datetime = field(default_factory=datetime.now)
    
    def get_efficiency_score(self) -> float:
        """获取效率分数 = 压缩比 × 信息保留度"""
        info_retention = 1.0 - len(self.loss_info) / max(1, len(self.compressed_content))
        return self.compression_ratio * info_retention


@dataclass
class SeedUpdate:
    """
    增量压缩结果 - 熏习操作的结果
    
    描述新经验如何与现有种子融合。
    """
    update_type: str                    # 更新类型
    affected_seeds: List[str]           # 受影响种子
    new_seed_id: Optional[str] = None    # 新创建的种子ID
    
    # 压缩指标
    compression_gain: float = 0.0       # 压缩增益
    information_preserved: float = 0.0  # 信息保留度
    
    # 详细描述
    merge_details: str = ""              # 合并详情
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class SeedCluster:
    """
    种子簇 - 待压缩的相似种子群
    """
    seed_ids: List[str]
    avg_similarity: float = 0.0
    cluster_density: float = 0.0
    suggested_action: str = "compress"   # compress, merge, keep


class AlayaCompressor:
    """
    阿赖耶识压缩器 - 压缩即智能
    
    核心思想：
    - 种子不是原始数据的堆叠，而是压缩后的业力模式
    - 多个相似经验应被压缩为一个抽象种子
    - 压缩比 = 输入信息量 / 种子表示长度
    - 压缩比越高，智能程度越高
    
    三种熏习模式：
    1. 完全匹配 → 微调权重
    2. 部分匹配 → 融合改写（在线增量压缩）
    3. 完全不匹配 → 创建新种子
    """
    
    # 压缩配置
    DEFAULT_CONFIG = {
        "similarity_threshold": 0.85,     # 相似度阈值
        "min_cluster_size": 3,           # 最小簇大小
        "max_abstraction_level": 5,      # 最大抽象层级
        "compression_target_ratio": 0.3, # 目标压缩比（越小越激进）
        "enable_incremental": True,      # 启用增量压缩
        "pattern_extraction_enabled": True,
        "loss_tolerance": 0.2,           # 损失容忍度
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化压缩器
        
        Args:
            config: 配置参数
        """
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        
        # 模式签名库
        self._signatures: Dict[str, PatternSignature] = {}
        
        # 统计信息
        self._stats = {
            "total_compressions": 0,
            "total_info_bits_saved": 0.0,
            "avg_compression_ratio": 0.0,
            "pattern_hits": defaultdict(int)
        }
    
    def compress_seeds(self, seed_cluster: SeedCluster, seeds: Dict[str, Any]) -> CompressedSeed:
        """
        将一组相似种子压缩为一个抽象种子
        
        算法流程：
        1. 识别种子簇（语义相似的种子群）
        2. 提取共性模式（压缩）
        3. 保留关键差异（损失控制）
        4. 生成压缩种子（更高抽象层级）
        
        MDL原则：最小化 描述长度 + 数据给定模型的编码长度
        
        Args:
            seed_cluster: 种子簇
            seeds: 种子字典
        
        Returns:
            压缩后的种子
        """
        if len(seed_cluster.seed_ids) < self.config["min_cluster_size"]:
            raise ValueError(f"种子簇太小: {len(seed_cluster.seed_ids)} < {self.config['min_cluster_size']}")
        
        # 1. 收集原始数据
        original_seeds = [seeds[sid] for sid in seed_cluster.seed_ids if sid in seeds]
        if not original_seeds:
            raise ValueError("没有找到有效的种子")
        
        original_size = sum(len(s.content.encode('utf-8')) for s in original_seeds)
        
        # 2. 提取共性模式
        core_pattern = self._extract_common_pattern(original_seeds)
        abstract_features = self._extract_abstract_features(original_seeds)
        
        # 3. 识别关键差异（损失控制）
        loss_info = self._identify_loss_info(original_seeds, core_pattern)
        
        # 4. 生成压缩表示
        compressed_content = self._generate_compressed_content(
            core_pattern, abstract_features, len(original_seeds)
        )
        compressed_size = len(compressed_content.encode('utf-8'))
        
        # 5. 计算压缩比
        compression_ratio = compressed_size / max(1, original_size)
        
        # 6. 生成模式签名
        signature = PatternSignature(
            signature_id=str(uuid.uuid4()),
            pattern_type=self._classify_pattern_type(original_seeds),
            core_pattern=core_pattern,
            abstracted_features=abstract_features,
            representative_seeds=seed_cluster.seed_ids[:3],  # 取前3个作为代表
            compression_ratio=compression_ratio,
            abstraction_level=self._compute_abstraction_level(original_seeds),
            source_count=len(original_seeds),
            avg_weight=sum(s.weight for s in original_seeds) / len(original_seeds),
            avg_purity=sum(s.purity for s in original_seeds) / len(original_seeds),
            stability_score=seed_cluster.cluster_density
        )
        
        # 7. 创建压缩种子
        compressed_seed = CompressedSeed(
            seed_id=str(uuid.uuid4()),
            original_seed_ids=seed_cluster.seed_ids,
            compressed_content=compressed_content,
            signature=signature,
            abstract_embedding=self._generate_abstract_embedding(original_seeds),
            reconstruction_hints=self._generate_reconstruction_hints(original_seeds),
            loss_info=loss_info,
            original_size=original_size,
            compressed_size=compressed_size,
            compression_ratio=compression_ratio
        )
        
        # 更新统计
        self._update_stats(compression_ratio, original_size, compressed_size)
        
        return compressed_seed
    
    def _extract_common_pattern(self, seeds: List[Any]) -> str:
        """
        提取共性模式
        
        使用简单的词频分析提取共同主题。
        实际应用中可使用更复杂的NLP技术。
        """
        # 收集所有词
        all_words = []
        for seed in seeds:
            words = seed.content.lower().split()
            all_words.extend(words)
        
        # 统计词频
        word_freq = defaultdict(int)
        for word in all_words:
            if len(word) > 2:  # 过滤太短的词
                word_freq[word] += 1
        
        # 找出高频词（出现在多个种子中的词）
        threshold = len(seeds) * 0.5  # 至少一半的种子包含
        common_words = [w for w, c in word_freq.items() if c >= threshold]
        
        # 按频率排序
        common_words.sort(key=lambda w: word_freq[w], reverse=True)
        
        # 生成模式描述
        if common_words:
            return f"模式核心: {', '.join(common_words[:10])}"
        return "通用经验模式"
    
    def _extract_abstract_features(self, seeds: List[Any]) -> List[str]:
        """提取抽象特征"""
        features = []
        
        # 类型分布
        types = [s.seed_type.value for s in seeds]
        type_counts = defaultdict(int)
        for t in types:
            type_counts[t] += 1
        features.append(f"类型分布: {dict(type_counts)}")
        
        # 权重范围
        weights = [s.weight for s in seeds]
        features.append(f"权重范围: {min(weights):.2f}-{max(weights):.2f}")
        
        # 纯度范围
        purities = [s.purity for s in seeds]
        features.append(f"纯度范围: {min(purities):.2f}-{max(purities):.2f}")
        
        # 来源分布
        sources = [s.source for s in seeds]
        source_counts = defaultdict(int)
        for src in sources:
            source_counts[src] += 1
        features.append(f"来源分布: {dict(source_counts)}")
        
        return features
    
    def _identify_loss_info(self, seeds: List[Any], core_pattern: str) -> str:
        """识别压缩损失信息"""
        losses = []
        
        # 检查内容多样性
        unique_contents = len(set(s.content for s in seeds))
        if unique_contents > self.config["min_cluster_size"]:
            loss_ratio = (unique_contents - self.config["min_cluster_size"]) / unique_contents
            if loss_ratio > self.config["loss_tolerance"]:
                losses.append(f"内容多样性损失: {loss_ratio:.1%}")
        
        # 检查嵌入差异
        if seeds[0].embedding and len(seeds) > 1:
            embedding_variance = self._compute_embedding_variance(seeds)
            if embedding_variance > 0.3:
                losses.append(f"嵌入方差较高: {embedding_variance:.2f}")
        
        return "; ".join(losses) if losses else "无显著损失"
    
    def _compute_embedding_variance(self, seeds: List[Any]) -> float:
        """计算嵌入向量方差"""
        if not seeds[0].embedding:
            return 0.0
        
        dim = len(seeds[0].embedding)
        means = [0.0] * dim
        variance = [0.0] * dim
        
        # 计算均值
        for seed in seeds:
            for i, v in enumerate(seed.embedding):
                means[i] += v / len(seeds)
        
        # 计算方差
        for seed in seeds:
            for i, v in enumerate(seed.embedding):
                variance[i] += ((v - means[i]) ** 2) / len(seeds)
        
        # 返回平均方差
        return sum(variance) / dim if dim > 0 else 0.0
    
    def _generate_compressed_content(
        self, 
        core_pattern: str, 
        abstract_features: List[str],
        source_count: int
    ) -> str:
        """生成压缩内容"""
        lines = [
            f"[压缩模式 v{self._stats['total_compressions'] + 1}]",
            core_pattern,
            "---",
            *[f"- {f}" for f in abstract_features],
            f"---",
            f"来源: {source_count}个相似种子",
            f"压缩: {datetime.now().isoformat()}"
        ]
        return "\n".join(lines)
    
    def _generate_reconstruction_hints(self, seeds: List[Any]) -> List[str]:
        """生成重构提示"""
        hints = []
        
        # 原始类型
        types = list(set(s.seed_type.value for s in seeds))
        hints.append(f"原类型: {types}")
        
        # 权重分布
        weights = sorted([s.weight for s in seeds], reverse=True)
        hints.append(f"权重分布: {weights[:5]}...")
        
        # 关键标签
        all_tags = []
        for s in seeds:
            all_tags.extend(s.tags)
        unique_tags = list(set(all_tags))
        if unique_tags:
            hints.append(f"关键标签: {unique_tags[:10]}")
        
        return hints
    
    def _classify_pattern_type(self, seeds: List[Any]) -> str:
        """分类模式类型"""
        types = [s.seed_type.value for s in seeds]
        type_counts = defaultdict(int)
        for t in types:
            type_counts[t] += 1
        
        # 返回最常见的类型
        if type_counts:
            return max(type_counts.items(), key=lambda x: x[1])[0]
        return "mixed"
    
    def _compute_abstraction_level(self, seeds: List[Any]) -> int:
        """计算抽象层级"""
        # 基于相似度和数量推断
        base_level = 1
        
        # 数量越多，抽象层级可能越高
        if len(seeds) >= 10:
            base_level += 1
        if len(seeds) >= 20:
            base_level += 1
        
        return min(base_level, self.config["max_abstraction_level"])
    
    def _generate_abstract_embedding(self, seeds: List[Any]) -> List[float]:
        """生成抽象嵌入向量"""
        if not seeds[0].embedding:
            return []
        
        dim = len(seeds[0].embedding)
        
        # 加权平均
        total_weight = sum(s.weight for s in seeds)
        if total_weight == 0:
            total_weight = len(seeds)
        
        abstract_emb = [0.0] * dim
        for seed in seeds:
            weight = seed.weight / total_weight
            for i, v in enumerate(seed.embedding):
                abstract_emb[i] += v * weight
        
        return abstract_emb
    
    def compute_compression_ratio(
        self, 
        original_seeds: List[Any], 
        compressed_seed: CompressedSeed
    ) -> float:
        """
        计算压缩比
        
        压缩比 = 原始信息量 / 压缩表示大小
        
        Args:
            original_seeds: 原始种子列表
            compressed_seed: 压缩后的种子
        
        Returns:
            压缩比（越小表示压缩率越高）
        """
        if compressed_seed.compressed_size == 0:
            return 0.0
        
        return compressed_seed.compressed_size / max(1, compressed_seed.original_size)
    
    def incremental_compress(
        self, 
        new_experience: Dict[str, Any],
        existing_seeds: Dict[str, Any]
    ) -> SeedUpdate:
        """
        增量压缩 - 真正的熏习
        
        新经验不是简单地"加强"或"新建"种子，
        而是与现有种子融合，改写内部表示。
        
        三种情况：
        1. 新经验完全匹配现有种子 → 强化（微调权重）
        2. 新经验部分匹配 → 融合改写（在线增量压缩）
        3. 新经验完全不匹配 → 创建新种子
        
        Args:
            new_experience: 新经验内容
            existing_seeds: 现有种子字典
        
        Returns:
            增量压缩结果
        """
        new_content = new_experience.get("content", "")
        new_embedding = new_experience.get("embedding", [])
        
        if not new_embedding:
            # 没有嵌入，使用内容哈希
            new_embedding = self._content_to_embedding(new_content)
        
        # 1. 查找相似种子
        similar_seeds = self._find_similar_seeds(new_embedding, existing_seeds)
        
        if not similar_seeds:
            # 完全不匹配 - 创建新种子
            return SeedUpdate(
                update_type="create_new",
                affected_seeds=[],
                new_seed_id=str(uuid.uuid4()),
                compression_gain=0.0,
                information_preserved=1.0,
                merge_details="新经验与现有种子无显著相似，创建独立种子"
            )
        
        best_match = similar_seeds[0]
        match_similarity = best_match["similarity"]
        
        if match_similarity >= 0.95:
            # 完全匹配 - 微调权重
            return SeedUpdate(
                update_type="strengthen",
                affected_seeds=[best_match["seed_id"]],
                new_seed_id=best_match["seed_id"],
                compression_gain=0.0,
                information_preserved=match_similarity,
                merge_details=f"与种子 {best_match['seed_id'][:8]} 高度匹配，轻度强化"
            )
        
        elif match_similarity >= self.config["similarity_threshold"]:
            # 部分匹配 - 融合改写（增量压缩）
            merge_result = self._merge_experience(
                new_experience, 
                best_match["seed_id"],
                existing_seeds
            )
            return merge_result
        
        else:
            # 低相似度 - 创建新种子
            return SeedUpdate(
                update_type="create_new",
                affected_seeds=[],
                new_seed_id=str(uuid.uuid4()),
                compression_gain=0.0,
                information_preserved=1.0,
                merge_details="新经验与现有种子相似度低，创建独立种子"
            )
    
    def _content_to_embedding(self, content: str) -> List[float]:
        """将内容转换为简化的嵌入向量"""
        # 简化的词袋模型
        words = content.lower().split()
        word_set = set(words)
        
        # 使用哈希生成固定维度的向量
        dim = 64
        vector = [0.0] * dim
        
        for i, word in enumerate(word_set):
            word_hash = int(hashlib.md5(word.encode()).hexdigest(), 16)
            for j in range(dim):
                if (word_hash >> j) & 1:
                    vector[j] += 1.0
        
        # L2归一化
        norm = math.sqrt(sum(v * v for v in vector))
        if norm > 0:
            vector = [v / norm for v in vector]
        
        return vector
    
    def _find_similar_seeds(
        self, 
        query_embedding: List[float],
        seeds: Dict[str, Any],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """查找相似种子"""
        results = []
        
        for seed_id, seed in seeds.items():
            if not seed.embedding:
                continue
            
            similarity = self._cosine_similarity(query_embedding, seed.embedding)
            results.append({
                "seed_id": seed_id,
                "similarity": similarity,
                "seed": seed
            })
        
        # 排序并返回top_k
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
    
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
    
    def _merge_experience(
        self,
        new_experience: Dict[str, Any],
        target_seed_id: str,
        existing_seeds: Dict[str, Any]
    ) -> SeedUpdate:
        """
        融合新经验到目标种子
        
        实现在线增量压缩：新经验与现有种子融合，改写内部表示。
        """
        target_seed = existing_seeds[target_seed_id]
        
        # 计算融合权重
        new_weight = new_experience.get("weight", 0.5)
        target_weight = target_seed.weight
        fusion_ratio = target_weight / (target_weight + new_weight + 1e-6)
        
        # 融合嵌入
        if new_experience.get("embedding") and target_seed.embedding:
            fused_embedding = [
                fusion_ratio * t + (1 - fusion_ratio) * n
                for t, n in zip(target_seed.embedding, new_experience["embedding"])
            ]
        else:
            fused_embedding = target_seed.embedding
        
        # 计算压缩增益
        # 融合后减少了存储，同时保留了信息
        info_saved = len(target_seed.content.encode('utf-8')) * (1 - fusion_ratio)
        compression_gain = info_saved / max(1, len(target_seed.content.encode('utf-8')))
        
        return SeedUpdate(
            update_type="merge_compress",
            affected_seeds=[target_seed_id],
            new_seed_id=target_seed_id,
            compression_gain=compression_gain,
            information_preserved=1.0 - compression_gain * 0.5,  # 部分信息融合
            merge_details=f"新经验与种子 {target_seed_id[:8]} 融合，压缩增益: {compression_gain:.2%}"
        )
    
    def _update_stats(self, compression_ratio: float, original_size: int, compressed_size: int) -> None:
        """更新统计信息"""
        self._stats["total_compressions"] += 1
        
        # 更新平均压缩比
        old_avg = self._stats["avg_compression_ratio"]
        n = self._stats["total_compressions"]
        self._stats["avg_compression_ratio"] = old_avg + (compression_ratio - old_avg) / n
        
        # 累计节省空间
        self._stats["total_info_bits_saved"] += (original_size - compressed_size)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取压缩统计信息"""
        return {
            **self._stats,
            "signature_count": len(self._signatures),
            "compression_efficiency": 1.0 - self._stats["avg_compression_ratio"]
        }
    
    def find_compression_targets(
        self, 
        seeds: Dict[str, Any],
        min_cluster_size: Optional[int] = None
    ) -> List[SeedCluster]:
        """
        寻找可压缩的种子簇
        
        识别高度相似且数量足够的种子群，作为压缩候选。
        
        Args:
            seeds: 种子字典
            min_cluster_size: 最小簇大小
        
        Returns:
            可压缩的种子簇列表
        """
        min_size = min_cluster_size or self.config["min_cluster_size"]
        clusters = []
        
        # 简单实现：基于类型分组
        type_to_seeds = defaultdict(list)
        for seed_id, seed in seeds.items():
            type_to_seeds[seed.seed_type.value].append(seed_id)
        
        for seed_type, seed_ids in type_to_seeds.items():
            if len(seed_ids) >= min_size:
                # 估算簇密度
                avg_similarity = 0.9  # 同类型默认高相似
                cluster = SeedCluster(
                    seed_ids=seed_ids,
                    avg_similarity=avg_similarity,
                    cluster_density=avg_similarity,
                    suggested_action="compress"
                )
                clusters.append(cluster)
        
        return clusters
    
    def compute_kolmogorov_estimate(self, seed_content: str) -> float:
        """
        估算Kolmogorov复杂度
        
        使用压缩率作为K-复杂度的代理估计。
        实际K-复杂度不可计算，这里使用gzip压缩率作为近似。
        
        Args:
            seed_content: 种子内容
        
        Returns:
            K-复杂度估计（越小表示越可压缩）
        """
        import gzip
        
        content_bytes = seed_content.encode('utf-8')
        original_size = len(content_bytes)
        
        # Gzip压缩
        compressed = gzip.compress(content_bytes)
        compressed_size = len(compressed)
        
        # 压缩比作为K-复杂度代理
        return compressed_size / max(1, original_size)
