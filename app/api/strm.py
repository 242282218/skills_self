"""
STRM API路由
"""

from fastapi import APIRouter, HTTPException
from app.services.strm_service import StrmGenerator
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/strm", tags=["STRM服务"])


@router.post("/scan")
async def scan_directory(remote_path: str, local_path: str, recursive: bool = True):
    """
    扫描目录并生成STRM

    参考: AlistAutoStrm mission.go:31-158
    """
    try:
        generator = StrmGenerator()
        strms = await generator.scan_directory(remote_path, local_path, recursive)
        return {"strms": strms, "count": len(strms)}
    except Exception as e:
        logger.error(f"Failed to scan directory: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
