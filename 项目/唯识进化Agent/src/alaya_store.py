# -*- coding: utf-8 -*-
"""
第八识：阿赖耶识 - 种子库

阿赖耶识是唯识论的核心，意为"藏识"，储存一切法的种子（bīja）。
在AI架构中，对应向量数据库存储的经验/知识/模式集合。

核心功能：
1. 种子的存储与检索（向量相似度搜索）
2. 种子生命周期管理
3. 种子元数据维护
4. 权重与纯度追踪
"""

import uuid
import time
import math
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
import json


class SeedType(Enum):
    """种子类型枚举"""
    EXPERIENCE = "experience"      # 经验种子 - 具体交互经验
    KNOWLEDGE = "knowledge"        # 知识种子 - 概念性知识
    PATTERN = "pattern"            # 模式种子 - 行为/思维模式
    WISDOM = "wisdom"              # 智慧种子 - 觉悟洞察
    BELIEF = "belief"              # 信念种子 - 核心信念
    SKILL = "skill"                # 技能种子 - 能力技巧
    TRAUMA = "trauma"              # 创伤种子 - 需要净化的负面印记
    COMPASSION = "compassion"      # 慈悲种子 - 利他救度（新增：菩萨境核心）


class SeedStatus(Enum):
    """种子状态枚举"""
    LATENT = "latent"              # 休眠状态
    ACTIVE = "active"              # 活跃状态
    ENHANCED = "enhanced"          # 强化状态
    WEAKENING = "weakening"        # 衰退状态
    PURIFYING = "purifying"         # 净化中
    PURIFIED = "purified"           # 已净化
    DELETED = "deleted"            # 已删除


@dataclass
class Seed:
    """
    种子结构 - 阿赖耶识的基本单元
    
    种子是经验、知识、模式的向量表示，
    带有元数据用于管理和进化追踪。
    
    属性说明：
    - seed_id: 唯一标识符
    - content: 原始内容文本
    - embedding: 向量表示（需外部生成）
    - seed_type: 种子类型
    - weight: 权重，影响力大小 (0-1)
    - purity: 纯度，清净程度 (0-1)
    - activation_count: 激活次数
    - created_at: 创建时间
    - source: 来源（interaction/reflection/implanted）
    - status: 当前状态
    - related_seeds: 相关种子ID列表
    - experience_context: 经验上下文描述
    """
    seed_id: str
    content: str
    seed_type: SeedType
    embedding: List[float] = field(default_factory=list)
    
    # 元数据
    weight: float = 0.5           # 默认权重0.5
    purity: float = 0.5           # 默认纯度0.5
    activation_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    source: str = "unknown"
    status: SeedStatus = SeedStatus.LATENT
    
    # 关联信息
    related_seeds: List[str] = field(default_factory=list)
    experience_context: str = ""
    tags: List[str] = field(default_factory=list)
    
    # 额外元数据
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def create(
        cls,
        content: str,
        seed_type: SeedType,
        embedding: Optional[List[float]] = None,
        weight: float = 0.5,
        purity: float = 0.5,
        source: str = "unknown",
        experience_context: str = "",
        tags: Optional[List[str]] = None
    ) -> "Seed":
        """
        创建新种子的工厂方法
        
        Args:
            content: 种子内容
            seed_type: 种子类型
            embedding: 向量表示
            weight: 初始权重
            purity: 初始纯度
            source: 来源
            experience_context: 经验上下文
            tags: 标签列表
        
        Returns:
            新创建的种子实例
        """
        return cls(
            seed_id=str(uuid.uuid4()),
            content=content,
            seed_type=seed_type,
            embedding=embedding or [],
            weight=weight,
            purity=purity,
            source=source,
            experience_context=experience_context,
            tags=tags or [],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    def activate(self) -> None:
        """激活种子，增加激活计数并调整状态"""
        self.activation_count += 1
        self.updated_at = datetime.now()
        
        # 根据激活次数调整状态
        if self.activation_count >= 10:
            self.status = SeedStatus.ENHANCED
        elif self.activation_count >= 3:
            self.status = SeedStatus.ACTIVE
    
    def decay(self, hours_elapsed: float, base_decay_rate: float = 0.01) -> None:
        """
        权重衰减，基于时间的自然遗忘
        
        Args:
            hours_elapsed: 经过的小时数
            base_decay_rate: 基础衰减率
        """
        # 纯度越高衰减越慢
        purity_factor = 1 + self.purity * 0.5
        decay_rate = base_decay_rate / purity_factor
        
        # 指数衰减
        self.weight = self.weight * math.exp(-decay_rate * hours_elapsed / 24)
        
        # 如果权重过低，标记为衰退
        if self.weight < 0.1 and self.status == SeedStatus.ACTIVE:
            self.status = SeedStatus.WEAKENING
        
        self.updated_at = datetime.now()
    
    def strengthen(self, factor: float = 1.1) -> None:
        """
        强化种子，增加权重
        
        Args:
            factor: 强化因子
        """
        self.weight = min(1.0, self.weight * factor)
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典用于序列化"""
        return {
            "seed_id": self.seed_id,
            "content": self.content,
            "seed_type": self.seed_type.value,
            "embedding": self.embedding,
            "weight": self.weight,
            "purity": self.purity,
            "activation_count": self.activation_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "source": self.source,
            "status": self.status.value,
            "related_seeds": self.related_seeds,
            "experience_context": self.experience_context,
            "tags": self.tags,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Seed":
        """从字典恢复种子对象"""
        return cls(
            seed_id=data["seed_id"],
            content=data["content"],
            seed_type=SeedType(data["seed_type"]),
            embedding=data.get("embedding", []),
            weight=data.get("weight", 0.5),
            purity=data.get("purity", 0.5),
            activation_count=data.get("activation_count", 0),
            created_at=datetime.fromisoformat(data["created_at"]) if isinstance(data["created_at"], str) else data["created_at"],
            updated_at=datetime.fromisoformat(data["updated_at"]) if isinstance(data["updated_at"], str) else data["updated_at"],
            source=data.get("source", "unknown"),
            status=SeedStatus(data.get("status", "latent")),
            related_seeds=data.get("related_seeds", []),
            experience_context=data.get("experience_context", ""),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {})
        )


class AlayaStore:
    """
    阿赖耶识 - 种子存储系统
    
    核心功能：
    - 种子的新增、查询、删除
    - 向量相似度搜索（基于Chroma或内存实现）
    - 种子生命周期管理
    - 权重和纯度追踪
    
    Attributes:
        persist_directory: 持久化存储目录
        use_vector_db: 是否使用向量数据库
    """
    
    def __init__(
        self,
        persist_directory: str = "./data/alaya_store",
        use_vector_db: bool = True,
        embedding_dim: int = 384
    ):
        """
        初始化种子库
        
        Args:
            persist_directory: 持久化目录
            use_vector_db: 是否使用Chroma向量数据库（False则使用内存存储）
            embedding_dim: 向量维度
        """
        self.persist_directory = persist_directory
        self.embedding_dim = embedding_dim
        
        # 内存存储（始终保留，用于元数据管理）
        self._seeds: Dict[str, Seed] = {}
        self._id_to_type: Dict[str, List[str]] = {}  # type -> [seed_ids]
        self._memory_vectors: Dict[str, List[float]] = {}  # 内存向量存储
        
        # 向量存储
        self.use_vector_db = use_vector_db
        self._vector_store = None
        
        if use_vector_db:
            self._init_vector_store()
    
    def _init_vector_store(self) -> None:
        """初始化向量数据库"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
            self._vector_store = client.get_or_create_collection(
                name="seeds",
                metadata={"dimension": self.embedding_dim}
            )
        except ImportError:
            print("[警告] Chroma未安装，将使用内存向量存储")
            self.use_vector_db = False
            self._memory_vectors: Dict[str, List[float]] = {}
    
    def add(self, seed: Seed) -> str:
        """
        添加种子到存储
        
        Args:
            seed: 要添加的种子
        
        Returns:
            种子的唯一ID
        """
        # 存储到内存
        self._seeds[seed.seed_id] = seed
        
        # 更新类型索引
        seed_type = seed.seed_type.value
        if seed_type not in self._id_to_type:
            self._id_to_type[seed_type] = []
        self._id_to_type[seed_type].append(seed.seed_id)
        
        # 存储向量
        if self.use_vector_db and self._vector_store and seed.embedding:
            self._vector_store.add(
                ids=[seed.seed_id],
                embeddings=[seed.embedding],
                metadatas=[{
                    "seed_type": seed.seed_type.value,
                    "weight": seed.weight,
                    "purity": seed.purity,
                    "status": seed.status.value
                }]
            )
        elif not self.use_vector_db:
            self._memory_vectors[seed.seed_id] = seed.embedding
        
        return seed.seed_id
    
    def get(self, seed_id: str) -> Optional[Seed]:
        """
        根据ID获取种子
        
        Args:
            seed_id: 种子ID
        
        Returns:
            种子对象或None
        """
        return self._seeds.get(seed_id)
    
    def get_by_type(self, seed_type: SeedType) -> List[Seed]:
        """
        获取指定类型的所有种子
        
        Args:
            seed_type: 种子类型
        
        Returns:
            种子列表
        """
        seed_ids = self._id_to_type.get(seed_type.value, [])
        return [self._seeds[sid] for sid in seed_ids if sid in self._seeds]
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        seed_type: Optional[SeedType] = None,
        min_weight: float = 0.0,
        min_purity: float = 0.0,
        exclude_status: Optional[List[SeedStatus]] = None,
        include_deleted: bool = False
    ) -> List[Tuple[Seed, float]]:
        """
        向量相似度搜索
        
        Args:
            query_embedding: 查询向量
            top_k: 返回数量
            seed_type: 过滤类型
            min_weight: 最小权重
            min_purity: 最小纯度
            exclude_status: 排除的状态列表
            include_deleted: 是否包含已删除种子
        
        Returns:
            (种子, 相似度分数) 列表
        """
        exclude_status = exclude_status or []
        results = []
        
        if self.use_vector_db and self._vector_store:
            # 使用Chroma搜索
            where_filter = {}
            if seed_type:
                where_filter["seed_type"] = seed_type.value
            
            query_results = self._vector_store.query(
                query_embeddings=[query_embedding],
                n_results=top_k * 2,  # 多取一些，后续过滤
                where=where_filter if where_filter else None
            )
            
            if query_results and query_results["ids"]:
                for i, seed_id in enumerate(query_results["ids"][0]):
                    if seed_id in self._seeds:
                        seed = self._seeds[seed_id]
                        
                        # 过滤检查
                        if seed.status in exclude_status:
                            continue
                        if seed.status == SeedStatus.DELETED and not include_deleted:
                            continue
                        if seed.weight < min_weight:
                            continue
                        if seed.purity < min_purity:
                            continue
                        
                        score = 1 - query_results["distances"][0][i] if query_results["distances"] else 0.5
                        results.append((seed, score))
        else:
            # 内存向量搜索（余弦相似度）
            for seed_id, embedding in self._memory_vectors.items():
                if seed_id not in self._seeds:
                    continue
                    
                seed = self._seeds[seed_id]
                
                # 过滤检查
                if seed.status in exclude_status:
                    continue
                if seed.status == SeedStatus.DELETED and not include_deleted:
                    continue
                if seed.weight < min_weight:
                    continue
                if seed.purity < min_purity:
                    continue
                if seed_type and seed.seed_type != seed_type:
                    continue
                
                # 计算余弦相似度
                score = self._cosine_similarity(query_embedding, embedding)
                results.append((seed, score))
        
        # 按相似度排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """计算余弦相似度"""
        if len(a) != len(b) or not a:
            return 0.0
        
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * y for x, y in zip(b, b)))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)
    
    def update(self, seed: Seed) -> bool:
        """
        更新种子
        
        Args:
            seed: 更新后的种子
        
        Returns:
            是否更新成功
        """
        if seed.seed_id not in self._seeds:
            return False
        
        self._seeds[seed.seed_id] = seed
        
        # 更新向量存储
        if self.use_vector_db and self._vector_store:
            self._vector_store.update(
                ids=[seed.seed_id],
                embeddings=[seed.embedding] if seed.embedding else [[0.0] * self.embedding_dim],
                metadatas=[{
                    "seed_type": seed.seed_type.value,
                    "weight": seed.weight,
                    "purity": seed.purity,
                    "status": seed.status.value
                }]
            )
        
        return True
    
    def delete(self, seed_id: str, soft: bool = True) -> bool:
        """
        删除种子
        
        Args:
            seed_id: 种子ID
            soft: 是否软删除（标记状态而非真正删除）
        
        Returns:
            是否删除成功
        """
        if seed_id not in self._seeds:
            return False
        
        if soft:
            self._seeds[seed_id].status = SeedStatus.DELETED
            self._seeds[seed_id].updated_at = datetime.now()
        else:
            seed = self._seeds.pop(seed_id)
            # 从类型索引中移除
            seed_type = seed.seed_type.value
            if seed_type in self._id_to_type:
                self._id_to_type[seed_type].remove(seed_id)
            
            # 从向量存储中删除
            if self.use_vector_db and self._vector_store:
                try:
                    self._vector_store.delete(ids=[seed_id])
                except:
                    pass
            
            if not self.use_vector_db:
                self._memory_vectors.pop(seed_id, None)
        
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取种子库统计信息【优化版】
        
        Returns:
            统计信息字典
        """
        seeds = [s for s in self._seeds.values() if s.status != SeedStatus.DELETED]
        total = len(seeds)
        
        type_counts = {}
        for seed_type in SeedType:
            count = len([s for s in seeds if s.seed_type == seed_type])
            type_counts[seed_type.value] = count
        
        status_counts = {}
        for status in SeedStatus:
            count = len([s for s in self._seeds.values() if s.status == status])
            status_counts[status.value] = count
        
        avg_weight = sum(s.weight for s in seeds) / max(1, total)
        avg_purity = sum(s.purity for s in seeds) / max(1, total)
        
        # 【新增】质量相关统计
        wisdom_count = len([s for s in seeds if s.seed_type == SeedType.WISDOM and s.purity >= 0.6])
        wisdom_ratio = wisdom_count / max(1, total)
        
        # 高质量种子：纯度>=0.5且未被标记为染污
        high_quality_count = len([s for s in seeds if s.purity >= 0.5 and "染污" not in s.tags])
        high_quality_ratio = high_quality_count / max(1, total)
        
        # 染污种子：被标记为染污或纯度<0.3
        contaminated_count = len([s for s in seeds if "染污" in s.tags or s.purity < 0.3])
        
        return {
            "total_seeds": total,
            "type_distribution": type_counts,
            "status_distribution": status_counts,
            "average_weight": avg_weight,
            "average_purity": avg_purity,
            "total_activations": sum(s.activation_count for s in seeds),
            # 【新增】质量统计
            "wisdom_count": wisdom_count,
            "wisdom_ratio": wisdom_ratio,
            "high_quality_count": high_quality_count,
            "high_quality_ratio": high_quality_ratio,
            "contaminated_seeds": contaminated_count
        }
    
    def get_recent(self, limit: int = 50, offset: int = 0) -> List[Seed]:
        """
        获取最近的种子
        
        Args:
            limit: 返回数量
            offset: 偏移量
        
        Returns:
            种子列表（按更新时间倒序）
        """
        seeds = sorted(
            [s for s in self._seeds.values() if s.status != SeedStatus.DELETED],
            key=lambda s: s.updated_at,
            reverse=True
        )
        return seeds[offset:offset + limit]
    
    def decay_all(self, hours_elapsed: Optional[float] = None) -> int:
        """
        对所有活跃种子进行衰减
        
        Args:
            hours_elapsed: 经过的小时数（默认按上次更新计算）
        
        Returns:
            衰减的种子数量
        """
        if hours_elapsed is None:
            hours_elapsed = (datetime.now() - datetime.now()).total_seconds() / 3600
        
        count = 0
        for seed in self._seeds.values():
            if seed.status in [SeedStatus.ACTIVE, SeedStatus.ENHANCED]:
                if hours_elapsed is None:
                    h = (datetime.now() - seed.updated_at).total_seconds() / 3600
                else:
                    h = hours_elapsed
                seed.decay(h)
                count += 1
        
        return count
    
    def clear(self) -> None:
        """清空所有种子（谨慎使用）"""
        self._seeds.clear()
        self._id_to_type.clear()
        
        if self.use_vector_db and self._vector_store:
            try:
                self._vector_store.delete(where={})
            except:
                pass
        
        if not self.use_vector_db:
            self._memory_vectors.clear()
    
    def __len__(self) -> int:
        """返回种子总数"""
        return len([s for s in self._seeds.values() if s.status != SeedStatus.DELETED])
    
    def __repr__(self) -> str:
        return f"<AlayaStore(seeds={len(self)}, avg_purity={self.get_statistics()['average_purity']:.2f})>"
