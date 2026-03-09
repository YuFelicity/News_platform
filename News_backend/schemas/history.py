from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.news import NewsItemBase


class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")

class HistoryAddResponse(BaseModel):
    id: int
    user_id: int = Field(..., alias="userId")
    news_id: int = Field(..., alias="newsId")
    view_time: datetime = Field(..., alias="viewTime")
    model_config = ConfigDict(
        from_attributes=True, # 允许从 ORM 模型属性中取值
        populate_by_name=True # alias / 字段名兼容
    )

class HistoryNewsItemBase(NewsItemBase):
    view_time: datetime = Field(..., alias="viewTime")

class HistoryListResponse(BaseModel):
    list: list[HistoryNewsItemBase]
    total: int
    has_more: bool = Field(False, alias="hasMore")
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )