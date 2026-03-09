from fastapi import APIRouter,Depends,Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud import news
from crud.news import get_news_count, increase_news_views
from models.users import User
from schemas.news import NewsListResponse, NewsCreateRequest, NewsItemBase, NewsDetailResponse
from utils.auth import get_current_user
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
async def get_news_detail(news_id: int = Query(default=0, alias="id"), db: AsyncSession = Depends(get_db)):
    # 获取新闻详情 + 浏览量+1 + 相关新闻
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    view_res = await increase_news_views(db, news_detail.id)
    if not view_res:
        raise HTTPException(status_code=404, detail="新闻不存在")

    related_news_orm = await news.get_related_news(db, news_detail.id, news_detail.category_id)

    news_detail_pydantic = NewsItemBase.model_validate(news_detail)
    related_news_pydantic = [NewsItemBase.model_validate(item) for item in related_news_orm]
    data = NewsDetailResponse(**news_detail_pydantic.model_dump(), relatedNews=related_news_pydantic)

    return success_response(message="获取新闻详情成功", data=data)

@router.post("/add")
async def add_news(news_data:NewsCreateRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    news_id, news_title = await news.add_news(db,user, news_data)
    return success_response(message="添加新闻成功", data={"newsId": news_id, "newsTitle": news_title})

@router.get("/search")
async def search_news(
    keyword: str = Query(default="...", alias="keyword"),
    page: int = 1,
    page_size: int = Query(default=10, alias="pageSize", le=100),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    news_search_list = await news.search_news_by_keyword(db, keyword, offset, page_size)
    total = await news.get_news_count_keyword(db, keyword)
    has_more = (offset + page_size) < total
    data = NewsListResponse(list=news_search_list, total=total, hasMore=has_more)
    return success_response(message="搜索新闻成功", data=data)
