import phonenumbers


def valid_phonenumber(phonenumber: str) -> str | bool:
    p = phonenumbers.parse(phonenumber, None)
    if phonenumbers.is_valid_number(p):
        return phonenumber
    return phonenumbers.is_valid_number(p)
