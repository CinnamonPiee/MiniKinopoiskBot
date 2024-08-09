import requests


def encrypt_password(password: str) -> str:
    url = "http://127.0.0.1:8000/encrypt/"
    payload = {"password": password}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        hashed_password = response.json().get("hashed_password")
        return hashed_password
    else:
        return "Сервер временно не доступен, попробуйте позже!"


def check_password(hashed_password: str, password: str) -> bool:
    url = "http://127.0.0.1:8000/check/"
    payload = {"password": password, "hashed_password": hashed_password}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        is_valid = response.json().get("is_valid")
        return is_valid
    else:
        return "Сервер временно не доступен, попробуйте позже!"


