---
name: call-graph-gen
version: 1.0.0
scope: code-comprehension
trigger:
  - when: 用户需要函数调用关系时
  - when: 用户询问"这个函数被谁调用了"时
  - when: 需要分析代码执行路径时
capabilities:
  - 生成函数调用图
  - 识别递归调用
  - 查找入口函数
  - 分析调用深度
  - 发现死代码
constraints:
  - 基于静态分析，动态调用可能遗漏
  - 函数指针/回调分析有限
  - 多态调用需要类型推断
inputs:
  - code_path: 代码路径
  - target_function: 目标函数（可选，分析全部则省略）
  - max_depth: 最大调用深度
outputs:
  - call_graph: 调用图结构
  - entry_points: 入口函数列表
  - recursive_functions: 递归函数列表
  - unreachable_functions: 不可达函数列表
references:
  - project: Code2Flow
    url: https://github.com/scottrogowski/code2flow
  - project: PyCallGraph
    capability: Python call graph generation
---

# Call Graph Generator

生成函数调用关系图，分析代码执行路径。

## When to Invoke

- 理解复杂函数调用链
- 识别递归和循环调用
- 查找代码入口点
- 分析性能瓶颈路径
- 发现未使用的函数

## Input Format

```yaml
code_path: "./src"
target_function: "process_request"  # optional
max_depth: 10
```

## Output Format

```yaml
call_graph:
  process_request:
    calls: ["validate_input", "query_database", "format_response"]
    called_by: ["handle_http_request"]
  validate_input:
    calls: ["check_schema", "sanitize_data"]
    called_by: ["process_request"]

entry_points:
  - "main"
  - "handle_http_request"

recursive_functions:
  - name: "traverse_tree"
    type: "direct"

unreachable_functions:
  - "legacy_handler"
  - "debug_print"
```

## Examples

### Example 1: Web 请求处理流程

**Input:** Flask 应用处理函数

**Output:**
- 请求处理完整调用链
- 中间件调用顺序
- 数据库访问路径
- 异常处理流程

### Example 2: C 算法实现

**Input:** 排序算法实现

**Output:**
- 递归调用树
- 基准情况识别
- 调用深度分析
- 栈空间估算

## Best Practices

1. **控制深度**: 大型项目限制调用深度避免爆炸
2. **区分类型**: 区分直接调用、回调、虚函数调用
3. **关注热点**: 优先分析高频调用路径
4. **结合动态**: 静态分析配合运行时 profiling
