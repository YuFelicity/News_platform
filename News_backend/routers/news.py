from fastapi import APIRouter,Depends,Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud import news
from crud.news import get_news_count, increase_news_views
from schemas.news import NewsListResponse, NewsDetailResponseBase
from utils.response import success_response

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    categories = await news.get_categories(db, skip, limit)
    return success_response(message="获取分类成功",data=categories)

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
    has_more = (offset + page_size) < total
    data = NewsListResponse(list=news_list, total=total, hasMore=has_more)
    return success_response(message="获取新闻列表成功", data=data)

@router.get("/detail")
async def get_news_detail(news_id: int = Query(0, alias="id"), db: AsyncSession = Depends(get_db)):
    bool_views = await increase_news_views(db, news_id)
    if not bool_views:
        raise HTTPException(status_code=404, detail="新闻不存在")
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    data = NewsDetailResponseBase.model_validate(news_detail)

    return success_response(message="获取新闻详情成功", data=data)

