import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .redis_client import redis_client

def get_room(room_key):
    return redis_client.get(room_key, default={"players": {}, "ready": []})

def save_room(room_key, room_data):
    redis_client.set(room_key, room_data)

def delete_room(room_key):
    redis_client.delete(room_key)

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "room1"
        self.room_group_name = f"game_{self.room_name}"
        self.room_key = f"room:{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        user = self.scope["user"]
        if isinstance(user, AnonymousUser):
            await self.close()
            return

        username = await self.get_username()

        # 获取房间并添加玩家
        room = get_room(self.room_key)
        room["players"][self.channel_name] = {
            "ready": False,
            "hand": [],
            "username": username,
        }
        save_room(self.room_key, room)

        # 返回当前用户名
        await self.send(text_data=json.dumps({
            "type": "joined",
            "player_id": self.channel_name,
            "username": username
        }))

    async def disconnect(self, close_code):
        room = get_room(self.room_key)
        room["players"].pop(self.channel_name, None)
        if self.channel_name in room["ready"]:
            room["ready"].remove(self.channel_name)

        save_room(self.room_key, room)

    async def receive(self, text_data):
        data = json.loads(text_data)
        room = get_room(self.room_key)

        player = room["players"].get(self.channel_name)
        if not player:
            return

        username = player["username"]

        if data["type"] == "ready":
            if self.channel_name not in room["ready"]:
                room["ready"].append(self.channel_name)
                save_room(self.room_key, room)

            await self.channel_layer.group_send(self.room_group_name, {
                "type": "status_update",
                "ready_count": len(room["ready"]),
            })

            if len(room["ready"]) == 3:
                deck = self.generate_deck()
                hands = [deck[i::3] for i in range(3)]
                players = list(room["players"].keys())

                for i, pid in enumerate(players):
                    room["players"][pid]["hand"] = hands[i]
                    await self.channel_layer.send(pid, {
                        "type": "deal_cards",
                        "hand": hands[i],
                        "username": room["players"][pid]["username"]
                    })

                save_room(self.room_key, room)

        elif data["type"] == "play_card":
            card = data["card"]
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "play_notify",
                "player": username,  # 显示用户名
                "card": card,
            })

    async def deal_cards(self, event):
        await self.send(text_data=json.dumps({
            "type": "deal",
            "hand": event["hand"],
            "username": event["username"]
        }))

    async def status_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "status",
            "ready_count": event["ready_count"],
        }))

    async def play_notify(self, event):
        await self.send(text_data=json.dumps({
            "type": "play",
            "player": event["player"],  # 用户名
            "card": event["card"],
        }))

    @database_sync_to_async
    def get_username(self):
        return self.scope["user"].username

    def generate_deck(self):
        suits = ['♠', '♥', '♣', '♦']
        ranks = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
        deck = [f"{suit}{rank}" for suit in suits for rank in ranks]
        deck += ["🃏小王", "🃏大王"]
        import random
        random.shuffle(deck)
        return deck

