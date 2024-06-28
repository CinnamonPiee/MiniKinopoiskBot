__all__ = ("router", )

from aiogram import Router

from .count import router as count_router
from .janr import router as janr_router
from .name import router as name_number

router = Router(name=__name__)

router.include_router(count_router)
router.include_router(janr_router)
router.include_router(name_number)