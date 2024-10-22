__all__ = ("router", )

from aiogram import Router

from .states import router as states_router
from .custom import router as custom_router
from .default import router as default_router
from .callbacks import router as callbacks_router

router = Router(name=__name__)

router.include_router(custom_router)
router.include_router(states_router)
router.include_router(callbacks_router)

# this router is last!
router.include_router(default_router)

