---
name: code-explainer
version: 1.0.0
scope: code-comprehension
trigger:
  - when: 用户需要理解陌生代码时
  - when: 用户询问"这段代码是做什么的"时
  - when: 用户需要代码逻辑解释时
capabilities:
  - 逐行解释代码逻辑
  - 识别代码设计模式
  - 解释算法和数据结构
  - 标注关键代码段
  - 解释代码依赖关系
constraints:
  - 不修改代码
  - 不假设代码意图（基于实际逻辑解释）
  - 对不确定的部分明确标注
inputs:
  - code: 需要解释的代码片段或文件路径
  - language: 编程语言（Python/C/其他）
  - focus_area: 关注的特定部分（可选）
outputs:
  - explanation: 代码逻辑解释
  - key_points: 关键要点列表
  - design_patterns: 识别的设计模式
  - complexity_notes: 复杂度说明
references:
  - project: MetaGPT
    url: https://github.com/geekan/MetaGPT
    section: AnalyzeCode action
  - project: OpenAI Codex
    capability: Code understanding and explanation
---

# Code Explainer

解释代码逻辑，帮助开发者理解陌生代码。

## When to Invoke

- 接手新项目需要快速理解代码库
- Code Review 时需要理解他人代码
- 学习开源项目源码
- 维护遗留代码

## Input Format

```yaml
code: |
  def fibonacci(n):
      if n <= 1:
          return n
      return fibonacci(n-1) + fibonacci(n-2)
language: python
focus_area: "递归逻辑"  # optional
```

## Output Format

```yaml
explanation: |
  这是一个递归实现的斐波那契数列函数。
  基本情况：当 n <= 1 时直接返回 n
  递归情况：返回前两个数之和
key_points:
  - "时间复杂度 O(2^n)，存在大量重复计算"
  - "空间复杂度 O(n)，递归栈深度"
  - "可以使用 memoization 优化"
design_patterns:
  - "递归模式"
complexity_notes:
  time: "O(2^n)"
  space: "O(n)"
```

## Examples

### Example 1: Python 装饰器

**Input:**
```python
@cache
def expensive_operation(x):
    return heavy_computation(x)
```

**Output:**
- 解释装饰器 `@cache` 的作用
- 说明缓存机制和适用场景
- 指出线程安全注意事项

### Example 2: C 指针操作

**Input:**
```c
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}
```

**Output:**
- 解释指针解引用操作
- 说明函数参数传递机制
- 指出内存安全注意事项

## Best Practices

1. **分层解释**: 先整体后细节
2. **关联上下文**: 解释代码在系统中的位置
3. **指出风险**: 标注潜在问题和改进点
4. **使用类比**: 用熟悉的概念解释复杂逻辑
