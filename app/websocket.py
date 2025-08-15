from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from broadcaster import Broadcast
from sqlalchemy.ext.asyncio import AsyncSession
import json
import asyncio
from contextlib import asynccontextmanager
from . import crud, schemas, db

broadcast = Broadcast("memory://")

@asynccontextmanager
async def lifespan(app: APIRouter):
    # startup
    await broadcast.connect()
    yield
    #shutdown
    await broadcast.disconnect()

router = APIRouter(lifespan=lifespan)

@router.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket, db_session: AsyncSession = Depends(db.get_db)):
    await websocket.accept()

    async with broadcast.subscribe(channel="chat_room") as subscriber:
        try:
            # Listen to broadcast messages in a separate task
            async def broadcast_listener():
                async for event in subscriber:
                    await websocket.send_text(event.message)

            listener_task = asyncio.create_task(broadcast_listener())

            while True:
                # Wait for client messages
                message = await websocket.receive_text()
                try:
                    data = json.loads(message)
                    sender_id = data["sender_id"]
                    content = data["content"]

                    # Save message to DB
                    new_msg = await crud.create_message(
                        db_session,
                        schemas.MessageCreate(content=content, sender_id=sender_id)
                    )

                    # Publish to channel
                    await broadcast.publish(
                        channel="chat_room",
                        message=json.dumps({
                            "id": new_msg.id,
                            "sender_id": sender_id,
                            "content": content,
                            "timestamp": str(new_msg.timestamp)
                        })
                    )
                except Exception as e:
                    await websocket.send_text(f"Error: {str(e)}")

        except WebSocketDisconnect:
            pass
        finally:
            listener_task.cancel()
