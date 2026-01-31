"""
代理API路由

参考: MediaHelp proxy.py
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse, Response
from app.services.proxy_service import ProxyService
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/proxy", tags=["代理服务"])


@router.get("/stream/{file_id}")
async def proxy_stream(request: Request, file_id: str):
    """
    代理视频流

    参考: MediaHelp proxy.py

    支持302重定向和Range请求
    """
    try:
        service = ProxyService()
        range_header = request.headers.get("Range")
        result = await service.proxy_stream(file_id, range_header)
        return result
    except Exception as e:
        logger.error(f"Failed to proxy stream: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
