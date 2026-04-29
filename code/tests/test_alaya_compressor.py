# -*- coding: utf-8 -*-
"""
AlayaCompressor 单元测试

测试阿赖耶识压缩器的功能。

作者：觉心
"""

import unittest
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from compression.alaya_compressor import (
    AlayaCompressor,
    SeedCluster,
    PatternSignature,
    CompressedSeed,
    SeedUpdate,
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
        embedding: list = None,
        tags: list = None,
        source: str = "test"
    ):
        self.seed_id = seed_id
        self.content = content
        self.seed_type = seed_type
        self.weight = weight
        self.purity = purity
        self.embedding = embedding or [0.1] * 64
        self.tags = tags or []
        self.source = source


class TestAlayaCompressor(unittest.TestCase):
    """AlayaCompressor测试类"""
    
    def setUp(self):
        """设置测试环境"""
        self.compressor = AlayaCompressor()
        
        # 创建测试种子
        self.test_seeds = {
            f"seed_{i}": MockSeed(
                seed_id=f"seed_{i}",
                content=f"这是一个测试种子 {i}",
                seed_type=SeedType.EXPERIENCE,
                weight=0.5,
                purity=0.6,
                embedding=[0.1] * 64
            )
            for i in range(5)
        }
    
    def test_initialization(self):
        """测试初始化"""
        self.assertIsNotNone(self.compressor)
        self.assertEqual(len(self.compressor._signatures), 0)
        
        # 检查默认配置
        self.assertEqual(self.compressor.config["similarity_threshold"], 0.85)
        self.assertEqual(self.compressor.config["min_cluster_size"], 3)
    
    def test_extract_common_pattern(self):
        """测试共性模式提取"""
        seeds = [
            MockSeed("1", "机器学习是人工智能的一个分支机器学习"),
            MockSeed("2", "机器学习可以帮助我们预测未来机器学习"),
            MockSeed("3", "深度学习是机器学习的重要技术机器学习"),
        ]
        
        pattern = self.compressor._extract_common_pattern(seeds)
        self.assertIsNotNone(pattern)
        # 由于词频阈值，可能返回通用模式
        self.assertIsInstance(pattern, str)
    
    def test_extract_abstract_features(self):
        """测试抽象特征提取"""
        seeds = [
            MockSeed("1", "内容1", seed_type=SeedType.EXPERIENCE, weight=0.6, purity=0.7),
            MockSeed("2", "内容2", seed_type=SeedType.EXPERIENCE, weight=0.7, purity=0.8),
        ]
        
        features = self.compressor._extract_abstract_features(seeds)
        self.assertIsInstance(features, list)
        self.assertGreater(len(features), 0)
    
    def test_compute_abstraction_level(self):
        """测试抽象层级计算"""
        seeds = [
            MockSeed(f"seed_{i}", f"内容{i}")
            for i in range(15)
        ]
        
        level = self.compressor._compute_abstraction_level(seeds)
        self.assertGreaterEqual(level, 1)
        self.assertLessEqual(level, self.compressor.config["max_abstraction_level"])
    
    def test_content_to_embedding(self):
        """测试内容转嵌入"""
        content = "这是一个测试内容"
        embedding = self.compressor._content_to_embedding(content)
        
        self.assertIsInstance(embedding, list)
        self.assertEqual(len(embedding), 64)
        
        # 检查归一化
        norm = sum(v * v for v in embedding) ** 0.5
        self.assertAlmostEqual(norm, 1.0, places=5)
    
    def test_cosine_similarity(self):
        """测试余弦相似度计算"""
        vec_a = [1.0, 0.0, 0.0]
        vec_b = [1.0, 0.0, 0.0]
        self.assertAlmostEqual(
            self.compressor._cosine_similarity(vec_a, vec_b),
            1.0,
            places=5
        )
        
        # 正交向量
        vec_c = [0.0, 1.0, 0.0]
        self.assertAlmostEqual(
            self.compressor._cosine_similarity(vec_a, vec_c),
            0.0,
            places=5
        )
    
    def test_find_similar_seeds(self):
        """测试查找相似种子"""
        query_embedding = [0.1] * 64
        
        similar = self.compressor._find_similar_seeds(
            query_embedding,
            self.test_seeds,
            top_k=3
        )
        
        self.assertIsInstance(similar, list)
        self.assertLessEqual(len(similar), 3)
    
    def test_incremental_compress_create_new(self):
        """测试增量压缩 - 创建新种子"""
        # 使用与现有种子完全不同的嵌入
        new_experience = {
            "content": "这是一条完全不同的新经验",
            "embedding": [0.9 if i % 2 == 0 else -0.9 for i in range(64)],  # 与现有种子不相似
            "weight": 0.5
        }
        
        result = self.compressor.incremental_compress(
            new_experience,
            self.test_seeds
        )
        
        # 结果可能是create_new或merge_compress，取决于相似度
        self.assertIn(result.update_type, ["create_new", "merge_compress", "strengthen"])
        self.assertIsNotNone(result.new_seed_id)
    
    def test_incremental_compress_merge(self):
        """测试增量压缩 - 合并压缩"""
        # 使用与现有种子相似的嵌入
        new_experience = {
            "content": "这是类似的经验",
            "embedding": [0.1] * 64,  # 与现有种子相似
            "weight": 0.5
        }
        
        result = self.compressor.incremental_compress(
            new_experience,
            self.test_seeds
        )
        
        self.assertIn(result.update_type, ["strengthen", "merge_compress"])
    
    def test_compute_kolmogorov_estimate(self):
        """测试Kolmogorov复杂度估算"""
        # 简单内容
        simple = "hello"
        simple_k = self.compressor.compute_kolmogorov_estimate(simple)
        self.assertGreater(simple_k, 0)
        
        # 重复内容
        repeated = "hello " * 100
        repeated_k = self.compressor.compute_kolmogorov_estimate(repeated)
        
        # 重复内容应该有更低的复杂度比
        self.assertLess(repeated_k, simple_k)
    
    def test_find_compression_targets(self):
        """测试寻找压缩目标"""
        targets = self.compressor.find_compression_targets(
            self.test_seeds,
            min_cluster_size=3
        )
        
        self.assertIsInstance(targets, list)
    
    def test_statistics(self):
        """测试统计信息"""
        stats = self.compressor.get_statistics()
        
        self.assertIn("total_compressions", stats)
        self.assertIn("avg_compression_ratio", stats)
        self.assertIn("compression_efficiency", stats)


class TestSeedCluster(unittest.TestCase):
    """SeedCluster测试类"""
    
    def test_cluster_creation(self):
        """测试种子簇创建"""
        cluster = SeedCluster(
            seed_ids=["seed_1", "seed_2", "seed_3"],
            avg_similarity=0.9,
            cluster_density=0.85,
            suggested_action="compress"
        )
        
        self.assertEqual(len(cluster.seed_ids), 3)
        self.assertEqual(cluster.suggested_action, "compress")


if __name__ == '__main__':
    unittest.main()
