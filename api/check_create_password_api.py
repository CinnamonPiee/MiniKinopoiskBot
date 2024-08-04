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
        raise Exception(f"Error encrypting password: {response.text}")


def check_password(password: str, hashed_password: str) -> bool:
    url = "http://127.0.0.1:8000/check/"
    payload = {"password": password, "hashed_password": hashed_password}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        is_valid = response.json().get("is_valid")
        return is_valid
    else:
        raise Exception(f"Error checking password: {response.text}")


