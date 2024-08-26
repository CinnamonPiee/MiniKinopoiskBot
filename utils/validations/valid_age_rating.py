def valid_age_rating(age_rating: str) -> str | None:
    try:
        if 1 <= len(age_rating) <= 2:
            if int(age_rating):
                if 0 <= int(age_rating) <= 18:
                    return age_rating
                return None
            return None
        
        elif 3 <= len(age_rating) <= 5:
            if len(age_rating.split("-")) == 2:
                if (0 <= int(age_rating.split("-")[0]) <= 18):
                    if (0 <= int(age_rating.split("-")[1]) <= 18):
                        if (int(age_rating.split("-")[0]) < int(age_rating.split("-")[1])):
                            return age_rating
                        return None
                    return None
                return None
            return None
        return None
    except:
        return None
