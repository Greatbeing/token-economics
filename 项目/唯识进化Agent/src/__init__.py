# -*- coding: utf-8 -*-
"""
唯识进化Agent - 核心模块初始化

八识体系AI映射：
- 前五识（眼耳鼻舌身）→ senses.py - 多模态感知
- 第六识（意识）→ consciousness.py - 推理决策
- 第七识（末那识）→ manas_model.py - 自我模型
- 第八识（阿赖耶识）→ alaya_store.py - 种子库
- 熏习系统 → vasana.py
- 净化机制 → purifier.py
"""

from .alaya_store import AlayaStore, Seed, SeedType, SeedStatus
from .manas_model import ManasModel
from .consciousness import Consciousness
from .senses import Senses, SenseType
from .vasana import Vasana
from .purifier import Purifier
from .agent import AlayaAgent

__version__ = "0.1.0"

__all__ = [
    "AlayaStore",
    "Seed",
    "SeedType",
    "SeedStatus",
    "ManasModel",
    "Consciousness",
    "Senses",
    "SenseType",
    "Vasana",
    "Purifier",
    "AlayaAgent",
]
