__all__ = ("router", )

from aiogram import Router

from .truncate_tables import router as truncate_tables_router

router = Router(name=__name__)

router.include_router(truncate_tables_router)
