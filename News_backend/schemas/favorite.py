from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.news import NewsDetailResponseBase


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")

class FavoriteAddResponse(BaseModel):
    news_id: int = Field(..., alias="newsId")

class FavoriteNewsItemBase(NewsDetailResponseBase):
    favorite_id: int = Field(..., alias="favoriteId")
    favorite_time: datetime = Field(..., alias="favoriteTime")

    model_config = ConfigDict(
        from_attributes=True, # 允许从 ORM 模型属性中取值
        populate_by_name=True # alias / 字段名兼容
    )

class FavoriteListResponse(BaseModel):
    list: list[FavoriteNewsItemBase]
    total: int
    has_more: bool = Field(..., alias="hasMore")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )