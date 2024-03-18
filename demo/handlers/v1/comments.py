from datetime import datetime, UTC
from math import ceil
from typing import Literal

from fastapi import APIRouter, Query, Path, HTTPException
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import count
from starlette import status
from starlette.requests import Request
from sqlalchemy.exc import IntegrityError

from demo.models import Cases, Comments
from demo.schemas import CasesDetail, CasesCreateForm, CasesCreateCommentForm, CommentsDetail
from src.dependencies import DBSession
# from src.schemas.paginator import Paginator

router = APIRouter(tags=["Comments"])


@router.get(
    path="/comments",
    response_model=list[CommentsDetail],
    name="demo_comments_list",
    response_model_exclude_none=True,
)
async def cases_list(
        session: DBSession,
        order_by: Literal["id", "name"] = Query(default="id", alias="orderBy"),
        # case_comment: list[PositiveInt] = Query(default=None),
        order: Literal["asc", "desc"] = Query(default="asc", alias="orderDirection")
):
    stmt = select(Comments)
    # stmt = stmt.options(joinedload(Cases.case_comment))
    objs = await session.scalars(
        statement=stmt
        .order_by(
            getattr(getattr(Comments, order_by), order)()
        )
    )
    return [CommentsDetail.model_validate(obj=obj, from_attributes=True) for obj in objs.unique()]