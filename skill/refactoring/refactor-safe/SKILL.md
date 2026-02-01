---
name: refactor-safe
version: 1.0.0
scope: refactoring
trigger:
  - when: 用户需要重构代码时
  - when: 用户询问"如何安全地重构这段代码"时
  - when: 需要改进代码结构但不改变行为时
capabilities:
  - 识别重构机会
  - 制定重构计划
  - 建立安全网（测试保护）
  - 执行小步重构
  - 验证重构正确性
constraints:
  - 不改变代码外部行为
  - 每次重构只做一件事
  - 必须有测试保护
  - 支持回滚
inputs:
  - code_path: 代码路径
  - refactor_goal: 重构目标
  - test_coverage: 当前测试覆盖率
outputs:
  - refactor_plan: 重构计划
  - safety_checks: 安全检查清单
  - step_by_step: 分步重构指南
  - rollback_plan: 回滚方案
references:
  - project: Refactoring (Martin Fowler)
    url: https://refactoring.com/
  - project: PyCharm Refactoring
    capability: Automated refactoring
---

# Safe Refactor

安全地重构代码，改进结构而不改变行为。

## When to Invoke

- 代码需要改进可读性
- 消除重复代码
- 简化复杂函数
- 改进命名和结构
- 技术债务偿还

## Input Format

```yaml
code_path: "./src/legacy_module.py"
refactor_goal: "提取重复代码到函数"
test_coverage: 0.75
```

## Output Format

```yaml
refactor_plan:
  steps:
    - "1. 识别重复代码块"
    - "2. 提取为新函数"
    - "3. 替换所有重复处"
    - "4. 运行测试验证"
  estimated_time: "30分钟"

safety_checks:
  - "测试覆盖率 > 70%"
  - "所有测试通过"
  - "静态检查无错误"

step_by_step:
  - step: 1
    action: "识别重复代码"
    code_before: "..."
    code_after: "..."
  - step: 2
    action: "提取函数"
    code_before: "..."
    code_after: "..."

rollback_plan:
  - "git checkout -- src/legacy_module.py"
  - "git stash pop (如果有暂存)"
```

## Examples

### Example 1: 提取函数

**Before:**
```python
# 多处重复的代码
result = []
for item in items:
    if item.active:
        result.append(item)
```

**After:**
```python
def filter_active(items):
    return [item for item in items if item.active]

result = filter_active(items)
```

### Example 2: 重命名变量

**Before:**
```python
def calc(a, b):
    return a + b
```

**After:**
```python
def calculate_sum(first_number, second_number):
    return first_number + second_number
```

## Best Practices

1. **小步前进**: 每次只做一个小重构
2. **频繁测试**: 每步都运行测试
3. **版本控制**: 使用 git 保存检查点
4. **代码审查**: 重构后请他人审查
