import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from schemas.users import RequestUser, UserUpdateRequest
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

async def exist_user(db: AsyncSession, user_name: str, user_psw: str):
    user = await get_user_by_username(db, user_name)
    if not user:
        return None
    if not security.verify_password(user_psw, user.password):
        return None
    return user

async def get_user_by_token(db: AsyncSession, token: str):
    query_token = select(UserToken).where(UserToken.token == token)
    result_token = await db.execute(query_token)
    db_token = result_token.scalar_one_or_none()

    if not db_token or db_token.expires_at < datetime.now():
        return None

    query_user = select(User).where(User.id == db_token.user_id)
    result_user = await db.execute(query_user)
    return result_user.scalar_one_or_none()

async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    query_user = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_none=True,
        exclude_unset=True
    ))
    result = await db.execute(query_user)
    await db.commit()

    # 检查更新
    if result.rowcount == 0:
        return HTTPException(status_code=404, detail="用户不存在")

    updated_user = await get_user_by_username(db, username)
    return updated_user

async def change_password(db: AsyncSession, user: User, old_password: str, new_password: str):
    if not security.verify_password(old_password, user.password):
        return False

    hashed_new_password = security.get_password_hash(new_password)
    user.password = hashed_new_password
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True