from email_validator import EmailNotValidError, validate_email


def valid_email(email: str) -> str | None:
    try:
        data = validate_email(email)
        email = data["email"]
        return email

    except EmailNotValidError:
        return None
