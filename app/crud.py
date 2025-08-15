from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(username=user.username)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).where(models.User.username == username))
    return result.scalars().first()

async def create_message(db: AsyncSession, message: schemas.MessageCreate):
    db_message = models.Message(
        content = message.content,
        sender_id = message.sender_id
    )
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message

async def get_chat_history(db: AsyncSession, limit: int = 50):
    result = await db.execute(
        select(models.Message).order_by(models.Message.timestamp.desc()).limit(limit)
    )
    return result.scalars().all()

async def update_message_status(db: AsyncSession, message_id: int, delivered: bool = None, read: bool = None):
    result = await db.execute(select(models.Message).where(models.Message.id == message_id))
    msg = result.scalars().first()
    if not msg:
        return None
    if delivered is not None:
        msg.delivered = delivered
    if read is not None:
        msg.read = read

    await db.commit()
    await db.refresh(msg)
    return msg
