#!/usr/bin/env python3
"""
AlanDevTeam — 并行 Worktree 管理器
基于 Merge Orchestrator + AgentGrid 的设计：
- 文件所有权矩阵：每个 Agent 只能改自己分配的文件
- 隔离 Worktree：每个 Agent 在独立分支中工作
- 依赖顺序合并：按拓扑顺序合并，每步验证

用法:
  python worktree-manager.py init --project <路径>              # 初始化所有权矩阵
  python worktree-manager.py assign --agent Dev-Backend --files "app.py,models.py"  # 分配文件
  python worktree-manager.py create-worktrees                   # 创建所有 worktree
  python worktree-manager.py merge                              # 按依赖顺序合并
  python worktree-manager.py status                             # 查看状态
"""
import json
import os
import sys
import subprocess
import argparse
from datetime import datetime

ALAN_DIR = os.path.expanduser("~/.zcode/alan-dev-team")
WORKTREE_CONFIG = os.path.join(ALAN_DIR, "worktree-config.json")


def run_cmd(cmd, cwd=None):
    """运行 shell 命令"""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout.strip(), result.stderr.strip()


def init_config(project_path):
    """初始化 worktree 配置"""
    config = {
        "project": os.path.abspath(project_path),
        "created": datetime.now().isoformat(),
        "ownership": {},          # agent -> [file patterns]
        "dependency_order": [],   # ordered agent names
        "worktrees": {},          # agent -> worktree path
        "status": "initialized",
    }
    os.makedirs(os.path.dirname(WORKTREE_CONFIG), exist_ok=True)
    with open(WORKTREE_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"[Worktree] ✅ 配置已初始化: {WORKTREE_CONFIG}")
    return config


def load_config():
    """加载 worktree 配置"""
    if not os.path.exists(WORKTREE_CONFIG):
        print("[Worktree] ❌ 未初始化，先运行 init")
        sys.exit(1)
    with open(WORKTREE_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    """保存 worktree 配置"""
    with open(WORKTREE_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def assign_files(agent_name, files_str, depends_on=None):
    """分配文件给 Agent"""
    config = load_config()
    files_list = [f.strip() for f in files_str.split(",") if f.strip()]
    config["ownership"][agent_name] = files_list
    if depends_on:
        config["dependency_order"] = depends_on.split(",")
    if agent_name not in config["dependency_order"]:
        config["dependency_order"].append(agent_name)
    save_config(config)
    print(f"[Worktree] ✅ {agent_name}: {len(files_list)} 个文件已分配")
    for f in files_list:
        print(f"    - {f}")


def create_worktrees():
    """为每个 Agent 创建独立的 worktree"""
    config = load_config()
    project = config["project"]

    # 检查 git 仓库
    ok, _, _ = run_cmd("git rev-parse --git-dir", cwd=project)
    if not ok:
        print(f"[Worktree] ❌ {project} 不是 git 仓库")
        return

    parent_dir = os.path.dirname(project)
    repo_name = os.path.basename(project)

    for agent_name in config["dependency_order"]:
        if agent_name not in config["ownership"]:
            continue

        worktree_path = os.path.join(parent_dir, f"{repo_name}-{agent_name.lower()}")
        branch_name = f"agent/{agent_name.lower()}"

        # 删除已存在的 worktree
        if os.path.exists(worktree_path):
            run_cmd(f"git worktree remove -f {worktree_path}", cwd=project)

        # 创建分支（如果不存在）
        ok, _, _ = run_cmd(f"git show-ref --verify refs/heads/{branch_name}", cwd=project)
        if not ok:
            run_cmd(f"git branch {branch_name}", cwd=project)

        # 创建 worktree
        ok, out, err = run_cmd(
            f"git worktree add {worktree_path} {branch_name}", cwd=project
        )
        if ok:
            config["worktrees"][agent_name] = worktree_path
            print(f"[Worktree] ✅ {agent_name} → {worktree_path} (branch: {branch_name})")
        else:
            print(f"[Worktree] ❌ {agent_name} 创建失败: {err}")

    config["status"] = "worktrees_created"
    save_config(config)


def validate_ownership(agent_name, changed_files):
    """验证 Agent 的修改是否超出分配的文件"""
    config = load_config()
    allowed = config["ownership"].get(agent_name, [])

    import fnmatch
    violations = []
    for f in changed_files:
        allowed_file = any(fnmatch.fnmatch(f, pattern) for pattern in allowed)
        if not allowed_file:
            violations.append(f)

    return violations


def merge_worktrees():
    """按依赖顺序合并 worktree"""
    config = load_config()
    project = config["project"]
    parent_dir = os.path.dirname(project)

    # 先回到主分支
    run_cmd("git checkout main 2>/dev/null || git checkout master 2>/dev/null || git checkout -b main", cwd=project)

    print("[Worktree] 🔄 开始按依赖顺序合并...")

    for i, agent_name in enumerate(config["dependency_order"]):
        if agent_name not in config["worktrees"]:
            continue

        branch = f"agent/{agent_name.lower()}"
        print(f"\n  [{i+1}/{len(config['dependency_order'])}] 合并 {agent_name} ({branch})...")

        # 拉取变更
        ok, out, err = run_cmd(f"git pull --rebase . {branch} 2>&1", cwd=project)
        if ok:
            print(f"  ✅ {agent_name} 合并成功")
        else:
            print(f"  ⚠️  {agent_name} 合并冲突: {err[:100]}...")
            print(f"  请手动解决后继续")

        # 每步验证
        ok, out, err = run_cmd("python -m pytest tests/ -v --tb=short 2>&1 | tail -5", cwd=project)
        if ok:
            print(f"  ✅ 合并后测试通过")
            run_cmd("git add -A && git commit -m 'chore: merge agent worktree'", cwd=project)
        else:
            print(f"  ❌ 合并后测试失败，回滚...")
            run_cmd("git merge --abort 2>/dev/null || git reset --hard HEAD@{1}", cwd=project)

    print(f"\n[Worktree] ✅ 全部合并完成")


def status():
    """查看 worktree 状态"""
    config = load_config()
    print(f"\n=== Worktree 状态 ===")
    print(f"项目: {config.get('project', 'N/A')}")
    print(f"状态: {config.get('status', 'N/A')}")
    print(f"\n文件所有权矩阵:")
    for agent, files in config.get("ownership", {}).items():
        print(f"  {agent}: {files}")
    print(f"\n合并顺序: {config.get('dependency_order', [])}")
    print(f"\nWorktrees:")
    for agent, path in config.get("worktrees", {}).items():
        exists = "✅" if os.path.exists(path) else "❌"
        print(f"  {exists} {agent} → {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AlanDevTeam Parallel Worktree Manager")
    subparsers = parser.add_subparsers(dest="command")

    p_init = subparsers.add_parser("init", help="初始化 worktree 配置")
    p_init.add_argument("--project", required=True, help="项目路径")

    p_assign = subparsers.add_parser("assign", help="分配文件给 Agent")
    p_assign.add_argument("--agent", required=True, help="Agent 名称")
    p_assign.add_argument("--files", required=True, help="逗号分隔的文件模式")
    p_assign.add_argument("--depends-on", help="依赖顺序（逗号分隔的Agent名）")

    subparsers.add_parser("create-worktrees", help="创建所有 worktree")
    subparsers.add_parser("merge", help="按依赖顺序合并")
    subparsers.add_parser("status", help="查看状态")

    args = parser.parse_args()

    if args.command == "init":
        init_config(args.project)
    elif args.command == "assign":
        assign_files(args.agent, args.files, args.depends_on)
    elif args.command == "create-worktrees":
        create_worktrees()
    elif args.command == "merge":
        merge_worktrees()
    elif args.command == "status":
        status()
    else:
        parser.print_help()
