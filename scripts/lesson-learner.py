#!/usr/bin/env python3
"""
AlanDevTeam — 长期记忆系统（Lesson Learner）
项目结束后自动总结经验和教训，用于优化下次项目

用法:
  python lesson-learner.py --project <项目名> --dir <项目路径>
  python lesson-learner.py --recall <项目名>   # 回忆上次的经验
  python lesson-learner.py --list              # 列出所有记忆
"""
import json
import os
import sys
import argparse
from datetime import datetime

MEMORY_DIR = os.path.expanduser("~/.zcode/alan-dev-team/memory")
EXPERIENCES_DIR = os.path.join(MEMORY_DIR, "experiences")
AGENT_PROFILES_DIR = os.path.join(MEMORY_DIR, "agent-profiles")
BEST_PRACTICES_FILE = os.path.join(MEMORY_DIR, "best-practices.json")


def ensure_dirs():
    for d in [MEMORY_DIR, EXPERIENCES_DIR, AGENT_PROFILES_DIR]:
        os.makedirs(d, exist_ok=True)


def load_best_practices():
    """加载团队最佳实践"""
    if os.path.exists(BEST_PRACTICES_FILE):
        with open(BEST_PRACTICES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"practices": [], "last_updated": None}


def save_best_practices(practices):
    """保存团队最佳实践"""
    with open(BEST_PRACTICES_FILE, "w", encoding="utf-8") as f:
        json.dump(practices, f, ensure_ascii=False, indent=2)


def learn_from_project(project_name, project_dir, lessons, agent_improvements):
    """从项目经验中学习"""
    ensure_dirs()

    # 1. 保存项目经验
    experience = {
        "project": project_name,
        "path": project_dir,
        "date": datetime.now().isoformat(),
        "lessons_learned": lessons,
        "agent_improvements": agent_improvements,
    }
    exp_file = os.path.join(EXPERIENCES_DIR, f"project-{project_name.lower().replace(' ', '-')}.json")
    with open(exp_file, "w", encoding="utf-8") as f:
        json.dump(experience, f, ensure_ascii=False, indent=2)

    # 2. 更新 Agent 画像
    for agent_name, improvement in agent_improvements.items():
        profile_file = os.path.join(AGENT_PROFILES_DIR, f"{agent_name.lower()}.json")
        if os.path.exists(profile_file):
            with open(profile_file, "r", encoding="utf-8") as f:
                profile = json.load(f)
        else:
            profile = {"agent": agent_name, "lessons": []}

        profile["lessons"].append({
            "lesson": improvement,
            "from_project": project_name,
            "date": datetime.now().isoformat(),
        })
        with open(profile_file, "w", encoding="utf-8") as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)

    # 3. 更新最佳实践库
    practices = load_best_practices()
    for lesson in lessons:
        if lesson not in practices["practices"]:
            practices["practices"].append(lesson)
    practices["last_updated"] = datetime.now().isoformat()
    save_best_practices(practices)

    print(f"[记忆] ✅ 项目 '{project_name}' 的经验已记录")
    print(f"   - {len(lessons)} 条经验教训")
    print(f"   - {len(agent_improvements)} 个 Agent 画像已更新")


def recall_memory(project_name):
    """回忆指定项目的经验"""
    exp_file = os.path.join(EXPERIENCES_DIR, f"project-{project_name.lower().replace(' ', '-')}.json")
    if not os.path.exists(exp_file):
        print(f"[记忆] ❌ 没有找到 '{project_name}' 的经验记录")
        return

    with open(exp_file, "r", encoding="utf-8") as f:
        exp = json.load(f)

    print(f"\n=== 记忆: {exp['project']} ===")
    print(f"日期: {exp['date']}")
    print(f"\n经验教训:")
    for i, lesson in enumerate(exp["lessons_learned"], 1):
        print(f"  {i}. {lesson}")
    print(f"\nAgent 改进:")
    for agent, imp in exp["agent_improvements"].items():
        print(f"  {agent}: {imp}")


def list_memories():
    """列出所有记忆"""
    ensure_dirs()
    experiences = []
    if os.path.isdir(EXPERIENCES_DIR):
        for fname in sorted(os.listdir(EXPERIENCES_DIR)):
            if fname.endswith(".json"):
                with open(os.path.join(EXPERIENCES_DIR, fname), "r", encoding="utf-8") as f:
                    exp = json.load(f)
                experiences.append(exp)

    if not experiences:
        print("[记忆] 还没有任何项目经验记录")
        return

    print(f"[记忆] 共有 {len(experiences)} 个项目经验:\n")
    for exp in experiences:
        print(f"  📁 {exp['project']} ({exp['date'][:10]})")
        print(f"     {len(exp['lessons_learned'])} 条经验, {len(exp['agent_improvements'])} 个 Agent 改进")


def get_agent_profile(agent_name):
    """获取 Agent 的改进建议（Orchestrator 在派发 Agent 时调用）"""
    profile_file = os.path.join(AGENT_PROFILES_DIR, f"{agent_name.lower()}.json")
    if not os.path.exists(profile_file):
        return None

    with open(profile_file, "r", encoding="utf-8") as f:
        profile = json.load(f)

    # 生成改进建议文本
    if not profile.get("lessons"):
        return None

    suggestions = []
    for lesson in profile["lessons"][-3:]:  # 最近3条
        suggestions.append(f"- {lesson['lesson']} (来自项目: {lesson['from_project']})")

    return "\n".join(suggestions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AlanDevTeam 长期记忆系统")
    parser.add_argument("--project", help="项目名称")
    parser.add_argument("--dir", help="项目路径")
    parser.add_argument("--learn", nargs="*", help="要学习的经验教训")
    parser.add_argument("--agent", nargs="*", help="Agent 改进建议 (格式: Agent名:改进内容)")
    parser.add_argument("--recall", help="回忆指定项目的经验")
    parser.add_argument("--list", action="store_true", help="列出所有记忆")
    parser.add_argument("--profile", help="获取指定 Agent 的改进建议")
    args = parser.parse_args()

    if args.list:
        list_memories()
    elif args.recall:
        recall_memory(args.recall)
    elif args.profile:
        suggestions = get_agent_profile(args.profile)
        if suggestions:
            print(suggestions)
        else:
            print(f"[记忆] {args.profile} 没有历史经验记录")
    elif args.project and args.learn is not None:
        # 学习模式
        agent_improvements = {}
        if args.agent:
            for item in args.agent:
                if ":" in item:
                    agent, imp = item.split(":", 1)
                    agent_improvements[agent] = imp
        learn_from_project(args.project, args.dir or "", args.learn, agent_improvements)
    else:
        parser.print_help()
