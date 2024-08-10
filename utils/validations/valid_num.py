def valid_num(num: str) -> str | None:
    if num.isdigit():
        return int(num)
    return None
