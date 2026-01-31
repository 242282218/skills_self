"""
数据库测试

参考: 开发方案 6.1.1 单元测试
"""

import pytest
import os
import tempfile
from app.core.database import Database
from app.models.strm import StrmModel


def test_database_init():
    """测试数据库初始化"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = Database(db_path)
        assert db is not None
        assert os.path.exists(db_path)


def test_save_and_get_strm():
    """测试保存和获取STRM"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = Database(db_path)

        strm = StrmModel(
            name="test.strm",
            local_dir="/tmp",
            remote_dir="/video",
            raw_url="http://example.com/video.mp4"
        )

        db.save_strm(strm.key, strm.name, strm.local_dir, strm.remote_dir, strm.raw_url)
        retrieved = db.get_strm(strm.key)

        assert retrieved is not None
        assert retrieved["name"] == "test.strm"
        assert retrieved["local_dir"] == "/tmp"
        assert retrieved["remote_dir"] == "/video"
        assert retrieved["raw_url"] == "http://example.com/video.mp4"


def test_delete_strm():
    """测试删除STRM"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = Database(db_path)

        strm = StrmModel(
            name="test.strm",
            local_dir="/tmp",
            remote_dir="/video",
            raw_url="http://example.com/video.mp4"
        )

        db.save_strm(strm.key, strm.name, strm.local_dir, strm.remote_dir, strm.raw_url)
        assert db.get_strm(strm.key) is not None

        db.delete_strm(strm.key)
        assert db.get_strm(strm.key) is None


def test_save_and_get_record():
    """测试保存和获取记录"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = Database(db_path)

        db.save_record("/video")
        records = db.get_records()

        assert "/video" in records
        assert records["/video"] is not None


def test_delete_record():
    """测试删除记录"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = Database(db_path)

        db.save_record("/video")
        assert "/video" in db.get_records()

        db.delete_record("/video")
        assert "/video" not in db.get_records()


def test_get_strms_by_remote_dir():
    """测试根据远程目录获取STRM列表"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = Database(db_path)

        strm1 = StrmModel(
            name="test1.strm",
            local_dir="/tmp",
            remote_dir="/video",
            raw_url="http://example.com/video1.mp4"
        )

        strm2 = StrmModel(
            name="test2.strm",
            local_dir="/tmp",
            remote_dir="/video",
            raw_url="http://example.com/video2.mp4"
        )

        strm3 = StrmModel(
            name="test3.strm",
            local_dir="/tmp",
            remote_dir="/music",
            raw_url="http://example.com/music.mp3"
        )

        db.save_strm(strm1.key, strm1.name, strm1.local_dir, strm1.remote_dir, strm1.raw_url)
        db.save_strm(strm2.key, strm2.name, strm2.local_dir, strm2.remote_dir, strm2.raw_url)
        db.save_strm(strm3.key, strm3.name, strm3.local_dir, strm3.remote_dir, strm3.raw_url)

        video_strms = db.get_strms_by_remote_dir("/video")
        assert len(video_strms) == 2

        music_strms = db.get_strms_by_remote_dir("/music")
        assert len(music_strms) == 1


def test_delete_strms_by_remote_dir():
    """测试删除指定远程目录下的所有STRM"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = Database(db_path)

        strm1 = StrmModel(
            name="test1.strm",
            local_dir="/tmp",
            remote_dir="/video",
            raw_url="http://example.com/video1.mp4"
        )

        strm2 = StrmModel(
            name="test2.strm",
            local_dir="/tmp",
            remote_dir="/video",
            raw_url="http://example.com/video2.mp4"
        )

        db.save_strm(strm1.key, strm1.name, strm1.local_dir, strm1.remote_dir, strm1.raw_url)
        db.save_strm(strm2.key, strm2.name, strm2.local_dir, strm2.remote_dir, strm2.raw_url)

        deleted_count = db.delete_strms_by_remote_dir("/video")
        assert deleted_count == 2

        assert db.get_strm(strm1.key) is None
        assert db.get_strm(strm2.key) is None


def test_get_all_strms():
    """测试获取所有STRM"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = Database(db_path)

        for i in range(5):
            strm = StrmModel(
                name=f"test{i}.strm",
                local_dir="/tmp",
                remote_dir="/video",
                raw_url=f"http://example.com/video{i}.mp4"
            )
            db.save_strm(strm.key, strm.name, strm.local_dir, strm.remote_dir, strm.raw_url)

        all_strms = db.get_all_strms()
        assert len(all_strms) == 5
