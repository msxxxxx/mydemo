from fastapi import APIRouter, Request, Depends

from demo.handlers.v1.cases import cases_list
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
