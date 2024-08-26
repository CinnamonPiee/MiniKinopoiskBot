def valid_name(name: str) -> str | None:
    if name.isalpha():
        if len(name) > 1:
            return name
        return None
    return None
