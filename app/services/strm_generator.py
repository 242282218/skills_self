"""
STRM生成器

参考: AlistAutoStrm mission.go:31-158
"""

import asyncio
import os
from typing import List, Optional
from app.models.strm import StrmModel
from app.models.quark import FileModel
from app.services.quark_service import QuarkService
from app.core.database import Database
from app.core.logging import get_logger

logger = get_logger(__name__)


class StrmGenerator:
    """
    STRM生成器

    参考: AlistAutoStrm Mission结构
    """

    def __init__(
        self,
        quark_service: QuarkService,
        database: Database,
        base_url: str,
        exts: List[str],
        alt_exts: List[str],
        create_sub_directory: bool = False,
        recursive: bool = True,
        force_refresh: bool = False
    ):
        """
        初始化STRM生成器

        Args:
            quark_service: 夸克服务
            database: 数据库实例
            base_url: 基础URL
            exts: 视频扩展名列表
            alt_exts: 字幕扩展名列表
            create_sub_directory: 是否创建子目录
            recursive: 是否递归扫描
            force_refresh: 是否强制刷新
        """
        self.quark_service = quark_service
        self.database = database
        self.base_url = base_url
        self.exts = exts
        self.alt_exts = alt_exts
        self.create_sub_directory = create_sub_directory
        self.recursive = recursive
        self.force_refresh = force_refresh
        self.semaphore = None
        self.strms: List[StrmModel] = []

    async def scan_directory(
        self,
        remote_path: str,
        local_path: str,
        concurrent_limit: int = 5
    ) -> List[StrmModel]:
        """
        扫描目录并生成STRM

        参考: AlistAutoStrm mission.go:31-158

        Args:
            remote_path: 远程目录路径
            local_path: 本地目录路径
            concurrent_limit: 并发限制

        Returns:
            STRM模型列表
        """
        self.strms = []
        self.semaphore = asyncio.Semaphore(concurrent_limit)

        logger.info(f"Starting scan: {remote_path} -> {local_path}")

        await self._scan_recursive(remote_path, local_path, use_semaphore=True)

        logger.info(f"Scan completed: {len(self.strms)} STRMs generated")
        return self.strms

    async def _scan_recursive(
        self,
        remote_path: str,
        local_path: str,
        use_semaphore: bool = False
    ):
        """
        递归扫描目录

        参考: AlistAutoStrm mission.go:31-158

        Args:
            remote_path: 远程目录路径
            local_path: 本地目录路径
            use_semaphore: 是否使用信号量
        """
        if use_semaphore:
            async with self.semaphore:
                await self._process_directory(remote_path, local_path)
        else:
            await self._process_directory(remote_path, local_path)

    async def _process_directory(
        self,
        remote_path: str,
        local_path: str
    ):
        """
        处理目录

        Args:
            remote_path: 远程目录路径
            local_path: 本地目录路径
        """
        try:
            files = await self.quark_service.get_files(remote_path)
            logger.debug(f"Got {len(files)} files from {remote_path}")

            for file in files:
                if file.is_dir and self.recursive:
                    logger.debug(f"Found directory: {remote_path}/{file.name}")

                    # 增量更新检查
                    full_remote_path = f"{remote_path}/{file.name}"
                    if not self.force_refresh:
                        records = self.database.get_records()
                        if full_remote_path in records:
                            logger.debug(f"Directory {full_remote_path} already processed, skip")
                            continue

                    # 计算本地路径
                    if self.create_sub_directory:
                        new_local_path = os.path.join(local_path, file.name)
                    else:
                        new_local_path = local_path

                    # 递归扫描子目录
                    await self._scan_recursive(full_remote_path, new_local_path, use_semaphore=False)

                elif not file.is_dir:
                    # 处理文件
                    ext = os.path.splitext(file.name)[1].lower()

                    if ext in self.exts:
                        # 生成STRM
                        await self._generate_strm(file, remote_path, local_path)
                    elif ext in self.alt_exts:
                        # 下载字幕文件
                        await self._download_subtitle(file, remote_path, local_path)

        except Exception as e:
            logger.error(f"Failed to scan {remote_path}: {str(e)}")

    async def _generate_strm(
        self,
        file: FileModel,
        remote_path: str,
        local_path: str
    ):
        """
        生成STRM

        参考: AlistAutoStrm mission.go:72-88

        Args:
            file: 文件对象
            remote_path: 远程目录路径
            local_path: 本地目录路径
        """
        try:
            # 获取下载直链
            link = await self.quark_service.get_download_link(file.id)

            # 生成STRM文件名
            name = os.path.splitext(file.name)[0] + ".strm"

            # 创建STRM模型
            strm = StrmModel(
                name=name,
                local_dir=local_path,
                remote_dir=remote_path,
                raw_url=link.url
            )

            # 保存到数据库
            self.database.save_strm(
                strm.key,
                strm.name,
                strm.local_dir,
                strm.remote_dir,
                strm.raw_url
            )

            # 生成STRM文件
            strm.gen_strm_file(overwrite=True)

            self.strms.append(strm)
            logger.debug(f"Generated STRM: {strm.full_path}")

        except Exception as e:
            logger.error(f"Failed to generate STRM for {file.name}: {str(e)}")

    async def _download_subtitle(
        self,
        file: FileModel,
        remote_path: str,
        local_path: str
    ):
        """
        下载字幕文件

        参考: AlistAutoStrm mission.go:89-154

        Args:
            file: 文件对象
            remote_path: 远程目录路径
            local_path: 本地目录路径
        """
        try:
            file_path = os.path.join(local_path, file.name)

            # 检查文件是否已存在
            if os.path.exists(file_path):
                logger.debug(f"Subtitle file {file_path} already exists, skip")
                return

            # 获取下载直链
            link = await self.quark_service.get_download_link(file.id)

            # 下载文件
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    link.url,
                    headers=link.headers
                ) as response:
                    if response.status == 200:
                        os.makedirs(local_path, exist_ok=True)
                        with open(file_path, 'wb') as f:
                            async for chunk in response.content.iter_chunked(8192):
                                f.write(chunk)

                        logger.debug(f"Downloaded subtitle: {file_path}")
                    else:
                        logger.error(f"Failed to download subtitle {file.name}: status {response.status}")

        except Exception as e:
            logger.error(f"Failed to download subtitle {file.name}: {str(e)}")
