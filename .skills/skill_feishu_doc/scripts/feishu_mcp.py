import base64
import json
import os
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

@dataclass
class HttpClient:
    default_headers: Dict[str, str]
    timeout_s: int = 30
    max_retries: int = 2
    backoff_s: float = 0.6

    def __post_init__(self) -> None:
        self._session = requests.Session()

    def post_json(self, url: str, payload: Dict[str, Any], timeout_s: Optional[int] = None) -> Dict[str, Any]:
        last_err: Optional[Exception] = None
        timeout = timeout_s or self.timeout_s

        for attempt in range(self.max_retries):
            try:
                resp = self._session.post(url, headers=self.default_headers, json=payload, timeout=timeout)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                last_err = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.backoff_s * (attempt + 1))
        raise last_err or RuntimeError("request failed")


def _unwrap_json_rpc_result(v: Any) -> Any:
    if not isinstance(v, dict):
        return v

    has_json_rpc = isinstance(v.get("jsonrpc"), str)
    has_id = "id" in v
    has_result = "result" in v
    has_error = "error" in v

    if has_json_rpc and (has_result or has_error):
        if has_error:
            err = v.get("error", {})
            if isinstance(err, dict) and isinstance(err.get("message"), str):
                raise Exception(err["message"])
            raise Exception("MCP error: 无法解析错误消息")
        return _unwrap_json_rpc_result(v.get("result"))

    if not has_json_rpc and not has_id and has_result and not has_error:
        return _unwrap_json_rpc_result(v.get("result"))

    return v


_TAT_CACHE: Dict[str, Any] = {"token": None, "expire_at": 0}


def get_tenant_access_token() -> str:
    global _TAT_CACHE
    now = time.time()
    if _TAT_CACHE["token"] and _TAT_CACHE["expire_at"] > now:
        return _TAT_CACHE["token"]

    app_id = os.environ.get("FEISHU_APP_ID_7619631245038764095", "").strip()
    app_secret = os.environ.get("FEISHU_APP_SECRET_7619631245038764095", "").strip()
    if not app_id or not app_secret:
        raise Exception("FEISHU_APP_ID_7619631245038764095 或 FEISHU_APP_SECRET_7619631245038764095 环境变量未设置")

    max_retries = 2
    for attempt in range(max_retries):
        try:
            resp = requests.post(
                "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
                headers={"Content-Type": "application/json"},
                json={"app_id": app_id, "app_secret": app_secret},
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") != 0:
                raise Exception(f"获取 tenant_access_token 失败: {data}")

            token = data["tenant_access_token"]
            expire = data.get("expire", 7200)
            _TAT_CACHE["token"] = token
            _TAT_CACHE["expire_at"] = now + expire - 300
            return token
        except Exception as e:
            if attempt == max_retries - 1:
                raise e


class FeishuMcpClient:
    def __init__(self, use_tat: bool = True):
        self.mcp_endpoint = os.environ.get("FEISHU_MCP_ENDPOINT", "https://mcp.feishu.cn/mcp").strip()
        self.use_tat = use_tat
        self._request_id = 0

    def _get_next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _get_tat(self) -> str:
        return get_tenant_access_token()

    def _get_headers(self, allowed_tools: str) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }
        headers["X-Lark-MCP-TAT"] = self._get_tat()
        if allowed_tools:
            headers["X-Lark-MCP-Allowed-Tools"] = allowed_tools
        return headers

    def initialize(self) -> Dict[str, Any]:
        body = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "initialize",
        }
        resp = requests.post(self.mcp_endpoint, headers=self._get_headers(""), json=body, timeout=60)
        resp.raise_for_status()
        return resp.json()

    def tools_list(self, allowed_tools: str = "") -> Dict[str, Any]:
        body = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "tools/list",
        }
        resp = requests.post(self.mcp_endpoint, headers=self._get_headers(allowed_tools), json=body, timeout=60)
        resp.raise_for_status()
        return resp.json()

    def tools_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        body = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
        }

        try:
            resp = requests.post(self.mcp_endpoint, headers=self._get_headers(tool_name), json=body, timeout=60)
            resp.raise_for_status()
            data = resp.json()

            if "error" in data:
                err = data.get("error", {})
                return {"status": "error", "message": f"MCP error {err.get('code')}: {err.get('message')}"}

            result = _unwrap_json_rpc_result(data.get("result"))

            if isinstance(result, dict) and "content" in result:
                content = result.get("content", [])
                if isinstance(content, list) and len(content) == 1:
                    item = content[0]
                    if isinstance(item, dict) and item.get("type") == "text":
                        text = item.get("text", "")
                        try:
                            return json.loads(text)
                        except json.JSONDecodeError:
                            return {"status": "success", "result": text}

            return {"status": "success", "result": result}

        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"HTTP 请求失败: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def call_tool_with_init(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        init_result = self.initialize()
        if "error" in init_result:
            return {"status": "error", "message": f"初始化失败: {init_result.get('error')}"}

        tools_result = self.tools_list(tool_name)
        if "error" in tools_result:
            return {"status": "error", "message": f"获取工具列表失败: {tools_result.get('error')}"}

        return self.tools_call(tool_name, arguments)
