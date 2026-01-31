"""
夸克服务模块

参考: OpenList driver.go
"""

from app.models.quark import FileModel
from app.models.strm import LinkModel
from app.core.logging import get_logger

logger = get_logger(__name__)


class QuarkService:
    """夸克服务（占位，P2阶段实现）"""

    async def get_files(self, parent: str, only_video: bool = False) -> list[FileModel]:
        """
        获取文件列表

        参考: OpenList quark_uc/util.go:69-111

        Args:
            parent: 父目录ID
            only_video: 是否只获取视频文件

        Returns:
            文件列表
        """
        logger.warning("QuarkService.get_files not implemented yet")
        return []

    async def get_download_link(self, file_id: str) -> LinkModel:
        """
        获取下载直链

        参考: OpenList quark_uc/util.go:113-137

        Args:
            file_id: 文件ID

        Returns:
            直链模型
        """
        logger.warning("QuarkService.get_download_link not implemented yet")
        raise NotImplementedError("QuarkService.get_download_link not implemented yet")

    async def get_transcoding_link(self, file_id: str) -> LinkModel:
        """
        获取转码直链

        参考: OpenList quark_uc/util.go:139-168

        Args:
            file_id: 文件ID

        Returns:
            直链模型
        """
        logger.warning("QuarkService.get_transcoding_link not implemented yet")
        raise NotImplementedError("QuarkService.get_transcoding_link not implemented yet")

    async def close(self):
        """关闭客户端"""
        logger.debug("QuarkService closed")
