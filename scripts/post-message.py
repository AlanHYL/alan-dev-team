#!/usr/bin/env python3
"""
AlanDevTeam — 写入消息到消息池
被 zcode PostToolUse Hook 调用，实现 Observe 步骤

用法:
  python post-message.py --type code_done --source Dev --file app.py --task TASK-004
  python post-message.py --type review_needed --source Reviewer --file app.py --task TASK-004
"""
import json
import sys
import os
import argparse
from datetime import datetime


MESSAGE_POOL_DIR = os.path.expanduser("~/.zcode/alan-dev-team/message-pool")


def post_message(msg_type, source, file_path, task="", detail=""):
    """写入一条消息到消息池"""
    os.makedirs(MESSAGE_POOL_DIR, exist_ok=True)

    now = datetime.now()
    msg_id = f"msg_{now.strftime('%Y%m%d_%H%M%S')}_{source}"
    filename = f"{now.strftime('%Y%m%d_%H%M%S')}_{msg_type}_{source}.json"

    message = {
        "id": msg_id,
        "timestamp": now.isoformat(),
        "type": msg_type,
        "source": source,
        "file": file_path,
        "task": task,
        "detail": detail,
        "status": "unprocessed",
    }

    filepath = os.path.join(MESSAGE_POOL_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(message, f, ensure_ascii=False, indent=2)

    print(f"[消息池] 写入消息: {filename}")
    print(f"  类型: {msg_type} | 来源: {source} | 文件: {file_path}")
    return filepath


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="写入消息到 AlanDevTeam 消息池")
    parser.add_argument("--type", required=True, help="消息类型: code_done / review_needed / test_failed / review_passed / security_check / bug_found")
    parser.add_argument("--source", required=True, help="消息来源: Dev-Backend / Dev-Frontend / Reviewer / QA / Security")
    parser.add_argument("--file", default="", help="关联文件路径")
    parser.add_argument("--task", default="", help="关联任务编号")
    parser.add_argument("--detail", default="", help="详细信息")
    args = parser.parse_args()

    post_message(args.type, args.source, args.file, args.task, args.detail)
