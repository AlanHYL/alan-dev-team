#!/usr/bin/env python3
"""
AlanDevTeam CLI — 统一入口
一个命令启动全自动编码团队

用法:
  alan init <项目名>         创建新项目脚手架
  alan start <项目路径>      启动全自动开发
  alan status [项目路径]     查看进度仪表盘
  alan log [--tail]          查看日志
  alan preview <项目路径>    沙箱模式预览变更
  alan team                  查看团队阵容
  alan help                  查看帮助
"""
import argparse
import json
import os
import sys
import subprocess
import time
from datetime import datetime

# 加载外部模板（支持从文件加载，避免字符串转义问题）
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")

ALAN_DIR = os.path.expanduser("~/.zcode/alan-dev-team")
LOG_FILE = os.path.join(ALAN_DIR, "logs", "alan.log")
MESSAGE_POOL_DIR = os.path.join(ALAN_DIR, "message-pool")
SCRIPTS_DIR = os.path.join(ALAN_DIR, "scripts")
PROJECTS_DIR = os.path.expanduser("~/Desktop")

# ──────────────────────────────────────────────
# 日志系统
# ──────────────────────────────────────────────

def log(level, message, detail=""):
    """集中式日志记录"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": timestamp,
        "level": level,
        "message": message,
        "detail": detail,
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"[{timestamp}] {level}: {message}")


def read_logs(tail=False, level=None):
    """读取日志"""
    if not os.path.exists(LOG_FILE):
        print("[日志] 还没有日志记录")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []
    for line in lines:
        try:
            entry = json.loads(line.strip())
            if level and entry.get("level") != level:
                continue
            entries.append(entry)
        except json.JSONDecodeError:
            continue

    if tail:
        entries = entries[-20:]

    print(f"\n=== AlanDevTeam 日志 ({'最近20条' if tail else '全部'}) ===\n")
    for entry in entries:
        icon = {"INFO": "ℹ️", "WARN": "⚠️", "ERROR": "❌", "DONE": "✅"}.get(entry["level"], "📝")
        print(f"  {icon} [{entry['timestamp']}] {entry['message']}")
        if entry.get("detail"):
            print(f"     {entry['detail']}")
    print(f"\n共 {len(entries)} 条记录")


# ──────────────────────────────────────────────
# 项目脚手架
# ──────────────────────────────────────────────

TEMPLATES = {
    "web-flask": {
        "description": "Flask Web 应用（HTML/CSS/JS + Python Flask + SQLite）",
        "files": {
            "app.py": """import os
from flask import Flask, jsonify, request, Response, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() in ('true', '1', 'yes')
    app.run(debug=debug)
""",
            "models.py": """from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()
""",
            "requirements.txt": "flask>=3.0\nflask-sqlalchemy>=3.1\npytest>=8.0\npytest-cov>=5.0\n",
            "templates/index.html": """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ project_name }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        <h1>{{ project_name }}</h1>
        <p>由 AlanDevTeam 全自动生成</p>
    </div>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
""",
            "static/css/style.css": "/* {{ project_name }} - Styles */\n* { margin: 0; padding: 0; box-sizing: border-box; }\nbody { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; color: #1a2332; }\n",
            "static/js/script.js": "// {{ project_name }} - Scripts\nconsole.log('{{ project_name }} loaded');\n",
            ".gitignore": "__pycache__/\n*.pyc\n*.db\n.env\n.DS_Store\n",
        },
        "post_create": "pip install -r requirements.txt && git init && git add -A && git commit -m 'chore: init project'"
    },
    "web-react": {
        "description": "React + Vite 前端应用",
        "files": {
            "package.json": '{"name": "{{ project_name }}", "version": "1.0.0", "private": true}\n',
            "index.html": '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>{{ project_name }}</title></head><body><div id="root"></div></body></html>\n',
            ".gitignore": "node_modules/\ndist/\n.env\n",
        },
        "post_create": "npm init -y && git init && git add -A && git commit -m 'chore: init project'"
    },
    "api": {
        "description": "Python FastAPI 后端服务",
        "files": {
            "main.py": "from fastapi import FastAPI\n\napp = FastAPI(title='{{ project_name }}')\n\n@app.get('/')\ndef root():\n    return {'message': '{{ project_name }} running'}\n",
            "requirements.txt": "fastapi>=0.100\nuvicorn>=0.20\npytest>=8.0\n",
            ".gitignore": "__pycache__/\n*.pyc\n.env\n",
        },
        "post_create": "pip install -r requirements.txt && git init && git add -A && git commit -m 'chore: init project'"
    },
    "cli": {
        "description": "Python CLI 工具",
        "files": {
            "main.py": "#!/usr/bin/env python3\nimport argparse\n\ndef main():\n    parser = argparse.ArgumentParser(description='{{ project_name }}')\n    parser.add_argument('--name', default='World', help='Your name')\n    args = parser.parse_args()\n    print(f'Hello, {args.name}!')\n\nif __name__ == '__main__':\n    main()\n",
            "requirements.txt": "pytest>=8.0\n",
            ".gitignore": "__pycache__/\n*.pyc\n.env\n",
        },
        "post_create": "chmod +x main.py && git init && git add -A && git commit -m 'chore: init project'"
    },
}


def load_template(project_type):
    """加载模板（优先从外部文件加载）"""
    # 外部文件模板
    ext_file = os.path.join(TEMPLATES_DIR, f"{project_type}.json")
    if os.path.exists(ext_file):
        with open(ext_file, "r", encoding="utf-8") as f:
            return json.load(f)
    # 内置模板
    if project_type in TEMPLATES:
        return TEMPLATES[project_type]
    return None


def init_project(project_name, project_type="web-flask", output_dir=None):
    """创建项目脚手架"""
    template = load_template(project_type)
    if not template:
        print(f"❌ 未知项目类型: {project_type}")
        print(f"   可用类型: {', '.join(list(TEMPLATES.keys()) + ['saas'])}")
        return
    base_dir = os.path.join(output_dir, project_name) if output_dir else os.path.join(PROJECTS_DIR, project_name)

    if os.path.exists(base_dir):
        print(f"❌ 目录已存在: {base_dir}")
        return

    log("INFO", f"创建项目: {project_name} ({template['description']})")

    # 创建目录结构
    dirs = set()
    for filepath in template["files"]:
        dirpath = os.path.dirname(filepath)
        if dirpath:
            dirs.add(dirpath)

    for d in dirs:
        os.makedirs(os.path.join(base_dir, d), exist_ok=True)

    # 写入文件
    for filepath, content in template["files"].items():
        full_path = os.path.join(base_dir, filepath)
        rendered = content.replace("{{ project_name }}", project_name)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"  📄 {filepath}")

    # 创建 artifacts 目录
    for d in ["artifacts/board", "artifacts/specs", "artifacts/reviews", "artifacts/reports"]:
        os.makedirs(os.path.join(base_dir, d), exist_ok=True)

    # 运行 post_create
    if template["post_create"]:
        print("\n[脚手架] 运行初始化命令...")
        os.chdir(base_dir)
        script = template["post_create"].replace("&&", "\n")
        result = subprocess.run(script, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            err = result.stderr.strip()[:200]
            if err:
                print(f"  ℹ️  {err}")
        else:
            print(f"  ✅ 初始化完成")

    log("DONE", f"项目 '{project_name}' 脚手架已创建", f"路径: {base_dir}")
    print(f"\n✅ 项目 '{project_name}' 已创建: {base_dir}")
    print(f"   类型: {template['description']}")
    print(f"   启动: alan start {base_dir}")


# ──────────────────────────────────────────────
# 进度仪表盘
# ──────────────────────────────────────────────

def show_status(project_dir=None):
    """显示进度仪表盘"""
    print("\n" + "=" * 60)
    print("  AlanDevTeam — 进度仪表盘")
    print("=" * 60)

    # 1. 消息池状态
    unprocessed = 0
    total = 0
    if os.path.isdir(MESSAGE_POOL_DIR):
        for fname in os.listdir(MESSAGE_POOL_DIR):
            if fname.endswith(".json"):
                total += 1
                fpath = os.path.join(MESSAGE_POOL_DIR, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        msg = json.load(f)
                    if msg.get("status") == "unprocessed":
                        unprocessed += 1
                except json.JSONDecodeError:
                    pass

    print(f"\n📨 消息池:")
    print(f"   总计: {total} 条 | 未处理: {unprocessed} 条")

    if unprocessed > 0:
        print(f"\n   未处理消息:")
        for fname in sorted(os.listdir(MESSAGE_POOL_DIR)):
            fpath = os.path.join(MESSAGE_POOL_DIR, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    msg = json.load(f)
                if msg.get("status") == "unprocessed":
                    print(f"     🆕 [{msg['type']}] {msg['source']} → {msg.get('file', 'N/A')}")
            except json.JSONDecodeError:
                pass

    # 2. 项目状态
    if project_dir and os.path.exists(project_dir):
        print(f"\n📁 项目: {project_dir}")

        # 检测git状态
        result = subprocess.run(
            "git rev-parse --short HEAD 2>/dev/null && git log --oneline -1",
            shell=True, cwd=project_dir, capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"   Git: {result.stdout.strip()[:80]}")

        # 检测测试
        result = subprocess.run(
            "python -m pytest tests/ -v --tb=no 2>&1 | tail -3",
            shell=True, cwd=project_dir, capture_output=True, text=True
        )
        if "passed" in result.stdout:
            import re
            match = re.search(r'(\d+) passed', result.stdout)
            if match:
                print(f"   🧪 测试: {match.group(1)} 个通过")

        # 检测 artifacts
        artifacts_dir = os.path.join(project_dir, "artifacts")
        if os.path.isdir(artifacts_dir):
            reviews = len(os.listdir(os.path.join(artifacts_dir, "reviews"))) if os.path.isdir(os.path.join(artifacts_dir, "reviews")) else 0
            print(f"   📋 Review 记录: {reviews} 条")

    # 3. 团队经验
    memory_file = os.path.join(ALAN_DIR, "memory", "best-practices.json")
    if os.path.exists(memory_file):
        with open(memory_file, "r", encoding="utf-8") as f:
            practices = json.load(f)
        print(f"\n🧠 团队经验: {len(practices.get('practices', []))} 条")
        for p in practices.get("practices", [])[-3:]:
            print(f"   • {p[:60]}...")

    # 4. 日志统计
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            log_count = sum(1 for _ in f)
        print(f"\n📝 日志: {log_count} 条")
        print(f"   查看: alan log --tail")

    print("\n" + "=" * 60)


# ──────────────────────────────────────────────
# 沙箱模式
# ──────────────────────────────────────────────

def preview_changes(project_dir):
    """沙箱模式: 预览将要发生的变更"""
    if not os.path.exists(project_dir):
        print(f"❌ 项目不存在: {project_dir}")
        return

    print(f"\n=== 沙箱预览: {project_dir} ===\n")

    # 检查 git 状态
    result = subprocess.run(
        "git status --short 2>/dev/null",
        shell=True, cwd=project_dir, capture_output=True, text=True
    )
    if result.stdout.strip():
        print("📝 待变更的文件:")
        for line in result.stdout.strip().split("\n"):
            print(f"  {line}")
    else:
        print("📝 工作区干净，无待变更")

    # 检查未处理消息
    print("\n📨 待处理消息:")
    for fname in sorted(os.listdir(MESSAGE_POOL_DIR)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(MESSAGE_POOL_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                msg = json.load(f)
            if msg.get("status") == "unprocessed":
                print(f"  🆕 [{msg['type']}] {msg['source']}")
                print(f"    文件: {msg.get('file', 'N/A')}")
                print(f"    详情: {msg.get('detail', 'N/A')}")
        except json.JSONDecodeError:
            pass

    # 预测将要派发的 Agent
    print("\n🤖 将要派发的 Agent:")
    for fname in sorted(os.listdir(MESSAGE_POOL_DIR)):
        if not fname.endswith(".json"):
            continue
        try:
            with open(os.path.join(MESSAGE_POOL_DIR, fname), "r", encoding="utf-8") as f:
                msg = json.load(f)
            if msg.get("status") == "unprocessed":
                action_map = {
                    "code_done": "Reviewer 审查代码",
                    "test_failed": "Dev 修复测试",
                    "bug_found": "Dev 修复 bug",
                    "security_check": "Security 安全审计",
                    "project_done": "LessonLearner 总结",
                }
                action = action_map.get(msg["type"], "Orchestrator 处理")
                print(f"  ▶ {action} (来自 {msg['source']})")
        except json.JSONDecodeError:
            pass

    print(f"\n⚠️  沙箱模式仅预览，不执行任何变更")
    print(f"   要执行: alan start {project_dir}")


# ──────────────────────────────────────────────
# 启动全自动开发
# ──────────────────────────────────────────────

def start_development(project_dir):
    """启动全自动开发流程"""
    if not os.path.exists(project_dir):
        print(f"❌ 项目不存在: {project_dir}")
        print(f"   先创建项目: alan init <项目名>")
        return

    log("INFO", f"启动全自动开发: {project_dir}")

    print("\n" + "=" * 60)
    print("  🚀 AlanDevTeam 启动全自动开发")
    print("=" * 60)
    print(f"\n📁 项目: {project_dir}")
    print(f"👥 团队: 10 个 Agent 并行协作")
    print(f"📋 流程: 需求分析 → 架构设计 → 编码 → 审查 → 集成 → 交付")

    # 检查是否有已完成的项目经验
    result = subprocess.run(
        [sys.executable, os.path.join(SCRIPTS_DIR, "lesson-learner.py"), "--list"],
        capture_output=True, text=True
    )
    if result.stdout:
        print(f"\n🧠 加载历史经验:")
        for line in result.stdout.split("\n")[:3]:
            print(f"   {line}")

    # 检查消息池
    result = subprocess.run(
        [sys.executable, os.path.join(SCRIPTS_DIR, "process-messages.py")],
        capture_output=True, text=True
    )
    if result.stdout.strip():
        print(f"\n📨 {result.stdout.strip()}")

    print("\n" + "-" * 60)
    print("  开发进行中... 查看进度: alan status")
    print("  查看日志: alan log --tail")
    print("-" * 60)


# ──────────────────────────────────────────────
# 团队信息
# ──────────────────────────────────────────────

TEAM = [
    ("PM", "需求分析、用户故事、验收标准"),
    ("Architect", "技术选型、API设计、文件所有权矩阵"),
    ("Dev-Backend", "后端API、数据层、业务逻辑"),
    ("Dev-Frontend", "UI组件、页面、交互逻辑"),
    ("Breaker", "敌对测试——攻破代码验证质量"),
    ("QA", "测试计划、全量回归、覆盖率"),
    ("Reviewer", "架构合规+代码质量+业务一致审查"),
    ("Integrator", "合并worktree、解决冲突、每步验证"),
    ("Security", "安全审计、漏洞扫描"),
    ("DevOps", "构建验证、环境配置、部署"),
]

def show_team():
    """显示团队阵容"""
    print("\n" + "=" * 60)
    print("  AlanDevTeam — 团队阵容")
    print("=" * 60)
    print(f"\n  👥 {len(TEAM)} 个 Agent 角色并行协作\n")

    for i, (role, desc) in enumerate(TEAM, 1):
        print(f"  {i:2d}. {role:15s} — {desc}")

    print(f"\n  📋 流程: CodeGraph → Sprint0 → Sprint1 → ReviewGate → FinalGate")
    print(f"  🔄 修复: 自动修复循环 (最多3次)")
    print(f"  🧠 记忆: 跨项目经验自动积累")
    print(f"  📨 通信: 消息池 + Worktree 隔离\n")


# ──────────────────────────────────────────────
# 新手引导
# ──────────────────────────────────────────────

def show_tutorial():
    """交互式新手引导"""
    print("\n" + "=" * 60)
    print("  🎓 AlanDevTeam — 新手引导")
    print("=" * 60)
    print("""
📖 什么是 AlanDevTeam？

  AlanDevTeam 是一个全自动多 Agent 编码团队。
  你只需要说"帮我做一个XX"，剩下的它全自动完成。

👥 团队有 10 个角色：

  PM → 架构师 → 后端开发 → 前端开发 → Breaker(敌对测试)
  → QA → Reviewer → Integrator → 安全 → DevOps

  他们并行工作、互相审查、自动修复，直到交付生产级代码。

🚀 快速开始（3 步）:

  第 1 步: 创建一个新项目
  ─────────────────────
  $ alan init my-blog
  → 自动生成项目脚手架（Flask Web 应用模板）

  第 2 步: 启动全自动开发
  ─────────────────────
  $ alan start ./my-blog
  → 团队开始工作：需求分析→设计→编码→测试→审查→交付

  第 3 步: 查看进度
  ─────────────────────
  $ alan status ./my-blog
  → 看消息池、Agent进度、团队经验

📌 常用命令:

  alan init <name>        创建项目脚手架
  alan start <path>       启动全自动开发
  alan status [path]      查看进度
  alan log --tail         查看最近日志
  alan preview <path>     沙箱预览变更
  alan team               看团队阵容
  alan doctor             检查系统健康
  alan feedback <path>    给项目评分反馈

🔍 想试试吗？

  第一步: alan init my-first-project --type web-flask
  第二步: cd ~/Desktop/my-first-project && alan start .
""")
    log("INFO", "用户查看新手引导")


# ──────────────────────────────────────────────
# 元级自愈 (alan doctor)
# ──────────────────────────────────────────────

HEALTH_CHECKS = [
    ("alan CLI 文件", lambda: os.path.exists(os.path.join(ALAN_DIR, "alan.sh"))),
    ("技能目录", lambda: os.path.isdir(os.path.join(ALAN_DIR, "scripts"))),
    ("消息池目录", lambda: os.path.isdir(os.path.join(ALAN_DIR, "message-pool"))),
    ("记忆目录", lambda: os.path.isdir(os.path.join(ALAN_DIR, "memory"))),
    ("日志目录", lambda: True),  # lazy create
    ("zcode Hook 注册", lambda: check_hook_registered()),
    ("zcode Skills 安装", lambda: os.path.isdir(os.path.expanduser("~/.zcode/skills/alan-dev-team"))),
    ("Git 可用", lambda: check_command("git")),
    ("Python 可用", lambda: check_command("python")),
    ("Node 可用", lambda: check_command("node")),
]

def check_command(cmd):
    """检查命令是否存在（兼容 Windows）"""
    result = subprocess.run(f"where {cmd} 2>nul || which {cmd} 2>/dev/null", shell=True, capture_output=True, text=True)
    return result.returncode == 0 and result.stdout.strip() != ""


def check_hook_registered():
    """检查 zcode hook 是否注册"""
    config_path = os.path.expanduser("~/.zcode/cli/config.json")
    if not os.path.exists(config_path):
        return False
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        for event_type, hooks in config.get("hooks", {}).get("events", {}).items():
            for hook_group in hooks:
                for hook in hook_group.get("hooks", []):
                    if "alan-dev-message" in hook.get("command", ""):
                        return True
    except (json.JSONDecodeError, OSError):
        pass
    return False


def doctor_check():
    """检查系统健康并自动修复"""
    print("\n" + "=" * 60)
    print("  🏥 AlanDevTeam — 系统自检")
    print("=" * 60)

    passed = 0
    failed = 0
    fixed = 0

    for name, check_fn in HEALTH_CHECKS:
        ok = check_fn()
        if ok:
            print(f"  ✅ {name}")
            passed += 1
        else:
            print(f"  ❌ {name} — 尝试修复...")
            failed += 1
            # 尝试自动修复
            if "消息池目录" in name:
                os.makedirs(os.path.join(ALAN_DIR, "message-pool"), exist_ok=True)
                print(f"     ✅ 已创建消息池目录")
                fixed += 1
            elif "记忆目录" in name:
                for d in ["memory/experiences", "memory/agent-profiles"]:
                    os.makedirs(os.path.join(ALAN_DIR, d), exist_ok=True)
                print(f"     ✅ 已创建记忆目录")
                fixed += 1
            elif "日志目录" in name:
                os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
                print(f"     ✅ 已创建日志目录")
                fixed += 1

    print(f"\n  📊 总计: {passed} 通过, {failed} 异常, {fixed} 已修复")
    print(f"  {'✅ 系统健康' if failed == 0 or fixed == failed else '⚠️  部分异常需手动处理'}")
    print("=" * 60)
    log("INFO" if failed == 0 else "WARN", f"系统自检: {passed}/{passed+failed} 通过, {fixed} 修复")


# ──────────────────────────────────────────────
# 反馈闭环
# ──────────────────────────────────────────────

FEEDBACK_FILE = os.path.join(ALAN_DIR, "memory", "feedback.json")


def load_feedback():
    """加载反馈数据"""
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"ratings": [], "suggestions": [], "avg_score": 0}


def save_feedback(data):
    """保存反馈数据"""
    os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def collect_feedback(project_dir):
    """收集用户对项目的评分和反馈"""
    print("\n" + "=" * 60)
    print("  💬 AlanDevTeam — 项目反馈")
    print("=" * 60)
    print(f"\n项目: {project_dir}")

    project_name = os.path.basename(project_dir.rstrip("/\\"))

    # 评分
    print("\n请为项目质量评分（1-5 分）：")
    print("  1 = 完全不能用")
    print("  5 = 完美，可直接上线")
    try:
        rating = int(input("  评分: ").strip())
        rating = max(1, min(5, rating))
    except (ValueError, EOFError):
        rating = 3

    # 反馈内容
    print("\n有什么想改进的？（直接回车跳过）:")
    try:
        suggestion = input("  建议: ").strip()
    except (EOFError):
        suggestion = ""

    # 保存反馈
    data = load_feedback()
    if not suggestion:
        suggestion = ""

    feedback_item = {
        "project": project_name,
        "path": project_dir,
        "rating": rating,
        "suggestion": suggestion,
        "timestamp": datetime.now().isoformat(),
    }
    data["ratings"].append(feedback_item)

    # 计算平均分
    scores = [r["rating"] for r in data["ratings"]]
    data["avg_score"] = round(sum(scores) / len(scores), 1)

    save_feedback(data)

    print(f"\n✅ 感谢反馈！评分: {rating}/5")
    print(f"📊 历史平均分: {data['avg_score']}/5 （共 {len(scores)} 次评分）")

    # 根据反馈改进最佳实践
    if rating <= 2 and suggestion:
        improve_from_feedback(project_name, suggestion)
    elif rating == 5:
        log("DONE", f"项目 '{project_name}' 获得满分评价")

    log("INFO", f"收到反馈: {project_name} = {rating}/5", suggestion)


def improve_from_feedback(project_name, suggestion):
    """从负面反馈中学习改进"""
    practices_file = os.path.join(ALAN_DIR, "memory", "best-practices.json")
    if not os.path.exists(practices_file):
        return

    with open(practices_file, "r", encoding="utf-8") as f:
        practices = json.load(f)

    lesson = f"[用户反馈] {project_name}: {suggestion[:80]}"
    if lesson not in practices["practices"]:
        practices["practices"].append(lesson)
        practices["last_updated"] = datetime.now().isoformat()
        with open(practices_file, "w", encoding="utf-8") as f:
            json.dump(practices, f, ensure_ascii=False, indent=2)
        log("INFO", "从用户反馈中学到新经验", lesson)
        print("\n🧠 已将此反馈加入团队经验库，下次项目会更注意这个问题。")



# ──────────────────────────────────────────────
# 主入口
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="AlanDevTeam — 全自动多Agent编码团队",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  alan init my-blog                    创建博客项目脚手架
  alan init my-api --type api          创建API服务脚手架
  alan start ./my-blog                 启动全自动开发
  alan status                          查看全局进度
  alan status ./my-blog                查看项目进度
  alan log --tail                      查看最近日志
  alan preview ./my-blog               预览将要发生的变更
  alan team                            查看团队阵容
  alan tutorial                        打开新手引导
  alan doctor                          检查系统健康
  alan feedback ./my-blog              给项目评分
        """
    )

    subparsers = parser.add_subparsers(dest="command")

    # init
    p_init = subparsers.add_parser("init", help="创建新项目脚手架")
    p_init.add_argument("project_name", help="项目名称")
    p_init.add_argument("--type", default="web-flask", choices=list(TEMPLATES.keys()) + ["saas"], help="项目类型")
    p_init.add_argument("--output", default=None, help="输出目录（默认桌面）")

    # start
    p_start = subparsers.add_parser("start", help="启动全自动开发")
    p_start.add_argument("project_dir", nargs="?", default=".", help="项目路径")

    # status
    p_status = subparsers.add_parser("status", help="查看进度仪表盘")
    p_status.add_argument("project_dir", nargs="?", default=None, help="项目路径（可选）")

    # log
    p_log = subparsers.add_parser("log", help="查看日志")
    p_log.add_argument("--tail", action="store_true", help="只显示最近20条")
    p_log.add_argument("--level", default=None, choices=["INFO", "WARN", "ERROR", "DONE"], help="按级别筛选")

    # preview
    p_preview = subparsers.add_parser("preview", help="沙箱模式预览变更")
    p_preview.add_argument("project_dir", nargs="?", default=".", help="项目路径")

    # team
    subparsers.add_parser("team", help="查看团队阵容")

    # tutorial
    subparsers.add_parser("tutorial", help="🎓 新手引导")

    # doctor
    subparsers.add_parser("doctor", help="🏥 系统健康检查 + 自愈")

    # feedback
    p_feedback = subparsers.add_parser("feedback", help="💬 给项目评分反馈")
    p_feedback.add_argument("project_dir", nargs="?", default=".", help="项目路径")

    args = parser.parse_args()

    if args.command == "init":
        init_project(args.project_name, args.type, args.output)
    elif args.command == "start":
        start_development(args.project_dir)
    elif args.command == "status":
        show_status(args.project_dir)
    elif args.command == "log":
        read_logs(tail=args.tail, level=args.level)
    elif args.command == "preview":
        preview_changes(args.project_dir)
    elif args.command == "team":
        show_team()
    elif args.command == "tutorial":
        show_tutorial()
    elif args.command == "doctor":
        doctor_check()
    elif args.command == "feedback":
        collect_feedback(args.project_dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
