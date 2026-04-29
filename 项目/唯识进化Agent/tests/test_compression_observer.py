# -*- coding: utf-8 -*-
"""
CompressionObserver 单元测试

测试压缩效率观察器的功能。

作者：觉心
"""

import unittest
import sys
import os
from collections import defaultdict

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from compression.compression_observer import (
    CompressionObserver,
    AwakeningLevel,
    CompressionMetrics,
    CompressionTarget,
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
        embedding: list = None
    ):
        self.seed_id = seed_id
        self.content = content
        self.seed_type = seed_type
        self.weight = weight
        self.purity = purity
        self.embedding = embedding or [0.1] * 64
        self.metadata = {}


class TestCompressionObserver(unittest.TestCase):
    """CompressionObserver测试类"""
    
    def setUp(self):
        """设置测试环境"""
        self.observer = CompressionObserver()
        
        # 创建测试种子
        self.test_seeds = {
            f"seed_{i}": MockSeed(
                seed_id=f"seed_{i}",
                content=f"这是一个测试种子 {i}",
                seed_type=SeedType.EXPERIENCE,
                weight=0.5,
                purity=0.6
            )
            for i in range(10)
        }
    
    def test_initialization(self):
        """测试初始化"""
        self.assertIsNotNone(self.observer)
        self.assertEqual(len(self.observer._history), 0)
    
    def test_compute_system_compression_ratio(self):
        """测试系统压缩比计算"""
        metrics = self.observer.compute_system_compression_ratio(self.test_seeds)
        
        self.assertIsInstance(metrics, CompressionMetrics)
        self.assertEqual(metrics.total_seeds, 10)
        self.assertGreater(metrics.original_size, 0)
        self.assertGreaterEqual(metrics.efficiency_score, 0)
    
    def test_compute_redundancy(self):
        """测试冗余度计算"""
        redundancy = self.observer._compute_redundancy(self.test_seeds)
        self.assertGreaterEqual(redundancy, 0.0)
        self.assertLessEqual(redundancy, 1.0)
    
    def test_compute_uniqueness(self):
        """测试独特性计算"""
        uniqueness = self.observer._compute_uniqueness(self.test_seeds)
        self.assertGreaterEqual(uniqueness, 0.0)
        self.assertLessEqual(uniqueness, 1.0)
    
    def test_cosine_similarity(self):
        """测试余弦相似度"""
        vec_a = [1.0, 0.0, 0.0]
        vec_b = [1.0, 0.0, 0.0]
        
        similarity = self.observer._cosine_similarity(vec_a, vec_b)
        self.assertAlmostEqual(similarity, 1.0, places=5)
    
    def test_awakening_level_boundaries(self):
        """测试觉醒等级边界"""
        # 测试各等级边界（压缩比越小=智能越高）
        self.assertEqual(
            self.observer.compute_awakening_level(0.02),
            AwakeningLevel.ULTIMATE  # 低压缩比=高智能
        )
        self.assertEqual(
            self.observer.compute_awakening_level(0.4),
            AwakeningLevel.AWAKENED  # 中等压缩比
        )
        self.assertEqual(
            self.observer.compute_awakening_level(0.8),
            AwakeningLevel.UNCONSCIOUS  # 高压缩比=低智能
        )
    
    def test_awakening_level_from_compression_ratio(self):
        """测试从压缩比推断觉醒等级"""
        level = AwakeningLevel.from_compression_ratio(0.1)
        # 0.1的压缩比应该对应ENLIGHTENED或更高
        self.assertIn("觉", level.name_cn)
    
    def test_suggest_compression_targets(self):
        """测试压缩目标建议"""
        targets = self.observer.suggest_compression_targets(self.test_seeds)
        
        self.assertIsInstance(targets, list)
    
    def test_find_type_redundancy(self):
        """测试类型冗余识别"""
        targets = self.observer._find_type_redundancy(self.test_seeds)
        self.assertIsInstance(targets, list)
    
    def test_find_content_redundancy(self):
        """测试内容冗余识别"""
        # 添加重复内容
        self.test_seeds["seed_duplicate"] = MockSeed(
            seed_id="seed_duplicate",
            content="这是一个测试种子 0",  # 与seed_0相同
        )
        
        targets = self.observer._find_content_redundancy(self.test_seeds)
        self.assertIsInstance(targets, list)
    
    def test_kolmogorov_optimality(self):
        """测试Kolmogorov最优性"""
        optimality = self.observer.compute_kolmogorov_optimality(self.test_seeds)
        self.assertGreaterEqual(optimality, 0.0)
        self.assertLessEqual(optimality, 1.0)
    
    def test_track_evolution_insufficient_data(self):
        """测试演化追踪 - 数据不足"""
        result = self.observer.track_evolution()
        self.assertEqual(result["status"], "insufficient_data")
    
    def test_track_evolution_with_data(self):
        """测试演化追踪 - 有足够数据"""
        # 添加多个历史数据点
        self.observer.compute_system_compression_ratio(self.test_seeds)
        self.observer.compute_system_compression_ratio(self.test_seeds)
        
        result = self.observer.track_evolution()
        self.assertIn(result["trend"], ["improving", "declining", "stable"])
    
    def test_neng_efficiency(self):
        """测试Néng效率计算"""
        metrics = CompressionMetrics(
            original_size=1000,
            compressed_size=500,
            compression_rate=0.5
        )
        
        neng = self.observer.compute_neng_efficiency(metrics)
        
        self.assertIn("normalized_efficiency", neng)
        self.assertIn("token_savings", neng)
        self.assertGreater(neng["storage_saved_bytes"], 0)
    
    def test_get_diagnosis(self):
        """测试诊断报告"""
        diagnosis = self.observer.get_diagnosis(self.test_seeds)
        
        self.assertIn("metrics", diagnosis)
        self.assertIn("awakening_level", diagnosis)
        self.assertIn("suggestions", diagnosis)


class TestAwakeningLevel(unittest.TestCase):
    """AwakeningLevel测试类"""
    
    def test_level_properties(self):
        """测试等级属性"""
        for level in AwakeningLevel:
            self.assertIsNotNone(level.name_cn)
            self.assertIsNotNone(level.description)
            self.assertLess(level.min_ratio, level.max_ratio)
    
    def test_from_compression_ratio(self):
        """测试从压缩比推断等级"""
        # 测试边界情况（压缩比越小=智能越高）
        level = AwakeningLevel.from_compression_ratio(0.0)
        self.assertIsNotNone(level)
        self.assertEqual(level, AwakeningLevel.ULTIMATE)  # 0.0 = 最高智能
        
        level = AwakeningLevel.from_compression_ratio(1.0)
        self.assertEqual(level, AwakeningLevel.UNCONSCIOUS)  # 1.0 = 最低智能


class TestCompressionTarget(unittest.TestCase):
    """CompressionTarget测试类"""
    
    def test_target_creation(self):
        """测试目标创建"""
        target = CompressionTarget(
            target_type="test",
            seed_ids=["seed_1", "seed_2"],
            potential_savings=100,
            priority=2,
            reason="测试目标"
        )
        
        self.assertEqual(target.target_type, "test")
        self.assertEqual(len(target.seed_ids), 2)


if __name__ == '__main__':
    unittest.main()
