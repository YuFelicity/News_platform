from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import News, NewsCategory


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 50):
    t = select(NewsCategory).offset(skip).limit(limit)
    result = await db.execute(t)
    return result.scalars().all()

async def get_news(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 50):
    t = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(t)
    return result.scalars().all()

async def get_news_count(db: AsyncSession, category_id: int):
    t = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(t)
    return result.scalars().one_or_none()

async def increase_news_views(db: AsyncSession,category_id: int):
    t = update(News).where(News.category_id == category_id).values(views=News.views + 1)
    result = await db.execute(t)
    await db.commit()
    return result.rowcount > 0 #检查是否命中数据 命中返回True

async def get_news_detail(db: AsyncSession, news_id: int):
    t = select(News).where(News.id == news_id)
    result = await db.execute(t)
    return result.scalars().one_or_none()