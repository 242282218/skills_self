---
name: plan-decomposer
version: 1.0.0
scope: meta
trigger:
  - when: 用户需要分解复杂任务时
  - when: 用户询问"如何规划这个项目"时
  - when: 任务太大需要拆分时
capabilities:
  - 分析任务复杂度
  - 拆分为子任务
  - 确定依赖关系
  - 估算工作量
  - 生成执行计划
constraints:
  - 子任务可独立完成
  - 明确依赖关系
  - 可量化进度
  - 支持并行执行
inputs:
  - task: 任务描述
  - complexity: 复杂度评估
  - deadline: 截止时间
  - resources: 可用资源
outputs:
  - subtasks: 子任务列表
  - dependencies: 依赖图
  - timeline: 时间线
  - milestones: 里程碑
references:
  - project: MetaGPT
    url: https://github.com/geekan/MetaGPT
  - project: CrewAI
    capability: Task decomposition
---

# Plan Decomposer

将复杂任务分解为可管理的子任务。

## When to Invoke

- 项目启动规划
- 大型功能开发
- 重构计划制定
- 冲刺规划
- 资源分配

## Input Format

```yaml
task: "开发一个电商平台的订单系统"
complexity: "high"
deadline: "2024-03-01"
resources:
  developers: 3
  budget: "limited"
```

## Output Format

```yaml
subtasks:
  - id: "T1"
    name: "数据库设计"
    description: "设计订单表结构"
    estimated_hours: 8
    assignee: "backend_dev"
    
  - id: "T2"
    name: "API 设计"
    description: "设计订单相关 API"
    estimated_hours: 12
    assignee: "backend_dev"
    dependencies: ["T1"]
    
  - id: "T3"
    name: "订单创建功能"
    description: "实现创建订单接口"
    estimated_hours: 16
    assignee: "backend_dev"
    dependencies: ["T2"]
    
  - id: "T4"
    name: "订单查询功能"
    description: "实现订单查询接口"
    estimated_hours: 12
    assignee: "backend_dev"
    dependencies: ["T2"]
    
  - id: "T5"
    name: "单元测试"
    description: "编写订单模块测试"
    estimated_hours: 16
    assignee: "qa_dev"
    dependencies: ["T3", "T4"]

dependencies:
  T1: []
  T2: ["T1"]
  T3: ["T2"]
  T4: ["T2"]
  T5: ["T3", "T4"]

timeline:
  week1:
    - "T1: 数据库设计"
    - "T2: API 设计"
  week2:
    - "T3: 订单创建功能"
    - "T4: 订单查询功能"
  week3:
    - "T5: 单元测试"
    - "集成测试"

milestones:
  - name: "设计完成"
    date: "2024-02-08"
    deliverables: ["数据库设计", "API 文档"]
  - name: "功能完成"
    date: "2024-02-22"
    deliverables: ["订单创建", "订单查询"]
  - name: "测试完成"
    date: "2024-03-01"
    deliverables: ["测试报告", "上线准备"]
```

## Examples

### Example 1: 系统重构

**Input:** "重构遗留系统"

**Output:**
- 模块拆分
- 重构顺序
- 风险缓解
- 回滚计划

### Example 2: 功能开发

**Input:** "开发用户认证系统"

**Output:**
- 子任务分解
- 技术选型
- 接口定义
- 测试计划

## Best Practices

1. **MECE 原则**: 子任务相互独立，完全穷尽
2. **SMART 目标**: 具体、可衡量、可达成
3. **缓冲时间**: 预留处理意外情况的时间
4. **定期回顾**: 根据进展调整计划
