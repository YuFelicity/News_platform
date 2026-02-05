from datetime import datetime
from sqlalchemy import Text,Index,ForeignKey
from typing import Optional
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy import Integer,String


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
        comment="更新时间"
    )

class NewsCategory(Base):
    __tablename__ = "news_category"
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻分类ID")
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="新闻分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="排序")

class News(Base):
    __tablename__ = "news"
    # 创建索引： 提升查询速度 -> 添加目录
    __table_args__ = (
        Index('fk_news_category_id', 'category_id'),
        Index('idx_publish_time', 'publish_time')
    )

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻ID")
    title: Mapped[str] = mapped_column(String(225), nullable=False, comment="新闻标题")
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=False, comment="新闻描述")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(225), nullable=False, comment="封面图片URL")
    author: Mapped[Optional[str]] = mapped_column(String(50), nullable=False, comment="作者")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("news_category.id"), nullable=False, comment="新闻分类ID")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False, comment="发布时间")