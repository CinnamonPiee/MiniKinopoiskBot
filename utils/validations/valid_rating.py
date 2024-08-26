def valid_rating(rating: str) -> str | None:
    try:
        if len(rating) == 1:
            if rating.isdigit():
                if 1 <= int(rating) <= 10:
                    return rating
                return None
            return None
        
        elif len(rating) == 3 and "." in rating:
            if 1 <= float(rating) <= 10:
                return rating
            return None
        
        elif len(rating) == 3 and "-" in rating:
            if (1 <= int(rating.split("-")[0]) <= 10):
                if (1 <= int(rating.split("-")[1]) <= 10):
                    if (int(rating.split("-")[0]) < int(rating.split("-")[1])):
                        return rating
                    return None
                return None
            return None
        
        elif 5 <= len(rating) <= 8:
            if (1 <= float(rating.split("-")[0]) <= 10):
                if (1 <= float(rating.split("-")[1]) <= 10):
                    if (float(rating.split("-")[0]) < float(rating.split("-")[1])):
                        return rating
                    return None
                return None
            return None
        return None
    except:
        return None
