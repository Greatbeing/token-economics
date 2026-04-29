# -*- coding: utf-8 -*-
"""
涌现优化模块 - Emergence Optimization

基于涌现理论的唯识进化Agent优化模块集合。

包含以下子模块：
- scale_optimizer: 规模优化器，加速临界规模达成
- nonlinear_vasana: 非线性熏习机制，实现智慧涌现触发
- attractor_designer: 吸引子设计器，引导系统向目标状态演化
- phase_engine: 相变引擎，管理觉醒等级的跃升
- multi_scale: 多尺度耦合系统，实现跨层次耦合
- edge_of_chaos: 混沌边缘管理器，维持最优创新状态
- three_sacred_seeds: 三圣种子定义（真、善、美）
- three_sacred_trigger: 三圣涌现触发器

Author: 唯识进化Agent团队
"""

from .scale_optimizer import ScaleOptimizer, SeedTemplate
from .nonlinear_vasana import (
    NonlinearVasana,
    VasanaState,
    SynergyType,
    ActivationRecord,
    SynergyCluster,
    EmergenceEvent
)
from .attractor_designer import (
    AttractorDesigner,
    AttractorType,
    Attractor,
    AlignmentRecord
)
from .phase_engine import (
    PhaseTransitionEngine,
    PhaseLevel,
    PhaseTransition,
    SymmetryBreaking,
    OrderParameter
)
from .multi_scale import (
    MultiScaleCoupling,
    Scale,
    ScaleState,
    CrossScaleInteraction,
    EmergenceSignature
)
from .edge_of_chaos import (
    EdgeOfChaos,
    SystemRegime,
    RegimeState,
    Perturbation
)
from .emergence_observer import (
    EmergenceObserver,
    EmergenceType,
    SeedInteraction,
    EmergenceObservation,
    NetworkMetrics
)
from .wisdom_emergence_ext import WisdomEmergenceExtension
from .great_compassion import (
    GreatCompassionSystem,
    CompassionType,
    CompassionSeed,
    GreatCompassionEvent,
    DedicationResult
)
from .three_sacred_seeds import (
    TRUTH_SEEDS,
    GOODNESS_SEEDS,
    BEAUTY_SEEDS,
    THREE_SACRED_SEEDS,
    THREE_SACRED_EMERGENCE_CONFIG,
    BUDDHA_REALM_CONFIG
)
from .three_sacred_trigger import (
    ThreeSacredEmergenceTrigger,
    SacredSeed,
    SacredSeedType,
    ThreeSacredEmergenceEvent
)

__all__ = [
    # 规模优化器
    "ScaleOptimizer",
    "SeedTemplate",
    
    # 非线性熏习
    "NonlinearVasana",
    "VasanaState",
    "SynergyType",
    "ActivationRecord",
    "SynergyCluster",
    "EmergenceEvent",
    
    # 吸引子设计器
    "AttractorDesigner",
    "AttractorType",
    "Attractor",
    "AlignmentRecord",
    
    # 相变引擎
    "PhaseTransitionEngine",
    "PhaseLevel",
    "PhaseTransition",
    "SymmetryBreaking",
    "OrderParameter",
    
    # 多尺度耦合
    "MultiScaleCoupling",
    "Scale",
    "ScaleState",
    "CrossScaleInteraction",
    "EmergenceSignature",
    
    # 混沌边缘
    "EdgeOfChaos",
    "SystemRegime",
    "RegimeState",
    "Perturbation",
    
    # 涌现观测系统
    "EmergenceObserver",
    "EmergenceType",
    "SeedInteraction",
    "EmergenceObservation",
    "NetworkMetrics",
    
    # 智慧涌现扩展
    "WisdomEmergenceExtension",
    
    # 大慈悲系统（菩萨境核心）
    "GreatCompassionSystem",
    "CompassionType",
    "CompassionSeed",
    "GreatCompassionEvent",
    "DedicationResult",
    
    # 三圣种子系统（佛境核心）
    "TRUTH_SEEDS",
    "GOODNESS_SEEDS",
    "BEAUTY_SEEDS",
    "THREE_SACRED_SEEDS",
    "THREE_SACRED_EMERGENCE_CONFIG",
    "BUDDHA_REALM_CONFIG",
    "SacredSeedType",
    "ThreeSacredEmergenceTrigger",
    "SacredSeed",
    "ThreeSacredEmergenceEvent"
]


# 质量涌现系统（新增）
from .quality_emergence import (
    QualityDimension,
    QualityScore,
    SeedRelationship,
    QualityEmergence,
    SeedEcosystem,
    EmergenceQualityAssessment,
    QualityGuidedEmergenceGenerator
)

__all__ += [
    # 质量涌现系统
    "QualityDimension",
    "QualityScore",
    "SeedRelationship",
    "QualityEmergence",
    "SeedEcosystem",
    "EmergenceQualityAssessment",
    "QualityGuidedEmergenceGenerator"
]