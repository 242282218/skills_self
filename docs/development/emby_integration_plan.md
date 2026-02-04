# Emby 深度集成开发方案

## 📋 文档信息
- **版本**: v1.0
- **创建时间**: 2026-02-04
- **状态**: 待实施
- **优先级**: P1

---

## 🎯 目标概述

### 核心需求
实现 Emby 媒体服务器与 quark_strm 系统的深度集成，实现以下功能：

1. **自动刷新媒体库** - STRM 生成/重命名后触发 Emby 扫描
2. **定时刷新** - 支持 cron 表达式定时触发刷新
3. **指定媒体库刷新** - 支持刷新特定媒体库而非全库
4. **刷新通知** - 刷新完成/失败时发送通知
5. **刷新日志** - 记录历史刷新操作

### 用户信息
| 配置项 | 值 |
|--------|-----|
| 媒体服务器 | Emby |
| 服务器地址 | http://YOUR_EMBY_HOST:8096 |
| API Key | YOUR_EMBY_API_KEY |
| 配置位置 | config.yaml + 前端页面 |

---

## 🏗️ 系统架构

### 整体架构图

```
┌──────────────────────────────────────────────────────────────────┐
│                        触发源 (Triggers)                          │
├────────────────┬────────────────┬────────────────────────────────┤
│  STRM 生成完成  │  智能重命名完成  │       定时任务 (Cron)           │
└───────┬────────┴───────┬────────┴───────────────┬────────────────┘
        │                │                        │
        └────────────────┴────────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────────┐
        │           EmbyService                   │
        │  ┌─────────────────────────────────────┐│
        │  │  - 刷新指定媒体库                    ││
        │  │  - 刷新全部媒体库                    ││
        │  │  - 获取媒体库列表                    ││
        │  │  - 测试连接                          ││
        │  └─────────────────────────────────────┘│
        └─────────────────┬───────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────────┐
        │         Emby API Client                 │
        │  ┌─────────────────────────────────────┐│
        │  │  POST /Library/Refresh              ││
        │  │  POST /Items/{id}/Refresh           ││
        │  │  GET /Library/MediaFolders          ││
        │  └─────────────────────────────────────┘│
        └─────────────────┬───────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────────┐
        │         Emby Server                     │
        │         http://YOUR_EMBY_HOST:8096      │
        └─────────────────────────────────────────┘
```

### 模块划分

```
quark_strm/
├── app/
│   ├── services/
│   │   └── emby_service.py       # 新增: Emby 服务核心逻辑
│   ├── api/
│   │   └── emby.py               # 新增: Emby API 路由
│   └── config/
│       └── settings.py           # 更新: 添加 Emby 配置模型
├── web/
│   └── src/
│       ├── views/
│       │   └── ConfigView.vue    # 更新: 添加 Emby 配置卡片
│       └── api/
│           └── emby.ts           # 新增: 前端 Emby API
└── config.yaml                   # 更新: 添加 emby 配置段
```

---

## 📝 详细设计

### 1. 配置结构

#### config.yaml 配置段
```yaml
# Emby 媒体服务器配置
emby:
  # 是否启用 Emby 集成
  enabled: true
  # Emby 服务器地址
  url: "http://YOUR_EMBY_HOST:8096"
  # Emby API Key (在 Emby 设置 -> 高级 -> API 密钥中获取)
  api_key: "YOUR_EMBY_API_KEY"
  # 刷新设置
  refresh:
    # STRM 生成后自动刷新
    on_strm_generate: true
    # 智能重命名后自动刷新
    on_rename: true
    # 定时刷新 (cron 表达式, 空则不启用)
    cron: "0 */6 * * *"  # 每6小时执行一次
    # 刷新的媒体库ID列表 (空则刷新全部)
    library_ids: []
  # 超时设置 (秒)
  timeout: 30
  # 刷新完成后发送通知
  notify_on_complete: true
```

#### Pydantic 配置模型
```python
# app/config/settings.py

from pydantic import BaseModel
from typing import Optional, List


class EmbyRefreshConfig(BaseModel):
    """
    Emby 刷新配置模型
    
    用途: 定义 Emby 媒体库刷新的触发条件和定时任务
    """
    on_strm_generate: bool = True
    on_rename: bool = True
    cron: Optional[str] = None
    library_ids: List[str] = []


class EmbyConfig(BaseModel):
    """
    Emby 服务器配置模型
    
    用途: 定义 Emby 服务器连接和刷新配置
    """
    enabled: bool = False
    url: str = ""
    api_key: str = ""
    refresh: EmbyRefreshConfig = EmbyRefreshConfig()
    timeout: int = 30
    notify_on_complete: bool = True
```

---

### 2. 后端服务实现

#### EmbyService 核心服务

```python
# app/services/emby_service.py

"""
Emby 媒体服务器集成服务

用途: 提供与 Emby 服务器交互的核心功能，包括媒体库刷新、连接测试等
"""

import aiohttp
import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass

from app.core.config_manager import ConfigManager
from app.core.logger import logger
from app.services.notification_service import NotificationService, NotificationType


@dataclass
class EmbyLibrary:
    """
    Emby 媒体库数据结构
    
    用途: 表示 Emby 中的一个媒体库
    """
    id: str
    name: str
    collection_type: Optional[str] = None  # movies, tvshows, music, etc.


@dataclass
class RefreshResult:
    """
    刷新结果数据结构
    
    用途: 记录单次刷新操作的结果
    """
    success: bool
    library_id: Optional[str]
    library_name: Optional[str]
    message: str
    timestamp: datetime


class EmbyService:
    """
    Emby 服务核心类
    
    用途: 封装所有与 Emby 服务器的交互逻辑
    输入: 通过 ConfigManager 获取配置
    输出: 刷新结果、媒体库列表等
    副作用: 
        - 调用 Emby REST API
        - 记录刷新日志
        - 发送通知
    """
    
    def __init__(self):
        self.config = ConfigManager().get_config()
        self._refresh_history: List[RefreshResult] = []
        self._max_history = 100
        self._is_refreshing = False
    
    @property
    def emby_config(self):
        """获取 Emby 配置"""
        return getattr(self.config, 'emby', None)
    
    @property
    def is_enabled(self) -> bool:
        """检查 Emby 集成是否启用"""
        return self.emby_config and self.emby_config.enabled and self.emby_config.url and self.emby_config.api_key
    
    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        发送 HTTP 请求到 Emby API
        
        用途: 统一的 HTTP 请求封装
        输入:
            - method (str): HTTP 方法 (GET, POST, etc.)
            - endpoint (str): API 端点路径
            - data (dict): 请求体数据
        输出:
            - dict: 响应 JSON 数据
        副作用: 发起网络请求
        """
        if not self.is_enabled:
            raise ValueError("Emby 集成未启用或配置不完整")
        
        url = f"{self.emby_config.url}/emby{endpoint}"
        params = {"api_key": self.emby_config.api_key}
        
        timeout = aiohttp.ClientTimeout(total=self.emby_config.timeout)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers={"Accept": "application/json", "Content-Type": "application/json"}
            ) as response:
                if response.status == 200 or response.status == 204:
                    if response.content_length and response.content_length > 0:
                        return await response.json()
                    return {"status": "ok"}
                else:
                    error_text = await response.text()
                    raise Exception(f"Emby API 错误 [{response.status}]: {error_text}")
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        测试 Emby 服务器连接
        
        用途: 验证 Emby 配置是否正确，服务器是否可达
        输入: 无
        输出:
            - dict: 包含 success, message, server_info 字段
        副作用: 无
        """
        try:
            # 获取系统信息来验证连接
            result = await self._request("GET", "/System/Info")
            return {
                "success": True,
                "message": "连接成功",
                "server_info": {
                    "server_name": result.get("ServerName", "Unknown"),
                    "version": result.get("Version", "Unknown"),
                    "operating_system": result.get("OperatingSystem", "Unknown")
                }
            }
        except Exception as e:
            logger.error(f"Emby 连接测试失败: {e}")
            return {
                "success": False,
                "message": f"连接失败: {str(e)}",
                "server_info": None
            }
    
    async def get_libraries(self) -> List[EmbyLibrary]:
        """
        获取所有媒体库列表
        
        用途: 获取 Emby 中配置的所有媒体库，用于选择刷新范围
        输入: 无
        输出:
            - List[EmbyLibrary]: 媒体库列表
        副作用: 无
        """
        try:
            result = await self._request("GET", "/Library/MediaFolders")
            libraries = []
            for item in result.get("Items", []):
                libraries.append(EmbyLibrary(
                    id=item.get("Id", ""),
                    name=item.get("Name", ""),
                    collection_type=item.get("CollectionType")
                ))
            return libraries
        except Exception as e:
            logger.error(f"获取 Emby 媒体库列表失败: {e}")
            return []
    
    async def refresh_library(self, library_id: str, library_name: str = "") -> RefreshResult:
        """
        刷新指定媒体库
        
        用途: 触发 Emby 重新扫描指定的媒体库
        输入:
            - library_id (str): 媒体库 ID
            - library_name (str): 媒体库名称（用于日志）
        输出:
            - RefreshResult: 刷新结果
        副作用: 
            - 触发 Emby 库扫描
            - 记录刷新历史
        """
        try:
            # POST /Items/{id}/Refresh
            await self._request("POST", f"/Items/{library_id}/Refresh")
            
            result = RefreshResult(
                success=True,
                library_id=library_id,
                library_name=library_name,
                message=f"媒体库 {library_name or library_id} 刷新已触发",
                timestamp=datetime.now()
            )
            logger.info(result.message)
            
        except Exception as e:
            result = RefreshResult(
                success=False,
                library_id=library_id,
                library_name=library_name,
                message=f"刷新失败: {str(e)}",
                timestamp=datetime.now()
            )
            logger.error(result.message)
        
        self._add_to_history(result)
        return result
    
    async def refresh_all_libraries(self) -> List[RefreshResult]:
        """
        刷新所有媒体库
        
        用途: 触发 Emby 扫描所有媒体库
        输入: 无
        输出:
            - List[RefreshResult]: 所有库的刷新结果
        副作用: 
            - 触发 Emby 全库扫描
            - 记录刷新历史
        """
        try:
            # 方式1: 直接刷新根库
            await self._request("POST", "/Library/Refresh")
            
            result = RefreshResult(
                success=True,
                library_id=None,
                library_name="所有媒体库",
                message="全部媒体库刷新已触发",
                timestamp=datetime.now()
            )
            logger.info(result.message)
            self._add_to_history(result)
            return [result]
            
        except Exception as e:
            result = RefreshResult(
                success=False,
                library_id=None,
                library_name="所有媒体库",
                message=f"全库刷新失败: {str(e)}",
                timestamp=datetime.now()
            )
            logger.error(result.message)
            self._add_to_history(result)
            return [result]
    
    async def refresh_configured_libraries(self) -> List[RefreshResult]:
        """
        刷新配置中指定的媒体库
        
        用途: 根据 config.yaml 中的 library_ids 配置刷新对应媒体库
        输入: 无
        输出:
            - List[RefreshResult]: 刷新结果列表
        副作用: 
            - 触发 Emby 库扫描
            - 记录刷新历史
            - 发送通知（如配置）
        """
        if self._is_refreshing:
            logger.warning("已有刷新任务正在进行中，跳过本次请求")
            return []
        
        self._is_refreshing = True
        results = []
        
        try:
            library_ids = self.emby_config.refresh.library_ids if self.emby_config.refresh else []
            
            if not library_ids:
                # 未指定则刷新全部
                results = await self.refresh_all_libraries()
            else:
                # 获取库名称映射
                libraries = await self.get_libraries()
                lib_map = {lib.id: lib.name for lib in libraries}
                
                for lib_id in library_ids:
                    lib_name = lib_map.get(lib_id, lib_id)
                    result = await self.refresh_library(lib_id, lib_name)
                    results.append(result)
                    # 间隔一小段时间，避免请求过快
                    await asyncio.sleep(0.5)
            
            # 发送通知
            if self.emby_config.notify_on_complete:
                await self._send_notification(results)
                
        finally:
            self._is_refreshing = False
        
        return results
    
    async def trigger_refresh_on_event(self, event_type: str) -> bool:
        """
        根据事件类型触发刷新
        
        用途: 供其他模块调用，在特定事件后触发 Emby 刷新
        输入:
            - event_type (str): 事件类型 ("strm_generate", "rename")
        输出:
            - bool: 是否成功触发
        副作用: 异步触发刷新任务
        """
        if not self.is_enabled:
            return False
        
        refresh_config = self.emby_config.refresh
        
        should_refresh = False
        if event_type == "strm_generate" and refresh_config.on_strm_generate:
            should_refresh = True
        elif event_type == "rename" and refresh_config.on_rename:
            should_refresh = True
        
        if should_refresh:
            logger.info(f"事件 [{event_type}] 触发 Emby 媒体库刷新")
            # 异步执行，不阻塞主流程
            asyncio.create_task(self.refresh_configured_libraries())
            return True
        
        return False
    
    def get_refresh_history(self, limit: int = 20) -> List[Dict]:
        """
        获取刷新历史记录
        
        用途: 提供刷新操作的历史记录
        输入:
            - limit (int): 返回记录数量限制
        输出:
            - List[Dict]: 历史记录列表
        副作用: 无
        """
        history = self._refresh_history[-limit:]
        return [
            {
                "success": r.success,
                "library_id": r.library_id,
                "library_name": r.library_name,
                "message": r.message,
                "timestamp": r.timestamp.isoformat()
            }
            for r in reversed(history)
        ]
    
    def _add_to_history(self, result: RefreshResult):
        """添加到历史记录"""
        self._refresh_history.append(result)
        # 保持历史记录不超过最大值
        if len(self._refresh_history) > self._max_history:
            self._refresh_history = self._refresh_history[-self._max_history:]
    
    async def _send_notification(self, results: List[RefreshResult]):
        """发送刷新完成通知"""
        try:
            notification_service = NotificationService()
            
            success_count = sum(1 for r in results if r.success)
            fail_count = len(results) - success_count
            
            if fail_count == 0:
                message = f"Emby 媒体库刷新完成，成功刷新 {success_count} 个库"
                await notification_service.send(
                    type_=NotificationType.INFO,
                    title="Emby 刷新完成",
                    message=message
                )
            else:
                message = f"Emby 媒体库刷新完成，成功 {success_count} 个，失败 {fail_count} 个"
                await notification_service.send(
                    type_=NotificationType.WARNING,
                    title="Emby 刷新部分失败",
                    message=message
                )
        except Exception as e:
            logger.error(f"发送 Emby 刷新通知失败: {e}")


# 全局服务实例
_emby_service: Optional[EmbyService] = None


def get_emby_service() -> EmbyService:
    """
    获取 EmbyService 单例实例
    
    用途: 提供全局唯一的 Emby 服务实例
    """
    global _emby_service
    if _emby_service is None:
        _emby_service = EmbyService()
    return _emby_service
```

---

### 3. API 路由

```python
# app/api/emby.py

"""
Emby API 路由

用途: 提供 Emby 相关的 REST API 接口
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List

from app.services.emby_service import get_emby_service
from app.core.logger import logger


router = APIRouter(prefix="/emby", tags=["Emby"])


class EmbyConfigUpdate(BaseModel):
    """Emby 配置更新请求体"""
    enabled: bool
    url: str
    api_key: str
    on_strm_generate: bool = True
    on_rename: bool = True
    cron: Optional[str] = None
    library_ids: List[str] = []
    notify_on_complete: bool = True


class RefreshRequest(BaseModel):
    """刷新请求体"""
    library_ids: Optional[List[str]] = None


@router.get("/test-connection")
async def test_connection():
    """
    测试 Emby 服务器连接
    
    用途: 验证当前配置的 Emby 服务器是否可达
    输入: 无
    输出: 连接测试结果
    """
    service = get_emby_service()
    result = await service.test_connection()
    return result


@router.get("/libraries")
async def get_libraries():
    """
    获取 Emby 媒体库列表
    
    用途: 获取所有可用的媒体库，供用户选择刷新范围
    输入: 无
    输出: 媒体库列表
    """
    service = get_emby_service()
    
    if not service.is_enabled:
        raise HTTPException(status_code=400, detail="Emby 集成未启用")
    
    libraries = await service.get_libraries()
    return {
        "success": True,
        "libraries": [
            {
                "id": lib.id,
                "name": lib.name,
                "collection_type": lib.collection_type
            }
            for lib in libraries
        ]
    }


@router.post("/refresh")
async def refresh_libraries(request: RefreshRequest = None):
    """
    手动触发媒体库刷新
    
    用途: 手动触发 Emby 媒体库刷新
    输入:
        - library_ids: 要刷新的媒体库 ID 列表（可选，空则刷新配置的库或全部）
    输出: 刷新结果
    """
    service = get_emby_service()
    
    if not service.is_enabled:
        raise HTTPException(status_code=400, detail="Emby 集成未启用")
    
    try:
        if request and request.library_ids:
            # 刷新指定的库
            results = []
            for lib_id in request.library_ids:
                result = await service.refresh_library(lib_id)
                results.append({
                    "success": result.success,
                    "library_id": result.library_id,
                    "message": result.message
                })
        else:
            # 刷新配置的库
            refresh_results = await service.refresh_configured_libraries()
            results = [
                {
                    "success": r.success,
                    "library_id": r.library_id,
                    "library_name": r.library_name,
                    "message": r.message
                }
                for r in refresh_results
            ]
        
        return {
            "success": True,
            "message": "刷新任务已触发",
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Emby 刷新失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/refresh/history")
async def get_refresh_history(limit: int = Query(default=20, ge=1, le=100)):
    """
    获取刷新历史记录
    
    用途: 查看最近的刷新操作记录
    输入:
        - limit: 返回记录数量（1-100）
    输出: 历史记录列表
    """
    service = get_emby_service()
    history = service.get_refresh_history(limit=limit)
    return {
        "success": True,
        "history": history
    }


@router.get("/status")
async def get_status():
    """
    获取 Emby 集成状态
    
    用途: 获取当前 Emby 集成的配置和运行状态
    输入: 无
    输出: 状态信息
    """
    service = get_emby_service()
    
    status = {
        "enabled": service.is_enabled,
        "connected": False,
        "server_info": None,
        "configuration": None
    }
    
    if service.is_enabled:
        # 测试连接
        connection_result = await service.test_connection()
        status["connected"] = connection_result["success"]
        status["server_info"] = connection_result.get("server_info")
        
        # 配置信息
        emby_config = service.emby_config
        status["configuration"] = {
            "url": emby_config.url,
            "api_key": "***" + emby_config.api_key[-4:] if len(emby_config.api_key) > 4 else "***",
            "refresh_on_strm": emby_config.refresh.on_strm_generate,
            "refresh_on_rename": emby_config.refresh.on_rename,
            "cron": emby_config.refresh.cron,
            "library_ids": emby_config.refresh.library_ids,
            "notify_on_complete": emby_config.notify_on_complete
        }
    
    return status
```

---

### 4. 定时任务集成

```python
# 在 app/services/cron_service.py 中添加 Emby 定时刷新任务

from app.services.emby_service import get_emby_service

async def setup_emby_cron_job():
    """
    设置 Emby 定时刷新任务
    
    用途: 根据配置设置 Emby 媒体库的定时刷新任务
    输入: 无
    输出: 无
    副作用: 向调度器添加定时任务
    """
    from apscheduler.triggers.cron import CronTrigger
    from app.core.scheduler import scheduler
    
    emby_service = get_emby_service()
    
    if not emby_service.is_enabled:
        logger.info("Emby 集成未启用，跳过定时任务设置")
        return
    
    cron_expr = emby_service.emby_config.refresh.cron
    if not cron_expr:
        logger.info("Emby 定时刷新未配置，跳过")
        return
    
    try:
        # 解析 cron 表达式 (分 时 日 月 周)
        parts = cron_expr.split()
        if len(parts) == 5:
            trigger = CronTrigger(
                minute=parts[0],
                hour=parts[1],
                day=parts[2],
                month=parts[3],
                day_of_week=parts[4]
            )
            
            # 添加任务
            scheduler.add_job(
                func=emby_service.refresh_configured_libraries,
                trigger=trigger,
                id="emby_refresh_job",
                name="Emby 媒体库定时刷新",
                replace_existing=True
            )
            
            logger.info(f"Emby 定时刷新任务已设置: {cron_expr}")
        else:
            logger.error(f"无效的 cron 表达式: {cron_expr}")
            
    except Exception as e:
        logger.error(f"设置 Emby 定时任务失败: {e}")
```

---

### 5. 触发点集成

#### STRM 生成后触发

```python
# 在 app/services/strm_service.py 的 scan_and_generate 方法末尾添加:

async def scan_and_generate(self, ...):
    """原有的 STRM 生成方法"""
    # ... 原有代码 ...
    
    # 生成完成后触发 Emby 刷新
    try:
        from app.services.emby_service import get_emby_service
        emby_service = get_emby_service()
        await emby_service.trigger_refresh_on_event("strm_generate")
    except Exception as e:
        logger.warning(f"触发 Emby 刷新失败（不影响主流程）: {e}")
    
    return result
```

#### 智能重命名后触发

```python
# 在 app/services/smart_rename_service.py 的 execute_rename 方法末尾添加:

async def execute_rename(self, ...):
    """原有的重命名执行方法"""
    # ... 原有代码 ...
    
    # 重命名完成后触发 Emby 刷新
    try:
        from app.services.emby_service import get_emby_service
        emby_service = get_emby_service()
        await emby_service.trigger_refresh_on_event("rename")
    except Exception as e:
        logger.warning(f"触发 Emby 刷新失败（不影响主流程）: {e}")
    
    return result
```

---

### 6. 前端界面

#### 配置卡片组件
```vue
<!-- web/src/components/EmbyConfigCard.vue -->

<template>
  <el-card class="emby-config-card">
    <template #header>
      <div class="card-header">
        <span class="title">
          <el-icon><Monitor /></el-icon>
          Emby 集成
        </span>
        <el-tag :type="statusType" size="small">{{ statusText }}</el-tag>
      </div>
    </template>
    
    <el-form :model="form" label-width="140px" :disabled="loading">
      <!-- 启用开关 -->
      <el-form-item label="启用 Emby 集成">
        <el-switch v-model="form.enabled" />
      </el-form-item>
      
      <!-- 服务器地址 -->
      <el-form-item label="服务器地址" required>
        <el-input 
          v-model="form.url" 
          placeholder="http://YOUR_EMBY_HOST:8096"
          :disabled="!form.enabled"
        >
          <template #append>
            <el-button :loading="testing" @click="testConnection">
              测试连接
            </el-button>
          </template>
        </el-input>
      </el-form-item>
      
      <!-- API Key -->
      <el-form-item label="API Key" required>
        <el-input 
          v-model="form.api_key" 
          type="password"
          show-password
          placeholder="Emby API Key"
          :disabled="!form.enabled"
        />
        <div class="form-tip">在 Emby 设置 → 高级 → API 密钥中获取</div>
      </el-form-item>
      
      <!-- 自动刷新设置 -->
      <el-divider>自动刷新设置</el-divider>
      
      <el-form-item label="STRM 生成后刷新">
        <el-switch v-model="form.on_strm_generate" :disabled="!form.enabled" />
      </el-form-item>
      
      <el-form-item label="重命名后刷新">
        <el-switch v-model="form.on_rename" :disabled="!form.enabled" />
      </el-form-item>
      
      <el-form-item label="定时刷新">
        <el-input 
          v-model="form.cron" 
          placeholder="0 */6 * * * (每6小时)"
          :disabled="!form.enabled"
        />
        <div class="form-tip">Cron 表达式，留空则不启用定时刷新</div>
      </el-form-item>
      
      <!-- 媒体库选择 -->
      <el-form-item label="刷新媒体库">
        <el-select 
          v-model="form.library_ids" 
          multiple 
          placeholder="全部媒体库"
          :disabled="!form.enabled"
          style="width: 100%"
        >
          <el-option
            v-for="lib in libraries"
            :key="lib.id"
            :label="lib.name"
            :value="lib.id"
          />
        </el-select>
        <div class="form-tip">留空则刷新全部媒体库</div>
      </el-form-item>
      
      <!-- 通知设置 -->
      <el-form-item label="刷新完成通知">
        <el-switch v-model="form.notify_on_complete" :disabled="!form.enabled" />
      </el-form-item>
    </el-form>
    
    <!-- 操作按钮 -->
    <div class="card-actions">
      <el-button type="primary" :loading="saving" @click="saveConfig">
        保存配置
      </el-button>
      <el-button :disabled="!form.enabled" @click="manualRefresh">
        立即刷新
      </el-button>
    </div>
    
    <!-- 服务器信息 -->
    <div v-if="serverInfo" class="server-info">
      <el-descriptions title="服务器信息" :column="3" size="small" border>
        <el-descriptions-item label="名称">{{ serverInfo.server_name }}</el-descriptions-item>
        <el-descriptions-item label="版本">{{ serverInfo.version }}</el-descriptions-item>
        <el-descriptions-item label="系统">{{ serverInfo.operating_system }}</el-descriptions-item>
      </el-descriptions>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Monitor } from '@element-plus/icons-vue'
import { embyApi } from '@/api/emby'

const loading = ref(false)
const saving = ref(false)
const testing = ref(false)
const connected = ref(false)
const serverInfo = ref(null)
const libraries = ref([])

const form = reactive({
  enabled: false,
  url: '',
  api_key: '',
  on_strm_generate: true,
  on_rename: true,
  cron: '',
  library_ids: [],
  notify_on_complete: true
})

const statusType = computed(() => {
  if (!form.enabled) return 'info'
  return connected.value ? 'success' : 'danger'
})

const statusText = computed(() => {
  if (!form.enabled) return '未启用'
  return connected.value ? '已连接' : '未连接'
})

const testConnection = async () => {
  testing.value = true
  try {
    const result = await embyApi.testConnection()
    if (result.success) {
      ElMessage.success('连接成功')
      connected.value = true
      serverInfo.value = result.server_info
      await loadLibraries()
    } else {
      ElMessage.error(result.message || '连接失败')
      connected.value = false
    }
  } catch (e) {
    ElMessage.error('连接测试失败')
  } finally {
    testing.value = false
  }
}

const loadLibraries = async () => {
  try {
    const result = await embyApi.getLibraries()
    libraries.value = result.libraries || []
  } catch (e) {
    console.error('加载媒体库失败', e)
  }
}

const saveConfig = async () => {
  saving.value = true
  try {
    await embyApi.updateConfig(form)
    ElMessage.success('配置已保存')
  } catch (e) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const manualRefresh = async () => {
  try {
    await embyApi.refresh()
    ElMessage.success('刷新任务已触发')
  } catch (e) {
    ElMessage.error('刷新失败')
  }
}

onMounted(async () => {
  // 加载当前状态
  loading.value = true
  try {
    const status = await embyApi.getStatus()
    if (status.enabled) {
      form.enabled = true
      connected.value = status.connected
      serverInfo.value = status.server_info
      if (status.configuration) {
        Object.assign(form, status.configuration)
      }
      await loadLibraries()
    }
  } catch (e) {
    console.error('加载配置失败', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.emby-config-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.card-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.server-info {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}
</style>
```

---

## 🔧 实施步骤

### Phase 1: 基础服务实现（约 2 小时）

1. [ ] 更新 `config.yaml` 添加 emby 配置段
2. [ ] 更新 `app/config/settings.py` 添加 Pydantic 模型
3. [ ] 创建 `app/services/emby_service.py` 核心服务
4. [ ] 创建 `app/api/emby.py` API 路由
5. [ ] 在 `app/main.py` 注册路由

### Phase 2: 触发点集成（约 1 小时）

6. [ ] 修改 `strm_service.py` 添加刷新触发
7. [ ] 修改 `smart_rename_service.py` 添加刷新触发
8. [ ] 在 `cron_service.py` 添加定时任务支持

### Phase 3: 前端界面（约 2 小时）

9. [ ] 创建 `web/src/api/emby.ts` 前端 API
10. [ ] 创建 `EmbyConfigCard.vue` 配置组件
11. [ ] 集成到 `ConfigView.vue` 系统配置页面

### Phase 4: 测试与文档（约 1 小时）

12. [ ] 测试连接功能
13. [ ] 测试手动刷新
14. [ ] 测试自动触发刷新
15. [ ] 测试定时刷新
16. [ ] 更新项目文档

---

## 🧪 测试用例

### 单元测试
```python
# tests/test_emby_service.py

import pytest
from app.services.emby_service import EmbyService, EmbyLibrary

class TestEmbyService:
    """Emby 服务单元测试"""
    
    @pytest.mark.asyncio
    async def test_connection_success(self, mock_emby_server):
        """测试连接成功"""
        service = EmbyService()
        result = await service.test_connection()
        assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_get_libraries(self, mock_emby_server):
        """测试获取媒体库列表"""
        service = EmbyService()
        libraries = await service.get_libraries()
        assert len(libraries) > 0
        assert isinstance(libraries[0], EmbyLibrary)
    
    @pytest.mark.asyncio
    async def test_refresh_library(self, mock_emby_server):
        """测试刷新指定媒体库"""
        service = EmbyService()
        result = await service.refresh_library("1", "Movies")
        assert result.success is True
```

---

## 📊 验收标准

| 功能 | 验收标准 | 优先级 |
|------|---------|--------|
| 配置保存 | 配置可保存到 config.yaml 并在启动时加载 | P0 |
| 连接测试 | 可测试 Emby 服务器连接并获取服务器信息 | P0 |
| 手动刷新 | 可手动触发媒体库刷新 | P0 |
| STRM 触发 | STRM 生成后自动触发刷新 | P1 |
| 重命名触发 | 智能重命名后自动触发刷新 | P1 |
| 定时刷新 | 支持 cron 表达式定时刷新 | P1 |
| 指定库刷新 | 支持只刷新指定的媒体库 | P1 |
| 刷新通知 | 刷新完成后发送通知 | P2 |
| 刷新历史 | 可查看最近的刷新记录 | P2 |

---

## 🔗 Emby API 参考

### 核心 API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/emby/System/Info` | GET | 获取服务器信息 |
| `/emby/Library/MediaFolders` | GET | 获取媒体库列表 |
| `/emby/Library/Refresh` | POST | 刷新所有媒体库 |
| `/emby/Items/{id}/Refresh` | POST | 刷新指定媒体库 |
| `/emby/Users` | GET | 获取用户列表 |

### 认证方式

所有请求需要在 URL 参数中添加 `api_key`:
```
GET /emby/System/Info?api_key=YOUR_EMBY_API_KEY
```

---

## 📝 注意事项

1. **异常处理**: Emby 刷新失败不应影响主流程（STRM 生成/重命名）
2. **并发控制**: 同时只允许一个刷新任务运行，避免重复刷新
3. **超时设置**: 网络请求设置合理超时（30秒）
4. **敏感信息**: API Key 在日志和响应中需脱敏显示
5. **兼容性**: 代码应同时兼容 Emby 和 Jellyfin（API 基本一致）

---

**文档作者**: Developer Agent  
**状态**: 待实施  
**预计工时**: 5-6 小时
