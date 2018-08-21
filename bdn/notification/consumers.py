import asyncio
import json
import logging
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
# from .models import Notification

logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        logger.info("connected", event)
        await self.send({
            "type": "websocket.accept",
        })
        await self.channel_layer.group_add(
            self.scope['user'].username.lower(),
            self.channel_name)

    async def websocket_receive(self, event):
        logger.info("receive", event)

    async def websocket_disconnect(self, event):
        logger.info("disconnect", event)
        await self.channel_layer.group_discard(
            self.scope['user'].username.lower(),
            self.channel_name)

    async def send_notification(self, notification_data):
        logger.error("sending notification", notification_data)
        await self.send({
            "type": "websocket.send",
            "text": json.dumps(notification_data),
        })
