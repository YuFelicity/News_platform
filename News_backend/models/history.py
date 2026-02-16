from datetime import datetime
from sqlalchemy import Index, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime


class Base(DeclarativeBase):
    pass

class History(Base):
    __tablename__ = "history"

    __table_args__ = (
        Index('fk_history_user_idx', 'user_id'),
        Index('fk_history_news_idx', 'news_id'),
        Index('idx_view_time', 'view_time'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="历史记录ID")
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="新闻ID")
    view_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False, comment="浏览时间")