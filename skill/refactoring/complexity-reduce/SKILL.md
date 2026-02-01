---
name: complexity-reduce
version: 1.0.0
scope: refactoring
trigger:
  - when: 用户需要降低代码复杂度时
  - when: 用户询问"这段代码太复杂了"时
  - when: 圈复杂度过高需要优化时
capabilities:
  - 计算圈复杂度
  - 识别复杂函数
  - 拆分长函数
  - 简化条件逻辑
  - 消除嵌套层级
constraints:
  - 保持功能等价
  - 不引入新 bug
  - 提高可读性
  - 便于测试
inputs:
  - code_path: 代码路径
  - max_complexity: 最大允许复杂度（默认10）
  - target_functions: 目标函数（可选）
outputs:
  - complexity_report: 复杂度报告
  - complex_functions: 复杂函数列表
  - simplification_plan: 简化方案
  - refactored_code: 重构后代码示例
references:
  - project: radon
    url: https://github.com/rubik/radon
  - project: mccabe
    capability: Cyclomatic complexity checker
---

# Complexity Reduce

降低代码复杂度，提高可读性和可维护性。

## When to Invoke

- 圈复杂度过高（>10）
- 函数过长（>50行）
- 嵌套层级过深（>3层）
- 条件逻辑过于复杂
- 代码难以测试

## Input Format

```yaml
code_path: "./src/business_logic.py"
max_complexity: 10
target_functions:
  - "process_order"
```

## Output Format

```yaml
complexity_report:
  average_complexity: 8.5
  max_complexity: 25
  functions_above_threshold: 3

complex_functions:
  - name: "process_order"
    complexity: 25
    lines: 120
    issues:
      - "嵌套层级: 5"
      - "条件分支: 12"
      - "循环嵌套: 3"

simplification_plan:
  - strategy: "提取条件为函数"
    example: |
      if is_valid_order(order) and not is_blocked_user(user):
          process()
  - strategy: "使用卫语句"
    example: |
      if not valid: return
      if not active: return
      # main logic
  - strategy: "拆分函数"
    example: |
      def validate_order(): ...
      def calculate_price(): ...
      def save_order(): ...

refactored_code: |
  # 重构后的代码示例
  def process_order(order):
      if not validate_order(order):
          return Error("Invalid order")
      price = calculate_price(order)
      return save_order(order, price)
```

## Examples

### Example 1: 简化条件嵌套

**Before:**
```python
if user:
    if user.active:
        if order:
            if order.valid:
                process()
```

**After:**
```python
if not user or not user.active:
    return
if not order or not order.valid:
    return
process()
```

### Example 2: 拆分复杂函数

**Before:**
```python
def process_order(order):  # 100行，复杂度20
    # 验证、计算、保存、通知全部在一起
```

**After:**
```python
def process_order(order):
    validate_order(order)
    price = calculate_price(order)
    save_order(order, price)
    notify_user(order)
```

## Best Practices

1. **单一职责**: 每个函数只做一件事
2. **卫语句**: 提前返回减少嵌套
3. **表驱动**: 用查表替代复杂条件
4. **策略模式**: 多分支条件使用策略模式
