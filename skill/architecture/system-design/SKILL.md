---
name: system-design
version: 1.0.0
scope: architecture
trigger:
  - when: 用户需要系统设计时
  - when: 用户询问"如何设计这个系统"时
  - when: 需要架构评审时
capabilities:
  - 设计系统架构
  - 选择技术栈
  - 定义组件边界
  - 设计数据流
  - 评估可扩展性
constraints:
  - 考虑实际约束
  - 避免过度设计
  - 关注非功能需求
  - 支持演进
inputs:
  - requirements: 系统需求
  - constraints: 约束条件
  - scale: 预期规模
  - tech_preferences: 技术偏好
outputs:
  - architecture_diagram: 架构图描述
  - component_design: 组件设计
  - data_flow: 数据流设计
  - tech_stack: 技术栈建议
references:
  - project: System Design Primer
    url: https://github.com/donnemartin/system-design-primer
  - project: MetaGPT Architect
    capability: Architecture design
---

# System Design

设计可扩展的系统架构。

## When to Invoke

- 新系统架构设计
- 现有系统重构
- 技术选型
- 性能优化设计
- 架构评审

## Input Format

```yaml
requirements:
  functional:
    - "支持 100万 DAU"
    - "实时消息推送"
  non_functional:
    - "可用性 99.99%"
    - "响应时间 < 200ms"
constraints:
  budget: "有限预算"
  timeline: "3个月"
scale:
  users: 1000000
  qps: 10000
tech_preferences:
  - "Python"
  - "开源优先"
```

## Output Format

```yaml
architecture_diagram:
  layers:
    - name: "API Gateway"
      components: ["Nginx", "Rate Limiter"]
    - name: "Service Layer"
      components: ["User Service", "Message Service"]
    - name: "Data Layer"
      components: ["PostgreSQL", "Redis", "Kafka"]

component_design:
  user_service:
    responsibility: "用户管理"
    interface: "REST API"
    dependencies: ["database", "cache"]

data_flow:
  - step: "客户端请求"
    component: "API Gateway"
  - step: "身份验证"
    component: "Auth Service"
  - step: "业务处理"
    component: "Business Service"

tech_stack:
  backend: "FastAPI + Python"
  database: "PostgreSQL"
  cache: "Redis"
  message_queue: "Kafka"
```

## Examples

### Example 1: 微服务架构

**Input:** 电商平台

**Output:**
- 服务拆分方案
- 通信机制设计
- 数据一致性策略
- 部署架构

### Example 2: 实时系统

**Input:** 即时通讯系统

**Output:**
- 长连接管理
- 消息路由设计
- 状态同步机制
- 水平扩展方案

## Best Practices

1. **关注点分离**: 清晰划分职责边界
2. **松耦合**: 减少组件间依赖
3. **高内聚**: 相关功能放在一起
4. **可观测性**: 设计监控和日志
