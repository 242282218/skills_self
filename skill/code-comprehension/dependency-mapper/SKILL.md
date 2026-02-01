---
name: dependency-mapper
version: 1.0.0
scope: code-comprehension
trigger:
  - when: 用户需要梳理项目依赖关系时
  - when: 用户询问"这个模块依赖哪些组件"时
  - when: 需要分析依赖循环或耦合时
capabilities:
  - 分析模块间依赖关系
  - 识别循环依赖
  - 生成依赖图描述
  - 评估耦合度
  - 发现未使用的依赖
constraints:
  - 基于静态分析，不执行代码
  - 对动态导入可能遗漏
  - 区分直接依赖和传递依赖
inputs:
  - project_path: 项目根目录
  - entry_points: 入口文件列表
  - include_external: 是否包含外部依赖
outputs:
  - dependency_graph: 依赖关系图（文本描述）
  - circular_dependencies: 循环依赖列表
  - unused_dependencies: 未使用依赖列表
  - coupling_metrics: 耦合度指标
references:
  - project: pydeps
    url: https://github.com/thebjorn/pydeps
  - project: CInclude2Dot
    capability: C dependency visualization
---

# Dependency Mapper

分析代码依赖关系，识别模块耦合和循环依赖。

## When to Invoke

- 重构前了解模块关系
- 解决循环依赖问题
- 评估代码架构健康度
- 剥离模块或微服务化

## Input Format

```yaml
project_path: "./myproject"
entry_points:
  - "src/main.py"
  - "src/cli.py"
include_external: false
```

## Output Format

```yaml
dependency_graph:
  modules:
    - name: "auth"
      depends_on: ["database", "cache"]
    - name: "api"
      depends_on: ["auth", "models"]
    - name: "models"
      depends_on: ["database"]

circular_dependencies:
  - cycle: ["module_a", "module_b", "module_a"]
    severity: "high"

unused_dependencies:
  - "legacy_utils"
  - "deprecated_api"

coupling_metrics:
  afferent_coupling:
    api: 5  # 被 5 个模块依赖
  efferent_coupling:
    utils: 8  # 依赖 8 个模块
```

## Examples

### Example 1: Python 项目依赖分析

**Input:** Flask Web 应用

**Output:**
- 蓝图之间的依赖关系
- 数据库模型依赖图
- 工具模块被引用情况
- 建议的模块拆分方案

### Example 2: C 项目头文件依赖

**Input:** 嵌入式 C 项目

**Output:**
- 头文件包含关系
- 前向声明优化建议
- 循环包含检测
- 编译时间优化建议

## Best Practices

1. **分层架构**: 依赖应该单向流动
2. **依赖倒置**: 高层模块不依赖低层实现
3. **接口隔离**: 通过接口减少直接依赖
4. **定期清理**: 移除未使用的依赖
