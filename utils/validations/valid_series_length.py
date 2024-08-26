def valid_series_length(series_length: str) -> str | None:
    try:
        if 2 <= len(series_length) <= 3:
            if 5 <= int(series_length) <= 200:
                return series_length
            return None
        
        elif 5 <= len(series_length) <= 7:
            if len(series_length.split("-")) == 2:
                if (5 <= int(series_length.split("-")[0]) <= 200):
                    if (5 <= int(series_length.split("-")[1]) <= 200):
                        if (int(series_length.split("-")[0]) < int(series_length.split("-")[1])):
                            return series_length
                        return None
                    return None
                return None
            return None
        return None
    except:
        return None
