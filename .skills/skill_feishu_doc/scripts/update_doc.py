#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any, Dict, Optional

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from feishu_mcp import FeishuMcpClient


def update_doc(
    doc_id: str,
    mode: str,
    markdown: Optional[str] = None,
    selection_with_ellipsis: Optional[str] = None,
    selection_by_title: Optional[str] = None,
    new_title: Optional[str] = None,
    task_id: Optional[str] = None,
) -> Dict[str, Any]:
    try:
        if not task_id and not doc_id:
            return {"status": "error", "message": "文档 ID 不能为空"}

        valid_modes = ["overwrite", "append", "replace_range", "replace_all", "insert_before", "insert_after", "delete_range"]
        if mode not in valid_modes:
            return {"status": "error", "message": f"update-doc: mode 必须是以下之一: {', '.join(valid_modes)}"}

        client = FeishuMcpClient(use_tat=True)

        init_result = client.initialize()
        if "error" in init_result:
            return {"status": "error", "message": f"初始化失败: {init_result.get('error')}"}

        tools_result = client.tools_list("update-doc")
        if "error" in tools_result:
            return {"status": "error", "message": f"获取工具列表失败: {tools_result.get('error')}"}

        arguments = {"mode": mode}

        if task_id:
            arguments["task_id"] = task_id
        else:
            if not doc_id:
                return {"status": "error", "message": "update-doc: 未提供 task_id 时必须提供 doc_id"}

            arguments["doc_id"] = doc_id

            need_selection = mode in ["replace_range", "insert_before", "insert_after", "delete_range"]
            if need_selection:
                has_ellipsis = bool(selection_with_ellipsis)
                has_title = bool(selection_by_title)
                if (has_ellipsis and has_title) or (not has_ellipsis and not has_title):
                    return {
                        "status": "error",
                        "message": "update-doc: mode 为 replace_range/insert_before/insert_after/delete_range 时，selection_with_ellipsis 与 selection_by_title 必须二选一"
                    }
                if selection_with_ellipsis:
                    arguments["selection_with_ellipsis"] = selection_with_ellipsis
                if selection_by_title:
                    arguments["selection_by_title"] = selection_by_title

            need_markdown = mode != "delete_range"
            if need_markdown and not markdown:
                return {"status": "error", "message": f"update-doc: mode={mode} 时必须提供 markdown"}

            if markdown:
                arguments["markdown"] = markdown

        if new_title:
            arguments["new_title"] = new_title

        result = client.tools_call("update-doc", arguments)

        if result.get("status") == "error":
            return result

        raw_result = result.get("result", result)
        if isinstance(raw_result, dict):
            if raw_result.get("success") or raw_result.get("task_id"):
                return {
                    "status": "success",
                    "result": raw_result,
                    "message": raw_result.get("message", "文档更新成功")
                }

        return {"status": "success", "result": raw_result}

    except Exception as e:
        return {"status": "error", "message": f"更新文档失败: {e}"}


def _parse_args(args):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--doc-id", dest="doc_id")
    parser.add_argument("--mode", dest="mode")
    parser.add_argument("--markdown", dest="markdown")
    parser.add_argument("--selection-with-ellipsis", dest="selection_with_ellipsis")
    parser.add_argument("--selection-by-title", dest="selection_by_title")
    parser.add_argument("--new-title", dest="new_title")
    parser.add_argument("--task-id", dest="task_id")
    ns, _ = parser.parse_known_args(args)
    return {
        "doc_id": ns.doc_id,
        "mode": ns.mode,
        "markdown": ns.markdown,
        "selection_with_ellipsis": ns.selection_with_ellipsis,
        "selection_by_title": ns.selection_by_title,
        "new_title": ns.new_title,
        "task_id": ns.task_id,
    }


def main(argv=None):
    argv = list(argv or sys.argv[1:])
    if not argv or argv[0] in {"help", "-h", "--help"}:
        print("Usage: update_doc.py --doc-id 'xxx' --mode 'xxx' --markdown '...' [--selection-with-ellipsis 'xxx'] [--selection-by-title 'xxx'] [--new-title 'xxx'] [--task-id 'xxx']")
        return 0

    parsed = _parse_args(argv)
    result = update_doc(
        doc_id=parsed.get("doc_id"),
        mode=parsed.get("mode"),
        markdown=parsed.get("markdown"),
        selection_with_ellipsis=parsed.get("selection_with_ellipsis"),
        selection_by_title=parsed.get("selection_by_title"),
        new_title=parsed.get("new_title"),
        task_id=parsed.get("task_id"),
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
