def valid_password(password: str) -> str | None:
    if len(password) >= 8:
        for i in password:
            if i.isdigit():
                second_str = password
                if not second_str.lower() == password:
                    return password
                return None
            return None
    return None
