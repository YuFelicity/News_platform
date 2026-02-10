from datetime import datetime
from typing import Optional
from sqlalchemy import Index, String, Enum, DateTime, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):

    __tablename__ = "user"

    __table_args__ = (
        Index( 'username_UNIQUE', 'username'),
        Index('phone_UNIQUE','phone'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username: Mapped[str] = mapped_column(String(50),unique=True,nullable=False,comment='用户名')
    password: Mapped[str] = mapped_column(String(255),nullable=False,comment='密码')
    nickname: Mapped[Optional[str]] = mapped_column(String(50),nullable=True,comment='昵称')
    avatar: Mapped[Optional[str]] = mapped_column(String(255),nullable=True,comment='头像URL',default="http://fastly.jsdeliver.net/npm/assets/cat.jpeg")
    gender: Mapped[Optional[str]] = mapped_column(Enum('male', 'female', 'unknown'),comment='性别', default='unknown')
    bio: Mapped[Optional[str]] = mapped_column(String(500),comment='个人简介',default='这个人很懒，什么也没留下')
    phone: Mapped[Optional[str]] = mapped_column(String(11),unique=True,nullable=True,comment='手机号')
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.now(),comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.now(),onupdate=datetime.now(),comment='更新时间')

class UserToken(Base):

    __tablename__ = "user_token"

    __table_args__ = (
        Index('token_UNIQUE', 'token'),
        Index('fk_user_token_user_idx', 'user_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='用户TokenID')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'),nullable=False,comment='用户ID')
    token: Mapped[str] = mapped_column(String(255),unique=True,nullable=False,comment='用户Token')
    expires_at: Mapped[datetime] = mapped_column(DateTime,nullable=False,comment='Token过期时间')
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.now(),comment='创建时间')
