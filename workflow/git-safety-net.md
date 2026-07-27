# Git 安全网操作规范

## 为什么需要 Git 安全网

多 Agent 团队中，一个 Agent 的修改可能破坏另一个 Agent 的工作。Git 安全网确保：
1. 修改前的代码始终可恢复
2. 测试不通过的代码不会留在工作区
3. 所有变更都有记录，可追溯

## 操作规范

### 修改前（必须执行）

```bash
# 1. 保存当前工作（如果有未提交的变更）
git stash push -m "auto-save-$(date +%s)"

# 2. 确保工作区干净
git checkout .
```

### 修改后（必须执行）

```bash
# 1. 运行全量测试
python -m pytest tests/ -v

# 2. 根据测试结果决定
# 全部通过:
git add -A
git commit -m "feat: <功能描述>"

# 有失败（立即回滚）:
git checkout .           # 回滚所有未暂存的更改
git stash drop           # 丢弃自动保存的stash
# 然后重新修复代码
```

### 功能分支规范

```bash
# 每个新功能创建独立分支
git checkout -b feature/<功能名>

# 在分支上开发
# ... (修改代码)

# 全量测试通过后
git add -A
git commit -m "feat: <功能名>"

# 全部门禁通过后合并到主分支
git checkout master
git merge feature/<功能名>
git tag v1.x.x
```

### 修复循环中的 Git

当 Reviewer 发现问题，Dev 修复时：

```bash
# 已经有上一个功能的 commit，所以工作区是干净的
# 直接在当前 commit 上修复

# 修复后运行测试
python -m pytest tests/ -v

# 全部通过
git add -A
git commit -m "fix: <修复内容>"

# 上次测试没通过
git checkout .  # 回滚
# 重新修复
```

### 紧急回滚

如果合并后发现严重问题：

```bash
# 回滚到上一个版本
git revert HEAD
git commit -m "revert: 回滚 <功能名> 引起的问题"
```

## 关键规则

1. **绝不提交未通过测试的代码** — 测试失败 = git checkout . 回滚
2. **每个功能一个 commit** — 方便回滚时精确定位
3. **commit message 用约定式** — feat: / fix: / chore:
4. **功能分支合并后删除** — `git branch -d feature/<功能名>`
