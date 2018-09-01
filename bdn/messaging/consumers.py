import json
import logging
from channels.consumer import AsyncConsumer


logger = logging.getLogger(__name__)


class ThreadConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        logger.info("connected messaging", event)
        await self.send({
            "type": "websocket.accept",
        })
        group_name = 'messages_{}'.format(self.scope['user'].username.lower())
        await self.channel_layer.group_add(
            group_name,
            self.channel_name)

    async def websocket_receive(self, event):
        logger.info("receive message", event)

    async def websocket_disconnect(self, event):
        logger.info("disconnect", event)
        group_name = 'messages_{}'.format(self.scope['user'].username.lower())
        await self.channel_layer.group_discard(
            group_name,
            self.channel_name)

    async def chat_message(self, message_data):
        logger.error("sending message", message_data)
        await self.send({
            "type": "websocket.send",
            "text": json.dumps(message_data['payload']),
        })
