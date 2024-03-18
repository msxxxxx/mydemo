from fastapi import APIRouter

from demo.handlers.v1 import cases,comments
# from blog.handlers.v1 import topics


router = APIRouter(
    prefix="/v1",
)
# router.include_router(router=tags.router)
router.include_router(router=cases.router)
router.include_router(router=comments.router)
