## 问题分析
根据截图和搜索结果，SKILL.md格式问题在于：
- 错误：使用了`instructions:`字段将内容放在YAML frontmatter中
- 正确：YAML frontmatter只包含元数据（name, description等），指令内容应该作为Markdown body放在`---`之后

## 正确格式示例
```markdown
---
name: api-design
description: 设计清晰、易用的API接口...
---

# API Design Skill

## 能力
- 设计RESTful API
- 设计GraphQL API
...

## 约束
- 遵循行业标准
...
```

## 实施步骤
1. 修改api-design的SKILL.md，将instructions内容移到YAML frontmatter之后作为Markdown body
2. 验证格式是否正确
3. 重新生成压缩包
4. 测试导入