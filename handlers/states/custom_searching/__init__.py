__all__ = ("router", )

from aiogram import Router

from .count import router as count_router
from .country import router as country_number
from .janr import router as janr_number
from .year import router as year_number
from .rating import router as rating_router
from .age_rating import router as age_rating_router
from .movie_length import router as movie_length_router
from .series_length import router as series_length_router
from .type_choice import router as type_choice_router


router = Router(name=__name__)

router.include_router(count_router)
router.include_router(country_number)
router.include_router(janr_number)
router.include_router(year_number)
router.include_router(rating_router)
router.include_router(age_rating_router)
router.include_router(movie_length_router)
router.include_router(series_length_router)
router.include_router(type_choice_router)
