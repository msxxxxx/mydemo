from typing import Literal

from fastapi import APIRouter, Query
from sqlalchemy import select

from demo.models import Comment
from demo.schemas import CommentDetail
from src.dependencies import DBSession

router = APIRouter(tags=["Comments"])


@router.get(
    path="/comments",
    response_model=list[CommentDetail],
    name="demo_comments_list",
    response_model_exclude_none=True,
)
async def cases_list(
    session: DBSession,
    order_by: Literal["id", "name"] = Query(default="id", alias="orderBy"),
    order: Literal["asc", "desc"] = Query(default="asc", alias="orderDirection"),
):
    stmt = select(Comment)
    objs = await session.scalars(
        statement=stmt.order_by(getattr(getattr(Comment, order_by), order)())
    )
    return [
        CommentDetail.model_validate(obj=obj, from_attributes=True)
        for obj in objs.unique()
    ]
