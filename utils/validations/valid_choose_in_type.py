def valid_choose_in_type(choose: str) -> str | None:
    if choose in ["Фильмы и сериалы", "Сериалы", "Фильмы"]:
        return choose
    return None

