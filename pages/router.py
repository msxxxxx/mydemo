from fastapi import APIRouter, Request, Depends, Form

from demo.handlers.v1.cases import cases_list, case_detail
from demo.handlers.v1.comments import comment_detail
from demo.schemas import CaseDetail
from src.config import templating
router = APIRouter(
    prefix="/cases",
    tags=["Pages"]
)


@router.get("/")
def get_base_page(request: Request):
    return templating.TemplateResponse("demo/index.html", {"request": request})


@router.get("/list")
def get_list_page(request: Request, cases=Depends(cases_list)):
    return templating.TemplateResponse("demo/case_list.html", {"request": request, "cases": cases})


@router.get("/list/{pk}")
def get_list_page(request: Request, comments=Depends(comment_detail), cases=Depends(case_detail)):
    return templating.TemplateResponse("demo/case_detail.html", {"request": request, "comments": comments, "cases": cases})


@router.get('/create')
def get_create_form(request: Request):
    return templating.TemplateResponse('demo/form.html', {'request': request})
