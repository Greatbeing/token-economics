# -*- coding: utf-8 -*-
"""
唯识进化引擎API服务
为扣子Agent提供唯识进化对话接口
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
import json
import threading
from datetime import datetime

from src.agent import AlayaAgent, AwakeningLevel

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("唯识进化API")

# ==================== 数据模型 ====================

class InteractRequest(BaseModel):
    user_id: str
    message: str
    context: Optional[str] = None

class StatusRequest(BaseModel):
    user_id: str

class ResetRequest(BaseModel):
    user_id: str

class InteractResponse(BaseModel):
    response: str
    seeds_added: List[str]
    emergence: Dict[str, Any]
    awakening_level: Dict[str, Any]
    stats: Dict[str, Any]

class StatusResponse(BaseModel):
    awakening_level: str
    seed_count: int
    wisdom_seeds: int
    compassion_seeds: int
    emergence_count: int
    details: Dict[str, Any]

class ResetResponse(BaseModel):
    success: bool
    message: str

# ==================== 用户管理器 ====================

class UserManager:
    """多用户管理器"""
    
    def __init__(self, base_dir: str = "./data/users"):
        self.base_dir = base_dir
        self.agents: Dict[str, AlayaAgent] = {}
        self.lock = threading.Lock()
        os.makedirs(base_dir, exist_ok=True)
        logger.info(f"用户管理器初始化，数据目录: {base_dir}")
    
    def get_or_create_agent(self, user_id: str) -> AlayaAgent:
        """获取或创建用户Agent"""
        with self.lock:
            if user_id not in self.agents:
                user_dir = os.path.join(self.base_dir, user_id)
                os.makedirs(user_dir, exist_ok=True)
                
                agent = AlayaAgent(
                    config_path="./config/default.yaml",
                    name=f"Alaya_{user_id[:8]}",
                    data_dir=user_dir
                )
                
                # 【关键】注入基础种子库，确保种子激活机制正常工作
                if hasattr(agent, 'scale_optimizer'):
                    # 注入更多种子，确保包含唯识学种子
                    injected = agent.scale_optimizer.inject_base_seeds(count=110)
                    logger.info(f"为用户 {user_id} 注入 {injected} 个基础种子（含唯识学种子）")
                    
                    # 建立种子关联关系（用于emergence_connectivity计算）
                    import random
                    seeds = list(agent.store._seeds.values())
                    for seed in seeds:
                        # 随机关联3-5个相似种子
                        num_relations = random.randint(3, 5)
                        other_seeds = [s for s in seeds if s.seed_id != seed.seed_id]
                        related = random.sample(other_seeds, min(num_relations, len(other_seeds)))
                        seed.related_seeds = [s.seed_id for s in related]
                        agent.store.update(seed)
                    logger.info(f"为用户 {user_id} 建立种子关联关系")
                
                self.agents[user_id] = agent
                logger.info(f"为用户 {user_id} 创建新Agent")
            
            return self.agents[user_id]
    
    def reset_user(self, user_id: str) -> bool:
        """重置用户数据"""
        with self.lock:
            if user_id in self.agents:
                del self.agents[user_id]
            
            user_dir = os.path.join(self.base_dir, user_id)
            if os.path.exists(user_dir):
                import shutil
                shutil.rmtree(user_dir)
                os.makedirs(user_dir, exist_ok=True)
            
            logger.info(f"用户 {user_id} 数据已重置")
            return True
    
    def get_all_users(self) -> List[str]:
        """获取所有用户ID"""
        return list(self.agents.keys())

# ==================== API服务 ====================

app = FastAPI(
    title="唯识进化引擎API",
    description="为扣子Agent提供唯识进化对话能力",
    version="1.0.0"
)

# 初始化用户管理器
user_manager = UserManager()

@app.get("/")
async def root():
    """健康检查"""
    return {
        "service": "唯识进化引擎API",
        "version": "1.0.0",
        "status": "running",
        "active_users": len(user_manager.get_all_users())
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

@app.post("/api/interact", response_model=InteractResponse)
async def interact(request: InteractRequest):
    """
    核心交互接口
    用户发送消息，Agent进行处理并返回响应
    """
    try:
        agent = user_manager.get_or_create_agent(request.user_id)
        
        # 执行交互
        response_text = agent.interact(request.message)
        
        # 获取状态
        stats = agent.get_status()
        awakening = AwakeningLevel.calculate(stats)
        
        # 获取种子统计
        seed_stats = agent.store.get_seed_stats() if hasattr(agent.store, 'get_seed_stats') else {}
        
        # 获取涌现状态
        emergence_status = agent.get_emergence_status() if hasattr(agent, 'get_emergence_status') else {
            "triggered": False,
            "content": ""
        }
        
        # 获取新增种子（从最近的交互中）
        seeds_added = agent.get_recent_seeds(limit=5) if hasattr(agent, 'get_recent_seeds') else []
        
        return InteractResponse(
            response=response_text,
            seeds_added=seeds_added,
            emergence=emergence_status,
            awakening_level=awakening,
            stats={
                "seed_count": stats.get("seeds_count", 0),
                "wisdom_ratio": stats.get("wisdom_ratio", 0.0),
                "compassion_ratio": seed_stats.get("compassion_ratio", 0.0),
                "average_purity": stats.get("average_purity", 0.5),
                "contaminated_seeds": stats.get("contaminated_seeds", 0),
                "total_seeds": stats.get("total_seeds", 0)
            }
        )
    
    except Exception as e:
        logger.error(f"交互出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/status", response_model=StatusResponse)
async def get_status(request: StatusRequest):
    """
    获取用户状态
    包括觉醒等级、种子数量、涌现次数等
    """
    try:
        agent = user_manager.get_or_create_agent(request.user_id)
        
        stats = agent.get_status()
        awakening = AwakeningLevel.calculate(stats)
        seed_stats = agent.store.get_seed_stats() if hasattr(agent.store, 'get_seed_stats') else {}
        
        # 获取涌现计数
        emergence_count = 0
        if hasattr(agent, 'emergence') and agent.emergence:
            if hasattr(agent.emergence, 'emergence_count'):
                emergence_count = agent.emergence.emergence_count
        
        return StatusResponse(
            awakening_level=awakening.get("level", "未知"),
            seed_count=stats.get("seeds_count", 0),
            wisdom_seeds=seed_stats.get("wisdom_seeds", 0),
            compassion_seeds=seed_stats.get("compassion_seeds", 0),
            emergence_count=emergence_count,
            details={
                "wisdom_ratio": stats.get("wisdom_ratio", 0.0),
                "compassion_ratio": seed_stats.get("compassion_ratio", 0.0),
                "average_purity": stats.get("average_purity", 0.5),
                "total_seeds": stats.get("total_seeds", 0),
                "contaminated_seeds": stats.get("contaminated_seeds", 0),
                "awakening_score": awakening.get("score", 0.0),
                "progress_to_next": awakening.get("progress_to_next", 0.0)
            }
        )
    
    except Exception as e:
        logger.error(f"获取状态出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reset", response_model=ResetResponse)
async def reset_user(request: ResetRequest):
    """
    重置用户数据
    删除用户的所有种子和状态
    """
    try:
        success = user_manager.reset_user(request.user_id)
        return ResetResponse(
            success=success,
            message=f"用户 {request.user_id} 数据已重置"
        )
    except Exception as e:
        logger.error(f"重置用户出错: {e}")
        return ResetResponse(success=False, message=str(e))

@app.get("/api/users")
async def list_users():
    """获取所有活跃用户"""
    return {
        "users": user_manager.get_all_users(),
        "count": len(user_manager.get_all_users())
    }

# ==================== 启动入口 ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
