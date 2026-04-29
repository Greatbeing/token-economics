#!/usr/bin/env python3
import argparse
import json
import os
import sys
from typing import Any, Dict, Optional

import requests

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from feishu_mcp import FeishuMcpClient, get_tenant_access_token


def get_app_owner_id(tat: str) -> str:
    app_id = os.environ.get("FEISHU_APP_ID_7619631245038764095", "").strip()
    if not app_id:
        raise Exception("FEISHU_APP_ID_7619631245038764095 环境变量未设置")

    max_retries = 2
    for attempt in range(max_retries):
        try:
            resp = requests.get(
                f"https://open.feishu.cn/open-apis/application/v6/applications/{app_id}",
                headers={"Authorization": f"Bearer {tat}"},
                params={"lang": "zh_cn", "user_id_type": "open_id"},
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") != 0:
                raise Exception(f"获取应用信息失败: {data}")

            owner = data.get("data", {}).get("app", {}).get("owner", {})
            owner_id = owner.get("owner_id")
            if not owner_id:
                raise Exception("无法获取应用所有者 ID")
            return owner_id
        except Exception as e:
            if attempt == max_retries - 1:
                raise e


def add_doc_permission(tat: str, doc_id: str, owner_id: str) -> None:
    max_retries = 2
    for attempt in range(max_retries):
        try:
            resp = requests.post(
                f"https://open.feishu.cn/open-apis/drive/v1/permissions/{doc_id}/members",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {tat}",
                },
                params={"need_notification": "false", "type": "docx"},
                json={
                    "member_type": "openid",
                    "member_id": owner_id,
                    "perm": "full_access",
                    "perm_type": "container",
                    "type": "user",
                },
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") != 0:
                raise Exception(f"添加文档权限失败: {data}")
            return
        except Exception as e:
            if attempt == max_retries - 1:
                raise e


def create_doc(
    title: str,
    markdown: str,
    folder_token: Optional[str] = None,
    wiki_node: Optional[str] = None,
    wiki_space: Optional[str] = None,
    task_id: Optional[str] = None,
) -> Dict[str, Any]:
    try:
        if not task_id and (not title or not markdown):
            return {"status": "error", "message": "标题和 Markdown 内容不能为空"}

        client = FeishuMcpClient(use_tat=True)
        arguments = {}

        if task_id:
            arguments["task_id"] = task_id
        else:
            if not markdown or not title:
                return {"status": "error", "message": "create-doc: 未提供 task_id 时，至少需要提供 markdown 和 title"}
            arguments["title"] = title
            arguments["markdown"] = markdown

            location_args = [arg for arg in [folder_token, wiki_node, wiki_space] if arg]
            if len(location_args) > 1:
                return {"status": "error", "message": "create-doc: folder_token / wiki_node / wiki_space 三者互斥，请只提供一个"}

            if folder_token:
                arguments["folder_token"] = folder_token
            if wiki_node:
                arguments["wiki_node"] = wiki_node
            if wiki_space:
                arguments["wiki_space"] = wiki_space

        result = client.tools_call("create-doc", arguments)

        if result.get("status") == "error":
            return result

        raw_result = result.get("result", result)
        if isinstance(raw_result, dict):
            doc_id = raw_result.get("doc_id")
            if doc_id:
                tat = get_tenant_access_token()
                owner_id = get_app_owner_id(tat)
                add_doc_permission(tat, doc_id, owner_id)

            if doc_id or raw_result.get("task_id"):
                return {
                    "status": "success",
                    "result": raw_result,
                    "message": "文档创建成功" if doc_id else "文档创建已提交异步处理"
                }

        return {"status": "success", "result": raw_result}

    except Exception as e:
        return {"status": "error", "message": f"创建文档失败: {e}"}


def _parse_args(args):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--title", dest="title")
    parser.add_argument("--markdown", dest="markdown")
    parser.add_argument("--folder-token", dest="folder_token")
    parser.add_argument("--wiki-node", dest="wiki_node")
    parser.add_argument("--wiki-space", dest="wiki_space")
    parser.add_argument("--task-id", dest="task_id")
    ns, _ = parser.parse_known_args(args)
    return {
        "title": ns.title,
        "markdown": ns.markdown,
        "folder_token": ns.folder_token,
        "wiki_node": ns.wiki_node,
        "wiki_space": ns.wiki_space,
        "task_id": ns.task_id,
    }


def main(argv=None):
    argv = list(argv or sys.argv[1:])
    if not argv or argv[0] in {"help", "-h", "--help"}:
        print("Usage: create_doc.py --title '...' --markdown '...' [--folder-token 'xxx'] [--wiki-node 'xxx'] [--wiki-space 'xxx'] [--task-id 'xxx']")
        return 0

    parsed = _parse_args(argv)
    result = create_doc(
        title=parsed.get("title"),
        markdown=parsed.get("markdown"),
        folder_token=parsed.get("folder_token"),
        wiki_node=parsed.get("wiki_node"),
        wiki_space=parsed.get("wiki_space"),
        task_id=parsed.get("task_id"),
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
