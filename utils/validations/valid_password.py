def valid_password(password: str) -> str | None:
    if 8 <= len(password) <= 40:
        for i in password:
            if i.isdigit():
                second_str = password
                if second_str.lower() != password:
                    return password
                return None
            return None
        return None
    return None
