#!/usr/bin/env python3
"""
AlanDevTeam — 读取并处理消息池中的未处理消息
被 Orchestrator 调用，实现 Act 步骤

用法:
  python process-messages.py                    # 列出所有未处理消息
  python process-messages.py --handle           # 处理所有消息（派发对应Agent）
  python process-messages.py --type review_needed  # 筛选特定类型
"""
import json
import os
import sys
import argparse
from datetime import datetime


MESSAGE_POOL_DIR = os.path.expanduser("~/.zcode/alan-dev-team/message-pool")


def get_unprocessed_messages(msg_type=None):
    """读取所有未处理的消息"""
    messages = []
    if not os.path.isdir(MESSAGE_POOL_DIR):
        return messages

    for fname in sorted(os.listdir(MESSAGE_POOL_DIR)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(MESSAGE_POOL_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                msg = json.load(f)
            if msg.get("status") == "unprocessed":
                if msg_type and msg.get("type") != msg_type:
                    continue
                messages.append((fpath, msg))
        except (json.JSONDecodeError, OSError):
            continue
    return messages


def suggest_action(msg):
    """根据消息类型建议要派发的 Agent"""
    action_map = {
        "code_done": "派发 Reviewer 审查代码",
        "review_needed": "Review 结果已出，通知对应 Dev 修复",
        "test_failed": "通知对应 Dev 修复测试失败",
        "review_passed": "审查通过，可进入下一阶段",
        "bug_found": "通知对应 Dev 修复 bug",
        "security_check": "派发 Security Agent 做安全审计",
        "project_done": "启动 LessonLearner 生成经验总结",
    }
    return action_map.get(msg.get("type", ""), "未知消息类型，请人工判断")


def main():
    parser = argparse.ArgumentParser(description="处理 AlanDevTeam 消息池")
    parser.add_argument("--handle", action="store_true", help="处理消息（显示建议操作）")
    parser.add_argument("--type", default=None, help="筛选特定类型的消息")
    args = parser.parse_args()

    messages = get_unprocessed_messages(args.type)

    if not messages:
        print("[消息池] 没有未处理的消息")
        return

    print(f"[消息池] 未处理消息 ({len(messages)} 条):")
    print("=" * 60)

    for fpath, msg in messages:
        print(f"\n📌 {msg.get('id', 'unknown')}")
        print(f"   类型: {msg.get('type')}")
        print(f"   来源: {msg.get('source')}")
        print(f"   文件: {msg.get('file')}")
        print(f"   时间: {msg.get('timestamp')}")
        if args.handle:
            action = suggest_action(msg)
            print(f"   ▶ 建议操作: {action}")

    if args.handle:
        print("\n" + "=" * 60)
        print("要处理这些消息，运行:")
        for fpath, msg in messages:
            fname = os.path.basename(fpath)
            print(f"  python ~/.zcode/alan-dev-team/scripts/ack-message.py {fname}")


if __name__ == "__main__":
    main()
