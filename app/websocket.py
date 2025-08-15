import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from broadcaster import Broadcast
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from . import crud, schemas, db
from .celery_app import send_notification

broadcast = Broadcast("memory://")  # Use Redis in production

@asynccontextmanager
async def lifespan(app: APIRouter):
    await broadcast.connect()
    yield
    await broadcast.disconnect()

router = APIRouter(lifespan=lifespan)

@router.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket, db_session: AsyncSession = Depends(db.get_db)):
    await websocket.accept()

    async with broadcast.subscribe(channel="chat_room") as subscriber:

        async def listen_to_client():
            try:
                async for message in websocket.iter_text():
                    try:
                        data = json.loads(message)
                        event_type = data.get("type")

                        if event_type == "message":
                            sender_id = data["sender_id"]
                            content = data["content"]

                            # Save message
                            new_msg = await crud.create_message(
                                db_session,
                                schemas.MessageCreate(content=content, sender_id=sender_id)
                            )

                            # Background notification
                            send_notification.delay(999, f"New message: {content}")

                            # Broadcast message
                            await broadcast.publish(
                                channel="chat_room",
                                message=json.dumps({
                                    "type": "message",
                                    "id": new_msg.id,
                                    "sender_id": sender_id,
                                    "content": content,
                                    "timestamp": str(new_msg.timestamp)
                                })
                            )

                        elif event_type == "typing":
                            await broadcast.publish(
                                channel="chat_room",
                                message=json.dumps({
                                    "type": "typing",
                                    "user_id": data["user_id"]
                                })
                            )

                        elif event_type == "status_update":
                            updated_msg = await crud.update_message_status(
                                db_session,
                                message_id=data["message_id"],
                                delivered=data.get("delivered"),
                                read=data.get("read")
                            )
                            if updated_msg:
                                await broadcast.publish(
                                    channel="chat_room",
                                    message=json.dumps({
                                        "type": "status_update",
                                        "message_id": updated_msg.id,
                                        "delivered": updated_msg.delivered,
                                        "read": updated_msg.read
                                    })
                                )
                    except Exception as e:
                        await websocket.send_text(f"Error: {str(e)}")
            except WebSocketDisconnect:
                pass

        async def listen_to_broadcast():
            try:
                async for event in subscriber:
                    await websocket.send_text(event.message)
            except WebSocketDisconnect:
                pass

        # Run both tasks concurrently
        client_task = asyncio.create_task(listen_to_client())
        broadcast_task = asyncio.create_task(listen_to_broadcast())

        await asyncio.wait([client_task, broadcast_task], return_when=asyncio.FIRST_COMPLETED)

        # Cancel both if one exits
        client_task.cancel()
        broadcast_task.cancel()
