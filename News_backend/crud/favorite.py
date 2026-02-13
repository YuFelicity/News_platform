from fastapi import Query, Depends
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from models.favorite import Favorite
from models.news import News
from models.users import User
from utils.auth import get_current_user


async def is_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    stmt = select(Favorite).where(Favorite.user_id == user_id,Favorite.news_id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None # 返回布尔值

async def add_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite

async def remove_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    stmt = delete(Favorite).where(Favorite.user_id == user_id,Favorite.news_id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

async def get_favorite_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):

    count_stmt = select(func.count()).where(Favorite.user_id == user.id)
    total = await db.scalar(count_stmt)  # 直接接收整数结果
    total = total or 0
    # 联表查询
    # select(查询主题模型，字段别名).join(关联模型类，联合查询条件)
    # 别名: Favorite.created_at.label("favorite_time")
    stmt = (select(News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id"))
            .join(Favorite, Favorite.news_id == News.id)
            .where(Favorite.user_id == user.id)
            .order_by(Favorite.created_at.desc())
            .offset(page_size * (page - 1))
            .limit(page_size))
    result = await db.execute(stmt)
    rows = result.all()

    return rows, total

async def remove_favorite_list(
        user_id: int,
        db: AsyncSession = Depends(get_db)):
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0

