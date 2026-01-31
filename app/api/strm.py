"""
STRM API路由
"""

from fastapi import APIRouter, HTTPException
from app.services.strm_service import StrmService
from app.core.database import Database
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/strm", tags=["STRM服务"])


@router.post("/scan")
async def scan_directory(
    remote_path: str,
    local_path: str,
    recursive: bool = True,
    concurrent_limit: int = 5
):
    """
    扫描目录并生成STRM

    参考: AlistAutoStrm mission.go:31-158
    """
    try:
        database = Database("quark_strm.db")
        service = StrmService(
            cookie="",
            database=database,
            recursive=recursive
        )
        strms = await service.scan_directory(remote_path, local_path, concurrent_limit)
        await service.close()
        return {"strms": strms, "count": len(strms)}
    except Exception as e:
        logger.error(f"Failed to scan directory: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
