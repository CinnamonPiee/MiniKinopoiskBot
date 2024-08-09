__all__ = ("router", )

from aiogram import Router

from .change_random_page import router as change_random_page_router
from .change_history_page import router as change_history_page_router
from .change_custom_page import router as change_custom_page_router

router = Router(name=__name__)

router.include_router(change_random_page_router)
router.include_router(change_history_page_router)
router.include_router(change_custom_page_router)
