# -*- coding: utf-8 -*-
"""
PurifierV2 单元测试

测试净化系统V2的功能。

作者：觉心
"""

import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from compression.purifier_v2 import (
    PurifierV2,
    PurificationStrategy,
    PurificationMetrics,
    WisdomSeed,
)
from src.alaya_store import Seed, SeedType, SeedStatus


class MockSeed:
    """模拟种子用于测试"""
    def __init__(
        self,
        seed_id: str,
        content: str,
        seed_type: SeedType = SeedType.EXPERIENCE,
        weight: float = 0.5,
        purity: float = 0.5,
        source: str = "test",
        tags: list = None
    ):
        self.seed_id = seed_id
        self.content = content
        self.seed_type = seed_type
        self.weight = weight
        self.purity = purity
        self.source = source
        self.tags = tags or []
        self.embedding = [0.1] * 64
        self.status = SeedStatus.ACTIVE
        self.metadata = {}


class MockStore:
    """模拟种子库"""
    def __init__(self):
        self.seeds = {}
    
    def add(self, seed):
        self.seeds[seed.seed_id] = seed
        return seed.seed_id
    
    def get(self, seed_id):
        return self.seeds.get(seed_id)
    
    def update(self, seed):
        self.seeds[seed.seed_id] = seed
        return True
    
    def delete(self, seed_id, soft=True):
        if seed_id in self.seeds:
            if soft:
                self.seeds[seed_id].status = SeedStatus.DELETED
            else:
                del self.seeds[seed_id]
            return True
        return False


class TestPurifierV2(unittest.TestCase):
    """PurifierV2测试类"""
    
    def setUp(self):
        """设置测试环境"""
        self.store = MockStore()
        self.purifier = PurifierV2(self.store)
        
        # 创建测试种子
        self.test_seeds = [
            MockSeed(
                seed_id=f"seed_{i}",
                content=f"机器学习是人工智能的重要分支 {i}",
                seed_type=SeedType.EXPERIENCE,
                weight=0.6,
                purity=0.7
            )
            for i in range(5)
        ]
    
    def test_initialization(self):
        """测试初始化"""
        self.assertIsNotNone(self.purifier)
        self.assertEqual(len(self.purifier._wisdom_seeds), 0)
        
        # 检查默认配置
        self.assertEqual(self.purifier.config["min_wisdom_score"], 0.5)
    
    def test_identify_common_pattern(self):
        """测试共性模式识别"""
        pattern = self.purifier._identify_common_pattern(self.test_seeds)
        self.assertIsNotNone(pattern)
        self.assertIn("机器学习", pattern)
    
    def test_extract_core_insights(self):
        """测试核心洞见提取"""
        insights = self.purifier._extract_core_insights(self.test_seeds)
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
    
    def test_identify_redundancy(self):
        """测试冗余识别"""
        redundancy = self.purifier._identify_redundancy(self.test_seeds)
        self.assertIsInstance(redundancy, str)
    
    def test_generate_wisdom_content(self):
        """测试智慧内容生成"""
        common_pattern = "核心模式"
        core_insights = ["洞见1", "洞见2"]
        redundancy_info = "无重复"
        
        content = self.purifier._generate_wisdom_content(
            common_pattern,
            core_insights,
            redundancy_info
        )
        
        self.assertIsInstance(content, str)
        self.assertIn("净化智慧", content)
        self.assertIn(common_pattern, content)
    
    def test_compute_wisdom_score(self):
        """测试智慧分数计算"""
        # 直接计算
        score = self.purifier.compute_wisdom_score(
            compression_ratio=0.3,
            purity=0.8,
            information_retention=0.9
        )
        
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
        
        # 高质量情况
        high_score = self.purifier.compute_wisdom_score(
            compression_ratio=0.1,  # 低压缩比=高智慧
            purity=1.0,
            information_retention=1.0
        )
        self.assertGreater(high_score, score)
    
    def test_select_purification_strategy(self):
        """测试净化策略选择"""
        # 高纯度种子 → 深度重编码
        high_purity_seeds = [
            MockSeed("1", "内容", purity=0.9, weight=0.8),
            MockSeed("2", "内容", purity=0.9, weight=0.8),
        ]
        strategy = self.purifier.select_purification_strategy(high_purity_seeds)
        self.assertEqual(strategy, PurificationStrategy.DEEP_REENCODING)
        
        # 低纯度种子 → 轻度压缩
        low_purity_seeds = [
            MockSeed("1", "内容", purity=0.3, weight=0.3),
            MockSeed("2", "内容", purity=0.3, weight=0.3),
        ]
        strategy = self.purifier.select_purification_strategy(low_purity_seeds)
        self.assertEqual(strategy, PurificationStrategy.LIGHT_RECOMPRESSION)
    
    def test_compute_size_variance(self):
        """测试大小方差计算"""
        seeds = [
            MockSeed("1", "短"),
            MockSeed("2", "中等长度内容"),
            MockSeed("3", "很长的内容" * 10),
        ]
        
        variance = self.purifier._compute_size_variance(seeds)
        self.assertGreater(variance, 0.0)
    
    def test_purify_by_recompression(self):
        """测试重编码净化"""
        wisdom_seeds, metrics = self.purifier.purify_by_recompression(self.test_seeds)
        
        self.assertEqual(len(wisdom_seeds), 1)
        self.assertIsInstance(wisdom_seeds[0], WisdomSeed)
        self.assertIsInstance(metrics, PurificationMetrics)
        
        # 检查度量
        self.assertEqual(metrics.original_seed_count, 5)
        self.assertEqual(metrics.new_seed_count, 1)
        self.assertLess(metrics.new_total_size, metrics.original_total_size)
    
    def test_purify_single_seed(self):
        """测试单种子净化"""
        seed = self.test_seeds[0]
        
        wisdom_seed, metrics = self.purifier.purify_single_seed(seed)
        
        self.assertIsInstance(wisdom_seed, WisdomSeed)
        self.assertIsInstance(metrics, PurificationMetrics)
        self.assertEqual(metrics.original_seed_count, 1)
    
    def test_extract_core_content(self):
        """测试核心内容提取"""
        seed = self.test_seeds[0]
        core_content = self.purifier._extract_core_content(seed)
        
        self.assertIsInstance(core_content, str)
        self.assertIn("智慧种子", core_content)
    
    def test_group_seeds(self):
        """测试种子分组"""
        groups = self.purifier._group_seeds(self.test_seeds)
        
        self.assertIsInstance(groups, dict)
        self.assertIn("type_experience", groups)
        self.assertEqual(len(groups["type_experience"]), 5)
    
    def test_optimize_batch(self):
        """测试批量优化"""
        result = self.purifier.optimize_batch(self.test_seeds)
        
        self.assertIn("groups_processed", result)
        self.assertIn("wisdom_seeds_created", result)
        self.assertIn("total_savings", result)
    
    def test_get_purification_report(self):
        """测试净化报告"""
        # 先执行一次净化
        self.purifier.purify_by_recompression(self.test_seeds[:3])
        
        report = self.purifier.get_purification_report()
        
        self.assertEqual(report["status"], "success")
        self.assertGreater(report["total_purifications"], 0)
    
    def test_empty_seeds(self):
        """测试空种子处理"""
        wisdom_seeds, metrics = self.purifier.purify_by_recompression([])
        
        self.assertEqual(len(wisdom_seeds), 0)
        self.assertEqual(metrics.original_seed_count, 0)


class TestPurificationStrategy(unittest.TestCase):
    """PurificationStrategy测试类"""
    
    def test_strategy_values(self):
        """测试策略枚举值"""
        self.assertEqual(PurificationStrategy.LIGHT_RECOMPRESSION.value, "light_recompression")
        self.assertEqual(PurificationStrategy.DEEP_REENCODING.value, "deep_reencoding")
        self.assertEqual(PurificationStrategy.ULTIMATE_WISDOM.value, "ultimate_wisdom")


class TestWisdomSeed(unittest.TestCase):
    """WisdomSeed测试类"""
    
    def test_wisdom_seed_creation(self):
        """测试智慧种子创建"""
        wisdom = WisdomSeed(
            seed_id="wisdom_1",
            content="智慧内容",
            source_seed_ids=["seed_1", "seed_2"],
            extracted_wisdom="提取的智慧",
            core_insights=["洞见1"],
            wisdom_score=0.8,
            compression_ratio=0.3,
            purity=0.9,
            reconstruction_paths=["路径1"],
            essential_features=["特征1"]
        )
        
        self.assertEqual(wisdom.seed_id, "wisdom_1")
        self.assertGreater(wisdom.wisdom_score, 0.5)


if __name__ == '__main__':
    unittest.main()
