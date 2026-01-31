"""
STRM服务模块

参考: AlistAutoStrm mission.go
"""

from app.models.strm import StrmModel
from app.core.logging import get_logger

logger = get_logger(__name__)


class StrmGenerator:
    """STRM生成器（占位，P3阶段实现）"""

    async def scan_directory(self, remote_path: str, local_path: str, recursive: bool = True) -> list[StrmModel]:
        """
        扫描目录并生成STRM

        参考: AlistAutoStrm mission.go:31-158

        Args:
            remote_path: 远程目录路径
            local_path: 本地目录路径
            recursive: 是否递归扫描

        Returns:
            STRM模型列表
        """
        logger.warning("StrmGenerator.scan_directory not implemented yet")
        return []


class ProxyService:
    """代理服务（占位，P4阶段实现）"""

    async def proxy_stream(self, file_id: str, range_header: str = None):
        """
        代理视频流

        参考: MediaHelp proxy.py

        Args:
            file_id: 文件ID
            range_header: Range请求头

        Returns:
            响应对象
        """
        logger.warning("ProxyService.proxy_stream not implemented yet")
        raise NotImplementedError("ProxyService.proxy_stream not implemented yet")
