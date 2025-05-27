from channels.generic.websocket import AsyncWebsocketConsumer
import json

class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("bus_tracking", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("bus_tracking", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Ожидается JSON вида: { "bus_number": "56", "lat": 42.87, "lng": 74.6 }

        await self.channel_layer.group_send(
            "bus_tracking",
            {
                "type": "broadcast_location",
                "message": data
            }
        )

    async def broadcast_location(self, event):
        await self.send(text_data=json.dumps(event["message"]))
