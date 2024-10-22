import requests
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from config_data.config import settings
from typing import Optional


def random_custom_movie_serial_search(
        type_choice: Optional[str] | None = None,
        year: Optional[str] | None = None,
        rating: Optional[str] | None = None,
        age_rating: Optional[str] | None = None,
        movie_length: Optional[str] | None = None,
        series_length: Optional[str] | None = None,
        janr: Optional[list] | None = None,
        country: Optional[list] | None = None
) -> dict:

    url = f"https://api.kinopoisk.dev/v1.4/movie/random?notNullFields=name"

    if type_choice:
        url = url + f"&type={type_choice}"
    if year:
        url = url + f"&year={year}"
    if rating:
        url = url + f"&rating.imdb={rating}"
    if age_rating:
        url = url + f"&ageRating={age_rating}"
    if movie_length:
        url = url + f"&movieLength={movie_length}"
    if series_length:
        url = url + f"&seriesLength={series_length}"
    if janr:
        if len(janr) == 1:
            url = url + f"&genres.name={janr[0]}"
        else:
            url = url + f"&genres.name=%2B{janr[0]}"
            for i in janr[1:]:
                url = url + f"&genres.name=%2B{i}"
    if country:
        if len(country) == 1:
            url = url + f"&countries.name={country[0]}"
        else:
            url = url + f"&countries.name=%2B{country[0]}"
            for j in country[1:]:
                url = url + f"&countries.name=%2B{j}"

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
        
    except ValueError:
        print("Ошибка декодирования JSON. Сервер вернул невалидный JSON.")
        return "Ошибка декодирования JSON. Сервер вернул невалидный JSON."
