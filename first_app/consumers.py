import json
from channels.generiic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

# WebSocketから受け取ったものを処理するクラス


class WSConsumer(WebsocketConsumer):

    # WebSocket接続時の処理
    def connect(self):

        self.room_id = self.scope['url_route']['kwargs']['room_id']

        self.strGroupName = self.room_id
        async_to_sync(self.channel_layer.group_add)(
            self.strGroupName, self.channel_name)

        self.accept()
        print('接続OK')

    # WebSocket切断時の処理
    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.strGroupName, self.channel_name)

    # WebSocketからのデータ受信時の処理
    def receive(self, text_data):

        data = json.loads(text_data)
        print(data)

        data = {
            'type': 'chatmessage',
            'message': data['flg'],
        }
        async_to_sync(self.channel_layer.group_send)(self.strGroupName, data)

    # 拡散メッセージ受信時の処理
    def chat_message(self, data):
        data_json = {
            'message': data['message'],
        }
