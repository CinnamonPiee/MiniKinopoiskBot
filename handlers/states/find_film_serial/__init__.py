__all__ = ("router", )

from aiogram import Router

from .name import router as name_router

router = Router(name=__name__)

router.include_router(name_router)
