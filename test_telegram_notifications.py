#!/usr/bin/env python3
"""
模拟 Telegram 推送测试脚本
测试各种场景的推送通知
"""

import sys
import os

# 添加 skill/.updater 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'skill', '.updater'))

from notifier import Notifier, NotificationMessage
from datetime import datetime

# Telegram 配置
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_USER_ID = ""


def test_update_success():
    """测试场景1: 更新成功"""
    print("=" * 50)
    print("📤 场景1: 更新成功")
    print("=" * 50)
    
    notifier = Notifier({
        'telegram': {
            'bot_token': TELEGRAM_BOT_TOKEN,
            'user_id': TELEGRAM_USER_ID
        }
    })
    
    message = NotificationMessage(
        title="🎉 Skill 自动更新成功",
        content="检测到以下 Skill 已更新并自动提交：",
        level="success",
        metadata={
            '更新时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '更新 Skill': 'testing/pytest-design',
            '版本变化': '1.0.0 → 1.1.0',
            '变更内容': '添加 pytest-asyncio 支持、更新最佳实践',
            '提交哈希': 'a1b2c3d',
            '触发方式': '定时任务 (Cron)'
        }
    )
    
    success = notifier.notify(message)
    print(f"✅ 推送结果: {'成功' if success else '失败'}")
    return success


def test_no_changes():
    """测试场景2: 无更新"""
    print("\n" + "=" * 50)
    print("📤 场景2: 无更新")
    print("=" * 50)
    
    notifier = Notifier({
        'telegram': {
            'bot_token': TELEGRAM_BOT_TOKEN,
            'user_id': TELEGRAM_USER_ID
        }
    })
    
    message = NotificationMessage(
        title="ℹ️ Skill 更新检查",
        content="所有 Skill 都是最新的，无需更新！",
        level="info",
        metadata={
            '检查时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '追踪项目': '8 个',
            'Skill 总数': '30 个',
            '状态': '✅ 全部最新'
        }
    )
    
    success = notifier.notify(message)
    print(f"✅ 推送结果: {'成功' if success else '失败'}")
    return success


def test_update_failure():
    """测试场景3: 更新失败"""
    print("\n" + "=" * 50)
    print("📤 场景3: 更新失败")
    print("=" * 50)
    
    notifier = Notifier({
        'telegram': {
            'bot_token': TELEGRAM_BOT_TOKEN,
            'user_id': TELEGRAM_USER_ID
        }
    })
    
    message = NotificationMessage(
        title="❌ Skill 自动更新失败",
        content="更新过程中发生错误，请检查工作流日志",
        level="error",
        metadata={
            '失败时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '错误类型': 'GitHub API 请求超时',
            '失败 Skill': 'devops/container-build',
            '重试次数': '3/3',
            '建议操作': '检查网络连接或手动重试'
        }
    )
    
    success = notifier.notify(message)
    print(f"✅ 推送结果: {'成功' if success else '失败'}")
    return success


def test_dry_run():
    """测试场景4: 试运行模式"""
    print("\n" + "=" * 50)
    print("📤 场景4: 试运行模式")
    print("=" * 50)
    
    notifier = Notifier({
        'telegram': {
            'bot_token': TELEGRAM_BOT_TOKEN,
            'user_id': TELEGRAM_USER_ID
        }
    })
    
    message = NotificationMessage(
        title="🧪 Skill 更新 - 试运行模式",
        content="检测到可更新的 Skill，但未应用变更（试运行模式）",
        level="warning",
        metadata={
            '检查时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '可更新 Skill': '3 个',
            'pytest-design': '1.0.0 → 1.1.0',
            'api-design': '1.0.0 → 1.0.1',
            'react-component': '1.0.0 → 1.1.0',
            '操作': '如需应用变更，请关闭试运行模式后重新运行'
        }
    )
    
    success = notifier.notify(message)
    print(f"✅ 推送结果: {'成功' if success else '失败'}")
    return success


def test_manual_trigger():
    """测试场景5: 手动触发"""
    print("\n" + "=" * 50)
    print("📤 场景5: 手动触发更新")
    print("=" * 50)
    
    notifier = Notifier({
        'telegram': {
            'bot_token': TELEGRAM_BOT_TOKEN,
            'user_id': TELEGRAM_USER_ID
        }
    })
    
    message = NotificationMessage(
        title="👤 Skill 手动更新完成",
        content="用户手动触发的工作流已成功完成",
        level="success",
        metadata={
            '触发时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '触发用户': 'admin',
            '工作流': 'skill-updater.yml',
            'Run ID': '#12345',
            '更新结果': '成功更新 2 个 Skill',
            '查看详情': 'https://github.com/user/repo/actions/runs/12345'
        }
    )
    
    success = notifier.notify(message)
    print(f"✅ 推送结果: {'成功' if success else '失败'}")
    return success


def test_review_required():
    """测试场景6: 需要人工审核"""
    print("\n" + "=" * 50)
    print("📤 场景6: 需要人工审核")
    print("=" * 50)
    
    notifier = Notifier({
        'telegram': {
            'bot_token': TELEGRAM_BOT_TOKEN,
            'user_id': TELEGRAM_USER_ID
        }
    })
    
    message = NotificationMessage(
        title="⚠️ Skill 更新需要审核",
        content="检测到重大版本变更，需要人工审核后合并",
        level="warning",
        metadata={
            '检测时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '涉及 Skill': 'architecture/api-design',
            '版本变化': '1.0.0 → 2.0.0',
            '变更类型': '⚠️ 破坏性变更 (Breaking Change)',
            '原因': 'FastAPI 发布 1.0 版本，API 有重大变更',
            '操作': '请前往 GitHub 查看 PR 并审核'
        }
    )
    
    success = notifier.notify(message)
    print(f"✅ 推送结果: {'成功' if success else '失败'}")
    return success


def test_weekly_summary():
    """测试场景7: 每周汇总"""
    print("\n" + "=" * 50)
    print("📤 场景7: 每周更新汇总")
    print("=" * 50)
    
    notifier = Notifier({
        'telegram': {
            'bot_token': TELEGRAM_BOT_TOKEN,
            'user_id': TELEGRAM_USER_ID
        }
    })
    
    message = NotificationMessage(
        title="📊 Skill 每周更新汇总",
        content="本周 Skill 自动更新统计报告",
        level="info",
        metadata={
            '统计周期': '2024-01-15 至 2024-01-21',
            '总检查次数': '7 次',
            '成功更新': '5 次',
            '失败': '0 次',
            '无变更': '2 次',
            '更新 Skill 数': '12 个',
            '新增功能': '8 个',
            'Bug 修复': '4 个'
        }
    )
    
    success = notifier.notify(message)
    print(f"✅ 推送结果: {'成功' if success else '失败'}")
    return success


def main():
    """主函数 - 运行所有测试"""
    print("\n" + "🚀" * 25)
    print("  Telegram 推送模拟测试")
    print("🚀" * 25 + "\n")
    
    print(f"Bot Token: {TELEGRAM_BOT_TOKEN[:20]}...")
    print(f"User ID: {TELEGRAM_USER_ID}\n")
    
    results = []
    
    # 运行所有测试场景
    results.append(("更新成功", test_update_success()))
    results.append(("无更新", test_no_changes()))
    results.append(("更新失败", test_update_failure()))
    results.append(("试运行模式", test_dry_run()))
    results.append(("手动触发", test_manual_trigger()))
    results.append(("需要审核", test_review_required()))
    results.append(("每周汇总", test_weekly_summary()))
    
    # 打印汇总
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    
    for name, success in results:
        status = "✅ 成功" if success else "❌ 失败"
        print(f"  {name}: {status}")
    
    success_count = sum(1 for _, s in results if s)
    print(f"\n总计: {success_count}/{len(results)} 个测试通过")
    
    return success_count == len(results)


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
