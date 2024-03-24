from datetime import datetime, UTC
from typing import Literal

from fastapi import APIRouter, Query, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette import status
from sqlalchemy.exc import IntegrityError

from demo.models import Comment, Case
from demo.schemas import CaseDetail, CaseCreateForm, CommentCreateForm, CommentDetail
from src.dependencies import DBSession

router = APIRouter(tags=["Cases"])


@router.get(
    path="/cases",
    response_model=list[CaseDetail],
    name="demo_cases_list",
    response_model_exclude_none=True,
)
async def cases_list(
    session: DBSession,
    order_by: Literal["id", "name"] = Query(default="id", alias="orderBy"),
    order: Literal["asc", "desc"] = Query(default="asc", alias="orderDirection"),
):
    objs = await session.scalars(
        statement=select(Case)
        .options(joinedload(Case.comments))
        .order_by(getattr(getattr(Case, order_by), order)())
    )
    return [
        CaseDetail.model_validate(obj=obj, from_attributes=True)
        for obj in objs.unique().all()
    ]


@router.get(path="/cases/{pk}", response_model=CaseDetail, name="demo_case_detail")
async def case_detail(session: DBSession, pk: int = Path(default=..., ge=1)):
    obj = await session.get(entity=Case, ident=pk, options=[joinedload(Case.comments)])
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Case {pk} not found"
        )
    return CaseDetail.model_validate(obj=obj, from_attributes=True)


@router.post(path="/cases", response_model=CaseDetail, name="Case_demo_create")
async def cases_create(session: DBSession, data: CaseCreateForm):
    obj = Case(
        slug=data.slug.lower(),
        body=data.body.upper(),
        title=data.title.upper(),
        date_created=datetime.now(),
    )
    session.add(instance=obj)
    try:
        await session.commit()
        await session.refresh(instance=obj)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Case {data.title} exist"
        )
    else:
        obj = await session.scalars(
            select(Case).options(joinedload(Case.comments)).filter(Case.id == obj.id)
        )
        return CaseDetail.model_validate(obj=obj, from_attributes=True)


@router.post(
    path="/cases/{pk}/comment", response_model=CommentDetail, name="Comment_demo_create"
)
async def cases_create_comment(
    session: DBSession,
    data: CommentCreateForm,
    pk: int = Path(default=..., ge=1, title="Case ID", examples=[42]),
):
    obj = Comment(text=data.text.upper(), case_id=pk, date_created=datetime.now())
    session.add(instance=obj)
    try:
        await session.commit()
        await session.refresh(instance=obj)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Case {pk} does not exist"
        )
    else:
        return CommentDetail.model_validate(obj=obj, from_attributes=True)
