---
name: api-design
version: 1.0.0
scope: architecture
trigger:
  - when: 用户需要设计 API 时
  - when: 用户询问"如何设计这个接口"时
  - when: 需要 API 评审时
capabilities:
  - 设计 RESTful API
  - 设计 GraphQL API
  - 定义请求/响应格式
  - 设计错误处理
  - 生成 API 文档
constraints:
  - 遵循行业标准
  - 保持向后兼容
  - 考虑安全性
  - 支持版本控制
inputs:
  - api_requirements: API 需求
  - api_type: API 类型（REST/GraphQL）
  - auth_requirements: 认证需求
outputs:
  - api_spec: API 规范
  - endpoint_design: 端点设计
  - schema_definition: 数据模型
  - error_codes: 错误码定义
references:
  - project: FastAPI
    url: https://github.com/fastapi/fastapi
  - project: OpenAPI
    capability: API specification
---

# API Design

设计清晰、易用的 API 接口。

## When to Invoke

- 设计新 API
- API 版本升级
- 第三方接口设计
- API 文档生成
- 接口评审

## Input Format

```yaml
api_requirements:
  resources:
    - name: "User"
      operations: ["CRUD"]
    - name: "Order"
      operations: ["create", "read", "list"]
api_type: "REST"
auth_requirements:
  type: "JWT"
  scopes: ["read", "write"]
```

## Output Format

```yaml
api_spec:
  openapi: "3.0.0"
  info:
    title: "E-commerce API"
    version: "1.0.0"

endpoint_design:
  - path: "/api/v1/users"
    method: "GET"
    description: "获取用户列表"
    parameters:
      - name: "page"
        type: "integer"
        default: 1
    responses:
      200:
        description: "成功"
        schema: "UserList"

schema_definition:
  User:
    type: "object"
    properties:
      id:
        type: "integer"
      name:
        type: "string"
      email:
        type: "string"
        format: "email"

error_codes:
  - code: 400
    message: "Bad Request"
    description: "请求参数错误"
  - code: 401
    message: "Unauthorized"
    description: "未授权访问"
```

## Examples

### Example 1: REST API

**Input:** 用户管理 API

**Output:**
- 资源 URI 设计
- HTTP 方法映射
- 请求/响应格式
- 分页和过滤

### Example 2: GraphQL API

**Input:** 数据查询 API

**Output:**
- Schema 设计
- Query/Mutation 定义
- 类型系统
- 解析器设计

## Best Practices

1. **资源导向**: URL 表示资源，HTTP 方法表示操作
2. **一致性**: 命名和格式保持一致
3. **版本控制**: URL 或 Header 中包含版本
4. **文档完善**: 自动生成 OpenAPI 文档
