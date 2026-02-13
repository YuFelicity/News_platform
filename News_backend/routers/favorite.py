from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud import favorite
from models.users import User
from schemas.favorite import FavoriteAddResponse, FavoriteCheckResponse, FavoriteListResponse, FavoriteNewsItemBase
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])

@router.get("/check")
async def check_favorite(
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    is_favorite = await favorite.is_news_favorite(db, user.id, news_id)

    return success_response(message="获取收藏状态成功", data=FavoriteCheckResponse(isFavorite=is_favorite))

@router.post("/add")
async def add_favorite(
    data: FavoriteAddResponse,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await favorite.add_news_favorite(db, user.id, data.news_id)
    return success_response(message="添加收藏成功", data=result)

@router.delete("/remove")
async def remove_favorite(
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await favorite.remove_news_favorite(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=404, detail="收藏不存在")
    return success_response(message="取消收藏成功")


@router.get("/list")
async def get_favorite_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rows_orm, total = await favorite.get_favorite_list(page, page_size, user,  db)
    favorite_list = [FavoriteNewsItemBase.model_validate({
        **row.News.__dict__,
        "favorite_id": row.favorite_id,
        "favorite_time": row.favorite_time,
    })for row in rows_orm]

    data = FavoriteListResponse(list=favorite_list, total=total, hasMore=total > page * page_size)

    return success_response(message="获取收藏列表成功", data=data)


@router.delete("/clear")
async def clear_favorite(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    count = await favorite.remove_favorite_list(user.id, db)
    return success_response(message=f"成功清空{count}条收藏")