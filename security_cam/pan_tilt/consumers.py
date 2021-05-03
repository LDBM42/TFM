import json
from random import randint
from asyncio import sleep

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Coordinates

from asgiref.sync import sync_to_async

from django.contrib.sessions.backends.db import SessionStore
obj = Coordinates.objects.get(id=1)
data = SessionStore(session_key=obj.sessionkey)


class WSConsumer(AsyncWebsocketConsumer):
        
    async def connect(self): 
        
        await self.accept()


    async def disconnect(self, close_code):
        # await self.accept()
        pass
    

    
    async def receive(self, text_data):
        with open('coordenadas.txt','r') as f:
            await self.send(f.read())
