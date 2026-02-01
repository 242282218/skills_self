---
name: log-analyzer
version: 1.0.0
scope: debugging
trigger:
  - when: 用户需要分析日志时
  - when: 用户询问"日志里有什么问题"时
  - when: 需要从日志中定位问题时
capabilities:
  - 解析日志格式
  - 识别错误模式
  - 时间序列分析
  - 异常检测
  - 生成分析报告
constraints:
  - 基于日志内容分析
  - 需要足够的日志样本
  - 不访问外部系统
  - 保护敏感信息
inputs:
  - log_content: 日志内容
  - log_format: 日志格式
  - time_range: 时间范围
  - filter_keywords: 过滤关键词
outputs:
  - error_summary: 错误摘要
  - pattern_analysis: 模式分析
  - timeline: 时间线
  - recommendations: 建议
references:
  - project: ELK Stack
    url: https://www.elastic.co/what-is/elk-stack
  - project: Splunk
    capability: Log analysis
---

# Log Analyzer

分析系统日志，识别问题和异常模式。

## When to Invoke

- 排查生产问题
- 监控系统健康
- 安全审计
- 性能分析
- 故障复盘

## Input Format

```yaml
log_content: |
  2024-01-15 10:23:45 ERROR Connection timeout
  2024-01-15 10:23:46 WARN Retrying connection
  2024-01-15 10:23:48 ERROR Connection failed
log_format: "timestamp level message"
time_range:
  start: "2024-01-15 10:00:00"
  end: "2024-01-15 11:00:00"
filter_keywords:
  - "ERROR"
  - "WARN"
```

## Output Format

```yaml
error_summary:
  total_errors: 45
  total_warnings: 12
  top_errors:
    - "Connection timeout": 23
    - "Database error": 15
    - "Memory warning": 7

pattern_analysis:
  - pattern: "Connection timeout"
    frequency: "每 5 分钟"
    correlation: "高负载时段"
    severity: "high"

timeline:
  - time: "10:23:45"
    event: "首次连接超时"
    level: "ERROR"
  - time: "10:23:48"
    event: "连接失败"
    level: "ERROR"

recommendations:
  - "检查网络连接"
  - "增加连接超时时间"
  - "实现连接池"
```

## Examples

### Example 1: Web 服务器日志

**Input:** Nginx access log

**Output:**
- 错误请求统计
- 慢请求分析
- 攻击模式检测
- 性能瓶颈识别

### Example 2: 应用日志

**Input:** Python 应用日志

**Output:**
- 异常堆栈分析
- 调用链追踪
- 性能指标提取
- 错误趋势分析

## Best Practices

1. **结构化日志**: 使用 JSON 格式便于分析
2. **日志级别**: 合理使用 DEBUG/INFO/WARN/ERROR
3. **上下文信息**: 包含请求 ID 等追踪信息
4. **定期归档**: 历史日志定期清理归档
