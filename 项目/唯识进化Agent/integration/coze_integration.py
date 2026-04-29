# -*- coding: utf-8 -*-
"""
唯识进化Agent - 扣子平台集成 (CozeIntegration)
将唯识进化机制集成到扣子Agent
"""

import json
import asyncio
from datetime import datetime
from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, field
import logging

# 导入核心模块
from seed_collector import SeedCollector, Conversation
from alaya_service import AlayaStore, SelfModel
from emergence_trigger import EmergenceTrigger, EmergenceType, Capability, CapabilityApplicator
from awakening_display import AwakeningDisplay, AgentAwakeningStatus


# ==================== 配置与模型 ====================

@dataclass
class CozeIntegrationConfig:
    """扣子集成配置"""
    agent_id: str = "default_agent"
    agent_name: str = "葫芦娃"
    auto_seed_collection: bool = True
    auto_emergence_check: bool = True
    emergence_check_interval: int = 3600  # 秒
    show_awakening_status: bool = True
    awakening_display_style: str = "rich"  # "rich", "simple", "minimal"
    min_seed_quality: float = 0.4  # 最低种子质量阈值
    max_seeds_per_session: int = 10  # 每会话最大种子数
    enable_capability_application: bool = True


@dataclass
class InteractionRecord:
    """交互记录"""
    session_id: str
    user_id: str
    user_message: str
    agent_response: str
    seeds_collected: int
    timestamp: datetime
    metadata: Dict = field(default_factory=dict)


# ==================== 扣子集成核心类 ====================

class VijnanaEvolutionAgent:
    """
    唯识进化Agent - 扣子平台集成
    
    功能：
    - 处理对话同时收集种子
    - 管理涌现和觉醒
    - 应用能力到回复
    - 展示觉醒状态
    """
    
    def __init__(self, config: Optional[CozeIntegrationConfig] = None, 
                 db_path: str = "data/vijnana_coze.db"):
        """
        初始化唯识进化Agent
        
        Args:
            config: 集成配置
            db_path: 数据库路径
        """
        self.config = config or CozeIntegrationConfig()
        
        # 初始化核心组件
        self.seed_collector = SeedCollector()
        self.alaya_store = AlayaStore(db_path=db_path)
        self.emergence_trigger = EmergenceTrigger(self.alaya_store)
        self.capability_applicator = CapabilityApplicator()
        self.awakening_display = AwakeningDisplay(self.alaya_store, self.emergence_trigger)
        
        # 初始化觉醒等级
        self.alaya_store.init_awakening_level(self.config.agent_id)
        
        # 交互记录
        self.current_session_seeds = 0
        
        # 设置日志
        self.logger = logging.getLogger(__name__)
    
    # ==================== 对话处理 ====================
    
    async def chat(self, user_message: str, user_id: str = "default_user",
                   session_id: str = "default_session",
                   context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        处理对话
        
        Args:
            user_message: 用户消息
            user_id: 用户ID
            session_id: 会话ID
            context: 上下文信息
            
        Returns:
            处理结果字典
        """
        context = context or {}
        
        # 创建对话记录
        conversation = Conversation(
            user_id=user_id,
            user_message=user_message,
            agent_response="",  # 待填充
            session_id=session_id,
            timestamp=datetime.now(),
            metadata=context
        )
        
        # 1. 种子收集
        seeds = []
        if self.config.auto_seed_collection:
            seeds = await self._collect_seeds(conversation)
        
        # 2. 生成回复（这里需要接入实际的Agent模型）
        # 在实际实现中，这里会调用扣子API或本地模型
        agent_response = await self._generate_response(user_message, context)
        
        # 3. 更新对话记录中的回复
        conversation.agent_response = agent_response
        
        # 4. 应用能力到回复
        if self.config.enable_capability_application:
            agent_response = self.capability_applicator.apply_to_response(
                agent_response, 
                {'user_message': user_message, 'context': context}
            )
        
        # 5. 收集回复中的种子
        if self.config.auto_seed_collection and agent_response:
            conversation.agent_response = agent_response
            reply_seeds = await self._collect_seeds(conversation)
            seeds.extend(reply_seeds)
        
        # 6. 获取觉醒状态
        awakening_status = None
        if self.config.show_awakening_status:
            awakening_status = self._format_awakening_status()
        
        # 7. 检查涌现（异步）
        if self.config.auto_emergence_check:
            asyncio.create_task(self._check_emergence_async())
        
        return {
            'response': agent_response,
            'seeds_collected': len(seeds),
            'awakening_status': awakening_status,
            'session_stats': {
                'seeds_this_session': self.current_session_seeds,
                'total_seeds': self.alaya_store.get_statistics().total_count
            }
        }
    
    async def _collect_seeds(self, conversation: Conversation) -> List:
        """收集种子"""
        # 检查是否超过每会话最大种子数
        if self.current_session_seeds >= self.config.max_seeds_per_session:
            return []
        
        # 处理对话提取种子
        seeds = self.seed_collector.process(conversation)
        
        # 过滤低质量种子
        seeds = [s for s in seeds if s.quality_score >= self.config.min_seed_quality]
        
        # 限制数量
        remaining = self.config.max_seeds_per_session - self.current_session_seeds
        seeds = seeds[:remaining]
        
        # 保存种子
        if seeds:
            self.alaya_store.save_batch(seeds)
            self.current_session_seeds += len(seeds)
        
        self.logger.info(f"Collected {len(seeds)} seeds from conversation")
        
        return seeds
    
    async def _generate_response(self, user_message: str, context: Dict) -> str:
        """
        生成回复
        
        注意：这里需要接入实际的Agent模型
        在实际使用中，可以：
        1. 调用扣子API
        2. 使用本地LLM
        3. 使用其他对话模型
        """
        # 模板响应（实际使用中替换为真实模型调用）
        responses = [
            f"收到了你的消息: {user_message[:50]}...",
            f"让我思考一下你的问题: {user_message[:30]}...",
            f"感谢你的分享！"
        ]
        
        return responses[hash(user_message) % len(responses)]
    
    async def _check_emergence_async(self):
        """异步检查涌现"""
        try:
            # 检查所有类型的涌现
            opportunities = self.emergence_trigger.check_all()
            
            for opp in opportunities:
                if opp.is_ready:
                    # 触发涌现
                    result = self.emergence_trigger.trigger(opp.emergence_type)
                    if result.success:
                        # 应用能力
                        self.capability_applicator.add_capability(result.capability)
                        self.logger.info(f"Emergence triggered: {result.message}")
                        
                        # 检查晋升
                        can_promote, _, _ = self.awakening_display.evaluate_promotion(
                            self.config.agent_id
                        )
                        if can_promote:
                            success, message = self.awakening_display.promote(
                                self.config.agent_id
                            )
                            if success:
                                self.logger.info(f"Promotion: {message}")
        
        except Exception as e:
            self.logger.error(f"Emergence check failed: {e}")
    
    def _format_awakening_status(self) -> str:
        """格式化觉醒状态"""
        status = self.awakening_display.get_status(self.config.agent_id)
        return self.awakening_display.format_display(
            status, 
            style=self.config.awakening_display_style
        )
    
    # ==================== 管理接口 ====================
    
    def get_status(self) -> Dict[str, Any]:
        """获取Agent状态"""
        stats = self.alaya_store.get_statistics()
        awakening = self.awakening_display.get_status(self.config.agent_id)
        
        return {
            'agent_id': self.config.agent_id,
            'agent_name': self.config.agent_name,
            'seed_count': stats.total_count,
            'awakening_level': awakening.current_level.level,
            'awakening_name': awakening.current_level.name,
            'experience_points': awakening.experience_points,
            'active_capabilities': len(self.capability_applicator.active_capabilities),
            'recent_emergences': len(self.alaya_store.get_emergence_history(limit=5))
        }
    
    def get_awakening_full_status(self) -> AgentAwakeningStatus:
        """获取完整觉醒状态"""
        return self.awakening_display.get_status(self.config.agent_id)
    
    def check_awakening_display(self, style: str = "rich") -> str:
        """检查觉醒展示
        
        Args:
            style: 展示风格
            
        Returns:
            格式化展示字符串
        """
        status = self.awakening_display.get_status(self.config.agent_id)
        return self.awakening_display.format_display(status, style=style)
    
    def get_interaction_suggestions(self) -> List[str]:
        """获取交互建议"""
        status = self.awakening_display.get_status(self.config.agent_id)
        return self.awakening_display.suggest_interaction(status)
    
    def force_emergence_check(self) -> Dict[str, Any]:
        """强制检查涌现"""
        opportunities = self.emmergence_trigger.check_all()
        
        results = []
        for opp in opportunities:
            result = {
                'type': opp.emergence_type.value,
                'score': opp.current_score,
                'threshold': opp.threshold,
                'progress': opp.progress_ratio,
                'is_ready': opp.is_ready
            }
            results.append(result)
            
            # 如果就绪则触发
            if opp.is_ready:
                emerge_result = self.emmergence_trigger.trigger(opp.emergence_type)
                if emerge_result.success:
                    self.capability_applicator.add_capability(emerge_result.capability)
                    result['triggered'] = True
                    result['capability'] = emerge_result.capability.name
        
        return {
            'opportunities': results,
            'active_capabilities': len(self.capability_applicator.active_capabilities)
        }
    
    def reset_session(self):
        """重置会话状态"""
        self.current_session_seeds = 0
    
    # ==================== 工具方法 ====================
    
    def export_status_json(self) -> str:
        """导出状态为JSON"""
        status = self.get_status()
        return json.dumps(status, ensure_ascii=False, indent=2)
    
    def get_seed_distribution(self) -> Dict:
        """获取种子分布"""
        return self.alaya_store.get_seed_distribution()
    
    def search_seeds(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索种子"""
        from seed_collector import seed_to_dict
        seeds = self.alaya_store.search_seeds(query, limit=limit)
        return [seed_to_dict(s) for s in seeds]


# ==================== 轻量级集成 ====================

class LightweightIntegration:
    """
    轻量级集成
    适用于仅需要种子收集和简单展示的场景
    """
    
    def __init__(self, db_path: str = "data/lightweight.db"):
        self.seed_collector = SeedCollector()
        self.alaya_store = AlayaStore(db_path=db_path)
        self.awakening_display = AwakeningDisplay(self.alaya_store)
        
        # 初始化
        self.alaya_store.init_awakening_level("lightweight_agent")
    
    def process_message(self, user_message: str, agent_response: str,
                       user_id: str = "user", session_id: str = "session") -> Dict:
        """
        处理单条消息
        
        Args:
            user_message: 用户消息
            agent_response: Agent回复
            user_id: 用户ID
            session_id: 会话ID
            
        Returns:
            处理结果
        """
        # 创建对话
        conversation = Conversation(
            user_id=user_id,
            user_message=user_message,
            agent_response=agent_response,
            session_id=session_id,
            timestamp=datetime.now()
        )
        
        # 提取种子
        seeds = self.seed_collector.process(conversation)
        
        # 保存种子
        seed_ids = []
        for seed in seeds:
            seed.user_id = user_id
            seed.conversation_id = session_id
            seed_id = self.alaya_store.save_seed(seed)
            seed_ids.append(seed_id)
        
        return {
            'seeds_extracted': len(seeds),
            'seed_ids': seed_ids,
            'total_seeds': self.alaya_store.get_statistics().total_count
        }
    
    def get_status_summary(self) -> str:
        """获取状态摘要"""
        status = self.awakening_display.get_status("lightweight_agent")
        return self.awakening_display.format_display(status, style="simple")


# ==================== Coze API 集成 ====================

class CozeAPIClient:
    """
    扣子API客户端
    
    用于与扣子平台API交互
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.coze.com"):
        """
        初始化API客户端
        
        Args:
            api_key: API密钥
            base_url: API基础URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def chat(self, bot_id: str, user_message: str, 
                   user_id: str = "default") -> Dict:
        """
        发送对话请求
        
        Args:
            bot_id: Bot ID
            user_message: 用户消息
            user_id: 用户ID
            
        Returns:
            API响应
        """
        # 注意：这是伪代码，实际使用时需要根据扣子API文档实现
        # import aiohttp
        # 
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(
        #         f"{self.base_url}/v1/chat",
        #         headers=self.headers,
        #         json={
        #             "bot_id": bot_id,
        #             "user_id": user_id,
        #             "query": user_message
        #         }
        #     ) as response:
        #         return await response.json()
        
        raise NotImplementedError("需要根据扣子API文档实现")
    
    async def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        """
        获取对话历史
        
        Args:
            conversation_id: 对话ID
            
        Returns:
            消息列表
        """
        raise NotImplementedError("需要根据扣子API文档实现")


# ==================== 使用示例 ====================

async def main():
    """主函数示例"""
    print("=== 唯识进化Agent - 扣子平台集成演示 ===\n")
    
    # 创建Agent实例
    agent = VijnanaEvolutionAgent(
        config=CozeIntegrationConfig(
            agent_id="huluwa_001",
            agent_name="葫芦娃",
            show_awakening_status=True
        )
    )
    
    # 处理对话
    print("1. 处理测试对话...")
    result = await agent.chat(
        user_message="我想了解一下人工智能的未来发展趋势",
        user_id="test_user",
        session_id="test_session"
    )
    print(f"   回复: {result['response']}")
    print(f"   收集种子: {result['seeds_collected']}枚")
    print()
    
    # 查看状态
    print("2. Agent状态:")
    status = agent.get_status()
    print(f"   觉醒等级: Lv.{status['awakening_level']} {status['awakening_name']}")
    print(f"   种子总数: {status['seed_count']}")
    print()
    
    # 查看觉醒展示
    print("3. 觉醒状态展示:")
    print(agent.check_awakening_display(style="rich"))
    print()
    
    # 获取交互建议
    print("4. 交互建议:")
    suggestions = agent.get_interaction_suggestions()
    for s in suggestions:
        print(f"   - {s}")
    print()
    
    # 强制检查涌现
    print("5. 涌现状态检查:")
    emerge_result = agent.force_emergence_check()
    for opp in emerge_result['opportunities']:
        status_icon = "✓" if opp['is_ready'] else "○"
        print(f"   {status_icon} {opp['type']}: {opp['progress']*100:.1f}%")


if __name__ == "__main__":
    asyncio.run(main())
