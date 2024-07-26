
def valid_password(password: str):
    if len(password) >= 8:
        if password.isalnum():
            second_str = password
            if not second_str.lower() == password:
                return password
            return None
        return None
    return None

            