# Skill 目录 GitHub 部署指南

本文档介绍如何将 Skill 目录完整部署到 GitHub，并配置自动更新系统。

---

## 目录

1. [准备工作](#准备工作)
2. [创建 GitHub 仓库](#创建-github-仓库)
3. [推送代码到 GitHub](#推送代码到-github)
4. [配置 Secrets](#配置-secrets)
5. [配置 GitHub Actions](#配置-github-actions)
6. [验证部署](#验证部署)
7. [测试自动更新](#测试自动更新)
8. [故障排查](#故障排查)

---

## 准备工作

### 1. 检查本地文件

确保所有文件已准备就绪：

```
skills_projiect/
├── .github/
│   └── workflows/
│       └── skill-updater.yml    # GitHub Actions 工作流
├── docs/
│   ├── github-deployment-guide.md  # 本文件
│   └── manual-trigger-guide.md     # 手动触发指南
├── skill/
│   ├── .updater/
│   │   ├── config.yaml          # 更新配置
│   │   ├── updater.py           # 更新引擎
│   │   └── notifier.py          # 通知模块
│   ├── architecture/            # 架构设计 Skill
│   ├── code-comprehension/      # 代码理解 Skill
│   ├── debugging/               # 调试排障 Skill
│   ├── devops/                  # 运维部署 Skill
│   ├── documentation/           # 文档交付 Skill
│   ├── frontend/                # 前端开发 Skill
│   ├── meta/                    # 元能力 Skill
│   ├── refactoring/             # 重构优化 Skill
│   ├── testing/                 # 测试验证 Skill
│   └── CHANGELOG.md             # 变更日志
└── test_telegram_notifications.py  # 测试脚本
```

### 2. 准备工具

- Git 客户端
- GitHub 账号
- Telegram Bot（用于通知）

---

## 创建 GitHub 仓库

### 方式一：GitHub 网页创建

1. 登录 [GitHub](https://github.com)
2. 点击右上角 **+** → **New repository**
3. 填写仓库信息：
   - **Repository name**: `skills`（或您喜欢的名字）
   - **Description**: `工程级 AI Skill 目录`
   - **Visibility**: `Public` 或 `Private`
   - **Initialize**: 不要勾选（已有本地文件）
4. 点击 **Create repository**

### 方式二：GitHub CLI 创建

```bash
# 安装 GitHub CLI（如果未安装）
# Windows
winget install --id GitHub.cli

# 登录
gh auth login

# 创建仓库
gh repo create skills \
  --description "工程级 AI Skill 目录" \
  --public \
  --source=. \
  --remote=origin \
  --push
```

---

## 推送代码到 GitHub

### 步骤 1：初始化 Git 仓库（如果尚未初始化）

```bash
# 进入项目目录
cd c:\Users\24228\Desktop\skills_projiect

# 初始化 Git（如果尚未初始化）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Add 30 engineering skills with auto-updater"
```

### 步骤 2：关联远程仓库

```bash
# 添加远程仓库（替换 YOUR_USERNAME 为您的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/skills.git

# 或者使用 SSH
git remote add origin git@github.com:YOUR_USERNAME/skills.git
```

### 步骤 3：推送代码

```bash
# 推送到 main 分支
git branch -M main
git push -u origin main
```

### 完整推送脚本（PowerShell）

```powershell
# 保存为 push-to-github.ps1

$repoUrl = Read-Host "请输入 GitHub 仓库 URL"

Write-Host "🚀 开始推送到 GitHub..." -ForegroundColor Green

# 检查是否在 git 仓库
if (-not (Test-Path .git)) {
    Write-Host "📦 初始化 Git 仓库..." -ForegroundColor Yellow
    git init
}

# 添加所有文件
Write-Host "➕ 添加文件到暂存区..." -ForegroundColor Yellow
git add .

# 提交
Write-Host "💾 提交更改..." -ForegroundColor Yellow
git commit -m "Initial commit: Add 30 engineering skills with auto-updater" -m "- 9 个维度共 30 个 Skill" -m "- 自动更新系统" -m "- Telegram 通知" -m "- GitHub Actions 工作流"

# 添加远程仓库
Write-Host "🔗 关联远程仓库..." -ForegroundColor Yellow
git remote add origin $repoUrl 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "远程仓库已存在，更新 URL..." -ForegroundColor Yellow
    git remote set-url origin $repoUrl
}

# 推送
Write-Host "📤 推送到 GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 推送成功！" -ForegroundColor Green
    Write-Host "🌐 仓库地址: $repoUrl" -ForegroundColor Cyan
} else {
    Write-Host "❌ 推送失败，请检查错误信息" -ForegroundColor Red
}
```

运行：
```powershell
.\push-to-github.ps1
```

---

## 配置 Secrets

### 步骤 1：获取 Telegram Bot Token

1. 打开 Telegram，搜索 [@BotFather](https://t.me/botfather)
2. 发送 `/newbot` 创建新 Bot
3. 按提示设置 Bot 名称和用户名
4. 保存获得的 **Bot Token**（格式：`123456789:ABCdefGHIjklMNOpqrSTUvwxyz`）
5. 发送 `/start` 给您的 Bot

### 步骤 2：获取 User ID

1. 打开 Telegram，搜索 [@userinfobot](https://t.me/userinfobot)
2. 发送 `/start`
3. 保存返回的 **Id** 数字（如：`5675490499`）

### 步骤 3：在 GitHub 配置 Secrets

1. 打开 GitHub 仓库页面
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下 Secrets：

| Secret 名称 | 值 | 说明 |
|------------|-----|------|
| `TELEGRAM_BOT_TOKEN` | `5807378696:AAHDfl1nCtTkhk9bvtvog3cjwByYjgv0grE` | Telegram Bot Token |
| `TELEGRAM_USER_ID` | `5675490499` | Telegram 用户 ID |
| `GITHUB_TOKEN` | （自动生成） | GitHub 自动提供，无需手动设置 |

### 配置截图示意

```
Settings > Secrets and variables > Actions
┌─────────────────────────────────────────┐
│  Repository secrets                     │
├─────────────────────────────────────────┤
│  [New repository secret]                │
│                                         │
│  Name: TELEGRAM_BOT_TOKEN               │
│  Secret: 5807378696:AAHD...             │
│                                         │
│  Name: TELEGRAM_USER_ID                 │
│  Secret: 5675490499                     │
│                                         │
└─────────────────────────────────────────┘
```

---

## 配置 GitHub Actions

### 启用 Actions

1. 打开仓库页面，点击 **Actions** 标签
2. 如果提示启用 Actions，点击 **I understand my workflows, go ahead and enable them**

### 验证工作流文件

确保 `.github/workflows/skill-updater.yml` 已正确提交：

```bash
# 检查文件是否存在
git ls-files .github/workflows/skill-updater.yml

# 查看文件内容
cat .github/workflows/skill-updater.yml
```

---

## 验证部署

### 1. 检查仓库文件

打开 GitHub 仓库网页，确认以下文件存在：

- [ ] `.github/workflows/skill-updater.yml`
- [ ] `skill/.updater/config.yaml`
- [ ] `skill/.updater/updater.py`
- [ ] `skill/.updater/notifier.py`
- [ ] `skill/CHANGELOG.md`
- [ ] 所有 Skill 目录（30 个）

### 2. 检查 Actions 工作流

1. 点击 **Actions** 标签
2. 应该看到 **Skill Auto Updater** 工作流
3. 工作流状态应为可运行（绿色）

### 3. 测试手动触发

1. 点击 **Actions** → **Skill Auto Updater**
2. 点击 **Run workflow**
3. 设置参数：
   - **dry_run**: `true`（试运行，不实际更新）
   - **skill_path**: 留空
4. 点击 **Run workflow**
5. 等待执行完成，查看日志

### 4. 验证 Telegram 通知

检查 Telegram 是否收到测试消息：

```
ℹ️ Skill 更新检查

所有 Skill 都是最新的，无需更新！
```

---

## 测试自动更新

### 测试 1：手动触发试运行

```bash
# 使用 GitHub CLI
gh workflow run skill-updater.yml \
  --repo YOUR_USERNAME/skills \
  -f dry_run=true
```

### 测试 2：手动触发实际更新

```bash
gh workflow run skill-updater.yml \
  --repo YOUR_USERNAME/skills \
  -f dry_run=false
```

### 测试 3：测试通知功能

本地运行测试脚本：

```bash
cd skill/.updater
python notifier.py test
```

---

## 故障排查

### 问题 1：推送失败

**症状**：`git push` 提示权限错误

**解决**：
```bash
# 检查远程仓库 URL
git remote -v

# 如果是 HTTPS，切换到 SSH
git remote set-url origin git@github.com:YOUR_USERNAME/skills.git

# 或配置 GitHub Token
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/skills.git
```

### 问题 2：Actions 未触发

**症状**：提交后 Actions 没有运行

**解决**：
1. 检查 `.github/workflows/skill-updater.yml` 是否存在
2. 检查文件语法是否正确
3. 确认 Actions 已启用（Settings > Actions > General）

### 问题 3：Telegram 未收到通知

**症状**：Actions 运行成功但未收到 Telegram 消息

**解决**：
1. 检查 Secrets 是否正确配置
2. 确认已向 Bot 发送 `/start`
3. 检查 User ID 是否正确
4. 查看 Actions 日志中的错误信息

### 问题 4：更新器运行失败

**症状**：updater.py 报错

**解决**：
```bash
# 本地测试
python skill/.updater/updater.py --dry-run

# 查看详细错误
python -m pdb skill/.updater/updater.py
```

---

## 部署检查清单

- [ ] 创建 GitHub 仓库
- [ ] 推送所有代码到 GitHub
- [ ] 配置 `TELEGRAM_BOT_TOKEN` Secret
- [ ] 配置 `TELEGRAM_USER_ID` Secret
- [ ] 启用 GitHub Actions
- [ ] 测试手动触发（试运行模式）
- [ ] 收到 Telegram 通知
- [ ] 验证所有文件已上传

---

## 后续维护

### 定期更新

- 每周日凌晨 2 点自动检查更新
- 手动触发：GitHub → Actions → Run workflow

### 添加新 Skill

1. 本地创建新 Skill 目录和 SKILL.md
2. 更新 `CHANGELOG.md`
3. 提交并推送到 GitHub
4. 更新 `.updater/config.yaml`（如果需要追踪新项目）

### 监控状态

- 查看 Actions 运行历史
- 检查 Telegram 通知
- 定期查看 `CHANGELOG.md`

---

## 相关文档

- [手动触发更新指南](./manual-trigger-guide.md)
- [项目 CHANGELOG](../skill/CHANGELOG.md)
- [GitHub Actions 文档](https://docs.github.com/cn/actions)
- [GitHub Secrets 文档](https://docs.github.com/cn/actions/security-guides/encrypted-secrets)
