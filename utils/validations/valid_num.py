def valid_num(num: str) -> str | None:
    if num.isdigit():
        if 1 <= int(num) <=5:
            return int(num)
        return None
    return None
