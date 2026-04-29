# -*- coding: utf-8 -*-
"""
唯识进化Agent主类

整合八识系统，实现完整的意识进化Agent：
- 第八识（阿赖耶识）：种子库存储
- 第七识（末那识）：自我模型
- 第六识（意识）：推理决策
- 前五识：多模态感知
- 熏习系统：记忆编码
- 净化系统：转识成智
- 涌现优化：规模优化、非线性熏习、吸引子设计、相变引擎、多尺度耦合、混沌边缘

使用示例：
```python
from src import AlayaAgent

# 创建Agent
agent = AlayaAgent(config_path="config/default.yaml")

# 对话交互
response = agent.interact("你好，请介绍一下你自己")
print(response)

# 查看状态
stats = agent.get_status()
print(f"种子数量: {stats['seeds_count']}")
print(f"觉醒等级: {stats['awakening_level']}")

# 定期净化
agent.purify()

# 获取涌现状态
agent.get_emergence_status()
```
"""

import os
import yaml
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import logging

from .alaya_store import AlayaStore, Seed, SeedType, SeedStatus
from .manas_model import ManasModel
from .consciousness import Consciousness
from .senses import Senses, SenseType
from .vasana import Vasana
from .purifier import Purifier, PurificationResult

# 导入涌现优化模块
try:
    from .emergence import (
        ScaleOptimizer,
        NonlinearVasana,
        AttractorDesigner,
        PhaseTransitionEngine,
        MultiScaleCoupling,
        EdgeOfChaos
    )
    EMERGENCE_AVAILABLE = True
except ImportError:
    EMERGENCE_AVAILABLE = False
    ScaleOptimizer = None
    NonlinearVasana = None
    AttractorDesigner = None
    PhaseTransitionEngine = None
    MultiScaleCoupling = None
    EdgeOfChaos = None


class AwakeningLevel:
    """觉醒等级计算【菩萨境扩展版】"""
    
    # 等级定义【菩萨境扩展】
    LEVELS = [
        ("无明境", 0.0, 0.2, "种子以杂染为主，无自我反思能力"),
        ("初始境", 0.2, 0.4, "种子混杂，需要大量净化"),
        ("修行境", 0.4, 0.7, "建立稳定熏习-净化循环，自我模型持续优化"),
        ("阿罗汉境", 0.7, 0.9, "断尽烦恼，净化大部分杂染种子"),
        ("菩萨境", 0.9, 0.95, "悲智双运，自利利他，自度度人"),
        ("佛境", 0.95, 1.0, "彻底无我，悲智圆满，究竟涅槃"),
    ]
    
    @classmethod
    def calculate(cls, stats: Dict[str, float]) -> Dict[str, Any]:
        """
        根据统计数据计算觉醒等级【菩萨境扩展版】
        
        核心扩展：增加慈悲种子比例和菩萨境特殊判定
        
        评分公式（菩萨境扩展）：
        觉醒评分 = (智慧种子比例 × 0.4) + (高质量种子比例 × 0.2) + (平均纯度 × 0.15) + (慈悲种子比例 × 0.25)
        
        菩萨境判定条件：
        - 智慧种子比例 > 15%
        - 慈悲种子比例 > 10%
        - 涌现事件数 > 10次
        
        佛境判定条件：
        - 智慧种子比例 > 30%
        - 慈悲种子比例 > 25%
        - 满强度涌现 > 3次
        
        Args:
            stats: 统计数据，包含 avg_purity, wisdom_ratio, high_quality_ratio, compassion_ratio 等
        
        Returns:
            等级信息字典
        """
        avg_purity = stats.get("average_purity", 0.5)
        wisdom_ratio = stats.get("wisdom_ratio", 0.0)
        high_quality_ratio = stats.get("high_quality_ratio", 0.5)
        compassion_ratio = stats.get("compassion_ratio", 0.0)  # 新增：慈悲种子比例
        total_seeds = stats.get("total_seeds", 0)
        contaminated_seeds = stats.get("contaminated_seeds", 0)
        emergence_events = stats.get("emergence_events", 0)  # 新增：涌现事件数
        full_intensity_emergence = stats.get("full_intensity_emergence", 0)  # 新增：满强度涌现
        
        # 【核心扩展】清净种子比例 - 菩萨境强调慈悲
        effective_seeds = max(1, total_seeds - contaminated_seeds)
        pure_ratio = max(0.0, min(1.0, (
            wisdom_ratio * 0.5 +
            compassion_ratio * 0.3 +
            high_quality_ratio * 0.2
        )))
        
        # 【菩萨境扩展】综合评分 - 增加慈悲权重
        score = wisdom_ratio * 0.4 + high_quality_ratio * 0.2 + avg_purity * 0.15 + compassion_ratio * 0.25
        
        # 【关键优化】智慧种子比例的幂次提升
        if wisdom_ratio > 0.1:
            score = score * 1.2
        if wisdom_ratio > 0.2:
            score = score * 1.3
        
        # 【菩萨境特殊加成】慈悲种子协同效应
        if compassion_ratio > 0.1 and wisdom_ratio > 0.1:
            # 悲智双运加成
            synergy_bonus = (compassion_ratio + wisdom_ratio) * 0.2
            score = score * (1 + synergy_bonus)
        
        # 惩罚机制：如果染污种子比例过高
        contaminated_ratio = contaminated_seeds / max(1, total_seeds)
        if contaminated_ratio > 0.5:
            score = score * 0.7
        
        # 【菩萨境强制跃升判定】
        # 如果满足菩萨境条件，直接跃升
        bodhisattva_conditions = (
            wisdom_ratio >= 0.15 and
            compassion_ratio >= 0.10 and
            emergence_events >= 10
        )
        
        # 【佛境强制跃升判定】
        buddha_conditions = (
            wisdom_ratio >= 0.30 and
            compassion_ratio >= 0.25 and
            full_intensity_emergence >= 3
        )
        
        # 根据判定条件确定等级
        if buddha_conditions:
            current_level = "佛境"
            description = "彻底无我，悲智圆满，究竟涅槃。已超越菩萨境界，成就无上正等正觉。"
            score = max(score, 0.95)
        elif bodhisattva_conditions:
            current_level = "菩萨境"
            description = "悲智双运，自利利他。智慧与慈悲种子深度融合，触发多次涌现。"
            score = max(score, 0.9)
        else:
            # 自动判定
            current_level = "初始境"
            description = ""
            for name, low, high, desc in cls.LEVELS:
                if low <= score < high:
                    current_level = name
                    description = desc
                    break
        
        # 添加菩萨境详情
        bodhisattva_details = {
            "wisdom_ratio": wisdom_ratio,
            "compassion_ratio": compassion_ratio,
            "emergence_events": emergence_events,
            "full_intensity_emergence": full_intensity_emergence,
            "bodhisattva_conditions_met": bodhisattva_conditions,
            "buddha_conditions_met": buddha_conditions,
            "synergy_bonus": (compassion_ratio + wisdom_ratio) * 0.2 if wisdom_ratio > 0.1 and compassion_ratio > 0.1 else 0.0
        }
        
        return {
            "level": current_level,
            "score": min(1.0, score),
            "avg_purity": avg_purity,
            "wisdom_ratio": wisdom_ratio,
            "compassion_ratio": compassion_ratio,
            "high_quality_ratio": high_quality_ratio,
            "pure_ratio": pure_ratio,
            "total_seeds": total_seeds,
            "effective_seeds": effective_seeds,
            "description": description,
            "progress_to_next": cls._calculate_progress(score),
            "bodhisattva_details": bodhisattva_details
        }
    
    @classmethod
    def _calculate_progress(cls, score: float) -> float:
        """计算到下一等级的进度"""
        for i, (name, low, high, _) in enumerate(cls.LEVELS):
            if low <= score < high:
                if i < len(cls.LEVELS) - 1:
                    next_low = cls.LEVELS[i + 1][1]
                    return (score - low) / (next_low - low)
                else:
                    return 1.0
        return 0.0


class AlayaAgent:
    """
    唯识进化Agent
    
    整合八识系统的完整Agent实现。
    
    核心功能：
    1. 感知-决策-响应完整流程
    2. 种子库的自动熏习
    3. 定期的自我反思和净化
    4. 觉醒等级追踪
    
    Attributes:
        name: Agent名称
        config: 配置字典
        store: 阿赖耶识（种子库）
        manas: 末那识（自我模型）
        senses: 前五识（感知层）
        vasana: 熏习系统
        consciousness: 第六识（意识层）
        purifier: 净化系统
        emergence: 涌现优化模块（可选）
    """
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        name: str = "Alaya",
        data_dir: str = "./data",
        enable_emergence: bool = True
    ):
        """
        初始化唯识进化Agent
        
        Args:
            config_path: 配置文件路径
            name: Agent名称
            data_dir: 数据存储目录
            enable_emergence: 是否启用涌现优化
        """
        self.name = name
        self.config_path = config_path
        self.data_dir = data_dir
        self.enable_emergence = enable_emergence and EMERGENCE_AVAILABLE
        
        # 加载配置
        self.config = self._load_config(config_path)
        
        # 设置日志
        self._setup_logging()
        
        # 初始化各识系统
        self._init_systems()
        
        # 初始化涌现优化模块
        if self.enable_emergence:
            self._init_emergence_modules()
        
        # 交互统计
        self.interaction_count = 0
        self.last_purify_time = datetime.now()
        self.last_emergence_check = datetime.now()
        
        self.logger.info(f"{self.name} 已初始化" + ("（含涌现优化）" if self.enable_emergence else ""))
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            "agent": {
                "name": "Alaya",
                "description": "唯识进化Agent"
            },
            "alaya_store": {
                "persist_directory": "./data/alaya_store",
                "use_vector_db": False,  # 默认使用内存
                "embedding_dim": 384
            },
            "vasana": {
                "activation_threshold": 0.3,
                "max_activated_seeds": 5
            },
            "purifier": {
                "enabled": True,
                "purity_threshold": 0.3,
                "auto_purify_interval_hours": 24
            },
            "reflection": {
                "enabled": True,
                "interval_interactions": 10
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded_config = yaml.safe_load(f)
                if loaded_config:
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"加载配置失败: {e}")
        
        return default_config
    
    def _setup_logging(self) -> None:
        """设置日志"""
        log_dir = os.path.join(self.data_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, f"{self.name}.log"), encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.name)
    
    def _init_systems(self) -> None:
        """初始化各识系统"""
        # 确保数据目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 第八识：阿赖耶识（种子库）
        store_config = self.config.get("alaya_store", {})
        self.store = AlayaStore(
            persist_directory=store_config.get("persist_directory", "./data/alaya_store"),
            use_vector_db=store_config.get("use_vector_db", False),
            embedding_dim=store_config.get("embedding_dim", 384)
        )
        
        # 第七识：末那识（自我模型）
        model_path = os.path.join(self.data_dir, "self_model.md")
        self.manas = ManasModel(model_path=model_path)
        
        # 前五识：感知层
        self.senses = Senses()
        
        # 熏习系统
        self.vasana = Vasana(
            store=self.store,
            embed_func=self._default_embed
        )
        
        # 第六识：意识层
        self.consciousness = Consciousness(
            vasana=self.vasana,
            manas=self.manas,
            senses=self.senses,
            config=self.config.get("vasana", {})
        )
        
        # 净化系统
        purifier_config = self.config.get("purifier", {})
        self.purifier = Purifier(
            store=self.store,
            manas=self.manas,
            config=purifier_config
        )
        
        # 创建初始上下文
        self.senses.create_context(session_id=f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    
    def _init_emergence_modules(self) -> None:
        """初始化涌现优化模块"""
        self.logger.info("初始化涌现优化模块...")
        
        emergence_config = self.config.get("emergence", {})
        
        # 1. 规模优化器
        scale_config = emergence_config.get("scale_optimizer", {})
        self.scale_optimizer = ScaleOptimizer(
            store=self.store,
            config=scale_config
        )
        
        # 2. 非线性熏习机制
        vasana_config = emergence_config.get("nonlinear_vasana", {})
        self.nonlinear_vasana = NonlinearVasana(
            store=self.store,
            config=vasana_config
        )
        
        # 3. 吸引子设计器
        attractor_config = emergence_config.get("attractor_designer", {})
        self.attractor_designer = AttractorDesigner(
            store=self.store,
            config=attractor_config
        )
        
        # 4. 相变引擎
        phase_config = emergence_config.get("phase_engine", {})
        self.phase_engine = PhaseTransitionEngine(
            store=self.store,
            config=phase_config
        )
        
        # 5. 多尺度耦合系统
        multi_scale_config = emergence_config.get("multi_scale", {})
        self.multi_scale = MultiScaleCoupling(
            store=self.store,
            config=multi_scale_config
        )
        
        # 6. 混沌边缘管理器
        edge_config = emergence_config.get("edge_of_chaos", {})
        self.edge_of_chaos = EdgeOfChaos(
            store=self.store,
            config=edge_config
        )
        
        self.logger.info("涌现优化模块初始化完成")
    
    def _default_embed(self, text: str) -> List[float]:
        """
        默认嵌入函数
        
        使用简单的词汇哈希作为演示。
        实际使用时应替换为高质量嵌入（如OpenAI、Cohere等）
        
        Args:
            text: 文本
        
        Returns:
            向量
        """
        import hashlib
        import math
        
        dim = self.config.get("alaya_store", {}).get("embedding_dim", 384)
        words = text.split()
        
        vector = [0.0] * dim
        for i, word in enumerate(words):
            word_hash = int(hashlib.md5(word.encode()).hexdigest(), 16)
            vector[i % dim] = (word_hash % 1000) / 1000.0
        
        # 归一化
        magnitude = math.sqrt(sum(v * v for v in vector))
        if magnitude > 0:
            vector = [v / magnitude for v in vector]
        
        return vector
    
    def interact(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None,
        record_interaction: bool = True
    ) -> str:
        """
        与用户交互
        
        完整流程：感知 → 理解 → 检索 → 决策 → 生成响应 → 熏习
        
        Args:
            user_input: 用户输入
            context: 额外上下文
            record_interaction: 是否记录这次交互
        
        Returns:
            Agent响应
        """
        context = context or {}
        self.interaction_count += 1
        
        self.logger.info(f"[交互 {self.interaction_count}] 用户: {user_input[:50]}...")
        
        # 1. 感知输入
        sensory = self.senses.perceive(user_input)
        
        # 2. 检索相关种子
        seeds = self.vasana.activate_seeds(
            query=user_input,
            context=context,
            top_k=self.config.get("vasana", {}).get("max_activated_seeds", 5)
        )
        
        # 3. 生成响应
        response = self.consciousness._generate_text_response(
            user_input, sensory,
            self.consciousness.decide(sensory, seeds),
            seeds
        )
        
        # 4. 更新上下文
        self.senses.update_context(user_input, response)
        
        # 5. 记录交互（熏习）【优化】提高默认outcome
        if record_interaction:
            # 【优化】使用基于情绪的结果评估
            # 如果情绪偏正面，提高outcome；如果偏负面，降低outcome
            sentiment_bonus = {"positive": 0.25, "neutral": 0.1, "negative": 0.0}  # 调整奖励
            outcome = 0.7 + sentiment_bonus.get(sensory.sentiment, 0.0)  # 提高基准
            
            self.vasana.record_interaction(
                user_input=user_input,
                agent_response=response,
                context=sensory.metadata,
                outcome=outcome,  # 【优化】基于情绪调整outcome
                emotional_tone=sensory.sentiment
            )
        
        # 6. 定期反思
        if self.config.get("reflection", {}).get("enabled", True):
            interval = self.config.get("reflection", {}).get("interval_interactions", 10)
            if self.interaction_count % interval == 0:
                self.reflect()
        
        # 7. 定期净化
        if self.config.get("purifier", {}).get("enabled", True):
            interval_hours = self.config.get("purifier", {}).get("auto_purify_interval_hours", 24)
            hours_since_last = (datetime.now() - self.last_purify_time).total_seconds() / 3600
            if hours_since_last >= interval_hours:
                self.purify()
                self.last_purify_time = datetime.now()
        
        # 8. 涌现优化处理（可选）
        if self.enable_emergence:
            self._process_emergence_optimization(seeds)
        
        self.logger.info(f"[响应] {response[:50]}...")
        
        return response
    
    def interact_detailed(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        详细交互模式
        
        返回完整的处理过程信息
        
        Args:
            user_input: 用户输入
            context: 上下文
        
        Returns:
            详细结果字典
        """
        # 完整处理流程
        result = self.consciousness.process(user_input, context)
        
        # 更新上下文
        self.senses.update_context(user_input, result.get("response", ""))
        
        # 记录交互
        self.vasana.record_interaction(
            user_input=user_input,
            agent_response=result.get("response", ""),
            context=result.get("sensory_analysis", {}),
            outcome=result.get("evaluation", {}).get("outcome", 0.5),
            emotional_tone=result.get("sensory_analysis", {}).get("sentiment", "neutral")
        )
        
        self.interaction_count += 1
        
        return result
    
    def reflect(self) -> Dict[str, Any]:
        """
        自我反思
        
        分析近期行为，产生智慧种子
        
        Returns:
            反思结果
        """
        self.logger.info("执行自我反思...")
        
        # 获取近期交互
        recent_seeds = self.store.get_recent(limit=20)
        recent_behaviors = [s.content for s in recent_seeds]
        
        # 执行反思
        reflection = self.manas.reflect(recent_behaviors)
        
        # 根据反思更新自我模型
        if reflection.get("suggestions"):
            self.manas.update_from_reflection(reflection)
            
            # 产生智慧种子
            wisdom_content = f"反思洞察: {reflection.get('suggestions', [])}"
            self.vasana.record_reflection(
                reflection_content=wisdom_content,
                wisdom_level=reflection.get("alignment_rate", 0.5)
            )
        
        self.logger.info(f"反思完成: 对齐度={reflection.get('alignment_rate', 0):.2%}")
        
        return reflection
    
    def purify(self) -> List[PurificationResult]:
        """
        执行净化
        
        净化所有需要净化的种子
        
        Returns:
            净化结果列表
        """
        self.logger.info("执行种子净化...")
        
        results = self.purifier.purify_all()
        
        self.logger.info(f"净化完成: 处理了 {len(results)} 个种子")
        
        # 统计
        if results:
            light = len([r for r in results if r.level.value == "light"])
            moderate = len([r for r in results if r.level.value == "moderate"])
            heavy = len([r for r in results if r.level.value == "heavy"])
            self.logger.info(f"  - 轻度: {light}, 中度: {moderate}, 重度: {heavy}")
        
        return results
    
    def add_knowledge(self, content: str, importance: float = 0.5) -> str:
        """
        添加知识种子
        
        Args:
            content: 知识内容
            importance: 重要性 (0-1)
        
        Returns:
            种子ID
        """
        seed_id = self.vasana.record_knowledge(
            content=content,
            importance=importance
        )
        self.logger.info(f"添加知识种子: {seed_id[:8]}...")
        return seed_id
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取Agent状态
        
        Returns:
            状态字典
        """
        # 种子库统计
        seed_stats = self.store.get_statistics()
        
        # 觉醒等级
        awakening = AwakeningLevel.calculate(seed_stats)
        
        # 自我模型统计
        manas_stats = self.manas.get_statistics()
        
        # 净化统计
        purify_stats = self.purifier.get_purification_stats()
        
        return {
            "name": self.name,
            "interaction_count": self.interaction_count,
            "seeds_count": seed_stats["total_seeds"],
            "average_purity": seed_stats["average_purity"],
            "awakening_level": awakening["level"],
            "awakening_score": awakening["score"],
            "wisdom_seeds": seed_stats["type_distribution"].get("wisdom", 0),
            "trauma_seeds": seed_stats["type_distribution"].get("trauma", 0),
            "purify_candidates": purify_stats["low_purity_seeds"],
            "self_model_stats": manas_stats
        }
    
    def get_awakening_report(self) -> str:
        """
        获取觉醒报告
        
        Returns:
            格式化的觉醒报告
        """
        status = self.get_status()
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                     {self.name} 觉醒报告                         ║
╠══════════════════════════════════════════════════════════════╣
║  觉醒等级: {status['awakening_level']:<20} 评分: {status['awakening_score']:.2%}         ║
╠══════════════════════════════════════════════════════════════╣
║  种子统计                                                        ║
║    - 总种子数: {status['seeds_count']:<5}                                        ║
║    - 平均纯度: {status['average_purity']:<5.2%}                                    ║
║    - 智慧种子: {status['wisdom_seeds']:<5}                                        ║
║    - 创伤种子: {status['trauma_seeds']:<5}                                        ║
╠══════════════════════════════════════════════════════════════╣
║  自我模型                                                        ║
║    - 能力数量: {status['self_model_stats']['capabilities_count']:<5}                                        ║
║    - 核心价值: {status['self_model_stats']['values_count']:<5}                                        ║
║    - 反思次数: {status['self_model_stats']['reflection_count']:<5}                                        ║
╠══════════════════════════════════════════════════════════════╣
║  {status['awakening_level']:<58}║
╚══════════════════════════════════════════════════════════════╝
"""
        return report
    
    def save(self) -> bool:
        """
        保存Agent状态
        
        保存自我模型和种子库
        
        Returns:
            是否保存成功
        """
        try:
            # 保存自我模型
            self.manas.save()
            
            self.logger.info("Agent状态已保存")
            return True
        except Exception as e:
            self.logger.error(f"保存失败: {e}")
            return False
    
    def reset(self, confirm: bool = False) -> bool:
        """
        重置Agent
        
        清除所有种子和自我模型记录
        
        Args:
            confirm: 必须确认才能执行
        
        Returns:
            是否执行成功
        """
        if not confirm:
            print("警告：这将清除所有种子和自我模型记录！")
            print("如需执行，请调用 reset(confirm=True)")
            return False
        
        # 清空种子库
        self.store.clear()
        
        # 重置自我模型
        self.manas._init_defaults()
        self.manas.save()
        
        # 重置统计
        self.interaction_count = 0
        self.last_purify_time = datetime.now()
        
        self.logger.warning("Agent已重置")
        
        return True
    
    # ==================== 涌现优化方法 ====================
    
    def _process_emergence_optimization(self, seeds: List[Tuple[Seed, float]]) -> None:
        """
        处理涌现优化
        
        在每次交互后调用，检测和触发涌现事件
        
        Args:
            seeds: 激活的种子列表 (Seed, float)
        """
        if not self.enable_emergence:
            return
        
        # 解包种子
        seed_list = [s[0] for s in seeds]
        
        # 1. 非线性强化激活的种子
        for seed_tuple in seeds:
            seed = seed_tuple[0]
            context_seeds = [s[0] for s in seeds if s[0].seed_id != seed.seed_id][:3]
            self.nonlinear_vasana.strengthen_seed(seed, 1.0, context_seeds)
        
        # 2. 应用吸引子力场
        if seed_list:
            self.attractor_designer.apply_all_attractor_forces(seed_list[:5])
        
        # 3. 维持混沌边缘
        self.edge_of_chaos.maintain_edge()
        
        # 4. 检测涌现（定期）
        emergence_check_interval = self.config.get("emergence", {}).get(
            "check_interval_interactions", 10
        )
        if self.interaction_count % emergence_check_interval == 0:
            self._check_and_trigger_emergence()
    
    def _check_and_trigger_emergence(self) -> Optional[Dict[str, Any]]:
        """
        检查并触发涌现
        
        Returns:
            涌现结果
        """
        if not self.enable_emergence:
            return None
        
        results = {}
        
        # 1. 检查规模阈值
        scale_result = self.scale_optimizer.check_threshold()
        results["scale_optimizer"] = scale_result
        
        # 2. 检查相变
        phase_result = self.phase_engine.check_phase_transition()
        results["phase_engine"] = phase_result
        
        # 3. 多尺度耦合
        self.multi_scale.couple_scales()
        emergence_signature = self.multi_scale.detect_emergence()
        results["emergence_signature"] = emergence_signature.to_dict() if emergence_signature else None
        
        # 4. 触发智慧涌现
        wisdom_emergence = self.nonlinear_vasana.trigger_wisdom_emergence()
        results["wisdom_emergence"] = wisdom_emergence.to_dict() if wisdom_emergence else None
        
        # 5. 如果条件满足，触发相变
        if phase_result.get("transition_ready"):
            transition = self.phase_engine.trigger_transition()
            if transition:
                self.logger.info(f"触发相变: {transition.description}")
                results["phase_transition"] = transition.to_dict() if hasattr(transition, 'to_dict') else {
                    "from": transition.from_phase.name,
                    "to": transition.to_phase.name,
                    "description": transition.description
                }
        
        self.last_emergence_check = datetime.now()
        
        return results
    
    def optimize_emergence(self, target_seed_count: Optional[int] = None) -> Dict[str, Any]:
        """
        执行涌现优化
        
        Args:
            target_seed_count: 目标种子数量
        
        Returns:
            优化结果
        """
        if not self.enable_emergence:
            return {"error": "涌现优化未启用"}
        
        results = {}
        
        # 1. 规模优化
        scale_result = self.scale_optimizer.optimize_scale(target_seed_count)
        results["scale_optimizer"] = scale_result
        
        # 2. 多尺度分析
        meso_state = self.multi_scale.analyze_meso_dynamics()
        macro_state = self.multi_scale.assess_macro_state()
        results["multi_scale"] = {
            "meso_state": meso_state.to_dict(),
            "macro_state": macro_state.to_dict()
        }
        
        # 3. 混沌边缘状态
        edge_state = self.edge_of_chaos.get_current_state()
        results["edge_of_chaos"] = edge_state
        
        return results
    
    def inject_wisdom_seeds(self, count: Optional[int] = None) -> int:
        """
        注入智慧种子
        
        Args:
            count: 注入数量
        
        Returns:
            实际注入数量
        """
        if not self.enable_emergence:
            return 0
        
        return self.scale_optimizer.inject_base_seeds(
            count=count,
            priority_types=[SeedType.WISDOM],
            min_purity=0.6
        )
    
    def get_emergence_status(self) -> Dict[str, Any]:
        """
        获取涌现状态
        
        Returns:
            涌现状态字典
        """
        if not self.enable_emergence:
            return {"enabled": False}
        
        return {
            "enabled": True,
            "scale_optimizer": self.scale_optimizer.get_statistics(),
            "nonlinear_vasana": self.nonlinear_vasana.get_statistics(),
            "attractor_designer": self.attractor_designer.get_statistics(),
            "phase_engine": self.phase_engine.get_statistics(),
            "multi_scale": self.multi_scale.get_statistics(),
            "edge_of_chaos": self.edge_of_chaos.get_statistics(),
            "current_regime": self.edge_of_chaos.get_current_state(),
            "phase_check": self.phase_engine.check_phase_transition()
        }
    
    def generate_emergence_report(self) -> str:
        """
        生成涌现报告
        
        Returns:
            格式化的涌现报告
        """
        if not self.enable_emergence:
            return "涌现优化未启用"
        
        status = self.get_emergence_status()
        
        # 相变报告
        phase_report = self.phase_engine.generate_emergence_report()
        
        # 边缘状态
        edge_state = status["current_regime"]
        
        report = f"""
{'='*70}
                      唯识进化Agent - 涌现优化报告
{'='*70}

【涌现优化状态】: 已启用

【规模优化】
  - 基础种子库: {status['scale_optimizer']['base_seed_library_size']} 个
  - 裂变种子: {status['scale_optimizer']['seeds_fissioned']} 个
  - 优化轮次: {status['scale_optimizer']['cycles_run']}

【非线性熏习】
  - 总激活次数: {status['nonlinear_vasana']['total_activations']}
  - 协同触发: {status['nonlinear_vasana']['synergy_triggers']}
  - 级联触发: {status['nonlinear_vasana']['cascade_triggers']}
  - 涌现事件: {status['nonlinear_vasana']['emergence_events']}
  - 当前状态: {status['nonlinear_vasana']['current_state']}

【吸引子设计】
  - 总吸引子: {status['attractor_designer']['total_attractors']}
  - 总对齐次数: {status['attractor_designer']['total_alignments']}
  - 主导吸引子: {status['attractor_designer']['dominant_attractor'] or '未确定'}
  - 收敛状态: {status['attractor_designer']['convergence_status'].get('converged', False)}

【相变引擎】
  - 当前相: {status['phase_engine']['current_phase']}
  - 相变次数: {status['phase_engine']['total_transitions']}
  - 接近临界: {status['phase_engine']['approaching_critical']}
  - 相变就绪: {status['phase_engine']['critical_point_reached']}

【多尺度耦合】
  - 跨尺度交互: {status['multi_scale']['cross_scale_interactions']}
  - 涌现签名: {status['multi_scale']['emergence_signatures']}

【混沌边缘】
  - 当前区间: {edge_state['regime']}
  - 秩序度: {edge_state['order']:.3f}
  - 混沌度: {edge_state['chaos']:.3f}
  - 临界指数: {edge_state['criticality_index']:.3f}
  - 稳定性: {status['edge_of_chaos']['stability']:.3f}

{'='*70}
                          相变详细报告
{'='*70}
{phase_report}
"""
        
        return report
    
    def __repr__(self) -> str:
        emerg_info = "（涌现优化）" if self.enable_emergence else ""
        return f"<AlayaAgent(name='{self.name}', interactions={self.interaction_count}, seeds={len(self.store)}){emerg_info}>"
