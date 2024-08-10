def valid_name(name: str) -> str | None:
    if name.isalpha() and len(name) > 1:
        return name
    return None
