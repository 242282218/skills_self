# Skill 目录变更日志

所有 Skill 的变更记录都保存在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### Added
- 初始化 Skill 目录结构
- 创建 30 个工程 Skill
  - code-comprehension: 4 个 Skill（代码理解）
  - refactoring: 4 个 Skill（重构优化）
  - testing: 4 个 Skill（测试验证）
  - debugging: 3 个 Skill（调试排障）
  - architecture: 3 个 Skill（架构设计）
  - devops: 4 个 Skill（运维部署）
  - documentation: 3 个 Skill（文档交付）
  - meta: 3 个 Skill（元能力）
  - frontend: 3 个 Skill（前端开发）
- 实现自动更新系统（.updater/）
  - 配置文件 config.yaml
  - 更新引擎 updater.py
  - 支持定时任务和手动触发

## [1.0.0] - 2024-02-01

### Added
#### Code Comprehension（代码理解）
- `code-explainer` - 代码解释器
- `code-summarizer` - 代码摘要生成器
- `dependency-mapper` - 依赖关系映射器
- `call-graph-gen` - 调用图生成器

#### Refactoring（重构优化）
- `refactor-safe` - 安全重构
- `performance-optimize` - 性能优化
- `dead-code-clean` - 死代码清理
- `complexity-reduce` - 复杂度降低

#### Testing（测试验证）
- `pytest-design` - pytest 测试设计
- `c-unit-test` - C 单元测试
- `test-coverage` - 测试覆盖率
- `fuzz-test-gen` - 模糊测试生成

#### Debugging（调试排障）
- `bug-localizer` - Bug 定位器
- `log-analyzer` - 日志分析器
- `crash-debug` - 崩溃调试器

#### Architecture（架构设计）
- `system-design` - 系统设计
- `api-design` - API 设计
- `module-design` - 模块设计

#### DevOps（运维部署）
- `ci-cd-config` - CI/CD 配置
- `container-build` - 容器构建
- `python-packaging` - Python 打包
- `c-build-system` - C 构建系统

#### Documentation（文档交付）
- `doc-generator` - 文档生成器
- `api-doc-gen` - API 文档生成
- `readme-writer` - README 编写

#### Meta（元能力）
- `skill-selector` - Skill 选择器
- `plan-decomposer` - 任务分解器
- `skill-updater` - Skill 更新器

#### Frontend（前端开发）
- `react-component` - React 组件
- `vue-component` - Vue 组件
- `frontend-optimize` - 前端优化

### 参考项目
- pytest-dev/pytest (11k+ stars)
- fastapi/fastapi (78k+ stars)
- docker/docker (69k+ stars)
- kubernetes/kubernetes (110k+ stars)
- facebook/react (230k+ stars)
- vuejs/core (Vue 3)
- Kitware/CMake
- python/cpython

---

## 更新规则

### 版本号升级规则

| 更新类型 | 版本升级 | 示例 |
|---------|---------|------|
| 破坏性变更 | major | 1.0.0 -> 2.0.0 |
| 新功能 | minor | 1.0.0 -> 1.1.0 |
| Bug 修复 | patch | 1.0.0 -> 1.0.1 |
| 文档更新 | patch | 1.0.0 -> 1.0.1 |
| 最佳实践更新 | minor | 1.0.0 -> 1.1.0 |

### 自动更新触发条件

1. **定时触发**: 每周日凌晨 2 点自动检查
2. **手动触发**: 运行 `python .updater/updater.py`
3. **事件触发**: 追踪的开源项目发布新版本

### 追踪的开源项目

| 项目 | 影响 Skill | 追踪内容 |
|------|-----------|---------|
| pytest | testing/pytest-design | Release |
| fastapi | architecture/api-design | Release |
| docker | devops/container-build | Release |
| kubernetes | devops/container-build | Release |
| react | frontend/react-component | Release |
| vue | frontend/vue-component | Release |
| cmake | devops/c-build-system | Release |
| cpython | devops/python-packaging | Release |

---

## 如何贡献

1. 提交 Issue 描述需要添加或修改的 Skill
2. 遵循 SKILL.md 格式规范
3. 更新本 CHANGELOG
4. 提交 Pull Request

## 联系方式

- 项目主页: https://github.com/your-org/skills
- Issue 追踪: https://github.com/your-org/skills/issues
