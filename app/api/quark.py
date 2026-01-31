"""
夸克API路由
"""

from fastapi import APIRouter, HTTPException
from app.services.quark_service import QuarkService
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/quark", tags=["夸克服务"])


@router.get("/files/{parent}")
async def get_files(parent: str, only_video: bool = False):
    """
    获取文件列表

    参考: OpenList quark_uc/util.go:69-111
    """
    try:
        service = QuarkService(cookie="")
        files = await service.get_files(parent, only_video)
        await service.close()
        return {"files": files, "count": len(files)}
    except Exception as e:
        logger.error(f"Failed to get files: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/link/{file_id}")
async def get_download_link(file_id: str):
    """
    获取下载直链

    参考: OpenList quark_uc/util.go:113-137
    """
    try:
        service = QuarkService(cookie="")
        link = await service.get_download_link(file_id)
        await service.close()
        return {"url": link.url, "headers": link.headers}
    except Exception as e:
        logger.error(f"Failed to get download link: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transcoding/{file_id}")
async def get_transcoding_link(file_id: str):
    """
    获取转码直链

    参考: OpenList quark_uc/util.go:139-168
    """
    try:
        service = QuarkService(cookie="")
        link = await service.get_transcoding_link(file_id)
        await service.close()
        return {"url": link.url, "headers": link.headers, "content_length": link.content_length}
    except Exception as e:
        logger.error(f"Failed to get transcoding link: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
