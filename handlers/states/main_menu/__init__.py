__all__ = ("router", )

from aiogram import Router

from .criteries import router as criteries_router

router = Router(name=__name__)

router.include_router(criteries_router)
