"""
STRM数据模型

参考: AlistAutoStrm strm.go:14-19
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import hashlib
import os


class StrmModel(BaseModel):
    """
    STRM数据模型

    参考: AlistAutoStrm strm.go:14-19
    """
    name: str = Field(..., description="STRM文件名")
    local_dir: str = Field(..., description="本地目录路径")
    remote_dir: str = Field(..., description="远程目录路径")
    raw_url: str = Field(..., description="原始URL")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    @property
    def key(self) -> str:
        """
        生成唯一键

        参考: AlistAutoStrm strm.go:22-25

        Returns:
            SHA1哈希字符串
        """
        return hashlib.sha1(self.raw_url.encode()).hexdigest()

    @property
    def full_path(self) -> str:
        """
        获取完整文件路径

        Returns:
            完整的文件路径
        """
        return os.path.join(self.local_dir, self.name)

    def gen_strm_file(self, overwrite: bool = False) -> bool:
        """
        生成STRM文件

        参考: AlistAutoStrm strm.go:60-70

        Args:
            overwrite: 是否覆盖已存在的文件

        Returns:
            是否成功
        """
        try:
            os.makedirs(self.local_dir, exist_ok=True)

            if not overwrite and os.path.exists(self.full_path):
                return False

            with open(self.full_path, 'w', encoding='utf-8') as f:
                f.write(self.raw_url)

            return True
        except Exception as e:
            raise RuntimeError(f"Failed to generate STRM file {self.full_path}: {str(e)}")

    def delete_strm_file(self) -> bool:
        """
        删除STRM文件

        Returns:
            是否成功
        """
        try:
            if os.path.exists(self.full_path):
                os.remove(self.full_path)
                return True
            return False
        except Exception as e:
            raise RuntimeError(f"Failed to delete STRM file {self.full_path}: {str(e)}")


class LinkModel(BaseModel):
    """
    直链数据模型

    参考: OpenList quark_uc/util.go:113-137
    """
    url: str = Field(..., description="直链URL")
    headers: dict = Field(default_factory=dict, description="请求头")
    content_length: Optional[int] = Field(None, description="内容长度")
    concurrency: int = Field(3, description="并发数")
    part_size: int = Field(10 * 1024 * 1024, description="分片大小")
