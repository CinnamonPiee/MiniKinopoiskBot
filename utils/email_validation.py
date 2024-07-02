from email_validator import EmailNotValidError, validate_email


def email_validation(email):
    try:
        v = validate_email(email)
        email = v["email"]
        return email

    except EmailNotValidError as e:
        print(str(e))
        return None
