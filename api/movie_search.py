import requests
from config_data.config import KINOPOISK_DEV_TOKEN
import json


def movie_search(film_name):
    url = "https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=1&query="

    headers = {
        "accept": "application/json",
        "X-API-KEY": KINOPOISK_DEV_TOKEN
    }

    response = requests.get(f"{url + film_name}", headers=headers)

    data = response.json()["docs"][0]["name"]

    return data


print(movie_search("avatar"))
