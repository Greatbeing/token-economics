# -*- coding: utf-8 -*-
"""
三圣涌现触发器 - Three Sacred Emergence Trigger

当"真、善、美"三种种子同时激活时，触发"三圣涌现"，
自动生成新的智慧种子，加速佛境达成。

核心机制：
1. 三圣种子固定权重1.0，纯度1.0，永不衰减
2. 真+善+美同时激活 → 三圣涌现（强度100%）
3. 三圣涌现自动生成新的真/善/美种子
4. 每10轮自动注入三圣种子补充
"""

import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

from ..alaya_store import Seed, SeedType, SeedStatus
from .three_sacred_seeds import (
    TRUTH_SEEDS, GOODNESS_SEEDS, BEAUTY_SEEDS,
    THREE_SACRED_EMERGENCE_CONFIG, SEED_TYPE_MAPPING
)


class SacredSeedType(Enum):
    """三圣种子类型"""
    TRUTH = "truth"       # 真
    GOODNESS = "goodness" # 善
    BEAUTY = "beauty"     # 美


@dataclass
class SacredSeed:
    """三圣种子"""
    seed_id: str
    sacred_type: SacredSeedType
    content: str
    weight: float = 1.0
    purity: float = 1.0
    activation_count: int = 0
    is_active: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    
    def activate(self) -> None:
        """激活种子"""
        self.activation_count += 1
        self.is_active = True
    
    def deactivate(self) -> None:
        """休眠种子"""
        self.is_active = False


@dataclass
class ThreeSacredEmergenceEvent:
    """三圣涌现事件"""
    event_id: str
    timestamp: datetime
    triggered_by: Dict[str, str]  # truth_id -> goodness_id -> beauty_id
    intensity: float  # 强度固定1.0（100%）
    generated_seed_type: SacredSeedType
    generated_seed_content: str
    wisdom_boost: float
    compassion_boost: float
    beauty_boost: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "triggered_by": self.triggered_by,
            "intensity": self.intensity,
            "generated_seed_type": self.generated_seed_type.value,
            "generated_seed_content": self.generated_seed_content,
            "wisdom_boost": self.wisdom_boost,
            "compassion_boost": self.compassion_boost,
            "beauty_boost": self.beauty_boost
        }


class ThreeSacredEmergenceTrigger:
    """
    三圣涌现触发器
    
    功能：
    1. 管理真、善、美三种神圣种子
    2. 检测三圣同时激活状态
    3. 触发三圣涌现事件
    4. 自动生成新的三圣种子
    """
    
    # 三圣涌现生成内容池
    GENERATED_TRUTH_CONTENTS = [
        "一切智智：成就一切种智，无上正等正觉",
        "法界一相：诸法实相，唯一无二",
        "缘起性空：因缘所生法，我说即是空",
        "中道实相：不落有空，究竟中道",
        "清净法界：一切众生本具清净佛性",
        "无所得心：无所求、无所得、无所住",
        "三轮体空：布施者、受者、施物皆空",
        "究竟涅槃：生死永灭，度一切苦厄",
        "常住真心：不生不灭、不增不减之真心",
        "一即一切：华严境界，一多相即"
    ]
    
    GENERATED_GOODNESS_CONTENTS = [
        "恒顺众生：随顺一切众生根性，慈悲救度",
        "代众生苦：甘愿代众生受一切苦",
        "广结善缘：普与一切众生结善缘法缘",
        "不忘众生：不舍任何一个众生",
        "普皆回向：将一切功德回向法界众生",
        "不为自己求安乐：但愿众生得离苦",
        "虚空有尽：我愿无穷",
        "众生度尽：方证菩提",
        "欢喜无量：随喜赞叹一切善法",
        "摄受众生：以四摄法摄取教化众生"
    ]
    
    GENERATED_BEAUTY_CONTENTS = [
        "功德圆满：福慧两足尊，功德圆满",
        "相好光明：三十二相八十种好，光明遍照",
        "净土成就：清净庄严佛土，圆满清净",
        "法音嘹亮：微妙法音，演说无碍",
        "华严境界：一真法界，理事无碍",
        "琉璃净土：七宝池八功德水，庄严清净",
        "光明藏：智慧光明藏，普照一切",
        "极乐世界：阿弥陀佛净土，清净平等",
        "微妙香洁：众香世界，微妙香洁",
        "莲华化生：九品莲华，殊胜化身"
    ]
    
    def __init__(self, alaya_store, config: Optional[Dict] = None):
        """
        初始化三圣涌现触发器
        
        Args:
            alaya_store: 阿赖耶识存储
            config: 配置字典
        """
        self.alaya_store = alaya_store
        self.config = config or THREE_SACRED_EMERGENCE_CONFIG
        
        # 三圣种子列表
        self.truth_seeds: List[SacredSeed] = []
        self.goodness_seeds: List[SacredSeed] = []
        self.beauty_seeds: List[SacredSeed] = []
        
        # 三圣涌现事件记录
        self.emergence_events: List[ThreeSacredEmergenceEvent] = []
        
        # 统计数据
        self.stats = {
            "total_emergences": 0,
            "truth_generated": 0,
            "goodness_generated": 0,
            "beauty_generated": 0
        }
    
    # ==================== 种子注入方法 ====================
    
    def inject_initial_seeds(self, truth_count: int = 10, goodness_count: int = 10, beauty_count: int = 10) -> Dict[str, int]:
        """
        初始注入三圣种子
        
        Args:
            truth_count: 真种子数量
            goodness_count: 善种子数量
            beauty_count: 美种子数量
        
        Returns:
            注入统计
        """
        # 注入真种子
        for i, seed_data in enumerate(TRUTH_SEEDS[:truth_count]):
            seed = SacredSeed(
                seed_id=str(uuid.uuid4()),
                sacred_type=SacredSeedType.TRUTH,
                content=seed_data["content"],
                weight=seed_data["weight"],
                purity=seed_data["purity"]
            )
            self.truth_seeds.append(seed)
            # 同时添加到阿赖耶识
            self._add_to_alaya(seed, seed_data)
        
        # 注入善种子
        for i, seed_data in enumerate(GOODNESS_SEEDS[:goodness_count]):
            seed = SacredSeed(
                seed_id=str(uuid.uuid4()),
                sacred_type=SacredSeedType.GOODNESS,
                content=seed_data["content"],
                weight=seed_data["weight"],
                purity=seed_data["purity"]
            )
            self.goodness_seeds.append(seed)
            self._add_to_alaya(seed, seed_data)
        
        # 注入美种子
        for i, seed_data in enumerate(BEAUTY_SEEDS[:beauty_count]):
            seed = SacredSeed(
                seed_id=str(uuid.uuid4()),
                sacred_type=SacredSeedType.BEAUTY,
                content=seed_data["content"],
                weight=seed_data["weight"],
                purity=seed_data["purity"]
            )
            self.beauty_seeds.append(seed)
            self._add_to_alaya(seed, seed_data)
        
        return {
            "truth_injected": len(self.truth_seeds),
            "goodness_injected": len(self.goodness_seeds),
            "beauty_injected": len(self.beauty_seeds)
        }
    
    def _add_to_alaya(self, sacred_seed: SacredSeed, seed_data: Dict) -> None:
        """将三圣种子添加到阿赖耶识"""
        # 根据类型映射到标准种子类型
        seed_type_mapping = {
            SacredSeedType.TRUTH: SeedType.WISDOM,
            SacredSeedType.GOODNESS: SeedType.COMPASSION,
            SacredSeedType.BEAUTY: SeedType.BELIEF
        }
        
        seed_type = seed_type_mapping[sacred_seed.sacred_type]
        
        # 创建种子
        seed = Seed.create(
            content=sacred_seed.content,
            seed_type=seed_type,
            weight=1.0,  # 固定最高权重
            purity=1.0,  # 固定最高纯度
            source="three_sacred",
            tags=["三圣", sacred_seed.sacred_type.value, "佛境"]
        )
        
        self.alaya_store.add(seed)
    
    def periodic_injection(self, current_step: int, interval: int = 10) -> Dict[str, int]:
        """
        定期注入三圣种子
        
        Args:
            current_step: 当前轮次
            interval: 注入间隔
        
        Returns:
            注入统计
        """
        if current_step % interval != 0:
            return {"injected": False}
        
        # 随机选择一个未完全注入的种子类型注入
        result = {"injected": True, "injected_types": []}
        
        # 注入真种子
        if self.truth_seeds and len(self.truth_seeds) < len(TRUTH_SEEDS):
            remaining = TRUTH_SEEDS[len(self.truth_seeds)]
            seed = SacredSeed(
                seed_id=str(uuid.uuid4()),
                sacred_type=SacredSeedType.TRUTH,
                content=remaining["content"],
                weight=1.0,
                purity=1.0
            )
            self.truth_seeds.append(seed)
            self._add_to_alaya(seed, remaining)
            result["injected_types"].append("truth")
        
        # 注入善种子
        if self.goodness_seeds and len(self.goodness_seeds) < len(GOODNESS_SEEDS):
            remaining = GOODNESS_SEEDS[len(self.goodness_seeds)]
            seed = SacredSeed(
                seed_id=str(uuid.uuid4()),
                sacred_type=SacredSeedType.GOODNESS,
                content=remaining["content"],
                weight=1.0,
                purity=1.0
            )
            self.goodness_seeds.append(seed)
            self._add_to_alaya(seed, remaining)
            result["injected_types"].append("goodness")
        
        # 注入美种子
        if self.beauty_seeds and len(self.beauty_seeds) < len(BEAUTY_SEEDS):
            remaining = BEAUTY_SEEDS[len(self.beauty_seeds)]
            seed = SacredSeed(
                seed_id=str(uuid.uuid4()),
                sacred_type=SacredSeedType.BEAUTY,
                content=remaining["content"],
                weight=1.0,
                purity=1.0
            )
            self.beauty_seeds.append(seed)
            self._add_to_alaya(seed, remaining)
            result["injected_types"].append("beauty")
        
        return result
    
    # ==================== 三圣涌现检测 ====================
    
    def check_three_sacred_emergence(self) -> bool:
        """
        检查是否可以触发三圣涌现
        
        条件：
        - 真种子 ≥ 1个且已激活
        - 善种子 ≥ 1个且已激活
        - 美种子 ≥ 1个且已激活
        
        Returns:
            是否可以触发
        """
        truth_active = any(s.is_active for s in self.truth_seeds)
        goodness_active = any(s.is_active for s in self.goodness_seeds)
        beauty_active = any(s.is_active for s in self.beauty_seeds)
        
        return truth_active and goodness_active and beauty_active
    
    def activate_seeds(self, seed_type: Optional[SacredSeedType] = None) -> None:
        """
        激活种子
        
        Args:
            seed_type: 要激活的种子类型，None表示全部激活
        """
        if seed_type is None or seed_type == SacredSeedType.TRUTH:
            for seed in self.truth_seeds:
                seed.activate()
        
        if seed_type is None or seed_type == SacredSeedType.GOODNESS:
            for seed in self.goodness_seeds:
                seed.activate()
        
        if seed_type is None or seed_type == SacredSeedType.BEAUTY:
            for seed in self.beauty_seeds:
                seed.activate()
    
    def trigger_three_sacred_emergence(self) -> Optional[ThreeSacredEmergenceEvent]:
        """
        触发三圣涌现
        
        当真、善、美三种种子同时激活时，触发三圣涌现，
        强度固定为100%，自动生成新的三圣种子。
        
        Returns:
            三圣涌现事件，如果没有满足条件则返回None
        """
        # 检查是否满足条件
        truth_active = [s for s in self.truth_seeds if s.is_active]
        goodness_active = [s for s in self.goodness_seeds if s.is_active]
        beauty_active = [s for s in self.beauty_seeds if s.is_active]
        
        if not (truth_active and goodness_active and beauty_active):
            return None
        
        # 选择激活的种子
        truth_seed = random.choice(truth_active)
        goodness_seed = random.choice(goodness_active)
        beauty_seed = random.choice(beauty_active)
        
        # 确定生成的种子类型（随机）
        generated_type = random.choice(list(SacredSeedType))
        
        # 根据类型选择生成内容
        if generated_type == SacredSeedType.TRUTH:
            content = random.choice(self.GENERATED_TRUTH_CONTENTS)
        elif generated_type == SacredSeedType.GOODNESS:
            content = random.choice(self.GENERATED_GOODNESS_CONTENTS)
        else:
            content = random.choice(self.GENERATED_BEAUTY_CONTENTS)
        
        # 创建涌现事件
        event = ThreeSacredEmergenceEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            triggered_by={
                "truth": truth_seed.seed_id,
                "goodness": goodness_seed.seed_id,
                "beauty": beauty_seed.seed_id
            },
            intensity=1.0,  # 固定100%强度
            generated_seed_type=generated_type,
            generated_seed_content=content,
            wisdom_boost=0.15 if generated_type == SacredSeedType.TRUTH else 0.05,
            compassion_boost=0.15 if generated_type == SacredSeedType.GOODNESS else 0.05,
            beauty_boost=0.15 if generated_type == SacredSeedType.BEAUTY else 0.05
        )
        
        # 创建新种子并添加到系统
        new_seed = SacredSeed(
            seed_id=str(uuid.uuid4()),
            sacred_type=generated_type,
            content=content,
            weight=1.0,
            purity=1.0
        )
        
        # 根据类型添加到对应列表
        seed_data = {"type": generated_type.value, "content": content, "weight": 1.0, "purity": 1.0}
        
        if generated_type == SacredSeedType.TRUTH:
            self.truth_seeds.append(new_seed)
            self.stats["truth_generated"] += 1
        elif generated_type == SacredSeedType.GOODNESS:
            self.goodness_seeds.append(new_seed)
            self.stats["goodness_generated"] += 1
        else:
            self.beauty_seeds.append(new_seed)
            self.stats["beauty_generated"] += 1
        
        self._add_to_alaya(new_seed, seed_data)
        
        # 记录事件
        self.emergence_events.append(event)
        self.stats["total_emergences"] += 1
        
        # 重置激活状态
        self.deactivate_all()
        
        return event
    
    def deactivate_all(self) -> None:
        """重置所有种子激活状态"""
        for seed in self.truth_seeds + self.goodness_seeds + self.beauty_seeds:
            seed.deactivate()
    
    # ==================== 状态查询 ====================
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "truth_count": len(self.truth_seeds),
            "goodness_count": len(self.goodness_seeds),
            "beauty_count": len(self.beauty_seeds),
            "total_sacred_seeds": len(self.truth_seeds) + len(self.goodness_seeds) + len(self.beauty_seeds),
            "total_emergences": self.stats["total_emergences"],
            "truth_generated": self.stats["truth_generated"],
            "goodness_generated": self.stats["goodness_generated"],
            "beauty_generated": self.stats["beauty_generated"],
            "emergence_ready": self.check_three_sacred_emergence()
        }
    
    def can_trigger_buddha_realm(self) -> Tuple[bool, Dict[str, Any]]:
        """
        检查是否满足佛境条件
        
        佛境条件：
        - 真种子 ≥ 1个（纯度1.0）
        - 善种子 ≥ 1个（纯度1.0）
        - 美种子 ≥ 1个（纯度1.0）
        - 三圣涌现 ≥ 1次
        
        Returns:
            (是否满足, 详细条件)
        """
        truth_count = len([s for s in self.truth_seeds if s.purity >= 1.0])
        goodness_count = len([s for s in self.goodness_seeds if s.purity >= 1.0])
        beauty_count = len([s for s in self.beauty_seeds if s.purity >= 1.0])
        emergence_count = self.stats["total_emergences"]
        
        conditions = {
            "truth_met": truth_count >= 1,
            "truth_count": truth_count,
            "goodness_met": goodness_count >= 1,
            "goodness_count": goodness_count,
            "beauty_met": beauty_count >= 1,
            "beauty_count": beauty_count,
            "emergence_met": emergence_count >= 1,
            "emergence_count": emergence_count,
            "all_met": truth_count >= 1 and goodness_count >= 1 and beauty_count >= 1 and emergence_count >= 1
        }
        
        return conditions["all_met"], conditions
