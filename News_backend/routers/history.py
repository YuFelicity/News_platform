from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud import history
from models.users import User
from schemas.history import HistoryAddRequest, HistoryAddResponse, HistoryNewsItemBase, HistoryListResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/history", tags=["history"])

@router.post("/add")
async def add_history(
    data: HistoryAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    添加历史记录
    """
    result = await history.add_news_history(db, user.id, data.news_id)
    data = HistoryAddResponse.model_validate(result)
    return success_response(message="添加历史记录成功", data=data)

@router.get("/list")
async def get_history_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100, alias="pageSize"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取历史记录列表
    """
    rows_orm, total = await history.get_history_list(page, page_size, user, db)
    history_list = [HistoryNewsItemBase.model_validate({
        **row.News.__dict__,
        "view_time": row.view_time
    }) for row in rows_orm]

    data = HistoryListResponse(list=history_list, total=total, hasMore=total > page * page_size)
    return success_response(message="获取历史记录列表成功", data=data)

@router.delete("/delete/{history_id}")
async def delete_history(
    history_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除历史记录
    """
    result = await history.delete_history(db, user.id, history_id)
    if not result:
        raise HTTPException(status_code=404, detail="历史记录不存在")
    return success_response(message="删除历史记录成功")

@router.delete("/clear")
async def clear_history(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    清空历史记录
    """
    result = await history.clear_history(db, user.id)
    if not result:
        raise HTTPException(status_code=404, detail="历史记录不存在")
    return success_response(message="清空历史记录成功")