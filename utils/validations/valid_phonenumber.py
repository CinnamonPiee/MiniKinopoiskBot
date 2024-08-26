import phonenumbers


def valid_phonenumber(phonenumber: str) -> str | bool:
    phone = phonenumbers.parse(phonenumber, None)
    if phonenumbers.is_valid_number(phone):
        return phonenumber
    return phonenumbers.is_valid_number(phone)
