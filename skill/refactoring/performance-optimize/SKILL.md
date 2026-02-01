---
name: performance-optimize
version: 1.0.0
scope: refactoring
trigger:
  - when: 用户需要优化代码性能时
  - when: 用户询问"这段代码太慢了"时
  - when: 需要降低时间/空间复杂度时
capabilities:
  - 性能瓶颈分析
  - 算法优化建议
  - 数据结构优化
  - 并发/并行优化
  - 内存使用优化
constraints:
  - 保持代码可读性
  - 避免过早优化
  - 基于 profiling 数据
  - 验证优化效果
inputs:
  - code_path: 代码路径
  - performance_issue: 性能问题描述
  - profiling_data: 性能分析数据（可选）
outputs:
  - bottleneck_analysis: 瓶颈分析
  - optimization_plan: 优化方案
  - expected_improvement: 预期改进
  - benchmark_code: 基准测试代码
references:
  - project: Python cProfile
    url: https://docs.python.org/3/library/profile.html
  - project: gprof
    capability: C performance profiling
---

# Performance Optimize

优化代码性能，降低时间和空间复杂度。

## When to Invoke

- 代码执行时间过长
- 内存占用过高
- 响应时间不满足要求
- 高并发性能瓶颈
- 资源利用率低

## Input Format

```yaml
code_path: "./src/data_processor.py"
performance_issue: "处理大数据集时内存溢出"
profiling_data: "memory_profile.log"
```

## Output Format

```yaml
bottleneck_analysis:
  hotspots:
    - location: "line 45: process_data()"
      issue: "O(n^2) 嵌套循环"
      severity: "high"
  memory_usage:
    peak: "2.5GB"
    leak_suspected: false

optimization_plan:
  - strategy: "使用生成器替代列表"
    effort: "low"
    impact: "high"
    code_changes: "..."
  - strategy: "使用向量化操作"
    effort: "medium"
    impact: "high"
    code_changes: "..."

expected_improvement:
  time_reduction: "60%"
  memory_reduction: "80%"

benchmark_code: |
  import timeit
  timeit.timeit('optimized_func()', setup='...', number=1000)
```

## Examples

### Example 1: Python 列表推导优化

**Before:**
```python
result = []
for x in data:
    if x > 0:
        result.append(x * 2)
```

**After:**
```python
result = [x * 2 for x in data if x > 0]
```

### Example 2: C 缓存优化

**Before:**
```c
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
        sum += a[j][i];  // 缓存不友好
```

**After:**
```c
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
        sum += a[i][j];  // 缓存友好
```

## Best Practices

1. **先测量**: 用 profiler 找到真正瓶颈
2. **渐进优化**: 小步优化，持续验证
3. **保持简单**: 复杂优化要有显著收益
4. **文档说明**: 复杂优化需要注释说明
