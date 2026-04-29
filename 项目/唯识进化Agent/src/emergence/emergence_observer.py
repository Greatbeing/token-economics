# -*- coding: utf-8 -*-
"""
涌现观测系统 - Emergence Observer

实时监测种子交互、记录涌现事件、计算涌现强度、生成涌现图谱

核心功能：
1. 实时监测种子交互网络
2. 记录涌现事件的完整信息
3. 计算涌现强度指数
4. 生成涌现图谱数据
5. 追踪智慧增长轨迹

Author: 唯识进化Agent团队
"""

import uuid
import json
import math
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict
import logging


class EmergenceType(Enum):
    """涌现类型枚举"""
    INSIGHT = "insight"           # 洞察涌现 - 多个经验种子协同产生新理解
    PATTERN = "pattern"           # 模式涌现 - 多个模式种子协同发现新规律
    WISDOM = "wisdom"             # 智慧涌现 - 跨类型种子协同产生高级智慧
    CREATIVITY = "creativity"     # 创造性涌现 - 产生全新的想法或解决方案
    INTEGRATION = "integration"   # 整合涌现 - 将碎片知识整合为系统理解


@dataclass
class SeedInteraction:
    """种子交互记录"""
    interaction_id: str
    timestamp: datetime
    seed1_id: str
    seed2_id: str
    interaction_type: str  # synergy, cascade, resonance
    strength: float
    result: str  # enhanced, emerged, stable


@dataclass
class EmergenceObservation:
    """涌现观测记录"""
    observation_id: str
    timestamp: datetime
    emergence_type: EmergenceType
    participant_seeds: List[str]
    participant_types: List[str]
    intensity: float
    novelty_score: float  # 创新程度 (0-1)
    impact_score: float   # 影响程度 (0-1)
    description: str
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "observation_id": self.observation_id,
            "timestamp": self.timestamp.isoformat(),
            "emergence_type": self.emergence_type.value,
            "participant_seeds": self.participant_seeds,
            "participant_types": self.participant_types,
            "intensity": self.intensity,
            "novelty_score": self.novelty_score,
            "impact_score": self.impact_score,
            "description": self.description,
            "context": self.context
        }


@dataclass
class NetworkMetrics:
    """网络指标"""
    density: float              # 网络密度
    clustering_coef: float      # 聚类系数
    avg_path_length: float      # 平均路径长度
    connectivity: float        # 连通性
    centrality_distribution: Dict[str, float]  # 中心性分布


class EmergenceObserver:
    """
    涌现观测系统
    
    实时监测和分析种子交互与涌现事件
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化观测系统
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        
        # 观测参数
        self.observation_interval = self.config.get("observation_interval", 1)  # 每N次交互观测一次
        self.interaction_counter = 0
        
        # 交互记录
        self.interactions: List[SeedInteraction] = []
        self.observations: List[EmergenceObservation] = []
        
        # 网络状态
        self.adjacency_matrix: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.seed_interaction_counts: Dict[str, int] = defaultdict(int)
        self.seed_emergence_counts: Dict[str, int] = defaultdict(int)
        
        # 涌现强度追踪
        self.intensity_history: List[float] = []
        self.novelty_history: List[float] = []
        
        # 时间窗口
        self.time_window = self.config.get("time_window", 60)  # 秒
        self.observation_start = datetime.now()
        
        # 日志
        self.logger = logging.getLogger("EmergenceObserver")
        
        # 涌现类型统计
        self.type_stats = {
            EmergenceType.INSIGHT: 0,
            EmergenceType.PATTERN: 0,
            EmergenceType.WISDOM: 0,
            EmergenceType.CREATIVITY: 0,
            EmergenceType.INTEGRATION: 0
        }
    
    def record_interaction(
        self,
        seed1_id: str,
        seed2_id: str,
        interaction_type: str,
        strength: float,
        result: str = "stable"
    ) -> SeedInteraction:
        """
        记录种子交互
        
        Args:
            seed1_id: 种子1 ID
            seed2_id: 种子2 ID
            interaction_type: 交互类型
            strength: 交互强度
            result: 交互结果
        
        Returns:
            交互记录
        """
        self.interaction_counter += 1
        
        interaction = SeedInteraction(
            interaction_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            seed1_id=seed1_id,
            seed2_id=seed2_id,
            interaction_type=interaction_type,
            strength=strength,
            result=result
        )
        
        self.interactions.append(interaction)
        
        # 更新邻接矩阵
        self.adjacency_matrix[seed1_id][seed2_id] = strength
        self.adjacency_matrix[seed2_id][seed1_id] = strength
        
        # 更新交互计数
        self.seed_interaction_counts[seed1_id] += 1
        self.seed_interaction_counts[seed2_id] += 1
        
        # 清理过期记录
        self._cleanup_old_records()
        
        return interaction
    
    def record_emergence(
        self,
        emergence_type: EmergenceType,
        participant_seeds: List[str],
        participant_types: List[str],
        intensity: float,
        description: str,
        context: Optional[Dict[str, Any]] = None
    ) -> EmergenceObservation:
        """
        记录涌现事件
        
        Args:
            emergence_type: 涌现类型
            participant_seeds: 参与种子ID列表
            participant_types: 参与种子类型列表
            intensity: 涌现强度
            description: 描述
            context: 额外上下文
        
        Returns:
            涌现观测记录
        """
        # 计算创新分数（基于参与种子的新颖组合）
        novelty_score = self._calculate_novelty(
            participant_seeds, participant_types
        )
        
        # 计算影响分数（基于参与种子的重要性）
        impact_score = self._calculate_impact(
            participant_seeds, intensity
        )
        
        observation = EmergenceObservation(
            observation_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            emergence_type=emergence_type,
            participant_seeds=participant_seeds,
            participant_types=participant_types,
            intensity=intensity,
            novelty_score=novelty_score,
            impact_score=impact_score,
            description=description,
            context=context or {}
        )
        
        self.observations.append(observation)
        
        # 更新统计
        self.type_stats[emergence_type] += 1
        self.intensity_history.append(intensity)
        self.novelty_history.append(novelty_score)
        
        # 更新种子涌现计数
        for seed_id in participant_seeds:
            self.seed_emergence_counts[seed_id] += 1
        
        self.logger.info(
            f"涌现事件记录: {emergence_type.value} | "
            f"强度={intensity:.2f} | 创新={novelty_score:.2f} | "
            f"参与={len(participant_seeds)}个种子"
        )
        
        return observation
    
    def _calculate_novelty(
        self,
        seed_ids: List[str],
        seed_types: List[str]
    ) -> float:
        """
        计算创新分数
        
        基于种子组合的新颖程度
        """
        if not seed_ids:
            return 0.0
        
        # 1. 类型多样性贡献
        unique_types = len(set(seed_types))
        type_diversity = unique_types / max(1, len(seed_types))
        
        # 2. 历史组合新颖性
        type_key = tuple(sorted(set(seed_types)))
        seen_combinations = set()
        
        for obs in self.observations:
            obs_types = tuple(sorted(set(obs.participant_types)))
            seen_combinations.add(obs_types)
        
        is_new_combination = type_key not in seen_combinations
        combination_novelty = 1.0 if is_new_combination else 0.3
        
        # 3. 参与种子数量（适度规模更有创新性）
        seed_count_factor = min(1.0, len(seed_ids) / 5)
        
        # 综合创新分数
        novelty = (
            type_diversity * 0.3 +
            combination_novelty * 0.5 +
            seed_count_factor * 0.2
        )
        
        return min(1.0, novelty)
    
    def _calculate_impact(
        self,
        seed_ids: List[str],
        intensity: float
    ) -> float:
        """
        计算影响分数
        
        基于参与种子的重要性和涌现强度
        """
        if not seed_ids:
            return 0.0
        
        # 参与种子的平均交互历史
        total_interactions = sum(
            self.seed_interaction_counts.get(sid, 0) for sid in seed_ids
        )
        avg_interactions = total_interactions / len(seed_ids)
        
        # 交互历史因子（有一定交互历史的种子影响更大）
        history_factor = min(1.0, avg_interactions / 10)
        
        # 强度因子
        intensity_factor = intensity
        
        # 规模因子（多个重要种子参与影响更大）
        scale_factor = min(1.0, len(seed_ids) / 4)
        
        impact = (
            history_factor * 0.3 +
            intensity_factor * 0.4 +
            scale_factor * 0.3
        )
        
        return min(1.0, impact)
    
    def _cleanup_old_records(self) -> None:
        """清理过期的记录"""
        cutoff_time = datetime.now() - timedelta(seconds=self.time_window)
        
        # 清理交互记录
        self.interactions = [
            i for i in self.interactions
            if i.timestamp > cutoff_time
        ]
        
        # 清理邻接矩阵（保留有活跃连接的节点）
        active_seeds = set()
        for interaction in self.interactions:
            active_seeds.add(interaction.seed1_id)
            active_seeds.add(interaction.seed2_id)
        
        # 移除不活跃节点
        for seed_id in list(self.adjacency_matrix.keys()):
            if seed_id not in active_seeds:
                del self.adjacency_matrix[seed_id]
    
    def calculate_network_metrics(self) -> NetworkMetrics:
        """
        计算网络指标
        
        Returns:
            网络指标
        """
        # 获取所有节点
        nodes = set()
        for seed1, connections in self.adjacency_matrix.items():
            nodes.add(seed1)
            nodes.add(seed1)  # 确保所有连接的节点也被计算
        
        # 添加有交互但可能没有连接的节点
        for interactions in self.interactions:
            nodes.add(interactions.seed1_id)
            nodes.add(interactions.seed2_id)
        
        nodes = list(nodes)
        n = len(nodes)
        
        if n == 0:
            return NetworkMetrics(
                density=0.0,
                clustering_coef=0.0,
                avg_path_length=0.0,
                connectivity=0.0,
                centrality_distribution={}
            )
        
        # 构建索引映射
        node_index = {node: i for i, node in enumerate(nodes)}
        
        # 1. 网络密度
        edges = sum(
            len(conns) for conns in self.adjacency_matrix.values()
        ) / 2
        max_edges = n * (n - 1) / 2
        density = edges / max_edges if max_edges > 0 else 0.0
        
        # 2. 聚类系数
        clustering_sum = 0.0
        for node in nodes:
            neighbors = list(self.adjacency_matrix.get(node, {}).keys())
            k = len(neighbors)
            if k < 2:
                continue
            
            triangles = 0
            for i, n1 in enumerate(neighbors):
                for n2 in neighbors[i+1:]:
                    if n2 in self.adjacency_matrix.get(n1, {}):
                        triangles += 1
            
            max_triangles = k * (k - 1) / 2
            if max_triangles > 0:
                clustering_sum += triangles / max_triangles
        
        clustering_coef = clustering_sum / n if n > 0 else 0.0
        
        # 3. 平均路径长度（简化计算）
        total_distance = 0.0
        path_count = 0
        for seed1 in nodes:
            for seed2 in nodes:
                if seed1 != seed2:
                    # 简单距离估算
                    dist = 1.0 / max(0.1, self.adjacency_matrix.get(seed1, {}).get(seed2, 0.1))
                    total_distance += dist
                    path_count += 1
        
        avg_path_length = total_distance / path_count if path_count > 0 else float('inf')
        
        # 4. 连通性（基于最大连通分量）
        visited = set()
        components = []
        
        def dfs(node):
            component = set()
            stack = [node]
            while stack:
                n = stack.pop()
                if n in component:
                    continue
                component.add(n)
                for neighbor in self.adjacency_matrix.get(n, {}):
                    if neighbor not in component:
                        stack.append(neighbor)
            return component
        
        for node in nodes:
            if node not in visited:
                component = dfs(node)
                components.append(component)
                visited.update(component)
        
        connectivity = len(max(components, default=set())) / n if n > 0 else 0.0
        
        # 5. 中心性分布（度中心性）
        centrality = {}
        for node in nodes:
            centrality[node] = len(self.adjacency_matrix.get(node, {}))
        
        return NetworkMetrics(
            density=density,
            clustering_coef=clustering_coef,
            avg_path_length=avg_path_length,
            connectivity=connectivity,
            centrality_distribution=centrality
        )
    
    def calculate_emergence_intensity_index(self) -> float:
        """
        计算涌现强度指数
        
        综合考虑：
        1. 近期涌现频率
        2. 涌现强度分布
        3. 创新程度
        4. 网络结构
        
        Returns:
            涌现强度指数 (0-1)
        """
        if not self.observations:
            return 0.0
        
        # 1. 频率因子（最近时间窗口内的涌现次数）
        recent_cutoff = datetime.now() - timedelta(seconds=self.time_window * 2)
        recent_observations = [
            o for o in self.observations
            if o.timestamp > recent_cutoff
        ]
        frequency = len(recent_observations) / max(1, self.time_window)
        frequency_factor = min(1.0, frequency / 0.5)  # 期望每秒0.5次
        
        # 2. 强度分布
        if self.intensity_history:
            avg_intensity = sum(self.intensity_history[-10:]) / min(10, len(self.intensity_history))
            avg_novelty = sum(self.novelty_history[-10:]) / min(10, len(self.novelty_history))
        else:
            avg_intensity = 0.0
            avg_novelty = 0.0
        
        # 3. 网络结构因子
        metrics = self.calculate_network_metrics()
        network_factor = (
            metrics.density * 0.3 +
            metrics.clustering_coef * 0.3 +
            metrics.connectivity * 0.4
        )
        
        # 综合指数
        intensity_index = (
            frequency_factor * 0.2 +
            avg_intensity * 0.3 +
            avg_novelty * 0.2 +
            network_factor * 0.3
        )
        
        return min(1.0, intensity_index)
    
    def get_emergence_graph_data(self) -> Dict[str, Any]:
        """
        获取涌现图谱数据（用于可视化）
        
        Returns:
            图谱数据字典
        """
        # 获取所有节点
        all_seeds = set()
        for interaction in self.interactions:
            all_seeds.add(interaction.seed1_id)
            all_seeds.add(interaction.seed2_id)
        
        for obs in self.observations:
            all_seeds.update(obs.participant_seeds)
        
        # 构建节点列表
        nodes = []
        for seed_id in all_seeds:
            nodes.append({
                "id": seed_id,
                "interaction_count": self.seed_interaction_counts.get(seed_id, 0),
                "emergence_count": self.seed_emergence_counts.get(seed_id, 0),
                "type": "wisdom" if self.seed_emergence_counts.get(seed_id, 0) > 2 else "normal"
            })
        
        # 构建边列表
        edges = []
        seen_edges = set()
        for interaction in self.interactions:
            edge_key = tuple(sorted([interaction.seed1_id, interaction.seed2_id]))
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                edges.append({
                    "source": interaction.seed1_id,
                    "target": interaction.seed2_id,
                    "strength": interaction.strength,
                    "type": interaction.interaction_type
                })
        
        # 涌现节点特殊标记
        for obs in self.observations:
            for node in nodes:
                if node["id"] in obs.participant_seeds:
                    if obs.intensity > 0.7:
                        node["type"] = "emergence_hub"
                    elif obs.intensity > 0.5:
                        node["type"] = "emergence_participant"
        
        return {
            "nodes": nodes,
            "edges": edges,
            "metrics": {
                "density": self.calculate_network_metrics().density,
                "clustering": self.calculate_network_metrics().clustering_coef,
                "connectivity": self.calculate_network_metrics().connectivity
            },
            "emergence_events": [o.to_dict() for o in self.observations[-20:]]
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取观测统计
        
        Returns:
            统计信息字典
        """
        metrics = self.calculate_network_metrics()
        
        return {
            "total_interactions": len(self.interactions),
            "total_emergence_events": len(self.observations),
            "emergence_intensity_index": self.calculate_emergence_intensity_index(),
            "type_distribution": {
                etype.value: count for etype, count in self.type_stats.items()
            },
            "network_metrics": {
                "density": metrics.density,
                "clustering_coef": metrics.clustering_coef,
                "avg_path_length": metrics.avg_path_length,
                "connectivity": metrics.connectivity
            },
            "recent_intensity": (
                sum(self.intensity_history[-5:]) / min(5, len(self.intensity_history))
                if self.intensity_history else 0.0
            ),
            "recent_novelty": (
                sum(self.novelty_history[-5:]) / min(5, len(self.novelty_history))
                if self.novelty_history else 0.0
            ),
            "top_emergence_seeds": sorted(
                self.seed_emergence_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }
    
    def generate_report(self) -> str:
        """
        生成观测报告
        
        Returns:
            报告文本
        """
        stats = self.get_statistics()
        
        report = []
        report.append("=" * 60)
        report.append("           涌现观测系统 - 观测报告")
        report.append("=" * 60)
        report.append(f"\n观测开始时间: {self.observation_start.isoformat()}")
        report.append(f"当前时间: {datetime.now().isoformat()}")
        report.append(f"时间窗口: {self.time_window}秒")
        
        report.append("\n【基础统计】")
        report.append(f"  交互记录数: {stats['total_interactions']}")
        report.append(f"  涌现事件数: {stats['total_emergence_events']}")
        report.append(f"  涌现强度指数: {stats['emergence_intensity_index']:.4f}")
        
        report.append("\n【涌现类型分布】")
        for etype, count in stats['type_distribution'].items():
            report.append(f"  {etype}: {count}")
        
        report.append("\n【网络结构指标】")
        nm = stats['network_metrics']
        report.append(f"  网络密度: {nm['density']:.4f}")
        report.append(f"  聚类系数: {nm['clustering_coef']:.4f}")
        report.append(f"  平均路径长度: {nm['avg_path_length']:.2f}")
        report.append(f"  连通性: {nm['connectivity']:.4f}")
        
        report.append("\n【质量指标】")
        report.append(f"  近期平均强度: {stats['recent_intensity']:.4f}")
        report.append(f"  近期平均创新度: {stats['recent_novelty']:.4f}")
        
        report.append("\n【涌现贡献种子TOP5】")
        for seed_id, count in stats['top_emergence_seeds']:
            report.append(f"  {seed_id[:8]}...: {count}次参与")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)
