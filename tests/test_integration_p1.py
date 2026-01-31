"""
集成测试

参考: 开发方案 6.1.2 集成测试
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app, init_app


@pytest.fixture(autouse=True)
def setup_config():
    """初始化配置（TestClient不会触发lifespan）"""
    init_app()


def test_api_health():
    """测试API健康检查"""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_api_root():
    """测试API根路径"""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "夸克STRM系统"
    assert data["version"] == "0.1.0"
    assert data["status"] == "running"


def test_config_endpoint():
    """测试配置端点"""
    client = TestClient(app)
    response = client.get("/config")
    assert response.status_code == 200
    data = response.json()
    assert "database" in data
    assert "log_level" in data
    assert "endpoints_count" in data


def test_quark_api_files():
    """测试夸克API文件列表端点"""
    client = TestClient(app)
    response = client.get("/api/quark/files/test")
    assert response.status_code == 200
    data = response.json()
    assert "files" in data
    assert "count" in data


def test_quark_api_link_not_implemented():
    """测试夸克API直链端点（未实现）"""
    client = TestClient(app)
    response = client.get("/api/quark/link/test")
    assert response.status_code == 500


def test_strm_api_scan():
    """测试STRM API扫描端点"""
    client = TestClient(app)
    response = client.post("/api/strm/scan?remote_path=/video&local_path=/tmp")
    assert response.status_code == 200
    data = response.json()
    assert "strms" in data
    assert "count" in data


def test_proxy_api_stream():
    """测试代理API流端点（未实现）"""
    client = TestClient(app)
    response = client.get("/api/proxy/stream/test")
    assert response.status_code == 500
