import requests
from config_data.config import settings
import pprint
from typing import Optional


def random_movie_search(
        year,
        rating,
        age_rating,
        movie_length,
        janr,
        country
):
    url = f"https://api.kinopoisk.dev/v1.4/movie/random?notNullFields=name&type=movie&"\
          f"year={year}&"\
          f"rating.imdb={rating}&"\
          f"ageRating={age_rating}&"\
          f"movieLength={movie_length}&"\
          f"genres.name={janr}&"\
          f"countries.name={country}"

    headers = {
        "accept": "application/json",
        "X-API-KEY": settings.kinopoisk_dev_token
    }

    try:
        response = requests.get(url=url, headers=headers)
        data = response.json()
        if not data:
            return "Ничего не найдено, пожалуйста попробуйте еще раз!"
        return data

    except KeyError:
        return "Сервер временно не доступен, попробуйте позже!"


pprint.pprint(random_movie_search(2021, [], [], [], "null", "null"))
