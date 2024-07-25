__all__ = ("router", )

from aiogram import Router

from. login_registration import router as login_registration_router
from .email import router as email_router
from .name import router as name_router
from .phone_number import router as phone_number_router
from .password import router as password_router

router = Router(name=__name__)

router.include_router(email_router)
router.include_router(name_router)
router.include_router(phone_number_router)
router.include_router(login_registration_router)
router.include_router(password_router)
