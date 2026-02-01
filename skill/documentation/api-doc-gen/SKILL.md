---
name: api-doc-gen
version: 1.0.0
scope: documentation
trigger:
  - when: 用户需要生成 API 文档时
  - when: 用户询问"如何写 API 文档"时
  - when: 需要 Swagger/OpenAPI 文档时
capabilities:
  - 生成 OpenAPI 规范
  - 配置 Swagger UI
  - 提取代码注释
  - 生成客户端 SDK
  - 维护 API 版本
constraints:
  - 与代码同步
  - 准确反映行为
  - 包含示例
  - 支持多版本
inputs:
  - api_code: API 代码
  - doc_format: 文档格式
  - include_examples: 是否包含示例
outputs:
  - open_api_spec: OpenAPI 规范
  - swagger_config: Swagger 配置
  - code_examples: 代码示例
  - changelog: API 变更日志
references:
  - project: Swagger
    url: https://github.com/swagger-api/swagger-ui
  - project: FastAPI
    capability: Auto API docs
---

# API Doc Generator

生成和维护 API 文档。

## When to Invoke

- 新项目 API 文档
- 更新 API 规范
- 生成客户端 SDK
- API 版本管理
- 开发者门户

## Input Format

```yaml
api_code: "./src/api"
doc_format: "openapi3"
include_examples: true
```

## Output Format

```yaml
open_api_spec: |
  openapi: 3.0.3
  info:
    title: Example API
    description: API description
    version: 1.0.0
  
  paths:
    /users:
      get:
        summary: List users
        parameters:
          - name: page
            in: query
            schema:
              type: integer
              default: 1
        responses:
          '200':
            description: Success
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/UserList'
  
  components:
    schemas:
      User:
        type: object
        properties:
          id:
            type: integer
          name:
            type: string

swagger_config: |
  swagger-ui:
    url: /openapi.json
    docExpansion: list
    defaultModelsExpandDepth: 1

code_examples:
  python: |
    import requests
    
    response = requests.get('https://api.example.com/users')
    users = response.json()
  
  javascript: |
    fetch('https://api.example.com/users')
      .then(res => res.json())
      .then(data => console.log(data))

changelog: |
  ## v1.1.0 (2024-01-15)
  - Added: New endpoint `/orders`
  - Changed: Updated response format for `/users`
  
  ## v1.0.0 (2024-01-01)
  - Initial release
```

## Examples

### Example 1: REST API 文档

**Input:** Flask API

**Output:**
- OpenAPI 规范
- Swagger UI 配置
- 请求/响应示例
- 认证说明

### Example 2: GraphQL 文档

**Input:** GraphQL API

**Output:**
- Schema 文档
- 查询示例
- Playground 配置
- 类型定义

## Best Practices

1. **代码优先**: 从代码自动生成文档
2. **实时同步**: 文档与代码保持同步
3. **完整示例**: 提供请求和响应示例
4. **版本控制**: 管理 API 版本变更
