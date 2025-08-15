import pytest
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_websocket_message_broadcast():
    with client.websocket_connect("/ws/chat") as ws1, client.websocket_connect("/ws/chat") as ws2:
        ws1.send_text(json.dumps({
            "type": "message",
            "sender_id": 1,
            "content": "Hello world"
        }))
        data1 = ws1.receive_text()
        data2 = ws2.receive_text()
        assert "Hello world" in data1
        assert "Hello world" in data2