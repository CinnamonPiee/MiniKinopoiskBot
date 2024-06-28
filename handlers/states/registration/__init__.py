__all__ = ("router", )

from aiogram import Router

from .email import router as email_router
from .name import router as name_router
from .phone_number import router as phone_number

router = Router(name=__name__)

router.include_router(email_router)
router.include_router(name_router)
router.include_router(phone_number)
