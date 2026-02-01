#!/usr/bin/env python3
"""
通知模块 - 支持多种通知渠道

支持：
- Telegram
- Webhook
- Email（预留）
"""

import os
import json
import logging
import requests
from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger('skill-updater.notifier')


class NotificationChannel(Enum):
    """通知渠道"""
    TELEGRAM = "telegram"
    WEBHOOK = "webhook"
    EMAIL = "email"


@dataclass
class NotificationMessage:
    """通知消息"""
    title: str
    content: str
    level: str  # info, success, warning, error
    metadata: Optional[Dict] = None


class TelegramNotifier:
    """Telegram 通知器"""
    
    def __init__(self, bot_token: str, user_id: str):
        self.bot_token = bot_token
        self.user_id = user_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send(self, message: NotificationMessage) -> bool:
        """发送 Telegram 消息"""
        if not self.bot_token or not self.user_id:
            logger.warning("Telegram 配置不完整，跳过通知")
            return False
        
        # 根据级别设置表情符号
        emoji_map = {
            'info': 'ℹ️',
            'success': '🎉',
            'warning': '⚠️',
            'error': '❌'
        }
        emoji = emoji_map.get(message.level, 'ℹ️')
        
        # 构建消息文本
        text = f"{emoji} *{message.title}*\n\n{message.content}"
        
        # 添加元数据
        if message.metadata:
            text += "\n\n📊 *详细信息：*"
            for key, value in message.metadata.items():
                text += f"\n• {key}: {value}"
        
        try:
            response = requests.post(
                f"{self.api_url}/sendMessage",
                data={
                    'chat_id': self.user_id,
                    'text': text,
                    'parse_mode': 'Markdown',
                    'disable_web_page_preview': True
                },
                timeout=30
            )
            response.raise_for_status()
            logger.info("Telegram 通知发送成功")
            return True
            
        except requests.RequestException as e:
            logger.error(f"Telegram 通知发送失败: {e}")
            return False


class WebhookNotifier:
    """Webhook 通知器"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send(self, message: NotificationMessage) -> bool:
        """发送 Webhook 请求"""
        if not self.webhook_url:
            logger.warning("Webhook URL 未配置，跳过通知")
            return False
        
        payload = {
            'title': message.title,
            'content': message.content,
            'level': message.level,
            'timestamp': str(datetime.now()),
            'metadata': message.metadata or {}
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            response.raise_for_status()
            logger.info("Webhook 通知发送成功")
            return True
            
        except requests.RequestException as e:
            logger.error(f"Webhook 通知发送失败: {e}")
            return False


class Notifier:
    """统一通知管理器"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.notifiers = []
        
        # 初始化 Telegram
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN') or self.config.get('telegram', {}).get('bot_token')
        telegram_user_id = os.getenv('TELEGRAM_USER_ID') or self.config.get('telegram', {}).get('user_id')
        
        if telegram_token and telegram_user_id:
            self.notifiers.append(TelegramNotifier(telegram_token, telegram_user_id))
        
        # 初始化 Webhook
        webhook_url = self.config.get('webhook', {}).get('url')
        if webhook_url:
            self.notifiers.append(WebhookNotifier(webhook_url))
    
    def notify(self, message: NotificationMessage) -> bool:
        """发送通知到所有渠道"""
        results = []
        
        for notifier in self.notifiers:
            try:
                result = notifier.send(message)
                results.append(result)
            except Exception as e:
                logger.error(f"通知发送异常: {e}")
                results.append(False)
        
        return any(results) if results else False
    
    def notify_update_success(self, skill_name: str, old_version: str, new_version: str, changes: list):
        """通知更新成功"""
        message = NotificationMessage(
            title="Skill 自动更新成功",
            content=f"Skill *{skill_name}* 已更新\n\n版本: `{old_version}` → `{new_version}`",
            level="success",
            metadata={
                '变更数': len(changes),
                '变更详情': ', '.join(changes[:3]) + ('...' if len(changes) > 3 else '')
            }
        )
        return self.notify(message)
    
    def notify_update_failure(self, skill_name: str, error: str):
        """通知更新失败"""
        message = NotificationMessage(
            title="Skill 更新失败",
            content=f"Skill *{skill_name}* 更新失败\n\n错误: {error}",
            level="error"
        )
        return self.notify(message)
    
    def notify_no_changes(self):
        """通知无变更"""
        message = NotificationMessage(
            title="Skill 更新检查",
            content="所有 Skill 都是最新的，无需更新",
            level="info"
        )
        return self.notify(message)
    
    def notify_check_started(self):
        """通知检查开始"""
        message = NotificationMessage(
            title="Skill 更新检查",
            content="开始检查 Skill 更新...",
            level="info"
        )
        return self.notify(message)


# 便捷函数
def get_notifier() -> Notifier:
    """获取通知器实例"""
    return Notifier()


if __name__ == '__main__':
    # 测试通知功能
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python notifier.py <test|notify>")
        sys.exit(1)
    
    command = sys.argv[1]
    notifier = get_notifier()
    
    if command == 'test':
        # 发送测试消息
        message = NotificationMessage(
            title="测试通知",
            content="这是一条测试消息\n\n如果您收到这条消息，说明通知配置正确！",
            level="info",
            metadata={
                '测试时间': str(datetime.now()),
                '通知渠道': 'Telegram'
            }
        )
        success = notifier.notify(message)
        print(f"通知发送{'成功' if success else '失败'}")
    
    elif command == 'notify':
        # 发送更新成功通知
        notifier.notify_update_success(
            skill_name="pytest-design",
            old_version="1.0.0",
            new_version="1.1.0",
            changes=["添加异步测试支持", "更新 pytest 版本引用"]
        )
