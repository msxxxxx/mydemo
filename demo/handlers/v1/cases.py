from datetime import datetime, UTC
from typing import Literal

from fastapi import APIRouter, Query, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette import status
from sqlalchemy.exc import IntegrityError

from demo.models import Cases, Comments
from demo.schemas import CasesDetail, CasesCreateForm, CasesCreateCommentForm, CommentsDetail
from src.dependencies import DBSession

router = APIRouter(tags=["Cases"])


@router.get(
    path="/cases",
    response_model=list[CasesDetail],
    name="demo_cases_list",
    response_model_exclude_none=True,
)
async def cases_list(
        session: DBSession,
        order_by: Literal["id", "name"] = Query(default="id", alias="orderBy"),
        order: Literal["asc", "desc"] = Query(default="asc", alias="orderDirection")
):
    stmt = select(Cases)
    stmt = stmt.options(joinedload(Cases.case_comment))
    objs = await session.scalars(
        statement=stmt
        .order_by(
            getattr(getattr(Cases, order_by), order)()
        )
    )
    return [CasesDetail.model_validate(obj=obj, from_attributes=True) for obj in objs.unique()]


@router.get(
    path="/cases/{pk}",
    response_model=CasesDetail,
    name="demo_case_detail"
)

async def case_detail(session: DBSession, pk: int = Path(default=..., ge=1)):
    obj = await session.get(entity=Cases, ident=pk, options=[joinedload(Cases.case_comment)])
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Case {pk} not found")
    return CasesDetail.model_validate(obj=obj, from_attributes=True)


@router.post(
    path="/cases",
    response_model=CasesCreateForm,
    name="Case_demo_create"
)
async def cases_create(session: DBSession, data: CasesCreateForm):
    obj = Cases(
        slug=data.slug.lower(),
        body=data.body.upper(),
        title=data.title.upper(),
        date_created=datetime.now()
    )
    session.add(instance=obj)
    try:
        await session.commit()
        await session.refresh(instance=obj)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Case {data.title} exist")
    else:
        return CasesCreateForm.model_validate(obj=obj, from_attributes=True)


@router.post(
    path="/cases/{pk}/comment",
    response_model=CommentsDetail,
    name="Comment_demo_create"
)
async def cases_create_comment(
        session: DBSession,
        data: CasesCreateCommentForm,
        pk: int = Path(
            default=...,
            ge=1,
            title="Case ID",
            examples=[42]
        )
):
    obj = Comments(
        text=data.text.upper(),
        case_id=pk,
        date_created=datetime.now()
    )
    session.add(instance=obj)
    try:
        await session.commit()
        await session.refresh(instance=obj)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Case {pk} does not exist")
    else:
        return CommentsDetail.model_validate(obj=obj, from_attributes=True)
