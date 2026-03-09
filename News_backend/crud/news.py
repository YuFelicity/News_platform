from sqlalchemy import select, func, update, or_
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import News, NewsCategory
from models.users import User
from schemas.news import NewsCreateRequest, NewsItemBase


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 50):
    t = select(NewsCategory).offset(skip).limit(limit)
    result = await db.execute(t)
    return result.scalars().all()

async def get_news(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 50):
    t = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(t)
    return result.scalars().all()

async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
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

async def get_related_news(db: AsyncSession, news_id: int, category_id: int,limit: int = 5):
    # order_by 排序 -> 浏览量和发布时间
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id,
    ).order_by(
        News.views.desc(), # 默认升序，降序 desc()
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    return [{
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
    } for news_detail in related_news]

async def add_news(db: AsyncSession, user: User, news_data: NewsCreateRequest):
    news = News(title=news_data.title,
                description=news_data.description,
                content=news_data.content,
                image=news_data.image,
                author=news_data.author,
                category_id=news_data.category_id,
                user_id=user.id)
    db.add(news)
    await db.commit()
    await db.refresh(news)
    return news.id,news.title

async def get_news_count_keyword(db: AsyncSession, keyword: str):
    stmt = (select(func.count(News.id))
    .where(
        or_(
            News.title.contains(keyword),
            News.description.contains(keyword)
        )
    )
    )
    result = await db.execute(stmt)
    return result.scalars().one_or_none() or 0


async def search_news_by_keyword(db: AsyncSession, keyword: str, skip: int = 0, limit: int = 50):
    stmt = select(News).where(
        or_(
            News.title.contains(keyword),
            News.description.contains(keyword)
        )
    ).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
