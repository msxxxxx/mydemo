from fastapi import APIRouter, Request, Depends

from demo.forms import CaseForm
from demo.handlers.v1.cases import cases_list, case_detail
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
def get_list_page(request: Request, cases=Depends(case_detail)):
    return templating.TemplateResponse("demo/case_detail.html", {"request": request, "cases": cases})


@router.get(path="/create")
async def get_create_case(request: Request):
    form = CaseForm(await request.form())
    return templating.TemplateResponse(
        request=request,
        name="demo/case_detail.html",
        context={
            "case_form": form
        }
    )
