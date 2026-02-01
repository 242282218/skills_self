---
name: doc-generator
version: 1.0.0
scope: documentation
trigger:
  - when: 用户需要生成文档时
  - when: 用户询问"如何写文档"时
  - when: 需要配置文档系统时
capabilities:
  - 配置 Sphinx
  - 配置 MkDocs
  - 生成 API 文档
  - 编写教程
  - 维护文档站点
constraints:
  - 文档与代码同步
  - 支持多版本
  - 易于维护
  - 搜索友好
inputs:
  - project_path: 项目路径
  - doc_tool: 文档工具
  - doc_types: 文档类型
outputs:
  - doc_config: 文档配置
  - doc_structure: 文档结构
  - template: 文档模板
  - publish_guide: 发布指南
references:
  - project: Sphinx
    url: https://github.com/sphinx-doc/sphinx
  - project: MkDocs
    capability: Static site generator
---

# Doc Generator

生成和维护项目文档。

## When to Invoke

- 新项目文档初始化
- 配置文档站点
- 生成 API 文档
- 编写用户指南
- 发布文档

## Input Format

```yaml
project_path: "./myproject"
doc_tool: "mkdocs"
doc_types:
  - "api"
  - "tutorial"
  - "faq"
```

## Output Format

```yaml
doc_config: |
  site_name: My Project
  site_url: https://myproject.readthedocs.io
  
  theme:
    name: material
    palette:
      - scheme: default
        primary: indigo
  
  nav:
    - Home: index.md
    - Getting Started:
      - Installation: getting-started/installation.md
      - Quick Start: getting-started/quickstart.md
    - API Reference: api/
    - User Guide:
      - Configuration: guide/configuration.md
      - Advanced Usage: guide/advanced.md
  
  plugins:
    - search
    - mkdocstrings:
        handlers:
          python:
            selection:
              docstring_style: google

doc_structure:
  docs/
    index.md
    getting-started/
      installation.md
      quickstart.md
    guide/
      configuration.md
      advanced.md
    api/
      index.md

template: |
  # Page Title
  
  ## Overview
  
  Brief description of the feature.
  
  ## Usage
  
  ```python
  example code
  ```
  
  ## API Reference
  
  ### Function Name
  
  Description of the function.
  
  **Parameters:**
  - `param1`: Description
  
  **Returns:**
  - Return value description

publish_guide:
  - "提交文档到仓库"
  - "配置 Read the Docs"
  - "设置 Webhook"
  - "验证文档构建"
```

## Examples

### Example 1: Python 库文档

**Input:** 工具库

**Output:**
- Sphinx 配置
- API 文档生成
- 教程编写
- 发布到 Read the Docs

### Example 2: C 项目文档

**Input:** C 库

**Output:**
- Doxygen 配置
- 代码注释规范
- 生成 HTML/PDF
- 版本文档管理

## Best Practices

1. **文档即代码**: 文档与代码一起版本控制
2. **示例丰富**: 提供可运行的示例
3. **及时更新**: 代码变更同步更新文档
4. **用户视角**: 从用户角度编写文档
