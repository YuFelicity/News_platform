from fastapi import APIRouter,Depends,Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud import news
from crud.news import get_news_count, increase_news_views

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "msg": "获取分类成功",
        "data": categories
    }

@router.get("/list")
async def get_news(
        category_id: int = Query(default=0, alias="categoryId"),
        page: int = 1,
        page_size: int = Query(default=10, alias="pageSize", le=100),
        db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    news_list = await news.get_news(db, category_id, offset, page_size)
    total =await get_news_count(db, category_id)
    more = (offset + page_size) < total
    return{
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total":total,
            "hasMore":more,
        }
    }

@router.get("/detail")
async def get_news_detail(news_id: int, db: AsyncSession = Depends(get_db)):
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")
    await increase_news_views(db, news_id)
    return {
        "code": 200,
        "msg": "获取新闻详情成功",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "description": news_detail.description,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "category_id": news_detail.category_id,
            "views": news_detail.views,
            "publish_time": news_detail.publish_time
        }
    }



