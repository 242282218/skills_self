---
name: dead-code-clean
version: 1.0.0
scope: refactoring
trigger:
  - when: 用户需要清理未使用代码时
  - when: 用户询问"哪些代码可以删除"时
  - when: 需要减少代码库体积时
capabilities:
  - 识别未使用函数/变量
  - 发现不可达代码
  - 检测重复代码
  - 清理无效导入
  - 评估删除影响
constraints:
  - 不删除测试代码
  - 保留公共 API
  - 确认无运行时调用
  - 支持回滚
inputs:
  - project_path: 项目路径
  - entry_points: 入口文件
  - exclude_patterns: 排除模式
outputs:
  - dead_code_list: 死代码列表
  - impact_analysis: 影响分析
  - cleanup_plan: 清理计划
  - safety_verification: 安全验证步骤
references:
  - project: vulture
    url: https://github.com/jendrikseipp/vulture
  - project: coverage.py
    capability: Code coverage analysis
---

# Dead Code Clean

清理未使用的代码，减少技术债务。

## When to Invoke

- 代码库体积过大
- 维护成本过高
- 遗留代码清理
- 重构前准备
- 代码审查发现冗余

## Input Format

```yaml
project_path: "./src"
entry_points:
  - "main.py"
  - "cli.py"
exclude_patterns:
  - "**/test_*.py"
  - "**/migrations/**"
```

## Output Format

```yaml
dead_code_list:
  unused_functions:
    - name: "legacy_handler"
      file: "handlers.py"
      line: 45
      confidence: "high"
  unused_variables:
    - name: "DEBUG_FLAG"
      file: "config.py"
      line: 12
  unreachable_code:
    - file: "utils.py"
      lines: "100-120"
      reason: "after return statement"

impact_analysis:
  safe_to_remove:
    - "legacy_handler"
  needs_review:
    - "DEBUG_FLAG (可能被动态使用)"

cleanup_plan:
  - step: 1
    action: "删除 legacy_handler"
    files: ["handlers.py"]
  - step: 2
    action: "清理未使用导入"
    files: ["*.py"]

safety_verification:
  - "运行完整测试套件"
  - "检查动态调用 (getattr, eval)"
  - "验证公共 API 完整性"
```

## Examples

### Example 1: 未使用函数

**Detected:**
```python
def unused_helper(x):
    return x * 2  # 从未被调用
```

**Action:** 安全删除

### Example 2: 不可达代码

**Detected:**
```python
def process():
    return result
    print("never reached")  # 死代码
```

**Action:** 删除不可达代码

## Best Practices

1. **逐步清理**: 不要一次性删除太多
2. **测试保护**: 每次删除后运行测试
3. **版本控制**: 保留删除历史
4. **文档更新**: 同步更新相关文档
