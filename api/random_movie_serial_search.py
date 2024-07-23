import requests
from config_data.config import settings
from typing import Optional


def random_movie_search(
        type_choice: Optional[str] = None,
        year: Optional[str] = None,
        rating: Optional[str] = None,
        age_rating: Optional[str] = None,
        movie_length: Optional[str] = None,
        series_length: Optional[str] = None,
        janr: Optional[list] = None,
        country: Optional[list] = None
):

    url = f"https://api.kinopoisk.dev/v1.4/movie/random?notNullFields=name"

    if type_choice:
        url = url + f"&type={type}"
    if year:
        url = url + f"&year={year}"
    if rating:
        url = url + f"&rating.imdb={rating}"
    if age_rating:
        url = url + f"&ageRating={age_rating}"
    if movie_length:
        url = url + f"&movieLength={movie_length}"
    if series_length:
        url = url + f"seriesLength={series_length}"
    if janr:
        if len(janr) == 1:
            url = url + f"&genres.name={janr[0]}"
        else:
            url = url + f"&genres.name={janr[0]}"
            for i in janr[1]:
                url = url + f"&genres.name=+{i}"
    if country:
        if len(country) == 1:
            url = url + f"&countries.name={country}"
        else:
            url = url + f"&countries.name={country}"
            for j in country:
                url = url + f"&countries.name=+{j}"

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
