from datetime import datetime
from fastapi import Depends, Query
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from models.history import History
from models.news import News
from models.users import User
from utils.auth import get_current_user


async def add_news_history(db: AsyncSession, user_id: int, news_id: int):
    query = select(History).where(History.user_id == user_id,History.news_id == news_id)
    result = await db.execute(query)
    exist_history = result.scalar_one_or_none()
    if exist_history:
        exist_history.view_time = datetime.now()
        await db.commit()
        await db.refresh(exist_history)
        return exist_history
    else:
        history = History(user_id=user_id, news_id=news_id)
        db.add(history)
        await db.commit()
        await db.refresh(history)
        return history

async def get_history_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, le=100, alias="pageSize"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):

    count_query = select(func.count()).where(History.user_id == user.id)
    total = await db.scalar(count_query)
    total = total or 0
    query = (select(News, History.id.label("history_id"), History.view_time.label("view_time"))
            .join(History, History.news_id == News.id)
            .where(History.user_id == user.id)
            .order_by(History.view_time.desc())
            .offset(page_size * (page - 1))
            .limit(page_size))
    result = await db.execute(query)
    rows = result.all()
    return rows, total

async def delete_history(db: AsyncSession, user_id: int, history_id: int):
    query = select(History).where(History.user_id == user_id,History.news_id == history_id)
    result = await db.execute(query)
    history = result.scalar_one_or_none()
    if history:
        await db.delete(history)
        await db.commit()
        return True
    else:
        return False

async def clear_history(db: AsyncSession, user_id: int):
    query = delete(History).where(History.user_id == user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount or 0
