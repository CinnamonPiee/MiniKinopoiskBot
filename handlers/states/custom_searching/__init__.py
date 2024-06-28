__all__ = ("router", )

from aiogram import Router

from .coast import router as coast_router
from .count import router as count_router
from .country import router as country_number
from .janr import router as janr_number
from .year import router as year_number

router = Router(name=__name__)

router.include_router(coast_router)
router.include_router(count_router)
router.include_router(country_number)
router.include_router(janr_number)
router.include_router(year_number)
