from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from crud import users
from schemas.users import RequestUser, UserAuthResponse, UserInfoResponse
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["user"])

@router.post("/register")
async def register(user_data: RequestUser, db:AsyncSession = Depends(get_db)):
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已经存在")
    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)

    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data=response_data)

@router.post("/login")
async def login():
    return {
        "code": 200,
        "message": "登录成功",
        "data": {
        "token": "用户访问令牌",
            "userInfo": {
              "id": 1,
              "username": "example_user",
              "nickname": 'null',
              "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
              "bio": "这个人很懒，什么都没留下"
            }
          }
}