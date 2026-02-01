---
name: skill-updater
version: 1.0.0
scope: meta
trigger:
  - when: 检测到开源项目重大更新时
  - when: 手动触发 Skill 更新检查时
  - when: 需要同步最新工程实践时
capabilities:
  - 监控开源项目 Release/PR/文档
  - 检测工程实践变化
  - 自动更新 SKILL.md 内容
  - 版本号自动升级（semver）
  - 生成 CHANGELOG 条目
  - 创建更新报告
constraints:
  - 不自动合并 breaking changes
  - 需要人工审核高风险变更
  - 保留历史版本可回滚
  - 只更新特定 section
inputs:
  - skill_path: Skill 路径
  - update_source: 更新来源
  - update_type: 更新类型
outputs:
  - update_plan: 更新计划
  - diff: 变更对比
  - changelog_entry: 变更日志条目
  - version_bump: 版本升级
references:
  - project: Dependabot
    url: https://github.com/dependabot
  - project: Renovate
    capability: Dependency update
---

# Skill Updater

自动更新 Skill 内容，保持与开源项目同步。

## When to Invoke

- 定时检查更新
- 开源项目发布新版本
- 工程实践变化
- 手动触发更新
- 批量更新多个 Skill

## Input Format

```yaml
skill_path: "skill/testing/pytest-design"
update_source: "pytest-dev/pytest"
update_type: "best_practice"
```

## Output Format

```yaml
update_plan:
  skill: "pytest-design"
  current_version: "1.0.0"
  new_version: "1.1.0"
  
  changes:
    - section: "capabilities"
      action: "add"
      content: "- 支持 pytest-asyncio"
      reason: "pytest 7.0 新增异步测试支持"
      
    - section: "references"
      action: "update"
      content: "version: '7.0+'"
      reason: "pytest 7.0 发布"
      
    - section: "examples"
      action: "add"
      content: |
        ### Example: 异步测试
        ```python
        @pytest.mark.asyncio
        async def test_async():
            result = await async_function()
            assert result == expected
        ```

diff: |
  --- a/skill/testing/pytest-design/SKILL.md
  +++ b/skill/testing/pytest-design/SKILL.md
  @@ -10,6 +10,7 @@ capabilities:
     - 设计单元测试用例
     - 使用 pytest fixture
     - 参数化测试设计
  +  - 异步测试设计
     - Mock/Stub 设计
     - 测试数据构造

changelog_entry: |
  ## [1.1.0] - 2024-01-15
  
  ### Added
  - 新增异步测试设计能力（参考 pytest 7.0）
  - 添加 pytest-asyncio 示例
  
  ### Changed
  - 更新 pytest 版本引用至 7.0+

version_bump:
  from: "1.0.0"
  to: "1.1.0"
  type: "minor"
  reason: "新增功能，向后兼容"
```

## Examples

### Example 1: 检测到新版本

**Input:** pytest 发布 8.0

**Output:**
- 分析新特性
- 更新 capabilities
- 添加新示例
- 升级版本号

### Example 2: 最佳实践变化

**Input:** 社区推荐新测试模式

**Output:**
- 更新 best_practices
- 修改示例代码
- 记录变更原因
- 生成更新报告

## Best Practices

1. **增量更新**: 只更新变化的部分
2. **版本控制**: 遵循 semver 规范
3. **变更记录**: 详细记录每次更新
4. **回滚准备**: 保留历史版本
