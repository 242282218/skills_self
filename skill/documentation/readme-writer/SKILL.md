---
name: readme-writer
version: 1.0.0
scope: documentation
trigger:
  - when: 用户需要写 README 时
  - when: 用户询问"README 应该包含什么"时
  - when: 需要优化项目介绍时
capabilities:
  - 编写项目介绍
  - 编写安装指南
  - 编写使用示例
  - 添加徽章
  - 生成目录
constraints:
  - 简洁明了
  - 重点突出
  - 易于理解
  - 格式规范
inputs:
  - project_info: 项目信息
  - target_audience: 目标读者
  - sections: 需要包含的章节
outputs:
  - readme_content: README 内容
  - badges: 徽章配置
  - toc: 目录结构
  - template: 模板
references:
  - project: Standard Readme
    url: https://github.com/RichardLitt/standard-readme
  - project: Awesome README
    capability: README examples
---

# README Writer

编写清晰、专业的项目 README。

## When to Invoke

- 新项目初始化
- 重写项目介绍
- 添加使用说明
- 优化项目展示
- 开源项目发布

## Input Format

```yaml
project_info:
  name: "My Awesome Project"
  description: "A tool for doing awesome things"
  language: "Python"
  license: "MIT"

target_audience: "developers"

sections:
  - "installation"
  - "usage"
  - "api"
  - "contributing"
```

## Output Format

```yaml
readme_content: |
  # My Awesome Project
  
  [![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()
  
  > A tool for doing awesome things
  
  ## Table of Contents
  
  - [Installation](#installation)
  - [Usage](#usage)
  - [API](#api)
  - [Contributing](#contributing)
  - [License](#license)
  
  ## Installation
  
  ```bash
  pip install my-awesome-project
  ```
  
  ## Usage
  
  ```python
  from my_project import Awesome
  
  tool = Awesome()
  result = tool.do_something()
  ```
  
  ## API
  
  ### `Awesome.do_something()`
  
  Does something awesome.
  
  **Returns:** `Result` - The result of the operation
  
  ## Contributing
  
  Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.
  
  ## License
  
  This project is licensed under the MIT License.

badges:
  build: "https://img.shields.io/badge/build-passing-brightgreen"
  license: "https://img.shields.io/badge/License-MIT-yellow.svg"
  version: "https://img.shields.io/pypi/v/my-project"

toc: |
  ## Table of Contents
  
  - [Installation](#installation)
  - [Usage](#usage)
  - [API](#api)
  - [Contributing](#contributing)
  - [License](#license)

template: |
  # {project_name}
  
  {badges}
  
  > {description}
  
  ## Table of Contents
  
  {toc}
  
  ## Installation
  
  {installation}
  
  ## Usage
  
  {usage}
  
  ## License
  
  {license}
```

## Examples

### Example 1: 开源库 README

**Input:** Python 工具库

**Output:**
- 项目介绍
- 安装说明
- 使用示例
- 贡献指南
- 许可证

### Example 2: 应用项目 README

**Input:** Web 应用

**Output:**
- 功能介绍
- 部署指南
- 环境配置
- 截图展示
- 联系方式

## Best Practices

1. **首屏原则**: 重要信息在第一屏展示
2. **示例驱动**: 用示例说明用法
3. **清晰结构**: 使用标题和列表
4. **视觉吸引**: 添加徽章和截图
