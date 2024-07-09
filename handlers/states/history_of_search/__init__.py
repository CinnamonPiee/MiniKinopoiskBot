__all__ = ("router", )

from aiogram import Router

from .first_date import router as first_date_router
from .second_date import router as second_date_router
from .choose_film_serial_all import router as choose_film_serial_all_router

router = Router(name=__name__)

router.include_router(first_date_router)
router.include_router(second_date_router)
router.include_router(choose_film_serial_all_router)
