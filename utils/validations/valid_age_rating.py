def valid_age_rating(age_rating: str) -> str | None:
    if len(age_rating) == 1:
        if 0 <= int(age_rating) <= 18:
            return age_rating
        return None
    
    elif 3 <= len(age_rating) <= 5 and len(age_rating.split("-")) == 2:
        if (0 <= int(age_rating.split("-")[0]) <= 18) and (0 <= int(age_rating.split("-")[1]) <= 18) and (int(age_rating.split("-")[0]) < int(age_rating.split("-")[1])):
            return age_rating
        return None
