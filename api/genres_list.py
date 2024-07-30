import requests
from config_data.config import settings
import pprint


def genres_list():
    url = "https://api.kinopoisk.dev/v1/movie/possible-values-by-field?field=genres.name"

    headers = {
        "accept": "application/json",
        "X-API-KEY": settings.kinopoisk_dev_token
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return data

    except IndexError:
        return "Ничего не найдено, пожалуйста попробуйте еще раз!"
    except KeyError:
        return "Сервер временно не доступен, попробуйте позже!"


pprint.pprint(genres_list())


