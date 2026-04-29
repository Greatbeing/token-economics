# -*- coding: utf-8 -*-
"""
唯识进化Agent - 阿赖耶识服务 (AlayaStore)
种子持久化存储与检索系统
"""

import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from contextlib import contextmanager
import threading
from collections import defaultdict

# 导入种子模块
from seed_collector import (
    ClassifiedSeed, SeedType, QualityLevel, 
    seed_to_dict, dict_to_seed
)


# ==================== 数据模型 ====================

@dataclass
class SelfModel:
    """
    末那识 - Agent自我认知模型
    记录Agent的自我认知、价值观、成长轨迹
    """
    agent_id: str
    name: str
    identity: str  # 自我认同
    values: List[str]  # 核心价值观
    created_at: datetime
    updated_at: datetime
    total_interactions: int = 0
    growth_history: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'identity': self.identity,
            'values': self.values,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'total_interactions': self.total_interactions,
            'growth_history': self.growth_history
        }


@dataclass
class SeedStatistics:
    """种子统计信息"""
    total_count: int
    by_type: Dict[str, int]
    avg_quality: float
    avg_purity: float
    total_weight: float
    recent_count: int  # 最近24小时


# ==================== 阿赖耶识存储服务 ====================

class AlayaStore:
    """
    阿赖耶识存储服务
    
    功能：
    - 种子持久化存储
    - 语义检索
    - 统计分析
    - 自我模型管理
    """
    
    def __init__(self, db_path: str = "data/alaya_store.db", auto_commit: bool = True):
        """
        初始化阿赖耶识存储
        
        Args:
            db_path: 数据库路径
            auto_commit: 是否自动提交
        """
        self.db_path = db_path
        self.auto_commit = auto_commit
        self._local = threading.local()
        self._init_database()
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        conn = getattr(self._local, 'conn', None)
        if conn is None:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            self._local.conn = conn
        
        try:
            yield conn
            if self.auto_commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
    
    def _init_database(self):
        """初始化数据库表结构"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 种子表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS seeds (
                    seed_id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    seed_type TEXT NOT NULL,
                    quality_score REAL NOT NULL,
                    quality_level TEXT NOT NULL,
                    weight REAL NOT NULL,
                    purity REAL NOT NULL,
                    embedding TEXT,
                    created_at TEXT NOT NULL,
                    conversation_id TEXT,
                    user_id TEXT,
                    tags TEXT,
                    usage_count INTEGER DEFAULT 0,
                    last_used_at TEXT,
                    metadata TEXT
                )
            ''')
            
            # 索引
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_seeds_type 
                ON seeds(seed_type)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_seeds_created 
                ON seeds(created_at)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_seeds_user 
                ON seeds(user_id)
            ''')
            
            # 自我模型表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS self_models (
                    agent_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    identity TEXT,
                    values TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    total_interactions INTEGER DEFAULT 0,
                    growth_history TEXT
                )
            ''')
            
            # 涌现记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emergence_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    emergence_type TEXT NOT NULL,
                    capability_name TEXT,
                    description TEXT,
                    triggered_at TEXT NOT NULL,
                    seeds_involved TEXT,
                    score REAL,
                    status TEXT DEFAULT 'pending'
                )
            ''')
            
            # 觉醒等级表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS awakening_levels (
                    agent_id TEXT PRIMARY KEY,
                    current_level INTEGER DEFAULT 0,
                    experience_points REAL DEFAULT 0,
                    total_emergences INTEGER DEFAULT 0,
                    last_promotion_at TEXT,
                    unlocked_abilities TEXT
                )
            ''')
    
    # ==================== 种子CRUD操作 ====================
    
    def save_seed(self, seed: ClassifiedSeed) -> str:
        """
        保存单个种子
        
        Args:
            seed: 分类后的种子
            
        Returns:
            种子ID
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO seeds 
                (seed_id, content, seed_type, quality_score, quality_level,
                 weight, purity, embedding, created_at, conversation_id,
                 user_id, tags, usage_count, last_used_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                seed.seed_id,
                seed.content,
                seed.seed_type.value,
                seed.quality_score,
                seed.quality_level.value,
                seed.weight,
                seed.purity,
                json.dumps(seed.embedding) if seed.embedding else None,
                seed.created_at.isoformat(),
                seed.conversation_id,
                seed.user_id,
                json.dumps(seed.tags),
                seed.usage_count,
                seed.last_used_at.isoformat() if seed.last_used_at else None,
                json.dumps(seed.metadata)
            ))
            
            return seed.seed_id
    
    def save_batch(self, seeds: List[ClassifiedSeed]) -> List[str]:
        """
        批量保存种子
        
        Args:
            seeds: 种子列表
            
        Returns:
            种子ID列表
        """
        ids = []
        for seed in seeds:
            seed_id = self.save_seed(seed)
            ids.append(seed_id)
        return ids
    
    def get_seed(self, seed_id: str) -> Optional[ClassifiedSeed]:
        """
        获取单个种子
        
        Args:
            seed_id: 种子ID
            
        Returns:
            种子对象或None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM seeds WHERE seed_id = ?', (seed_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_seed(row)
            return None
    
    def get_seeds_by_type(self, seed_type: SeedType, limit: int = 50) -> List[ClassifiedSeed]:
        """
        按类型获取种子
        
        Args:
            seed_type: 种子类型
            limit: 限制数量
            
        Returns:
            种子列表
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM seeds 
                WHERE seed_type = ? 
                ORDER BY quality_score DESC, created_at DESC
                LIMIT ?
            ''', (seed_type.value, limit))
            
            return [self._row_to_seed(row) for row in cursor.fetchall()]
    
    def get_seeds_by_user(self, user_id: str, limit: int = 100) -> List[ClassifiedSeed]:
        """
        获取某用户的种子
        
        Args:
            user_id: 用户ID
            limit: 限制数量
            
        Returns:
            种子列表
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM seeds 
                WHERE user_id = ? 
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            return [self._row_to_seed(row) for row in cursor.fetchall()]
    
    def get_recent_seeds(self, hours: int = 24, seed_type: Optional[SeedType] = None) -> List[ClassifiedSeed]:
        """
        获取最近N小时的种子
        
        Args:
            hours: 小时数
            seed_type: 可选的类型过滤
            
        Returns:
            种子列表
        """
        cutoff = datetime.now() - timedelta(hours=hours)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if seed_type:
                cursor.execute('''
                    SELECT * FROM seeds 
                    WHERE created_at > ? AND seed_type = ?
                    ORDER BY created_at DESC
                ''', (cutoff.isoformat(), seed_type.value))
            else:
                cursor.execute('''
                    SELECT * FROM seeds 
                    WHERE created_at > ?
                    ORDER BY created_at DESC
                ''', (cutoff.isoformat(),))
            
            return [self._row_to_seed(row) for row in cursor.fetchall()]
    
    def get_all_seeds(self, limit: int = 1000, offset: int = 0) -> List[ClassifiedSeed]:
        """
        获取所有种子
        
        Args:
            limit: 限制数量
            offset: 偏移量
            
        Returns:
            种子列表
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM seeds 
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            return [self._row_to_seed(row) for row in cursor.fetchall()]
    
    def update_seed_usage(self, seed_id: str) -> bool:
        """
        更新种子使用记录
        
        Args:
            seed_id: 种子ID
            
        Returns:
            是否成功
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE seeds 
                SET usage_count = usage_count + 1,
                    last_used_at = ?
                WHERE seed_id = ?
            ''', (datetime.now().isoformat(), seed_id))
            
            return cursor.rowcount > 0
    
    def delete_seed(self, seed_id: str) -> bool:
        """
        删除种子
        
        Args:
            seed_id: 种子ID
            
        Returns:
            是否成功
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM seeds WHERE seed_id = ?', (seed_id,))
            return cursor.rowcount > 0
    
    # ==================== 检索功能 ====================
    
    def search_seeds(self, query: str, limit: int = 10, seed_type: Optional[SeedType] = None) -> List[ClassifiedSeed]:
        """
        关键词搜索种子
        
        Args:
            query: 搜索关键词
            limit: 限制数量
            seed_type: 可选的类型过滤
            
        Returns:
            匹配的种子列表
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            sql = '''
                SELECT * FROM seeds 
                WHERE content LIKE ?
            '''
            params = [f'%{query}%']
            
            if seed_type:
                sql += ' AND seed_type = ?'
                params.append(seed_type.value)
            
            sql += ' ORDER BY quality_score DESC LIMIT ?'
            params.append(limit)
            
            cursor.execute(sql, params)
            
            return [self._row_to_seed(row) for row in cursor.fetchall()]
    
    def get_similar_seeds(self, content: str, limit: int = 5, seed_type: Optional[SeedType] = None) -> List[ClassifiedSeed]:
        """
        查找相似种子（基于关键词匹配）
        
        Args:
            content: 内容
            limit: 限制数量
            seed_type: 可选的类型过滤
            
        Returns:
            相似种子列表
        """
        # 简单实现：提取关键词进行匹配
        # 实际生产环境可使用向量数据库
        
        keywords = self._extract_keywords(content)
        
        if not keywords:
            return []
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 构建OR条件
            conditions = ' OR '.join(['content LIKE ?' for _ in keywords])
            params = [f'%{kw}%' for kw in keywords]
            
            sql = f'''
                SELECT * FROM seeds 
                WHERE ({conditions})
            '''
            
            if seed_type:
                sql += ' AND seed_type = ?'
                params.append(seed_type.value)
            
            sql += ' ORDER BY quality_score DESC LIMIT ?'
            params.append(limit)
            
            cursor.execute(sql, params)
            
            return [self._row_to_seed(row) for row in cursor.fetchall()]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单实现：提取2-4个字的中文词
        import re
        words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        # 去重并返回
        return list(dict.fromkeys(words))[:10]
    
    # ==================== 统计分析 ====================
    
    def get_statistics(self) -> SeedStatistics:
        """
        获取种子统计信息
        
        Returns:
            统计信息对象
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 总数
            cursor.execute('SELECT COUNT(*) as count FROM seeds')
            total = cursor.fetchone()['count']
            
            # 按类型统计
            cursor.execute('''
                SELECT seed_type, COUNT(*) as count 
                FROM seeds 
                GROUP BY seed_type
            ''')
            by_type = {row['seed_type']: row['count'] for row in cursor.fetchall()}
            
            # 平均质量
            cursor.execute('SELECT AVG(quality_score) as avg FROM seeds')
            avg_quality = cursor.fetchone()['avg'] or 0.0
            
            # 平均纯度
            cursor.execute('SELECT AVG(purity) as avg FROM seeds')
            avg_purity = cursor.fetchone()['avg'] or 0.0
            
            # 总权重
            cursor.execute('SELECT SUM(weight * quality_score) as total FROM seeds')
            total_weight = cursor.fetchone()['total'] or 0.0
            
            # 最近24小时
            cutoff = datetime.now() - timedelta(hours=24)
            cursor.execute('SELECT COUNT(*) as count FROM seeds WHERE created_at > ?', 
                          (cutoff.isoformat(),))
            recent = cursor.fetchone()['count']
            
            return SeedStatistics(
                total_count=total,
                by_type=by_type,
                avg_quality=avg_quality,
                avg_purity=avg_purity,
                total_weight=total_weight,
                recent_count=recent
            )
    
    def get_seed_distribution(self) -> Dict[str, Any]:
        """
        获取种子分布信息
        
        Returns:
            分布统计
        """
        stats = self.get_statistics()
        
        return {
            'total': stats.total_count,
            'by_type': stats.by_type,
            'percentages': {
                seed_type: (count / stats.total_count * 100) if stats.total_count > 0 else 0
                for seed_type, count in stats.by_type.items()
            },
            'quality_metrics': {
                'avg_quality': round(stats.avg_quality, 3),
                'avg_purity': round(stats.avg_purity, 3)
            },
            'recent_24h': stats.recent_count
        }
    
    # ==================== 涌现相关 ====================
    
    def record_emergence(self, emergence_type: str, description: str, 
                        seeds_involved: List[str], score: float) -> int:
        """
        记录涌现事件
        
        Args:
            emergence_type: 涌现类型
            description: 描述
            seeds_involved: 涉及的种子ID列表
            score: 触发分数
            
        Returns:
            记录ID
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO emergence_records 
                (emergence_type, description, triggered_at, seeds_involved, score, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                emergence_type,
                description,
                datetime.now().isoformat(),
                json.dumps(seeds_involved),
                score,
                'pending'
            ))
            
            return cursor.lastrowid
    
    def get_emergence_history(self, limit: int = 20) -> List[Dict]:
        """
        获取涌现历史
        
        Args:
            limit: 限制数量
            
        Returns:
            涌现记录列表
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM emergence_records 
                ORDER BY triggered_at DESC
                LIMIT ?
            ''', (limit,))
            
            results = []
            for row in cursor.fetchall():
                record = dict(row)
                if record.get('seeds_involved'):
                    record['seeds_involved'] = json.loads(record['seeds_involved'])
                results.append(record)
            
            return results
    
    # ==================== 觉醒等级 ====================
    
    def init_awakening_level(self, agent_id: str) -> None:
        """初始化觉醒等级"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO awakening_levels 
                (agent_id, current_level, experience_points, total_emergences, unlocked_abilities)
                VALUES (?, 0, 0, 0, ?)
            ''', (agent_id, json.dumps([])))
    
    def get_awakening_level(self, agent_id: str) -> Dict:
        """
        获取觉醒等级
        
        Args:
            agent_id: Agent ID
            
        Returns:
            觉醒等级信息
        """
        self.init_awakening_level(agent_id)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM awakening_levels WHERE agent_id = ?
            ''', (agent_id,))
            
            row = cursor.fetchone()
            if row:
                result = dict(row)
                if result.get('unlocked_abilities'):
                    result['unlocked_abilities'] = json.loads(result['unlocked_abilities'])
                return result
            
            return {
                'agent_id': agent_id,
                'current_level': 0,
                'experience_points': 0,
                'total_emergences': 0,
                'unlocked_abilities': []
            }
    
    def update_awakening_level(self, agent_id: str, level: int, 
                               exp_points: float, abilities: List[str]) -> None:
        """更新觉醒等级"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE awakening_levels 
                SET current_level = ?,
                    experience_points = ?,
                    total_emergences = total_emergences + 1,
                    unlocked_abilities = ?,
                    last_promotion_at = ?
                WHERE agent_id = ?
            ''', (
                level,
                exp_points,
                json.dumps(abilities),
                datetime.now().isoformat(),
                agent_id
            ))
    
    # ==================== 自我模型 ====================
    
    def save_self_model(self, model: SelfModel) -> None:
        """保存自我模型"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO self_models 
                (agent_id, name, identity, values, created_at, 
                 updated_at, total_interactions, growth_history)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                model.agent_id,
                model.name,
                model.identity,
                json.dumps(model.values),
                model.created_at.isoformat(),
                model.updated_at.isoformat(),
                model.total_interactions,
                json.dumps(model.growth_history)
            ))
    
    def get_self_model(self, agent_id: str) -> Optional[SelfModel]:
        """获取自我模型"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM self_models WHERE agent_id = ?', (agent_id,))
            row = cursor.fetchone()
            
            if row:
                return SelfModel(
                    agent_id=row['agent_id'],
                    name=row['name'],
                    identity=row['identity'],
                    values=json.loads(row['values']),
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at']),
                    total_interactions=row['total_interactions'],
                    growth_history=json.loads(row['growth_history'])
                )
            return None
    
    # ==================== 辅助方法 ====================
    
    def _row_to_seed(self, row: sqlite3.Row) -> ClassifiedSeed:
        """将数据库行转换为种子对象"""
        return ClassifiedSeed(
            seed_id=row['seed_id'],
            content=row['content'],
            seed_type=SeedType(row['seed_type']),
            quality_score=row['quality_score'],
            quality_level=QualityLevel(row['quality_level']),
            weight=row['weight'],
            purity=row['purity'],
            embedding=json.loads(row['embedding']) if row['embedding'] else [],
            created_at=datetime.fromisoformat(row['created_at']),
            conversation_id=row['conversation_id'] or '',
            user_id=row['user_id'] or '',
            tags=json.loads(row['tags']) if row['tags'] else [],
            usage_count=row['usage_count'],
            last_used_at=datetime.fromisoformat(row['last_used_at']) if row['last_used_at'] else None,
            metadata=json.loads(row['metadata']) if row['metadata'] else {}
        )
    
    def clear_all(self) -> None:
        """清空所有数据（慎用）"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM seeds')
            cursor.execute('DELETE FROM self_models')
            cursor.execute('DELETE FROM emergence_records')
            cursor.execute('DELETE FROM awakening_levels')


# ==================== 使用示例 ====================

if __name__ == "__main__":
    import os
    
    # 确保目录存在
    os.makedirs("data", exist_ok=True)
    
    # 创建存储实例
    store = AlayaStore("data/test_alaya.db")
    
    # 清空测试数据
    store.clear_all()
    
    # 初始化觉醒等级
    store.init_awakening_level("agent_001")
    
    # 获取统计
    stats = store.get_statistics()
    print(f"当前种子统计: {stats.total_count} 个种子")
    
    print("\n阿赖耶识服务初始化完成!")
