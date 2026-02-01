---
name: skill-selector
version: 1.0.0
scope: meta
trigger:
  - when: 用户需要选择合适的 Skill 时
  - when: 用户询问"应该使用哪个 Skill"时
  - when: 任务需要多个 Skill 协作时
capabilities:
  - 分析任务需求
  - 匹配最佳 Skill
  - 组合多个 Skill
  - 评估执行顺序
  - 处理 Skill 冲突
constraints:
  - 基于明确的需求
  - 考虑 Skill 依赖
  - 避免循环调用
  - 提供备选方案
inputs:
  - task_description: 任务描述
  - context: 上下文信息
  - constraints: 约束条件
outputs:
  - recommended_skills: 推荐的 Skill
  - execution_order: 执行顺序
  - rationale: 选择理由
  - alternatives: 备选方案
references:
  - project: LangChain Router
    url: https://github.com/langchain-ai/langchain
  - project: AutoGPT Planning
    capability: Task routing
---

# Skill Selector

智能选择最合适的 Skill 执行任务。

## When to Invoke

- 不确定使用哪个 Skill
- 复杂任务需要分解
- 多个 Skill 可以处理
- 需要 Skill 组合
- 优化执行路径

## Input Format

```yaml
task_description: "我需要重构这段代码并添加测试"
context:
  language: "python"
  current_stage: "development"
  test_coverage: 0.3
constraints:
  - "不改变外部行为"
  - "需要测试保护"
```

## Output Format

```yaml
recommended_skills:
  - name: "refactor-safe"
    priority: 1
    reason: "首先需要安全重构代码"
  - name: "pytest-design"
    priority: 2
    reason: "重构后需要添加测试"
  - name: "test-coverage"
    priority: 3
    reason: "最后验证覆盖率"

execution_order:
  - step: 1
    skill: "refactor-safe"
    input: "代码路径和重构目标"
    output: "重构后的代码"
  - step: 2
    skill: "pytest-design"
    input: "重构后的代码"
    output: "测试用例"
  - step: 3
    skill: "test-coverage"
    input: "运行测试"
    output: "覆盖率报告"

rationale: |
  1. 首先使用 refactor-safe 进行安全重构
  2. 重构完成后使用 pytest-design 添加测试
  3. 最后使用 test-coverage 验证覆盖率
  
  这个顺序确保：
  - 重构有测试保护
  - 测试覆盖重构后的代码
  - 最终验证质量

alternatives:
  - option: "直接添加测试再重构"
    pros: ["先有测试保护"]
    cons: ["测试可能覆盖旧代码"]
  - option: "使用 complexity-reduce 先简化"
    pros: ["降低复杂度"]
    cons: ["可能改变行为"]
```

## Examples

### Example 1: 代码质量问题

**Input:** "这段代码性能慢且难以维护"

**Output:**
- 推荐 performance-optimize
- 推荐 complexity-reduce
- 推荐 code-review
- 执行顺序建议

### Example 2: 新功能开发

**Input:** "需要设计一个新 API"

**Output:**
- 推荐 api-design
- 推荐 pytest-design
- 推荐 api-doc-gen
- 完整开发流程

## Best Practices

1. **理解需求**: 充分理解任务需求
2. **考虑依赖**: 注意 Skill 间的依赖关系
3. **提供理由**: 解释为什么推荐这些 Skill
4. **备选方案**: 提供备选执行路径
