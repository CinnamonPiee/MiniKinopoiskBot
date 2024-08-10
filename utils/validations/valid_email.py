from email_validator import EmailNotValidError, validate_email


def valid_email(email: str) -> str | None:
    try:
        v = validate_email(email)
        email = v["email"]
        return email

    except EmailNotValidError as e:
        print(str(e))
        return None
