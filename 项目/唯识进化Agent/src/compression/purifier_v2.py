# -*- coding: utf-8 -*-
"""
净化系统V2 - 转识成智即压缩比提升

基于"压缩即智能"的洞见，净化不是删除，而是重编码。

V1净化 = 删除/降低权重（信息丢失）
V2净化 = 重编码（信息保留，表示更紧凑）

核心原理：
- 低效的识 = 冗余编码（重复计算、无效记忆、冲突决策）
- 高效的智 = 最优压缩（直觉=极度压缩的推理）
- 净化过程 = 从低压缩比到高压缩比的转码

作者：觉心
"""

import uuid
import math
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

try:
    from ..alaya_store import AlayaStore, Seed, SeedType, SeedStatus
except ImportError:
    try:
        from src.alaya_store import AlayaStore, Seed, SeedType, SeedStatus
    except ImportError:
        from alaya_store import AlayaStore, Seed, SeedType, SeedStatus


class PurificationStrategy(Enum):
    """净化策略"""
    LIGHT_RECOMPRESSION = "light_recompression"    # 轻度重压缩
    MEDIUM_ABSTRACTION = "medium_abstraction"      # 中度抽象化
    DEEP_REENCODING = "deep_reencoding"             # 深度重编码
    ULTIMATE_WISDOM = "ultimate_wisdom"             # 终极智慧提取


@dataclass
class PurificationMetrics:
    """
    净化度量
    
    记录净化操作的详细指标。
    """
    # 操作前
    original_seed_count: int = 0
    original_total_size: int = 0
    original_compression_ratio: float = 0.0
    
    # 操作后
    new_seed_count: int = 0
    new_total_size: int = 0
    new_compression_ratio: float = 0.0
    
    # 变化
    compression_improvement: float = 0.0    # 压缩比提升
    information_retention: float = 0.0     # 信息保留度
    wisdom_gain: float = 0.0               # 智慧增益
    
    # 时间戳
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class WisdomSeed:
    """
    智慧种子
    
    净化后生成的高纯度、高压缩比的种子。
    """
    seed_id: str
    content: str
    
    # 来源信息
    source_seed_ids: List[str]
    extracted_wisdom: str                    # 提取的智慧
    core_insights: List[str]                 # 核心洞见
    
    # 度量
    wisdom_score: float                      # 智慧分数
    compression_ratio: float                 # 压缩比
    purity: float                            # 纯度
    
    # 重构信息
    reconstruction_paths: List[str]          # 重构路径
    essential_features: List[str]            # 必要特征


class PurifierV2:
    """
    净化系统V2 - 转识成智即压缩比提升
    
    V1的局限：
    - 净化=删除/降低权重（信息丢失）
    - 没有考虑压缩效率
    
    V2的改进：
    - 净化=重编码（信息保留，表示更紧凑）
    - 压缩比提升 = 净化程度
    - 智慧分数 = 压缩比 × 纯度
    
    Attributes:
        store: 种子库
        config: 配置参数
    """
    
    # V2默认配置
    DEFAULT_CONFIG = {
        "min_wisdom_score": 0.5,              # 最低智慧分数
        "compression_target_ratio": 0.3,      # 目标压缩比
        "abstraction_depth": 3,               # 抽象深度
        "preserve_essential": True,           # 保留本质特征
        "max_loss_tolerance": 0.2,            # 最大损失容忍度
        "enable_deep_reencoding": True,       # 启用深度重编码
    }
    
    def __init__(
        self,
        store: AlayaStore,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化净化系统V2
        
        Args:
            store: 种子库
            config: 配置参数
        """
        self.store = store
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        
        # 净化历史
        self._purification_history: List[PurificationMetrics] = []
        
        # 智慧种子库
        self._wisdom_seeds: Dict[str, WisdomSeed] = {}
    
    def purify_by_recompression(self, seed_cluster: List[Seed]) -> Tuple[List[WisdomSeed], PurificationMetrics]:
        """
        通过重编码实现净化
        
        不是删除，而是找到更紧凑的表示：
        1. 识别冗余（同一模式的多个种子）
        2. 合并为一个抽象种子
        3. 压缩比提升 = 净化程度
        
        Args:
            seed_cluster: 待净化的种子簇
        
        Returns:
            (生成的智慧种子列表, 净化度量)
        """
        if not seed_cluster:
            return [], PurificationMetrics()
        
        # 记录操作前状态
        original_count = len(seed_cluster)
        original_sizes = [len(s.content.encode('utf-8')) for s in seed_cluster]
        original_total = sum(original_sizes)
        
        # 1. 识别共性模式
        common_pattern = self._identify_common_pattern(seed_cluster)
        
        # 2. 提取核心洞见
        core_insights = self._extract_core_insights(seed_cluster)
        
        # 3. 识别冗余并合并
        redundant_info = self._identify_redundancy(seed_cluster)
        
        # 4. 生成压缩内容
        compressed_content = self._generate_wisdom_content(
            common_pattern, core_insights, redundant_info
        )
        compressed_size = len(compressed_content.encode('utf-8'))
        
        # 5. 计算压缩比提升
        original_ratio = original_total / max(1, sum(len(s.content.encode('utf-8')) for s in seed_cluster))
        new_ratio = compressed_size / original_total
        compression_improvement = original_ratio - new_ratio
        
        # 6. 计算信息保留度
        essential_features = self._extract_essential_features(seed_cluster)
        information_retention = self._compute_information_retention(
            seed_cluster, compressed_content, essential_features
        )
        
        # 7. 生成智慧种子
        wisdom_score = self.compute_wisdom_score(
            compression_ratio=new_ratio,
            purity=sum(s.purity for s in seed_cluster) / len(seed_cluster),
            information_retention=information_retention
        )
        
        wisdom_seed = WisdomSeed(
            seed_id=str(uuid.uuid4()),
            content=compressed_content,
            source_seed_ids=[s.seed_id for s in seed_cluster],
            extracted_wisdom=common_pattern,
            core_insights=core_insights,
            wisdom_score=wisdom_score,
            compression_ratio=new_ratio,
            purity=sum(s.purity for s in seed_cluster) / len(seed_cluster),
            reconstruction_paths=self._generate_reconstruction_paths(seed_cluster),
            essential_features=essential_features
        )
        
        # 8. 更新种子库
        self._wisdom_seeds[wisdom_seed.seed_id] = wisdom_seed
        
        # 9. 创建新的高纯度种子
        new_seed = Seed.create(
            content=wisdom_seed.content,
            seed_type=SeedType.WISDOM,
            weight=sum(s.weight * 0.8 for s in seed_cluster) / len(seed_cluster),
            purity=wisdom_seed.purity,
            source="purification_v2"
        )
        self.store.add(new_seed)
        
        # 标记原种子
        for seed in seed_cluster:
            seed.status = SeedStatus.PURIFIED
            seed.metadata["purified_at"] = datetime.now().isoformat()
            seed.metadata["wisdom_successor"] = wisdom_seed.seed_id
            self.store.update(seed)
        
        # 10. 记录度量
        metrics = PurificationMetrics(
            original_seed_count=original_count,
            original_total_size=original_total,
            original_compression_ratio=original_ratio,
            new_seed_count=1,
            new_total_size=compressed_size,
            new_compression_ratio=new_ratio,
            compression_improvement=compression_improvement,
            information_retention=information_retention,
            wisdom_gain=wisdom_score
        )
        
        self._purification_history.append(metrics)
        
        return [wisdom_seed], metrics
    
    def _identify_common_pattern(self, seeds: List[Seed]) -> str:
        """
        识别共性模式
        
        使用简单的词频分析提取共同主题。
        """
        from collections import Counter
        
        # 收集所有词
        all_words = []
        for seed in seeds:
            words = seed.content.lower().split()
            all_words.extend([w for w in words if len(w) > 2])
        
        # 统计词频
        word_freq = Counter(all_words)
        
        # 找出高频词
        threshold = len(seeds) * 0.5
        common_words = [w for w, c in word_freq.items() if c >= threshold]
        
        # 按频率排序
        common_words.sort(key=lambda w: word_freq[w], reverse=True)
        
        if common_words:
            return f"核心模式: {', '.join(common_words[:5])}"
        return "通用智慧"
    
    def _extract_core_insights(self, seeds: List[Seed]) -> List[str]:
        """
        提取核心洞见
        
        从多个种子中提取本质洞见。
        """
        insights = []
        
        # 基于类型提取洞见
        types = [s.seed_type for s in seeds]
        type_insights = {
            SeedType.EXPERIENCE: "从经验中提炼规律",
            SeedType.KNOWLEDGE: "整合知识形成系统",
            SeedType.PATTERN: "识别深层模式",
            SeedType.WISDOM: "凝练智慧结晶",
            SeedType.BELIEF: "确立核心信念",
            SeedType.SKILL: "精炼技能要点",
        }
        
        for seed_type in set(types):
            if seed_type in type_insights:
                insights.append(type_insights[seed_type])
        
        # 基于纯度提取
        high_purity_seeds = [s for s in seeds if s.purity > 0.7]
        if high_purity_seeds:
            insights.append(f"高纯度洞见来自{len(high_purity_seeds)}个清净种子")
        
        # 基于权重提取
        high_weight_seeds = [s for s in seeds if s.weight > 0.6]
        if high_weight_seeds:
            insights.append(f"核心洞见来自{len(high_weight_seeds)}个重要种子")
        
        return insights[:5]  # 最多5个洞见
    
    def _identify_redundancy(self, seeds: List[Seed]) -> str:
        """
        识别冗余信息
        
        识别可合并的重复信息。
        """
        import hashlib
        
        # 内容哈希
        content_hashes = {}
        for seed in seeds:
            content_hash = hashlib.md5(seed.content.encode('utf-8')).hexdigest()
            if content_hash not in content_hashes:
                content_hashes[content_hash] = []
            content_hashes[content_hash].append(seed.seed_id)
        
        # 找出重复
        duplicates = {h: ids for h, ids in content_hashes.items() if len(ids) > 1}
        
        if duplicates:
            total_dups = sum(len(ids) - 1 for ids in duplicates.values())
            return f"发现{total_dups}个重复内容，可合并"
        
        return "无显著重复"
    
    def _generate_wisdom_content(
        self,
        common_pattern: str,
        core_insights: List[str],
        redundancy_info: str
    ) -> str:
        """
        生成智慧内容
        
        将多个种子的信息压缩为一条智慧内容。
        """
        lines = [
            "【净化智慧】",
            f"模式: {common_pattern}",
            "---",
            "核心洞见:",
            *[f"- {insight}" for insight in core_insights],
            "---",
            f"冗余处理: {redundancy_info}",
            "---",
            f"净化时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        ]
        return "\n".join(lines)
    
    def _extract_essential_features(self, seeds: List[Seed]) -> List[str]:
        """
        提取必要特征
        
        确定哪些特征必须保留在压缩后。
        """
        features = []
        
        # 类型分布
        types = list(set(s.seed_type.value for s in seeds))
        features.append(f"类型: {types}")
        
        # 权重分布
        weights = sorted(set(round(s.weight, 2) for s in seeds))
        features.append(f"权重: {weights}")
        
        # 纯度范围
        min_purity = min(s.purity for s in seeds)
        max_purity = max(s.purity for s in seeds)
        features.append(f"纯度范围: {min_purity:.2f}-{max_purity:.2f}")
        
        # 关键标签
        all_tags = []
        for seed in seeds:
            all_tags.extend(seed.tags)
        unique_tags = list(set(all_tags))
        if unique_tags:
            features.append(f"关键标签: {unique_tags}")
        
        return features
    
    def _compute_information_retention(
        self,
        seeds: List[Seed],
        compressed_content: str,
        essential_features: List[str]
    ) -> float:
        """
        计算信息保留度
        
        评估压缩后保留了原始信息的多少。
        """
        # 原始信息量
        original_info = sum(len(s.content.encode('utf-8')) for s in seeds)
        
        # 压缩后信息量
        compressed_info = len(compressed_content.encode('utf-8'))
        
        # 必要特征匹配度
        feature_match = 0.0
        for feature in essential_features:
            if feature.lower() in compressed_content.lower():
                feature_match += 1.0
        feature_ratio = feature_match / max(1, len(essential_features))
        
        # 综合信息保留度
        size_ratio = compressed_info / max(1, original_info)
        retention = (size_ratio + feature_ratio) / 2
        
        return min(1.0, retention)
    
    def _generate_reconstruction_paths(self, seeds: List[Seed]) -> List[str]:
        """
        生成重构路径
        
        记录如何从压缩内容重构原始信息。
        """
        paths = []
        
        # 基于来源路径
        for seed in seeds:
            paths.append(f"来源: {seed.source} ({seed.seed_id[:8]})")
        
        # 基于类型路径
        type_groups = defaultdict(list)
        for seed in seeds:
            type_groups[seed.seed_type.value].append(seed.seed_id)
        
        for seed_type, seed_ids in type_groups.items():
            paths.append(f"类型聚合: {seed_type} × {len(seed_ids)}")
        
        return paths[:10]  # 最多10条路径
    
    def compute_wisdom_score(self, seed: Optional[Seed] = None, **kwargs) -> float:
        """
        计算智慧分数
        
        智慧分数 = 压缩比 × 纯度 × 信息保留
        
        高压缩比 + 高纯度 + 高信息保留 = 高智慧
        
        Args:
            seed: 种子对象（可选）
            **kwargs: 直接传入的参数
        
        Returns:
            智慧分数 (0-1)
        """
        if seed is not None:
            compression_ratio = seed.weight  # 使用权重作为压缩比代理
            purity = seed.purity
            information_retention = 0.9  # 假设保留90%
        else:
            compression_ratio = kwargs.get("compression_ratio", 0.5)
            purity = kwargs.get("purity", 0.5)
            information_retention = kwargs.get("information_retention", 0.9)
        
        # 智慧分数计算
        # 压缩比权重：0.4
        # 纯度权重：0.4
        # 信息保留权重：0.2
        wisdom_score = (
            (1 - compression_ratio) * 0.4 +  # 低压缩比=高智慧
            purity * 0.4 +
            information_retention * 0.2
        )
        
        return min(1.0, max(0.0, wisdom_score))
    
    def select_purification_strategy(self, seeds: List[Seed]) -> PurificationStrategy:
        """
        选择净化策略
        
        根据种子特征选择合适的净化深度。
        
        Args:
            seeds: 待净化的种子
        
        Returns:
            净化策略
        """
        if not seeds:
            return PurificationStrategy.LIGHT_RECOMPRESSION
        
        # 计算特征
        avg_purity = sum(s.purity for s in seeds) / len(seeds)
        avg_weight = sum(s.weight for s in seeds) / len(seeds)
        size_variance = self._compute_size_variance(seeds)
        
        # 基于特征选择策略
        if avg_purity > 0.8 and avg_weight > 0.7:
            # 高纯度、高权重 → 深度重编码
            return PurificationStrategy.DEEP_REENCODING
        elif avg_purity > 0.5:
            # 中等纯度 → 中度抽象
            return PurificationStrategy.MEDIUM_ABSTRACTION
        elif size_variance < 0.2:
            # 大小一致 → 轻度压缩
            return PurificationStrategy.LIGHT_RECOMPRESSION
        else:
            # 其他 → 深度重编码提取智慧
            return PurificationStrategy.ULTIMATE_WISDOM
    
    def _compute_size_variance(self, seeds: List[Seed]) -> float:
        """计算种子大小方差"""
        if len(seeds) < 2:
            return 0.0
        
        sizes = [len(s.content.encode('utf-8')) for s in seeds]
        mean = sum(sizes) / len(sizes)
        variance = sum((s - mean) ** 2 for s in sizes) / len(sizes)
        
        return variance / max(1, mean ** 2)  # 归一化方差
    
    def purify_single_seed(self, seed: Seed) -> Tuple[WisdomSeed, PurificationMetrics]:
        """
        净化单个种子
        
        对于单个种子，通过重编码提升压缩比。
        
        Args:
            seed: 待净化的种子
        
        Returns:
            (智慧种子, 净化度量)
        """
        # 单个种子的净化 = 重编码优化
        original_size = len(seed.content.encode('utf-8'))
        
        # 提取核心内容
        core_content = self._extract_core_content(seed)
        compressed_size = len(core_content.encode('utf-8'))
        
        # 计算改进
        original_ratio = 1.0
        new_ratio = compressed_size / max(1, original_size)
        
        # 计算智慧分数
        wisdom_score = self.compute_wisdom_score(
            compression_ratio=new_ratio,
            purity=seed.purity,
            information_retention=0.95
        )
        
        # 创建智慧种子
        wisdom_seed = WisdomSeed(
            seed_id=str(uuid.uuid4()),
            content=core_content,
            source_seed_ids=[seed.seed_id],
            extracted_wisdom=self._identify_common_pattern([seed]),
            core_insights=[f"纯度提升: {seed.purity:.2f} → 0.9"],
            wisdom_score=wisdom_score,
            compression_ratio=new_ratio,
            purity=min(1.0, seed.purity + 0.2),
            reconstruction_paths=[f"重构自: {seed.seed_id}"],
            essential_features=self._extract_essential_features([seed])
        )
        
        # 更新原种子
        seed.status = SeedStatus.PURIFIED
        seed.metadata["purified_at"] = datetime.now().isoformat()
        seed.metadata["wisdom_successor"] = wisdom_seed.seed_id
        self.store.update(seed)
        
        # 创建新种子
        new_seed = Seed.create(
            content=wisdom_seed.content,
            seed_type=SeedType.WISDOM,
            weight=seed.weight,
            purity=wisdom_seed.purity,
            source="purification_v2_single"
        )
        self.store.add(new_seed)
        
        # 记录度量
        metrics = PurificationMetrics(
            original_seed_count=1,
            original_total_size=original_size,
            original_compression_ratio=original_ratio,
            new_seed_count=1,
            new_total_size=compressed_size,
            new_compression_ratio=new_ratio,
            compression_improvement=1 - new_ratio,
            information_retention=0.95,
            wisdom_gain=wisdom_score
        )
        
        self._purification_history.append(metrics)
        
        return wisdom_seed, metrics
    
    def _extract_core_content(self, seed: Seed) -> str:
        """
        提取种子核心内容
        
        通过重编码优化，去除冗余。
        """
        # 简化的重编码
        content = seed.content.strip()
        
        # 添加标记
        lines = [
            f"【智慧种子】{seed.seed_type.value}",
            content,
            f"纯度: {seed.purity:.2f}",
            f"权重: {seed.weight:.2f}",
        ]
        
        return "\n".join(lines)
    
    def get_purification_report(self) -> Dict[str, Any]:
        """
        获取净化报告
        
        汇总净化历史和当前状态。
        
        Returns:
            净化报告
        """
        if not self._purification_history:
            return {
                "status": "no_history",
                "message": "暂无净化历史"
            }
        
        latest = self._purification_history[-1]
        
        # 计算汇总统计
        total_original = sum(m.original_total_size for m in self._purification_history)
        total_new = sum(m.new_total_size for m in self._purification_history)
        total_compression = sum(m.compression_improvement for m in self._purification_history)
        total_wisdom = sum(m.wisdom_gain for m in self._purification_history)
        
        return {
            "status": "success",
            "total_purifications": len(self._purification_history),
            "latest_purification": {
                "compression_improvement": latest.compression_improvement,
                "wisdom_gain": latest.wisdom_gain,
                "information_retention": latest.information_retention
            },
            "cumulative": {
                "original_size": total_original,
                "new_size": total_new,
                "total_savings": total_original - total_new,
                "avg_compression_improvement": total_compression / len(self._purification_history),
                "avg_wisdom_gain": total_wisdom / len(self._purification_history)
            },
            "wisdom_seeds_count": len(self._wisdom_seeds)
        }
    
    def optimize_batch(self, seeds: List[Seed]) -> Dict[str, Any]:
        """
        批量优化
        
        对一批种子进行整体优化。
        
        Args:
            seeds: 待优化的种子
        
        Returns:
            优化结果
        """
        if not seeds:
            return {"status": "no_seeds", "message": "没有种子需要优化"}
        
        # 1. 分组（同类型、同源等）
        groups = self._group_seeds(seeds)
        
        results = {
            "groups_processed": 0,
            "wisdom_seeds_created": [],
            "total_savings": 0,
            "details": []
        }
        
        # 2. 对每个组进行处理
        for group_name, group_seeds in groups.items():
            if len(group_seeds) < 2:
                continue
            
            # 选择策略
            strategy = self.select_purification_strategy(group_seeds)
            
            # 执行净化
            wisdom_seeds, metrics = self.purify_by_recompression(group_seeds)
            
            results["groups_processed"] += 1
            results["wisdom_seeds_created"].extend([w.seed_id for w in wisdom_seeds])
            results["total_savings"] += metrics.original_total_size - metrics.new_total_size
            results["details"].append({
                "group": group_name,
                "strategy": strategy.value,
                "original_count": metrics.original_seed_count,
                "new_count": metrics.new_seed_count,
                "savings": metrics.original_total_size - metrics.new_total_size
            })
        
        return results
    
    def _group_seeds(self, seeds: List[Seed]) -> Dict[str, List[Seed]]:
        """
        种子分组
        
        按类型、来源等分组。
        """
        groups = defaultdict(list)
        
        for seed in seeds:
            # 按类型分组
            groups[f"type_{seed.seed_type.value}"].append(seed)
        
        return dict(groups)
