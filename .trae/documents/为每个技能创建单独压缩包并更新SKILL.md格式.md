## 目标
为每个技能创建单独的压缩包（如api-design.zip），压缩包内直接是SKILL.md文件，并更新SKILL.md格式以符合Trae标准。

## 实施步骤

### 1. 修改updater.py
- 修改`create_category_zips`方法，改为为每个技能创建单独的压缩包
- 压缩包直接放在all目录下，格式为`skill-name.zip`
- 压缩包内直接是SKILL.md文件（不包含目录）

### 2. 更新SKILL.md格式
根据Trae标准，SKILL.md需要包含：
- **技能名称**：name字段
- **描述**：description字段（简短描述技能用途）
- **指令**：instructions字段（详细的使用说明、规则、示例等）

将现有的SKILL.md内容转换为Trae标准格式，保留原有的capabilities、constraints等信息作为指令的一部分。

### 3. 实施细节
- 遍历all目录下的所有技能目录
- 为每个技能创建单独的zip文件
- zip文件内直接包含SKILL.md（不在子目录中）
- 更新后的SKILL.md格式示例：
```yaml
---
name: api-design
description: 设计清晰、易用的API接口，包括RESTful和GraphQL API
instructions: |
  # API Design Skill
  
  ## 能力
  - 设计RESTful API
  - 设计GraphQL API
  - 定义请求/响应格式
  - 设计错误处理
  - 生成API文档
  
  ## 约束
  - 遵循行业标准
  - 保持向后兼容
  - 考虑安全性
  - 支持版本控制
  
  ## 使用示例
  ...
---
```

### 4. 验证
- 检查每个压缩包是否正确创建
- 验证压缩包内SKILL.md的位置（根目录）
- 确认SKILL.md格式符合Trae标准