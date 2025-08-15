from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import schemas, crud, db

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/history", response_model=List[schemas.MessageResponse])
async def chat_history(limit: int = 50, db_session: AsyncSession = Depends(db.get_db)):
    messages = await crud.get_chat_history(db_session, limit)
    return messages