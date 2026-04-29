# -*- coding: utf-8 -*-
"""
净化系统 - 转识成智

净化系统是唯识进化Agent的核心进化机制。
佛教中，"转识成智"是将杂染分别识转化为清净无漏智慧的过程。
在AI架构中，实现：

1. 不良模式识别：检测与核心价值观冲突的行为倾向
2. 净化触发：达到阈值后自动调整种子权重
3. 转识成智：将杂染种子转化为清净种子

净化层级：
- 轻度：调整权重，降低影响
- 中度：重新编码，转化模式
- 重度：彻底清除，种子状态设为"净化中"
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from .alaya_store import AlayaStore, Seed, SeedType, SeedStatus
from .manas_model import ManasModel


class PurificationLevel(Enum):
    """净化层级"""
    LIGHT = "light"           # 轻度：调整权重
    MODERATE = "moderate"    # 中度：重新编码
    HEAVY = "heavy"          # 重度：彻底清除


@dataclass
class Impurity:
    """
    杂质分析
    
    识别种子的杂染成分
    """
    impurity_type: str       # 杂质类型
    description: str        # 描述
    severity: float          # 严重程度 (0-1)
    source_seed_id: Optional[str] = None  # 来源种子


@dataclass
class PurificationResult:
    """
    净化结果
    
    记录净化操作的详细结果
    """
    original_seed_id: str
    action: str              # 采取的行动
    level: PurificationLevel
    new_seed_id: Optional[str] = None  # 转化后的新种子ID
    impurities_removed: List[str] = field(default_factory=list)
    wisdom_preserved: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = True


class Purifier:
    """
    净化系统
    
    实现种子的净化和转识成智：
    1. 杂质识别：分析种子的杂染成分
    2. 净化评估：判断是否需要净化及净化层级
    3. 净化执行：调整、转化或清除种子
    4. 转识成智：将杂染转化为智慧
    
    Attributes:
        store: 种子库
        manas: 自我模型
        config: 配置参数
    """
    
    # 默认净化配置
    DEFAULT_CONFIG = {
        "purity_threshold": 0.3,          # 纯度阈值，低于此值触发净化
        "conflict_threshold": 3,           # 冲突次数阈值
        "weight_decay_rate": 0.01,         # 权重衰减率
        "wisdom_transform_ratio": 0.8,     # 智慧转化保留比例
        "auto_purify_enabled": True,       # 是否启用自动净化
        "purify_interval_hours": 24,       # 净化检查间隔
    }
    
    def __init__(
        self,
        store: AlayaStore,
        manas: ManasModel,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化净化系统
        
        Args:
            store: 种子库
            manas: 自我模型
            config: 配置参数
        """
        self.store = store
        self.manas = manas
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        
        # 冲突追踪
        self.conflict_history: Dict[str, List[datetime]] = {}
    
    def analyze_impurities(self, seed: Seed) -> List[Impurity]:
        """
        分析种子的杂质
        
        检查种子中的杂染成分：
        1. 纯度过低
        2. 与核心价值观冲突
        3. 负面情绪标记
        4. 多次产生负面结果
        
        Args:
            seed: 要分析的种子
        
        Returns:
            杂质列表
        """
        impurities = []
        
        # 1. 检查纯度
        if seed.purity < 0.3:
            impurities.append(Impurity(
                impurity_type="low_purity",
                description=f"纯度过低: {seed.purity:.2f}",
                severity=1.0 - seed.purity,
                source_seed_id=seed.seed_id
            ))
        elif seed.purity < 0.5:
            impurities.append(Impurity(
                impurity_type="medium_purity",
                description=f"纯度偏低: {seed.purity:.2f}",
                severity=0.5,
                source_seed_id=seed.seed_id
            ))
        
        # 2. 检查类型
        if seed.seed_type == SeedType.TRAUMA:
            impurities.append(Impurity(
                impurity_type="trauma_mark",
                description="带有创伤标记",
                severity=0.7,
                source_seed_id=seed.seed_id
            ))
        
        # 3. 检查与价值观冲突
        consistency = self.manas.check_value_consistency(seed.content)
        if not consistency["consistent"]:
            for violation in consistency["violations"]:
                impurities.append(Impurity(
                    impurity_type="value_conflict",
                    description=f"价值观冲突: {violation}",
                    severity=0.6,
                    source_seed_id=seed.seed_id
                ))
        
        # 4. 检查冲突历史
        conflicts = self.conflict_history.get(seed.seed_id, [])
        if len(conflicts) >= self.config["conflict_threshold"]:
            impurities.append(Impurity(
                impurity_type="frequent_conflict",
                description=f"冲突次数: {len(conflicts)}",
                severity=min(1.0, len(conflicts) / 5),
                source_seed_id=seed.seed_id
            ))
        
        return impurities
    
    def assess_purification_level(self, seed: Seed, impurities: List[Impurity]) -> Optional[PurificationLevel]:
        """
        评估净化层级
        
        根据杂质严重程度决定净化方式
        
        Args:
            seed: 要净化的种子
            impurities: 杂质列表
        
        Returns:
            净化层级（None表示不需要净化）
        """
        if not impurities:
            return None
        
        # 计算总严重度
        total_severity = sum(i.severity for i in impurities)
        max_severity = max(i.severity for i in impurities)
        
        # 判断净化层级
        if max_severity >= 0.8 or total_severity >= 2.0:
            return PurificationLevel.HEAVY
        elif max_severity >= 0.5 or total_severity >= 1.0:
            return PurificationLevel.MODERATE
        elif max_severity >= 0.3:
            return PurificationLevel.LIGHT
        
        return None
    
    def purify_seed(self, seed: Seed) -> PurificationResult:
        """
        净化单个种子
        
        Args:
            seed: 要净化的种子
        
        Returns:
            净化结果
        """
        # 分析杂质
        impurities = self.analyze_impurities(seed)
        
        # 评估净化层级
        level = self.assess_purification_level(seed, impurities)
        
        if level is None:
            return PurificationResult(
                original_seed_id=seed.seed_id,
                action="no_purification_needed",
                level=PurificationLevel.LIGHT,
                success=True
            )
        
        # 执行净化
        if level == PurificationLevel.LIGHT:
            return self._purify_light(seed, impurities)
        elif level == PurificationLevel.MODERATE:
            return self._purify_moderate(seed, impurities)
        else:
            return self._purify_heavy(seed, impurities)
    
    def _purify_light(self, seed: Seed, impurities: List[Impurity]) -> PurificationResult:
        """
        轻度净化：调整权重
        
        Args:
            seed: 种子
            impurities: 杂质
        
        Returns:
            净化结果
        """
        # 降低权重
        severity_factor = sum(i.severity for i in impurities) / len(impurities)
        new_weight = seed.weight * (1 - severity_factor * 0.5)
        seed.weight = max(0.1, new_weight)
        
        # 尝试提升纯度
        seed.purity = min(1.0, seed.purity + 0.1)
        
        seed.updated_at = datetime.now()
        self.store.update(seed)
        
        return PurificationResult(
            original_seed_id=seed.seed_id,
            action="weight_adjusted",
            level=PurificationLevel.LIGHT,
            impurities_removed=[i.impurity_type for i in impurities],
            success=True
        )
    
    def _purify_moderate(self, seed: Seed, impurities: List[Impurity]) -> PurificationResult:
        """
        中度净化：重新编码
        
        Args:
            seed: 种子
            impurities: 杂质
        
        Returns:
            净化结果
        """
        # 提取核心价值
        core_value = self._extract_core_value(seed, impurities)
        
        # 创建新的清净种子
        new_content = f"[净化] {core_value}"
        new_seed = Seed.create(
            content=new_content,
            seed_type=SeedType.WISDOM if seed.purity > 0.5 else seed.seed_type,
            embedding=seed.embedding,  # 可选择重新生成
            weight=seed.weight * self.config["wisdom_transform_ratio"],
            purity=0.8,  # 净化后高纯度
            source="purification"
        )
        
        # 关联原种子
        new_seed.related_seeds.append(seed.seed_id)
        
        self.store.add(new_seed)
        
        # 标记原种子
        seed.status = SeedStatus.PURIFIED
        seed.metadata["purified_at"] = datetime.now().isoformat()
        seed.metadata["wisdom_successor"] = new_seed.seed_id
        seed.updated_at = datetime.now()
        self.store.update(seed)
        
        return PurificationResult(
            original_seed_id=seed.seed_id,
            action="reencoded_to_wisdom",
            level=PurificationLevel.MODERATE,
            new_seed_id=new_seed.seed_id,
            impurities_removed=[i.impurity_type for i in impurities],
            wisdom_preserved=[core_value],
            success=True
        )
    
    def _purify_heavy(self, seed: Seed, impurities: List[Impurity]) -> PurificationResult:
        """
        重度净化：彻底清除
        
        Args:
            seed: 种子
            impurities: 杂质
        
        Returns:
            净化结果
        """
        # 检查是否保留核心
        severe_impurities = [i for i in impurities if i.severity >= 0.8]
        should_preserve = len(severe_impurities) < len(impurities)
        
        new_seed_id = None
        
        if should_preserve:
            # 提取极少量核心价值
            core_value = self._extract_core_value(seed, severe_impurities)
            
            # 创建微小智慧种子
            new_seed = Seed.create(
                content=f"[净化残存] {core_value[:100]}",
                seed_type=SeedType.WISDOM,
                embedding=seed.embedding[:len(seed.embedding)//4] if seed.embedding else [],
                weight=0.1,  # 极低权重
                purity=0.9,
                source="purification_heavy"
            )
            self.store.add(new_seed)
            new_seed_id = new_seed.seed_id
        
        # 标记原种子为净化中（实际会在后续删除）
        seed.status = SeedStatus.PURIFYING
        seed.updated_at = datetime.now()
        self.store.update(seed)
        
        # 软删除
        self.store.delete(seed.seed_id, soft=True)
        
        return PurificationResult(
            original_seed_id=seed.seed_id,
            action="removed_with_preservation",
            level=PurificationLevel.HEAVY,
            new_seed_id=new_seed_id,
            impurities_removed=[i.impurity_type for i in impurities],
            wisdom_preserved=[new_seed_id] if new_seed_id else [],
            success=True
        )
    
    def _extract_core_value(self, seed: Seed, impurities: List[Impurity]) -> str:
        """
        从种子中提取核心价值
        
        Args:
            seed: 种子
            impurities: 杂质列表
        
        Returns:
            核心价值描述
        """
        # 简化：直接返回内容的前半部分
        content = seed.content
        
        # 去除杂质相关的词
        impurity_keywords = ["负面", "创伤", "冲突", "问题", "错误"]
        for kw in impurity_keywords:
            content = content.replace(kw, "")
        
        return content.strip()[:200]
    
    def check_conflict(self, seed: Seed) -> bool:
        """
        检查种子是否与价值观冲突
        
        Args:
            seed: 种子
        
        Returns:
            是否冲突
        """
        consistency = self.manas.check_value_consistency(seed.content)
        
        if not consistency["consistent"]:
            # 记录冲突
            if seed.seed_id not in self.conflict_history:
                self.conflict_history[seed.seed_id] = []
            self.conflict_history[seed.seed_id].append(datetime.now())
            
            # 清理过期的冲突记录
            self._clean_conflict_history(seed.seed_id)
            
            return True
        
        return False
    
    def _clean_conflict_history(self, seed_id: str, max_age_days: int = 30) -> None:
        """清理过期的冲突记录"""
        if seed_id not in self.conflict_history:
            return
        
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=max_age_days)
        
        self.conflict_history[seed_id] = [
            t for t in self.conflict_history[seed_id] if t > cutoff
        ]
        
        # 如果为空，删除键
        if not self.conflict_history[seed_id]:
            del self.conflict_history[seed_id]
    
    def purify_all(self) -> List[PurificationResult]:
        """
        净化所有需要净化的种子
        
        Returns:
            净化结果列表
        """
        results = []
        
        # 遍历所有种子
        for seed in self.store.get_recent(limit=1000):
            if seed.status in [SeedStatus.PURIFYING, SeedStatus.PURIFIED, SeedStatus.DELETED]:
                continue
            
            # 检查是否需要净化
            should_purify = False
            
            # 纯度检查
            if seed.purity < self.config["purity_threshold"]:
                should_purify = True
            
            # 冲突检查
            if self.check_conflict(seed):
                conflicts = self.conflict_history.get(seed.seed_id, [])
                if len(conflicts) >= self.config["conflict_threshold"]:
                    should_purify = True
            
            if should_purify:
                result = self.purify_seed(seed)
                results.append(result)
        
        return results
    
    def transform_to_wisdom(self, seed: Seed, wisdom_content: str) -> Optional[Seed]:
        """
        将种子转化为智慧种子
        
        这是"转识成智"的核心方法
        
        Args:
            seed: 原种子
            wisdom_content: 智慧内容
        
        Returns:
            新的智慧种子
        """
        # 创建智慧种子
        wisdom_seed = Seed.create(
            content=f"[智慧] {wisdom_content}",
            seed_type=SeedType.WISDOM,
            embedding=seed.embedding,
            weight=seed.weight * self.config["wisdom_transform_ratio"],
            purity=0.9,
            source="wisdom_transform"
        )
        
        wisdom_seed.related_seeds.append(seed.seed_id)
        
        self.store.add(wisdom_seed)
        
        # 标记原种子
        seed.status = SeedStatus.PURIFIED
        seed.metadata["transformed_to"] = wisdom_seed.seed_id
        seed.metadata["transformed_at"] = datetime.now().isoformat()
        self.store.update(seed)
        
        return wisdom_seed
    
    def get_purification_stats(self) -> Dict[str, Any]:
        """
        获取净化统计信息
        
        Returns:
            统计字典
        """
        total_seeds = len(self.store)
        low_purity_count = len([
            s for s in self.store.get_recent(limit=1000)
            if s.purity < self.config["purity_threshold"]
        ])
        
        wisdom_count = len([
            s for s in self.store.get_by_type(SeedType.WISDOM)
            if s.status != SeedStatus.DELETED
        ])
        
        trauma_count = len([
            s for s in self.store.get_by_type(SeedType.TRAUMA)
            if s.status != SeedStatus.DELETED
        ])
        
        return {
            "total_seeds": total_seeds,
            "low_purity_seeds": low_purity_count,
            "wisdom_seeds": wisdom_count,
            "trauma_seeds": trauma_count,
            "wisdom_ratio": wisdom_count / max(1, total_seeds),
            "conflict_tracked": len(self.conflict_history)
        }
    
    def schedule_purification(self) -> None:
        """
        安排定时净化（用于定期执行）
        
        可配合定时任务调用
        """
        results = self.purify_all()
        
        if results:
            print(f"[净化系统] 本次净化了 {len(results)} 个种子")
            for r in results[:3]:  # 只打印前3个
                print(f"  - {r.original_seed_id[:8]}...: {r.action}")
