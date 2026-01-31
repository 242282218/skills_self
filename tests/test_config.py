"""
配置测试

参考: 开发方案 6.1.1 单元测试
"""

import pytest
from app.config.settings import AppConfig, EndpointConfig, DirConfig
from pydantic import ValidationError


def test_endpoint_config_validation():
    """测试端点配置验证"""
    config = EndpointConfig(
        base_url="http://localhost:5244",
        token="test_token",
        dirs=[]
    )
    assert config.base_url == "http://localhost:5244"
    assert config.token == "test_token"
    assert config.max_connections == 5


def test_endpoint_config_base_url_trailing_slash():
    """测试base_url去除尾部斜杠"""
    config = EndpointConfig(
        base_url="http://localhost:5244/",
        dirs=[]
    )
    assert config.base_url == "http://localhost:5244"


def test_endpoint_config_empty_base_url():
    """测试空base_url验证"""
    with pytest.raises(ValidationError):
        EndpointConfig(base_url="", dirs=[])


def test_dir_config_validation():
    """测试目录配置验证"""
    config = DirConfig(
        local_directory="/tmp/strm",
        remote_directories=["/video"]
    )
    assert config.local_directory == "/tmp/strm"
    assert len(config.remote_directories) == 1
    assert config.remote_directories[0] == "/video"


def test_dir_config_empty_local_directory():
    """测试空local_directory验证"""
    with pytest.raises(ValidationError):
        DirConfig(
            local_directory="",
            remote_directories=["/video"]
        )


def test_app_config_validation():
    """测试应用配置验证"""
    config = AppConfig(
        database="test.db",
        log_level="INFO",
        timeout=30
    )
    assert config.database == "test.db"
    assert config.log_level == "INFO"
    assert config.timeout == 30
    assert len(config.exts) == 4


def test_app_config_log_level_validation():
    """测试日志级别验证"""
    config = AppConfig(
        database="test.db",
        log_level="DEBUG"
    )
    assert config.log_level == "DEBUG"


def test_app_config_invalid_log_level():
    """测试无效日志级别验证"""
    with pytest.raises(ValidationError):
        AppConfig(
            database="test.db",
            log_level="INVALID"
        )


def test_app_config_log_level_case_insensitive():
    """测试日志级别大小写不敏感"""
    config = AppConfig(
        database="test.db",
        log_level="debug"
    )
    assert config.log_level == "DEBUG"
