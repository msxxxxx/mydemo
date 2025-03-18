import fastapi
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from demo.handlers import router
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from demo.dependencies import check_session, authenticate
from demo.models import User
from demo.schemas import UserRegisterForm, UserLoginForm, TokenPairDetail
from demo.utils import create_password_hash, verify_password, create_jwt, create_access_token
from src.dependencies import DBSession
from pages.router import router as router_pages
from src.config import static, templating
from demo.config import config

app = FastAPI()
# app.include_router(router=router)
app.include_router(router=router, dependencies=[authenticate])
app.include_router(router=router_pages)
app.mount(path="/static", app=static, name="static")


app.add_middleware(
    middleware_class=SessionMiddleware,
    secret_key="w8yuehfoqiebvoewpjvewvr",
    session_cookie="sessionID",
)
app.add_middleware(middleware_class=ProxyHeadersMiddleware, trusted_hosts=("*",))


@app.get(path="/login")
async def index(request: Request):
    return templating.TemplateResponse(request=request, name="demo/sign-in.html")


@app.get(path="/logout")
async def index(request: Request, response: Response):
    response = templating.TemplateResponse(request=request, name="demo/sign-in.html")
    response.delete_cookie("access_token")
    return response


@app.get(path="/register")
async def index(request: Request):
    return templating.TemplateResponse(request=request, name="demo/sign-up.html")


@app.post(path="/signup", name="signup", status_code=status.HTTP_201_CREATED)
async def signup(session: DBSession, form: UserRegisterForm):
    password_hash = create_password_hash(password=form.password)
    user = User(
        **form.model_dump(exclude={"confirm_password"}) | {"password": password_hash}
    )
    session.add(instance=user)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"user with email {form.email} exist",
        )
    return "OK"


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
            status_code=status.HTTP_403_FORBIDDEN, detail="user or password invalid"
        )

    if not verify_password(hashed_password=user.password, plain_password=form.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user or password invalid"
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


if __name__ == "__main__":
    from uvicorn import run

    run(app=app, host="0.0.0.0", port=80)
