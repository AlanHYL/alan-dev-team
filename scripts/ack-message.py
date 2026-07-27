#!/usr/bin/env python3
"""
AlanDevTeam — 标记消息为已处理

用法:
  python ack-message.py <文件名>
  python ack-message.py 20260728_120000_code_done_dev-backend.json
"""
import json
import os
import sys

MESSAGE_POOL_DIR = os.path.expanduser("~/.zcode/alan-dev-team/message-pool")


def ack_message(filename):
    """标记消息为已处理"""
    if not filename.endswith(".json"):
        filename += ".json"

    fpath = os.path.join(MESSAGE_POOL_DIR, filename)
    if not os.path.exists(fpath):
        print(f"❌ 消息文件不存在: {fpath}")
        return False

    with open(fpath, "r", encoding="utf-8") as f:
        msg = json.load(f)

    msg["status"] = "done"
    msg["processed_at"] = __import__("datetime").datetime.now().isoformat()

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(msg, f, ensure_ascii=False, indent=2)

    print(f"✅ 消息已标记为 done: {filename} ({msg.get('type')} from {msg.get('source')})")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python ack-message.py <文件名>")
        sys.exit(1)
    ack_message(sys.argv[1])
