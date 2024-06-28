__all__ = ("router", )

from aiogram import Router

from .custom_searching import router as custom_searching_router
from .find_film_serial import router as find_film_serial_router
from .history_of_search import router as history_of_search_router
from .registration import router as registration_router

router = Router(name=__name__)

router.include_router(custom_searching_router)
router.include_router(find_film_serial_router)
router.include_router(history_of_search_router)
router.include_router(registration_router)
