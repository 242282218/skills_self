"""
代理服务模块

参考: MediaHelp proxy.py
"""

from app.core.logging import get_logger

logger = get_logger(__name__)


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
