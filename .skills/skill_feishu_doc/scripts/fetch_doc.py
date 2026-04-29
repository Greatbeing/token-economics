#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any, Dict, Optional

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from feishu_mcp import FeishuMcpClient


def fetch_doc(
    doc_id: str,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Dict[str, Any]:
    try:
        if not doc_id:
            return {"status": "error", "message": "文档 ID 不能为空"}

        client = FeishuMcpClient(use_tat=True)

        init_result = client.initialize()
        if "error" in init_result:
            return {"status": "error", "message": f"初始化失败: {init_result.get('error')}"}

        tools_result = client.tools_list("fetch-doc")
        if "error" in tools_result:
            return {"status": "error", "message": f"获取工具列表失败: {tools_result.get('error')}"}

        arguments = {"doc_id": doc_id}
        if offset is not None:
            arguments["offset"] = offset
        if limit is not None:
            arguments["limit"] = limit

        result = client.tools_call("fetch-doc", arguments)

        if result.get("status") == "error":
            return result

        raw_result = result.get("result", result)
        if isinstance(raw_result, dict):
            if "title" in raw_result or "markdown" in raw_result:
                return {
                    "status": "success",
                    "result": raw_result,
                    "message": "获取文档成功"
                }

        return {"status": "success", "result": raw_result}

    except Exception as e:
        return {"status": "error", "message": f"获取文档失败: {e}"}


def _parse_args(args):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--doc-id", dest="doc_id")
    parser.add_argument("--offset", dest="offset", type=int)
    parser.add_argument("--limit", dest="limit", type=int)
    ns, _ = parser.parse_known_args(args)
    return {
        "doc_id": ns.doc_id,
        "offset": ns.offset,
        "limit": ns.limit,
    }


def main(argv=None):
    argv = list(argv or sys.argv[1:])
    if not argv or argv[0] in {"help", "-h", "--help"}:
        print("Usage: fetch_doc.py --doc-id 'xxx' [--offset 0] [--limit 10000]")
        return 0

    parsed = _parse_args(argv)
    result = fetch_doc(
        doc_id=parsed.get("doc_id"),
        offset=parsed.get("offset"),
        limit=parsed.get("limit"),
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
