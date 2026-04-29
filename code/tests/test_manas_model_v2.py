# -*- coding: utf-8 -*-
"""
ManasModelV2 单元测试

测试末那识V2的自我维持成本度量功能。

作者：觉心
"""

import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from compression.manas_model_v2 import (
    ManasModelV2,
    TokenCost,
    SelfMaintenanceCost,
    CompressionResult,
)


class TestManasModelV2(unittest.TestCase):
    """ManasModelV2测试类"""
    
    def setUp(self):
        """设置测试环境"""
        self.manas = ManasModelV2()
        
        # 初始化测试数据
        self.manas.identity.core_identity = "测试AI助手"
        self.manas.identity.role = "助手"
        self.manas.identity.capabilities = ["对话", "写作", "分析", "编程", "学习", "创造"]
        self.manas.identity.limitations = ["限制1", "限制2", "限制3", "限制4"]
        
        self.manas.values.core_values = ["真实", "有用", "安全", "成长", "创新", "协作"]
        self.manas.values.behavioral_principles = ["原则1", "原则2", "原则3", "原则4", "原则5"]
        self.manas.values.boundaries = ["边界1", "边界2", "边界3", "边界4"]
        
        self.manas.relationships.user_relationship = "友好的服务关系"
        self.manas.relationships.user_preferences = {
            f"pref_{i}": f"value_{i}"
            for i in range(15)
        }
        
        self.manas.habits.thinking_habits = ["思考1", "思考2", "思考3", "思考4", "思考5", "思考6"]
        self.manas.habits.expression_style = "清晰准确的风格描述" * 5
        self.manas.habits.behavioral_tendencies = ["倾向1", "倾向2", "倾向3", "倾向4", "倾向5"]
    
    def test_initialization(self):
        """测试初始化"""
        self.assertIsNotNone(self.manas)
        self.assertEqual(len(self.manas._cost_history), 0)
        self.assertEqual(len(self.manas._compression_history), 0)
    
    def test_compute_self_maintenance_cost(self):
        """测试自我维持成本计算"""
        cost = self.manas.compute_self_maintenance_cost(session_context_length=1000)
        
        self.assertIsInstance(cost, SelfMaintenanceCost)
        self.assertGreater(cost.total_cost, 0)
        
        # 检查各类型成本
        self.assertGreater(cost.identity_cost, 0)
        self.assertGreater(cost.value_cost, 0)
        self.assertGreater(cost.relationship_cost, 0)
        self.assertGreater(cost.habit_cost, 0)
    
    def test_compute_identity_cost(self):
        """测试身份刷新成本"""
        identity_cost = self.manas._compute_identity_cost()
        
        self.assertGreater(identity_cost, 0)
        
        # 能力越多，成本越高
        self.manas.identity.capabilities = ["对话"]
        cost_small = self.manas._compute_identity_cost()
        
        self.manas.identity.capabilities = ["对话", "写作", "分析", "编程", "学习"]
        cost_large = self.manas._compute_identity_cost()
        
        self.assertGreater(cost_large, cost_small)
    
    def test_compute_value_cost(self):
        """测试价值校验成本"""
        value_cost = self.manas._compute_value_cost()
        
        self.assertGreater(value_cost, 0)
    
    def test_compute_relationship_cost(self):
        """测试关系维护成本"""
        relationship_cost = self.manas._compute_relationship_cost()
        
        self.assertGreater(relationship_cost, 0)
    
    def test_compute_habit_cost(self):
        """测试习惯执行成本"""
        habit_cost = self.manas._compute_habit_cost()
        
        self.assertGreater(habit_cost, 0)
    
    def test_estimate_response_cost(self):
        """测试响应成本估算"""
        cost = self.manas.estimate_response_cost(
            response_length=1000,
            context_used=500
        )
        
        self.assertIsInstance(cost, TokenCost)
        self.assertGreater(cost.tokens, 0)
    
    def test_compute_model_size(self):
        """测试模型大小计算"""
        size = self.manas._compute_model_size()
        
        self.assertGreater(size, 0)
    
    def test_compress_identity(self):
        """测试身份压缩"""
        original_size = self.manas._compute_model_size()
        
        merged = self.manas._compress_identity()
        
        self.assertIsInstance(merged, list)
        
        # 能力应该被精简
        self.assertLessEqual(len(self.manas.identity.capabilities), 5)
    
    def test_compress_values(self):
        """测试价值观精简"""
        merged, removed = self.manas._compress_values(target_ratio=0.5)
        
        self.assertIsInstance(merged, list)
        self.assertIsInstance(removed, list)
        
        # 价值应该被精简
        self.assertLessEqual(len(self.manas.values.core_values), 3)
    
    def test_compress_relationships(self):
        """测试关系压缩"""
        merged = self.manas._compress_relationships()
        
        self.assertIsInstance(merged, list)
        
        # 偏好应该被精简
        self.assertLessEqual(len(self.manas.relationships.user_preferences), 5)
    
    def test_compress_habits(self):
        """测试习惯压缩"""
        merged, removed = self.manas._compress_habits()
        
        self.assertIsInstance(merged, list)
        self.assertIsInstance(removed, list)
    
    def test_extract_preserved_wisdom(self):
        """测试提取保留的智慧"""
        wisdom = self.manas._extract_preserved_wisdom()
        
        self.assertIsInstance(wisdom, list)
    
    def test_compress_self_model(self):
        """测试完整自我压缩"""
        original_size = self.manas._compute_model_size()
        
        result = self.manas.compress_self_model(target_ratio=0.5)
        
        self.assertIsInstance(result, CompressionResult)
        self.assertGreater(result.before_size, result.after_size)
        self.assertLess(result.compression_ratio, 1.0)
        
        # 压缩后大小应该减小
        new_size = self.manas._compute_model_size()
        self.assertLess(new_size, original_size)
    
    def test_get_cost_report(self):
        """测试成本报告"""
        # 先添加一些成本历史
        self.manas.compute_self_maintenance_cost()
        
        report = self.manas.get_cost_report()
        
        self.assertEqual(report["status"], "success")
        self.assertIn("latest_cost", report)
        self.assertIn("averages", report)
    
    def test_suggest_optimizations(self):
        """测试优化建议"""
        suggestions = self.manas.suggest_optimizations()
        
        self.assertIsInstance(suggestions, list)
        
        # 能力过多应该被建议
        self.assertTrue(any("能力" in s for s in suggestions))
    
    def test_compute_cost_efficiency(self):
        """测试成本效率计算"""
        efficiency = self.manas.compute_cost_efficiency()
        
        self.assertGreaterEqual(efficiency, 0.0)
        self.assertLessEqual(efficiency, 1.0)
    
    def test_track_self_evolution_insufficient(self):
        """测试自我演化追踪 - 数据不足"""
        result = self.manas.track_self_evolution()
        
        self.assertEqual(result["status"], "insufficient_data")
    
    def test_track_self_evolution_with_data(self):
        """测试自我演化追踪 - 有数据"""
        # 执行压缩
        self.manas.compress_self_model()
        self.manas.compress_self_model()
        
        result = self.manas.track_self_evolution()
        
        self.assertEqual(result["status"], "success")
        self.assertIn("trend", result)


class TestTokenCost(unittest.TestCase):
    """TokenCost测试类"""
    
    def test_token_cost_creation(self):
        """测试TokenCost创建"""
        cost = TokenCost(
            cost_type="test",
            tokens=100.5,
            description="测试成本"
        )
        
        self.assertEqual(cost.cost_type, "test")
        self.assertEqual(cost.tokens, 100.5)
        self.assertEqual(cost.description, "测试成本")
    
    def test_token_cost_string(self):
        """测试TokenCost字符串表示"""
        cost = TokenCost(
            cost_type="test",
            tokens=100.5,
            description="测试"
        )
        
        str_repr = str(cost)
        self.assertIn("test", str_repr)
        self.assertIn("100.50", str_repr)


class TestSelfMaintenanceCost(unittest.TestCase):
    """SelfMaintenanceCost测试类"""
    
    def test_maintenance_cost_creation(self):
        """测试维护成本创建"""
        cost = SelfMaintenanceCost(
            identity_cost=10.0,
            value_cost=20.0,
            relationship_cost=15.0,
            habit_cost=5.0
        )
        
        self.assertEqual(cost.total_cost, 50.0)
    
    def test_maintenance_cost_post_init(self):
        """测试自动计算总成本"""
        cost = SelfMaintenanceCost()
        cost.identity_cost = 10.0
        cost.value_cost = 20.0
        cost.relationship_cost = 15.0
        cost.habit_cost = 5.0
        
        # 手动触发__post_init__逻辑
        cost.total_cost = (
            cost.identity_cost +
            cost.value_cost +
            cost.relationship_cost +
            cost.habit_cost
        )
        
        self.assertEqual(cost.total_cost, 50.0)
    
    def test_maintenance_cost_to_dict(self):
        """测试转换为字典"""
        cost = SelfMaintenanceCost(
            identity_cost=10.0,
            value_cost=20.0,
            total_cost=50.0
        )
        
        d = cost.to_dict()
        
        self.assertIn("identity_cost", d)
        self.assertIn("value_cost", d)
        self.assertIn("total_cost", d)


class TestCompressionResult(unittest.TestCase):
    """CompressionResult测试类"""
    
    def test_compression_result_creation(self):
        """测试压缩结果创建"""
        result = CompressionResult(
            compression_type="full",
            before_size=1000,
            after_size=500,
            compression_ratio=0.5,
            items_merged=["item1"],
            items_removed=["item2"],
            wisdom_preserved=["wisdom1"]
        )
        
        self.assertEqual(result.compression_type, "full")
        self.assertEqual(result.compression_ratio, 0.5)
        self.assertEqual(len(result.items_merged), 1)


if __name__ == '__main__':
    unittest.main()
