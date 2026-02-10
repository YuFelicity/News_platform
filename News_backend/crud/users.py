import uuid
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from schemas.users import RequestUser
from utils import security



async def get_user_by_username(db: AsyncSession, username: str):
    t = select(User).where(User.username == username)
    result = await db.execute(t)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: RequestUser):

    hashed_password = security.get_password_hash(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_token(db: AsyncSession, user_id: int):

    token = str(uuid.uuid4())

    expires_at = datetime.now() + timedelta(days=7)
    t = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(t)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
        await db.commit()
        await db.refresh(user_token)
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()
        await db.refresh(user_token)

    return token