---
name: code-summarizer
version: 1.0.0
scope: code-comprehension
trigger:
  - when: 用户需要代码文件摘要时
  - when: 用户询问"这个模块是做什么的"时
  - when: 需要生成代码文档概述时
capabilities:
  - 生成文件/模块功能摘要
  - 提取关键类和函数
  - 识别主要职责和依赖
  - 生成代码统计信息
constraints:
  - 摘要长度控制在 200-500 字
  - 突出核心功能，省略实现细节
  - 保持客观，不添加主观评价
inputs:
  - file_path: 代码文件路径
  - code_content: 代码内容（可选，如果提供 file_path）
  - summary_type: 摘要类型（brief/detailed）
outputs:
  - summary: 功能摘要
  - key_components: 关键组件列表
  - dependencies: 主要依赖
  - statistics: 代码统计
references:
  - project: Semantic Kernel
    url: https://github.com/microsoft/semantic-kernel
    section: SummarizeSkill
  - project: LangChain
    capability: Document summarization
---

# Code Summarizer

生成代码文件或模块的简洁摘要。

## When to Invoke

- 快速了解代码文件功能
- 生成项目文档
- 代码库导航和索引
- 编写 README 或技术文档

## Input Format

```yaml
file_path: "src/auth/middleware.py"
summary_type: "detailed"
```

## Output Format

```yaml
summary: |
  该模块实现了基于 JWT 的认证中间件。
  主要功能包括：Token 验证、权限检查、
  用户上下文注入、错误处理。
key_components:
  - name: "JWTAuthMiddleware"
    type: "class"
    purpose: "主中间件类"
  - name: "validate_token"
    type: "function"
    purpose: "验证 JWT Token"
dependencies:
  - "jwt"
  - "fastapi"
  - "redis"
statistics:
  lines: 150
  functions: 8
  classes: 2
```

## Examples

### Example 1: Python 模块摘要

**Input:** 一个数据处理模块

**Output:**
- 一句话概括：数据清洗和转换模块
- 核心功能列表
- 输入输出格式说明
- 关键配置项

### Example 2: C 头文件摘要

**Input:** 一个网络库头文件

**Output:**
- 模块用途概述
- 导出的函数列表
- 数据结构定义
- 使用注意事项

## Best Practices

1. **金字塔结构**: 最重要的信息放在前面
2. **量化描述**: 使用具体数字（函数数、行数）
3. **职责单一**: 每个模块只描述一个主要职责
4. **依赖透明**: 明确列出外部依赖
