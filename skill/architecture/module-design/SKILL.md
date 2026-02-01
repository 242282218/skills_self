---
name: module-design
version: 1.0.0
scope: architecture
trigger:
  - when: 用户需要设计模块时
  - when: 用户询问"如何划分模块"时
  - when: 需要模块重构时
capabilities:
  - 划分模块边界
  - 设计模块接口
  - 定义依赖关系
  - 设计模块内结构
  - 评估内聚和耦合
constraints:
  - 单一职责原则
  - 最小依赖原则
  - 接口稳定原则
  - 可测试性
inputs:
  - system_description: 系统描述
  - module_candidates: 候选模块
  - constraints: 约束条件
outputs:
  - module_structure: 模块结构
  - interface_design: 接口设计
  - dependency_graph: 依赖图
  - organization: 代码组织
references:
  - project: Clean Architecture
    url: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
  - project: Modular Monolith
    capability: Module design
---

# Module Design

设计高内聚、低耦合的代码模块。

## When to Invoke

- 新系统模块划分
- 单体应用拆分
- 代码重构
- 库/框架设计
- 代码审查

## Input Format

```yaml
system_description: |
  电商平台，包含用户管理、商品管理、
  订单处理、支付、物流等模块。

module_candidates:
  - "user"
  - "product"
  - "order"
  - "payment"
  - "logistics"

constraints:
  - "订单模块不能依赖支付模块"
  - "用户模块是核心模块"
```

## Output Format

```yaml
module_structure:
  user:
    responsibility: "用户管理"
    exports: ["User", "UserService"]
    internal: ["UserRepository", "UserValidator"]
  order:
    responsibility: "订单处理"
    exports: ["Order", "OrderService"]
    dependencies: ["user", "product"]

interface_design:
  user_service:
    methods:
      - name: "create_user"
        params: ["user_data"]
        returns: "User"
      - name: "get_user"
        params: ["user_id"]
        returns: "User"

dependency_graph:
  user: []  # 核心模块，无依赖
  product: []
  order: ["user", "product"]
  payment: ["order"]

organization:
  src/
    user/
      __init__.py
      models.py
      service.py
      repository.py
    order/
      __init__.py
      models.py
      service.py
```

## Examples

### Example 1: Python 包设计

**Input:** 数据处理库

**Output:**
- 包结构划分
- 公开接口定义
- 内部模块组织
- 导入路径设计

### Example 2: C 模块设计

**Input:** 嵌入式系统

**Output:**
- 头文件组织
- 模块接口定义
- 编译依赖管理
- 链接顺序

## Best Practices

1. **单一职责**: 每个模块只做一件事
2. **稳定接口**: 接口设计要稳定
3. **信息隐藏**: 内部实现不暴露
4. **依赖倒置**: 依赖抽象而非具体
