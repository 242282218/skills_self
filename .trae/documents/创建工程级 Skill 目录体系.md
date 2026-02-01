## 目标
添加 GitHub Actions 工作流，实现 Skill 的自动更新

## 需要创建的文件

### 1. `.github/workflows/skill-updater.yml`
GitHub Actions 工作流配置文件，包含：
- 定时触发（每周日凌晨 2 点）
- 手动触发（workflow_dispatch）
- 自动运行更新脚本
- 自动提交更新后的 Skill
- 生成更新报告

### 2. 更新后的 `.updater/config.yaml`
添加 GitHub Actions 相关配置：
- 工作流触发方式
- 提交信息模板
- 分支策略

## 工作流程

```
定时触发 / 手动触发
    ↓
检出代码
    ↓
设置 Python 环境
    ↓
安装依赖
    ↓
运行 updater.py
    ↓
检测是否有变更
    ↓
是 → 提交变更 → 推送 → 生成报告
否 → 结束
```

## 特性

1. **定时触发**: 每周日凌晨 2 点（UTC）
2. **手动触发**: 支持 workflow_dispatch
3. **自动提交**: 检测到变更自动提交
4. **更新报告**: 生成详细的更新日志
5. **失败通知**: 更新失败时发送通知

请确认后，我将创建 GitHub Actions 工作流文件。