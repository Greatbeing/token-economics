# -*- coding: utf-8 -*-
"""
压缩模块 - 压缩即智能

基于"压缩即智能"的核心理念，提供完整的压缩算法实现。

子模块：
- alaya_compressor: 阿赖耶识压缩器
- compression_observer: 压缩效率观察器
- purifier_v2: 净化系统V2
- manas_model_v2: 末那识V2

作者：觉心
"""

from .alaya_compressor import (
    AlayaCompressor,
    PatternSignature,
    CompressedSeed,
    SeedUpdate,
    SeedCluster,
)

from .compression_observer import (
    CompressionObserver,
    AwakeningLevel,
    CompressionMetrics,
    CompressionTarget,
)

from .purifier_v2 import (
    PurifierV2,
    PurificationStrategy,
    PurificationMetrics,
    WisdomSeed,
)

from .manas_model_v2 import (
    ManasModelV2,
    TokenCost,
    SelfMaintenanceCost,
    CompressionResult,
)


__all__ = [
    # AlayaCompressor
    "AlayaCompressor",
    "PatternSignature",
    "CompressedSeed",
    "SeedUpdate",
    "SeedCluster",
    
    # CompressionObserver
    "CompressionObserver",
    "AwakeningLevel",
    "CompressionMetrics",
    "CompressionTarget",
    
    # PurifierV2
    "PurifierV2",
    "PurificationStrategy",
    "PurificationMetrics",
    "WisdomSeed",
    
    # ManasModelV2
    "ManasModelV2",
    "TokenCost",
    "SelfMaintenanceCost",
    "CompressionResult",
]
