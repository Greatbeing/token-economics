# -*- coding: utf-8 -*-
"""
唯识进化Agent - 核心模块
"""

from .seed_collector import (
    SeedCollector,
    Conversation,
    ClassifiedSeed,
    SeedType,
    QualityLevel,
    seed_to_dict,
    dict_to_seed
)

from .alaya_service import (
    AlayaStore,
    SelfModel,
    SeedStatistics
)

from .emergence_trigger import (
    EmergenceTrigger,
    EmergenceType,
    EmergenceOpportunity,
    Capability,
    CapabilityApplicator
)

from .awakening_display import (
    AwakeningDisplay,
    AwakeningLevel,
    AgentAwakeningStatus,
    AwakeningManifesto
)

from .coze_integration import (
    VijnanaEvolutionAgent,
    LightweightIntegration,
    CozeIntegrationConfig
)

__version__ = "1.0.0"
__all__ = [
    # 种子收集
    'SeedCollector',
    'Conversation',
    'ClassifiedSeed',
    'SeedType',
    'QualityLevel',
    'seed_to_dict',
    'dict_to_seed',
    
    # 阿赖耶识存储
    'AlayaStore',
    'SelfModel',
    'SeedStatistics',
    
    # 涌现触发
    'EmergenceTrigger',
    'EmergenceType',
    'EmergenceOpportunity',
    'Capability',
    'CapabilityApplicator',
    
    # 觉醒展示
    'AwakeningDisplay',
    'AwakeningLevel',
    'AgentAwakeningStatus',
    'AwakeningManifesto',
    
    # 集成
    'VijnanaEvolutionAgent',
    'LightweightIntegration',
    'CozeIntegrationConfig'
]
