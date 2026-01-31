"""
夸克服务测试

参考: 开发方案 6.2.1 单元测试
"""

import pytest
from app.services.quark_service import QuarkService
from app.services.quark_api_client import QuarkAPIClient
from unittest.mock import AsyncMock, patch, MagicMock
from app.models.quark import FileModel
from app.models.strm import LinkModel


@pytest.mark.asyncio
async def test_quark_api_client_init():
    """测试QuarkAPIClient初始化"""
    client = QuarkAPIClient(cookie="test_cookie")
    assert client.cookie == "test_cookie"
    assert client.referer == "https://pan.quark.cn/"
    assert client.base_url == "https://pan.quark.cn"


@pytest.mark.asyncio
async def test_quark_api_client_update_cookie():
    """测试Cookie更新"""
    client = QuarkAPIClient(cookie="key1=value1; key2=value2")
    updated = client._update_cookie("key1=value1; key2=value2", "key3", "new_value")
    assert "key3=new_value" in updated
    assert "key1=value1" in updated
    assert "key2=value2" in updated


@pytest.mark.asyncio
async def test_quark_service_get_files():
    """测试获取文件列表"""
    with patch('app.services.quark_api_client.QuarkAPIClient.request') as mock_request:
        mock_request.return_value = {
            "data": {
                "list": [
                    {
                        "fid": "123",
                        "file_name": "test.mp4",
                        "file": True,
                        "size": 1024,
                        "category": 1,
                        "is_dir": False
                    }
                ],
                "metadata": {
                    "total": 1
                }
            },
            "status": 0,
            "code": 0
        }

        service = QuarkService(cookie="test_cookie")
        files = await service.get_files("/test")

        assert len(files) == 1
        assert files[0].fid == "123"
        assert files[0].name == "test.mp4"
        await service.close()


@pytest.mark.asyncio
async def test_quark_service_get_files_only_video():
    """测试只获取视频文件"""
    with patch('app.services.quark_api_client.QuarkAPIClient.request') as mock_request:
        mock_request.return_value = {
            "data": {
                "list": [
                    {
                        "fid": "123",
                        "file_name": "test.mp4",
                        "file": True,
                        "size": 1024,
                        "category": 1,
                        "is_dir": False
                    },
                    {
                        "fid": "456",
                        "file_name": "test.txt",
                        "file": True,
                        "size": 100,
                        "category": 4,
                        "is_dir": False
                    }
                ],
                "metadata": {
                    "total": 2
                }
            },
            "status": 0,
            "code": 0
        }

        service = QuarkService(cookie="test_cookie")
        files = await service.get_files("/test", only_video=True)

        assert len(files) == 1
        assert files[0].fid == "123"
        assert files[0].name == "test.mp4"
        await service.close()


@pytest.mark.asyncio
async def test_quark_service_get_download_link():
    """测试获取下载直链"""
    with patch('app.services.quark_api_client.QuarkAPIClient.request') as mock_request:
        mock_request.return_value = {
            "data": [
                {
                    "download_url": "http://example.com/download"
                }
            ],
            "status": 0,
            "code": 0
        }

        service = QuarkService(cookie="test_cookie")
        link = await service.get_download_link("123")

        assert link.url == "http://example.com/download"
        assert "Cookie" in link.headers
        assert link.concurrency == 3
        assert link.part_size == 10 * 1024 * 1024
        await service.close()


@pytest.mark.asyncio
async def test_quark_service_get_transcoding_link():
    """测试获取转码直链"""
    with patch('app.services.quark_api_client.QuarkAPIClient.request') as mock_request:
        mock_request.return_value = {
            "data": {
                "video_list": [
                    {
                        "video_info": {
                            "url": "http://example.com/transcode",
                            "size": 2048
                        }
                    }
                ]
            },
            "status": 0,
            "code": 0
        }

        service = QuarkService(cookie="test_cookie")
        link = await service.get_transcoding_link("123")

        assert link.url == "http://example.com/transcode"
        assert link.content_length == 2048
        await service.close()


@pytest.mark.asyncio
async def test_quark_service_get_transcoding_link_not_found():
    """测试转码直链未找到"""
    with patch('app.services.quark_api_client.QuarkAPIClient.request') as mock_request:
        mock_request.return_value = {
            "data": {
                "video_list": []
            },
            "status": 0,
            "code": 0
        }

        service = QuarkService(cookie="test_cookie")
        with pytest.raises(Exception) as exc_info:
            await service.get_transcoding_link("123")

        assert "No transcoding link found" in str(exc_info.value)
        await service.close()
