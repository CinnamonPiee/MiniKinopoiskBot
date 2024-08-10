def valid_rating(rating: str) -> str | None:
    if 1 <= len(rating) <= 3:
        if 1 <= float(rating) <= 10:
            return rating
        return None
    elif 3 <= len(rating) <= 7 and len(rating.split("-")) == 2:
        if (1 <= float(rating.split("-")[0]) <= 10) and (1 <= float(rating.split("-")[1]) <= 10) and (float(rating.split("-")[0]) < float(rating.split("-")[1])):
            return rating
        return None
