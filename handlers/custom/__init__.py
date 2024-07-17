__all__ = ("router", )

from aiogram import Router

from .truncate_tables import router as truncate_tables_router
from .user_info import router as user_info_router

router = Router(name=__name__)

router.include_router(truncate_tables_router)
router.include_router(user_info_router)
