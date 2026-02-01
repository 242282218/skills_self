---
name: ci-cd-config
version: 1.0.0
scope: devops
trigger:
  - when: 用户需要配置 CI/CD 时
  - when: 用户询问"如何设置自动化部署"时
  - when: 需要优化构建流程时
capabilities:
  - 配置 GitHub Actions
  - 配置 GitLab CI
  - 配置 Jenkins
  - 设计构建流程
  - 设置部署策略
constraints:
  - 使用标准工具
  - 保持配置简洁
  - 确保安全凭证管理
  - 支持回滚
inputs:
  - project_type: 项目类型
  - ci_platform: CI 平台
  - deployment_target: 部署目标
  - requirements: 需求
outputs:
  - ci_config: CI 配置
  - pipeline_design: 流水线设计
  - deployment_strategy: 部署策略
  - best_practices: 最佳实践
references:
  - project: GitHub Actions
    url: https://github.com/features/actions
  - project: GitLab CI
    capability: Continuous Integration
---

# CI/CD Config

配置持续集成和持续部署流水线。

## When to Invoke

- 新项目搭建 CI/CD
- 迁移 CI 平台
- 优化构建时间
- 设置自动化测试
- 配置部署策略

## Input Format

```yaml
project_type: "python"
ci_platform: "github_actions"
deployment_target: "aws_ec2"
requirements:
  - "运行单元测试"
  - "代码覆盖率检查"
  - "自动部署到 staging"
  - "生产环境手动触发"
```

## Output Format

```yaml
ci_config: |
  name: CI/CD Pipeline
  
  on:
    push:
      branches: [main, develop]
    pull_request:
      branches: [main]
  
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Set up Python
          uses: actions/setup-python@v4
          with:
            python-version: '3.11'
        - name: Install dependencies
          run: pip install -r requirements.txt
        - name: Run tests
          run: pytest --cov=src
    
    deploy:
      needs: test
      runs-on: ubuntu-latest
      if: github.ref == 'refs/heads/main'
      steps:
        - name: Deploy to production
          run: ./deploy.sh

pipeline_design:
  stages:
    - "build"
    - "test"
    - "security_scan"
    - "deploy_staging"
    - "deploy_production"

deployment_strategy:
  type: "blue_green"
  rollback: "automatic_on_failure"
```

## Examples

### Example 1: Python 项目 CI

**Input:** Flask Web 应用

**Output:**
- 依赖安装
- 代码检查 (flake8, black)
- 单元测试
- 覆盖率报告
- Docker 构建

### Example 2: C 项目 CI

**Input:** 嵌入式固件

**Output:**
- 交叉编译
- 静态分析
- 单元测试
- 固件打包
- 版本发布

## Best Practices

1. **快速反馈**: 快速阶段优先执行
2. **并行执行**: 独立的任务并行运行
3. **缓存优化**: 缓存依赖和构建产物
4. **安全凭证**: 使用 secrets 管理敏感信息
