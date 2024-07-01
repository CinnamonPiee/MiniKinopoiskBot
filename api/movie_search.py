import requests
from config_data.config import KINOPOISK_DEV_TOKEN


def movie_search(film_name):
    url = "https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=1&query="

    headers = {
        "accept": "application/json",
        "X-API-KEY": KINOPOISK_DEV_TOKEN
    }
    try:
        response = requests.get(f"{url + film_name}", headers=headers)
        data = response.json()["docs"][0]
        return data

    except IndexError:
        return "Ничего не найдено, пожалуйста попробуйте еще раз!"