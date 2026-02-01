---
name: crash-debug
version: 1.0.0
scope: debugging
trigger:
  - when: 用户需要调试崩溃时
  - when: 用户询问"程序为什么崩溃"时
  - when: 需要分析 core dump 时
capabilities:
  - 分析崩溃堆栈
  - 解析 core dump
  - 识别内存问题
  - 定位崩溃原因
  - 提供修复建议
constraints:
  - 需要调试符号
  - 可能需要 core dump 文件
  - 复杂问题需要复现
  - 保护敏感数据
inputs:
  - crash_report: 崩溃报告
  - core_dump: core dump 文件路径
  - binary_path: 可执行文件路径
  - reproduction_steps: 复现步骤
outputs:
  - crash_cause: 崩溃原因
  - stack_analysis: 堆栈分析
  - memory_state: 内存状态
  - fix_suggestion: 修复建议
references:
  - project: GDB
    url: https://www.gnu.org/software/gdb/
  - project: LLDB
    capability: LLVM debugger
---

# Crash Debugger

调试程序崩溃，分析 core dump。

## When to Invoke

- 程序异常终止
- 段错误 (Segmentation Fault)
- 内存访问错误
- 断言失败
- 死锁检测

## Input Format

```yaml
crash_report: |
  Segmentation fault (core dumped)
  #0 0x00007f8b in strcpy ()
  #1 0x00007f8c in process_data ()
  #2 0x00007f8d in main ()
core_dump: "/var/crash/core.1234"
binary_path: "./myapp"
reproduction_steps:
  - "启动程序"
  - "输入长字符串"
  - "触发崩溃"
```

## Output Format

```yaml
crash_cause: "缓冲区溢出，strcpy 未检查目标缓冲区大小"

stack_analysis:
  - frame: 0
    function: "strcpy"
    location: "libc.so.6"
    issue: "被调用处"
  - frame: 1
    function: "process_data"
    location: "app.c:45"
    issue: "未检查输入长度"
  - frame: 2
    function: "main"
    location: "main.c:20"

memory_state:
  fault_address: "0x7fff1234"
  access_type: "write"
  buffer_size: "16 bytes"
  input_size: "256 bytes"

fix_suggestion: |
  使用 strncpy 替代 strcpy，并确保目标缓冲区足够大：
  
  strncpy(dest, src, sizeof(dest) - 1);
  dest[sizeof(dest) - 1] = '\0';
```

## Examples

### Example 1: 缓冲区溢出

**Input:** C 程序崩溃

**Output:**
- 定位溢出位置
- 分析内存布局
- 提供安全替代函数
- 建议边界检查

### Example 2: 空指针解引用

**Input:** Python 崩溃

**Output:**
- 定位空指针位置
- 分析对象生命周期
- 建议空值检查
- 提供防御式代码

## Best Practices

1. **启用调试符号**: 编译时保留符号信息
2. **生成 Core Dump**: 配置系统生成 core 文件
3. **保护现场**: 崩溃时保存足够信息
4. **逐步缩小**: 使用二分法定位问题
