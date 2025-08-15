from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db import engine, Base
from . import websocket, chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
        # Shutdown
        # (Add cleanup logic here if needed)

app = FastAPI(title="Live Chat API", lifespan=lifespan)

app.include_router(websocket.router)
app.include_router(chat.router)
