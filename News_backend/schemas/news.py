from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class NewsItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    author: str
    category_id: int = Field(..., alias="categoryId")
    views: int
    publish_time: Optional[datetime] = Field(None, alias="publishTime")

    model_config = ConfigDict(
        from_attributes=True, # 允许从 ORM 模型属性中取值
        populate_by_name=True # 忽略未设置字段，允许字段名不一致
    )

class NewsListResponse(BaseModel):
    list: list[NewsItemBase]
    total: int
    has_more: bool = Field(False, alias="hasMore")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

class NewsDetailResponse(NewsItemBase ):
    related_news: list[NewsItemBase] = Field(None, alias="relatedNews")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

class NewsCreateRequest(BaseModel):
    title: str
    description: Optional[str]
    content: Optional[str]
    image: Optional[str] = None
    author: str
    category_id: int = Field(..., alias="categoryId")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )