__all__ = ("router", )

from aiogram import Router

from .change_random_page import router as change_random_page_router
from .change_page_callback_handler import router as change_page_callback_handler_router

router = Router(name=__name__)

router.include_router(change_random_page_router)
router.include_router(change_page_callback_handler_router)
