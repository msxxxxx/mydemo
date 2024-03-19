from fastapi import APIRouter

from demo.handlers.v1 import cases, comments


router = APIRouter(
    prefix="/v1",
)
router.include_router(router=cases.router)
router.include_router(router=comments.router)
