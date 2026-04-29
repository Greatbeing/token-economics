# -*- coding: utf-8 -*-
"""
扣子Agent集成示例

提供多种方式让扣子Agent调用唯识进化引擎API
"""

import requests
import json
from typing import Dict, Any, Optional

# API基础地址（需要根据实际云电脑IP配置）
API_BASE_URL = "http://localhost:8080"

class CozeIntegration:
    """扣子Agent集成类"""
    
    def __init__(self, api_url: str = API_BASE_URL):
        self.api_url = api_url.rstrip('/')
    
    def interact(self, user_id: str, message: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        发送消息并获取响应
        
        Args:
            user_id: 用户唯一标识
            message: 用户消息
            context: 上下文（可选）
        
        Returns:
            API响应字典
        """
        url = f"{self.api_url}/api/interact"
        payload = {
            "user_id": user_id,
            "message": message,
            "context": context
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "response": "抱歉，API服务暂时不可用。"
            }
    
    def get_status(self, user_id: str) -> Dict[str, Any]:
        """获取用户状态"""
        url = f"{self.api_url}/api/status"
        payload = {"user_id": user_id}
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def reset(self, user_id: str) -> bool:
        """重置用户数据"""
        url = f"{self.api_url}/api/reset"
        payload = {"user_id": user_id}
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json().get("success", False)
        except requests.exceptions.RequestException as e:
            print(f"重置失败: {e}")
            return False


# ==================== 扣子Webhook集成示例 ====================

def coze_webhook_handler(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    扣子Webhook事件处理器
    
    在扣子工作流的Webhook节点中调用此函数
    
    Args:
        event_data: 扣子传递的事件数据，包含：
            - session_id: 对话会话ID
            - user_id: 用户ID
            - message: 用户消息
            - text: 用户输入文本
    
    Returns:
        需要返回给扣子的响应
    """
    # 解析扣子事件数据
    session_id = event_data.get("session_id", "default")
    user_input = event_data.get("text", event_data.get("message", ""))
    
    # 初始化集成
    integration = CozeIntegration()
    
    # 调用API
    result = integration.interact(user_id=session_id, message=user_input)
    
    # 构造扣子响应
    return {
        "success": True,
        "response": result.get("response", ""),
        "awakening_level": result.get("awakening_level", {}).get("level", "未知"),
        "stats": result.get("stats", {})
    }


# ==================== 扣子代码节点示例 ====================

COZE_CODE_TEMPLATE = '''
const API_URL = "http://<云电脑IP>:8080";

// 获取用户输入
const userInput = {{user_input}};
const sessionId = {{session_id}};

// 调用唯识进化API
const response = await fetch(`${API_URL}/api/interact`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    user_id: sessionId,
    message: userInput
  })
});

const result = await response.json();

// 输出结果
output.result = result.response;
output.awakening_level = result.awakening_level?.level || "未知";
output.stats = result.stats;
'''

# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 初始化
    integration = CozeIntegration()
    
    # 示例对话
    print("=== 唯识进化引擎 API 测试 ===")
    
    # 1. 发送消息
    result = integration.interact(
        user_id="coze_test_001",
        message="你好，请介绍一下唯识学"
    )
    
    print(f"Agent响应: {result.get('response', '')}")
    print(f"觉醒等级: {result.get('awakening_level', {}).get('level', '未知')}")
    print(f"种子数: {result.get('stats', {}).get('seed_count', 0)}")
    
    # 2. 查看状态
    status = integration.get_status("coze_test_001")
    print(f"\\n当前状态:")
    print(f"  - 觉醒等级: {status.get('awakening_level')}")
    print(f"  - 种子总数: {status.get('seed_count')}")
    print(f"  - 智慧种子: {status.get('wisdom_seeds')}")
    print(f"  - 慈悲种子: {status.get('compassion_seeds')}")
    
    # 3. 继续对话
    result2 = integration.interact(
        user_id="coze_test_001",
        message="什么是阿赖耶识？"
    )
    print(f"\\n追问响应: {result2.get('response', '')}")
