---
name: api-design
description: 设计清晰、易用的API接口，包括RESTful和GraphQL API的设计、请求响应格式定义、错误处理和API文档生成
---

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

## 输入格式
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

## 输出格式
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

## 使用场景
- 设计新API
- API版本升级
- 第三方接口设计
- API文档生成
- 接口评审

## 最佳实践
1. **资源导向**: URL表示资源，HTTP方法表示操作
2. **一致性**: 命名和格式保持一致
3. **版本控制**: URL或Header中包含版本
4. **文档完善**: 自动生成OpenAPI文档

## 参考项目
- FastAPI: https://github.com/fastapi/fastapi
- OpenAPI: API specification
