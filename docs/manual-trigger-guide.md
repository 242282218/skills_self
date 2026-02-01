# Skill 手动触发更新指南

本文档介绍 4 种手动触发 Skill 自动更新的方法。

---

## 目录

1. [方式一：GitHub Actions 网页界面（推荐）](#方式一github-actions-网页界面推荐)
2. [方式二：GitHub CLI 命令行](#方式二github-cli-命令行)
3. [方式三：本地手动运行](#方式三本地手动运行)
4. [方式四：API 调用](#方式四api-调用)

---

## 方式一：GitHub Actions 网页界面（推荐）

适合：所有用户，可视化操作

### 步骤

1. **进入 Actions 页面**
   - 打开 GitHub 仓库页面
   - 点击顶部菜单栏的 **Actions** 标签

2. **选择工作流**
   - 在左侧工作流列表中找到 **"Skill Auto Updater"**
   - 点击进入工作流详情页

3. **运行工作流**
   - 点击右侧绿色的 **"Run workflow"** 按钮
   - 展开参数配置面板：

   | 参数 | 选项 | 说明 |
   |------|------|------|
   | **dry_run** | `true` / `false` | `true`=仅检查，`false`=实际更新 |
   | **skill_path** | 路径或留空 | 如 `testing/pytest-design`，留空=全部 |

4. **确认执行**
   - 选择参数后点击 **"Run workflow"**
   - 页面自动刷新显示新的工作流运行

5. **查看结果**
   - 点击运行记录查看详细日志
   - 等待 Telegram 通知推送

### 截图示意

```
┌─────────────────────────────────────────┐
│  Actions > Skill Auto Updater           │
├─────────────────────────────────────────┤
│                                         │
│  [Run workflow] ▼                       │
│  ├─ dry_run: false                      │
│  └─ skill_path: (可选)                  │
│                                         │
│  [Run workflow] 按钮                    │
│                                         │
└─────────────────────────────────────────┘
```

---

## 方式二：GitHub CLI 命令行

适合：熟悉命令行的开发者

### 前置要求

```bash
# 安装 GitHub CLI
# macOS
brew install gh

# Windows
winget install --id GitHub.cli

# 或使用 scoop
scoop install gh
```

### 步骤

1. **登录 GitHub**
   ```bash
   gh auth login
   # 按提示完成浏览器授权
   ```

2. **触发工作流（实际更新）**
   ```bash
   gh workflow run skill-updater.yml \
     --repo your-username/your-repo \
     -f dry_run=false
   ```

3. **试运行模式（仅检查）**
   ```bash
   gh workflow run skill-updater.yml \
     --repo your-username/your-repo \
     -f dry_run=true
   ```

4. **更新指定 Skill**
   ```bash
   gh workflow run skill-updater.yml \
     --repo your-username/your-repo \
     -f dry_run=false \
     -f skill_path=testing/pytest-design
   ```

5. **查看运行状态**
   ```bash
   # 列出最近运行
   gh run list --workflow=skill-updater.yml

   # 查看特定运行日志
   gh run view <run-id>

   # 实时监控日志
   gh run watch <run-id>
   ```

### 常用命令速查

| 命令 | 说明 |
|------|------|
| `gh workflow list` | 列出所有工作流 |
| `gh workflow view skill-updater.yml` | 查看工作流详情 |
| `gh run list -L 10` | 列出最近 10 次运行 |
| `gh run view --log` | 查看完整日志 |

---

## 方式三：本地手动运行

适合：开发调试、无 GitHub Actions 环境

### 前置要求

- Python 3.9+
- pip
- GitHub Token（可选，用于访问 API）

### 步骤

1. **进入项目目录**
   ```bash
   cd c:\Users\24228\Desktop\skills_projiect
   ```

2. **安装依赖**
   ```bash
   pip install pyyaml requests
   ```

3. **配置环境变量**

   **Windows (PowerShell)**
   ```powershell
   $env:GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
   $env:TELEGRAM_BOT_TOKEN="5807378696:AAHDfl1nCtTkhk9bvtvog3cjwByYjgv0grE"
   $env:TELEGRAM_USER_ID="5675490499"
   ```

   **Windows (CMD)**
   ```cmd
   set GITHUB_TOKEN=ghp_xxxxxxxxxxxx
   set TELEGRAM_BOT_TOKEN=5807378696:AAHDfl1nCtTkhk9bvtvog3cjwByYjgv0grE
   set TELEGRAM_USER_ID=5675490499
   ```

   **Linux/macOS**
   ```bash
   export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
   export TELEGRAM_BOT_TOKEN="5807378696:AAHDfl1nCtTkhk9bvtvog3cjwByYjgv0grE"
   export TELEGRAM_USER_ID="5675490499"
   ```

4. **运行更新器**

   **实际更新**
   ```bash
   cd skill
   python .updater/updater.py
   ```

   **试运行模式**
   ```bash
   python .updater/updater.py --dry-run
   ```

   **更新指定 Skill**
   ```bash
   python .updater/updater.py --skill testing/pytest-design
   ```

   **组合参数**
   ```bash
   python .updater/updater.py --skill testing/pytest-design --dry-run
   ```

5. **发送测试通知**
   ```bash
   python .updater/notifier.py test
   ```

### 本地运行参数

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--skill` | `-s` | 指定 Skill 路径 | `--skill testing/pytest-design` |
| `--dry-run` | `-d` | 试运行模式 | `--dry-run` |
| `--config` | `-c` | 指定配置文件 | `--config .updater/config.yaml` |

---

## 方式四：API 调用

适合：程序化触发、集成到其他系统

### 前置要求

- GitHub Personal Access Token
- HTTP 客户端（curl、Postman、代码库）

### 使用 curl

1. **基本调用**
   ```bash
   curl -X POST \
     -H "Authorization: token ghp_xxxxxxxxxxxx" \
     -H "Accept: application/vnd.github.v3+json" \
     https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/actions/workflows/skill-updater.yml/dispatches \
     -d '{
       "ref": "main",
       "inputs": {
         "dry_run": "false",
         "skill_path": ""
       }
     }'
   ```

2. **试运行模式**
   ```bash
   curl -X POST \
     -H "Authorization: token ghp_xxxxxxxxxxxx" \
     -H "Accept: application/vnd.github.v3+json" \
     https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/actions/workflows/skill-updater.yml/dispatches \
     -d '{
       "ref": "main",
       "inputs": {
         "dry_run": "true",
         "skill_path": "testing/pytest-design"
       }
     }'
   ```

### 使用 Python

```python
import requests

# 配置
TOKEN = "ghp_xxxxxxxxxxxx"
REPO = "YOUR_USERNAME/YOUR_REPO"
WORKFLOW = "skill-updater.yml"

# API 调用
url = f"https://api.github.com/repos/{REPO}/actions/workflows/{WORKFLOW}/dispatches"
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
data = {
    "ref": "main",
    "inputs": {
        "dry_run": "false",
        "skill_path": ""
    }
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 204:
    print("✅ 工作流触发成功")
else:
    print(f"❌ 触发失败: {response.status_code}")
    print(response.json())
```

### 使用 JavaScript/Node.js

```javascript
const axios = require('axios');

const TOKEN = 'ghp_xxxxxxxxxxxx';
const REPO = 'YOUR_USERNAME/YOUR_REPO';

async function triggerWorkflow() {
  try {
    const response = await axios.post(
      `https://api.github.com/repos/${REPO}/actions/workflows/skill-updater.yml/dispatches`,
      {
        ref: 'main',
        inputs: {
          dry_run: 'false',
          skill_path: ''
        }
      },
      {
        headers: {
          'Authorization': `token ${TOKEN}`,
          'Accept': 'application/vnd.github.v3+json'
        }
      }
    );
    
    if (response.status === 204) {
      console.log('✅ 工作流触发成功');
    }
  } catch (error) {
    console.error('❌ 触发失败:', error.message);
  }
}

triggerWorkflow();
```

---

## 参数说明

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `dry_run` | choice | 否 | `false` | `true`=仅检查，`false`=实际更新 |
| `skill_path` | string | 否 | `""` | Skill 路径，如 `testing/pytest-design` |

### 参数组合建议

| 场景 | dry_run | skill_path | 说明 |
|------|---------|------------|------|
| 全面更新 | `false` | `""` | 更新所有 Skill |
| 安全检查 | `true` | `""` | 检查所有，不应用 |
| 指定更新 | `false` | `testing/pytest-design` | 只更新指定 Skill |
| 测试指定 | `true` | `testing/pytest-design` | 测试指定 Skill |

---

## 触发后流程

```
触发更新
    ↓
GitHub Actions 启动
    ↓
Telegram 通知（开始检查）
    ↓
运行 updater.py
    ↓
检测开源项目更新
    ↓
有变更？
    ├── 是 → 更新 Skill → 提交代码 → Telegram 通知（成功）
    └── 否 → Telegram 通知（无需更新）
    ↓
完成
```

---

## 故障排查

### 常见问题

1. **工作流未触发**
   - 检查 GitHub Token 权限（需要 `workflow` 权限）
   - 确认工作流文件路径正确

2. **Telegram 未收到通知**
   - 检查 Bot Token 和 User ID 是否正确
   - 确认已向 Bot 发送 `/start`

3. **更新失败**
   - 查看 Actions 日志获取详细错误
   - 检查 GitHub API 限流

4. **本地运行报错**
   - 确认 Python 版本 >= 3.9
   - 检查依赖是否安装完整

### 获取帮助

- 查看 Actions 日志：GitHub → Actions → 选择运行记录 → 查看日志
- 本地调试：使用 `--dry-run` 参数测试
- 测试通知：运行 `python .updater/notifier.py test`

---

## 相关文档

- [GitHub Actions 文档](https://docs.github.com/cn/actions)
- [GitHub CLI 手册](https://cli.github.com/manual/)
- [GitHub REST API](https://docs.github.com/cn/rest)
- [项目 CHANGELOG](../CHANGELOG.md)
