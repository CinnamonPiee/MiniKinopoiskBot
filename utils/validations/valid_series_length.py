def valid_series_length(series_length: str) -> str | None:
    if 2 <= len(series_length) <= 3:
        if 10 <= int(series_length) <= 150:
            return series_length
        return None
    elif 5 <= len(series_length) <= 7 and len(series_length.split("-")) == 2:
        if (10 <= int(series_length.split("-")[0]) <= 150) and (10 <= int(series_length.split("-")[1]) <= 150) and (int(series_length.split("-")[0]) < int(series_length.split("-")[1])):
            return series_length
        return None
