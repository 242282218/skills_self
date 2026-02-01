---
name: bug-localizer
version: 1.0.0
scope: debugging
trigger:
  - when: 用户需要定位 Bug 时
  - when: 用户询问"这个 Bug 在哪里"时
  - when: 需要根据错误信息定位问题时
capabilities:
  - 分析错误堆栈
  - 定位问题代码位置
  - 识别根本原因
  - 提供修复建议
  - 生成调试步骤
constraints:
  - 基于提供的错误信息
  - 不保证一定能定位
  - 需要代码访问权限
  - 可能需要复现步骤
inputs:
  - error_message: 错误信息
  - stack_trace: 堆栈跟踪
  - code_context: 相关代码
  - reproduction_steps: 复现步骤
outputs:
  - root_cause: 根本原因
  - location: 问题位置
  - fix_suggestion: 修复建议
  - debug_steps: 调试步骤
references:
  - project: PDB
    url: https://docs.python.org/3/library/pdb.html
  - project: GDB
    capability: C/C++ debugger
---

# Bug Localizer

定位代码中的 Bug，分析错误根本原因。

## When to Invoke

- 程序抛出异常
- 行为不符合预期
- 测试失败
- 用户报告问题
- 日志中出现错误

## Input Format

```yaml
error_message: "IndexError: list index out of range"
stack_trace: |
  File "app.py", line 45, in process
    item = items[index]
  File "app.py", line 30, in handle
    process(data)
code_context: |
  def process(items):
      for i in range(len(items) + 1):
          item = items[i]  # line 45
reproduction_steps:
  - "启动应用"
  - "发送空列表"
  - "触发错误"
```

## Output Format

```yaml
root_cause: "循环范围错误，i 的范围超出列表长度"
location:
  file: "app.py"
  line: 45
  function: "process"

fix_suggestion: |
  将 range(len(items) + 1) 改为 range(len(items))
  
  修改后代码：
  def process(items):
      for i in range(len(items)):
          item = items[i]

debug_steps:
  - "在 line 44 设置断点"
  - "检查 items 长度和 i 的值"
  - "验证循环边界条件"
```

## Examples

### Example 1: Python IndexError

**Input:** 列表索引越界错误

**Output:**
- 定位越界位置
- 分析循环边界
- 提供修复代码
- 建议防御式编程

### Example 2: C 段错误

**Input:** Segmentation fault

**Output:**
- 分析指针使用
- 定位空指针解引用
- 建议内存检查工具
- 提供修复方案

## Best Practices

1. **收集信息**: 完整的错误信息和上下文
2. **最小复现**: 创建最小复现案例
3. **二分定位**: 使用二分法缩小范围
4. **验证修复**: 确保修复不引入新问题
