# 夸克 STRM 最小实现方案 —— 开源项目调研报告

> 本文档为 **Markdown (.md)** 文件，可直接用于 GitHub / Obsidian / Typora。

---

## 一、目标与技术路线回顾

目标：实现 **Emby/Jellyfin 可播放的夸克网盘 STRM 最小闭环**，满足：

- `.strm` 文件稳定不变  
- 支持 Range / Seek  
- 夸克直链不稳定 → 由**反向代理/播放网关**兜底  
- 全流程尽量 **开源可审计**

技术拆解为 3 层：

1. **夸克接入层**（获取文件、直链、302）
2. **STRM 生成层**（生成本地媒体库结构）
3. **播放网关层**（反向代理 / 302 重定向）

---

## 二、可以覆盖该技术路线的开源项目清单

> ⚠️ 结论先行：  
> **没有一个“单项目”完整实现全部能力**，但以下项目**组合后可以 100% 覆盖最小实现方案**。

---

## 三、夸克接入 / 直链层（必选）

### 1️⃣ OpenList（AList Fork）

- 项目地址：https://github.com/OpenListTeam/OpenList
- 许可证：AGPL-3.0
- 状态：**活跃维护**

#### 能力
- 支持 **夸克网盘（Quark / QuarkTV）**
- 提供：
  - 本地代理下载
  - HTTP 直链
  - 302 重定向
- 对夸克的官方说明明确指出：**只能使用本地代理方式传输**

#### 你要重点参考的部分
- Quark Driver 实现
- 本地代理下载逻辑
- Range 转发逻辑
- QuarkTV 的 302 行为

📌 结论：  
**这是目前唯一稳定、开源、可用的夸克访问基础设施**

---

## 四、STRM 生成层（核心但相对简单）

### 2️⃣ alist-strm

- 项目地址：https://github.com/tefuirZ/alist-strm
- 许可证：MIT
- 语言：Python
- 形态：脚本 / Docker

#### 能力
- 扫描 OpenList 路径
- 批量生成 `.strm`
- 目录 → 本地媒体库结构
- 定时任务支持

#### STRM 内容示例
```text
http://openlist-host:5244/d/quark/电影/xxx.mkv
```

#### 你要参考的部分
- 路径遍历与映射逻辑
- STRM 文件生成规则
- 媒体目录结构设计

---

### 3️⃣ AlistAutoStrm（更工程化）

- 项目地址：https://github.com/imshuai/AlistAutoStrm
- 许可证：MIT
- 语言：Go
- 状态：持续更新

#### 优势
- 数据库存储（避免重复生成）
- 多 OpenList Endpoint
- 并发控制
- 更适合长期运行

📌 建议：  
**如果你要写自己的 STRM 生成器，这个项目非常值得直接读源码**

---

## 五、播放网关 / 反向代理层（最关键）

### 4️⃣ go-emby2openlist（高度推荐）

- 项目地址：https://github.com/AmbitiousJun/go-emby2openlist
- 许可证：MIT
- 语言：Go

#### 能力
- Emby API 级反向代理
- 自动拦截播放请求
- 请求 OpenList → 获取直链
- 返回：
  - 302 给客户端  
  - 或代理流（支持 Range）

#### 你要重点看的
- Range 处理
- Header 保留策略
- 直链缓存与刷新
- Emby PlaybackInfo Hook

📌 结论：  
**这是“你之前说的技术路线”最接近的完整实现**

---

### 5️⃣ MediaHelp（参考，不推荐直接用）

- 项目地址：https://github.com/JieWSOFT/MediaHelp
- 状态：⚠️ 源码已停更，Docker 仍更新
- 许可证：MIT

#### 能力
- 多网盘（含夸克）
- 自动 STRM
- Emby 302 播放

📌 问题
- 源码停止维护
- 强耦合 UI / 功能复杂
- 不适合作为“自研参考母本”

---

## 六、组合方案（强烈推荐）

### ✅ 最稳妥的最小实现组合

```text
[Quark]
   ↓
[OpenList]  ←—— 夸克 Cookie / TV Token
   ↓
[go-emby2openlist]  ←—— 播放反向代理 / Range / 302
   ↓
[Emby / Jellyfin]
   ↑
[AlistAutoStrm]  ←—— 批量生成 .strm
```

### STRM 内容写法（推荐）
```text
http://emby-proxy-host:8096/emby/videos/stream/xxx
```

---

## 七、重要现实结论（请认真看）

1. **SmartStrm = 闭源黑盒**
2. **开源世界是“拼图式方案”，不是一体化产品**
3. 真正困难的不是 `.strm`
   - 而是：
     - 夸克鉴权
     - 直链失效
     - Range 正确性
     - Emby 客户端兼容性

---

## 八、你下一步如果要“自己写”

我可以继续直接帮你做三件事之一：

1. ✍️ 生成 **FastAPI 版最小播放网关代码**
2. ✍️ 拆解 **go-emby2openlist 的关键模块图**
3. ✍️ 帮你设计一个 **“不依赖 OpenList 的纯夸克 STRM MVP”**

你一句话选方向即可。
