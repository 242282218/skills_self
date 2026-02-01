## 修改目标
修改 updater.py，使其在爬取项目时生成标准格式的 SKILL.md，文件名包含 global/project 类型。

## 标准格式要求
```yaml
---
name: skill-name
description: 一句话描述技能功能
---

# Skill Title

## 能力
- 能力1
- 能力2

## 约束
- 约束1
- 约束2

## 使用场景
...

## 最佳实践
...
```

## 具体修改内容

### 1. 添加技能类型映射
在 SkillUpdater 类中添加分类规则：
```python
# 技能类型映射（根据路径判断）
SKILL_TYPE_MAP = {
    'architecture': 'global',
    'code-comprehension': 'global',
    'debugging': 'global',
    'documentation': 'global',
    'meta': 'global',
    'refactoring': 'global',
    'devops': 'project',
    'frontend': 'project',
    'testing': 'project',
}
```

### 2. 添加生成标准格式 SKILL.md 的方法
```python
def generate_standard_skill_md(self, skill_name: str, skill_type: str, 
                                description: str, capabilities: list,
                                constraints: list, **kwargs) -> str:
    """生成标准格式的 SKILL.md 内容"""
    content = f"""---
name: {skill_name}
description: {description}
---

# {skill_name.replace('-', ' ').title()} Skill

## 能力
"""
    for cap in capabilities:
        content += f"- {cap}\n"
    
    content += "\n## 约束\n"
    for cons in constraints:
        content += f"- {cons}\n"
    
    # 添加其他章节...
    return content
```

### 3. 修改 create_skill_zips_in_all 方法
- 根据技能路径判断类型（global/project）
- 生成标准格式的 SKILL.md
- 压缩包内使用带类型的文件名（如 `global-api-design/SKILL.md`）
- 压缩包文件名也包含类型（如 `global-api-design.zip`）

### 4. 修改 apply_update 方法
- 更新 SKILL.md 时使用标准格式
- 保留原有 Markdown 内容，只简化 YAML frontmatter

## 文件名格式
- 压缩包文件名：`{type}-{skill-name}.zip`（如 `global-api-design.zip`）
- 压缩包内结构：`{type}-{skill-name}/SKILL.md`（如 `global-api-design/SKILL.md`）

## 范围
- 修改文件：`skill/.updater/updater.py`
- 影响：所有生成的压缩包和 SKILL.md 格式

## 验证
1. 运行 updater.py 生成新的压缩包
2. 检查压缩包内 SKILL.md 格式是否符合标准
3. 测试导入 Trae IDE 验证