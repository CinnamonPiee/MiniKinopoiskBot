__all__ = ("router", )

from aiogram import Router

from .country import router as country_router
from .criteries_yes_or_no import router as criteries_router
from .janr import router as janr_router
from .rating import router as rating_router
from .year import router as year_router
from .type_choice import router as type_choice_router
from .movie_length import router as movie_length_router
from .count import router as count_router
from .age_rating import router as age_ration_router


router = Router(name=__name__)

router.include_router(country_router)
router.include_router(criteries_router)
router.include_router(janr_router)
router.include_router(rating_router)
router.include_router(year_router)
router.include_router(type_choice_router)
router.include_router(movie_length_router)
router.include_router(count_router)
router.include_router(age_ration_router)
