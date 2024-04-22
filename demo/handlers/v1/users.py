from datetime import datetime, UTC
from typing import Literal

from fastapi import APIRouter, Query, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette import status
from sqlalchemy.exc import IntegrityError

from demo.models import Comment, Case, User
from demo.schemas import CaseDetail, CaseCreateForm, CommentCreateForm, CommentDetail
from src.dependencies import DBSession

router = APIRouter(tags=["users"])

@app.post(
    path="/signin",
    name="signin",
    status_code=status.HTTP_200_OK,
    response_model=TokenPairDetail,
)
async def signin(session: DBSession, form: UserLoginForm):
    user = await session.scalar(statement=select(User).filter(User.email == form.email))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    if not verify_password(hashed_password=user.password, plain_password=form.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect password"
        )

    payload = {
        "sub": user.id
    }
    access_token = create_access_token(payload=payload)
    refresh_token = create_access_token(payload=payload)
    user_name = user.email
    return TokenPairDetail(
        user_name=user_name,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer"
    )

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user