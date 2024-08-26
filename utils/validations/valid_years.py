def valid_years(year: str) -> str | None:
    try:
        if len(year) == 4:
            if year.isdigit():
                if 1800 < int(year) <= 2024:
                    return year
                return None
            return None

        elif len(year) == 9:
            if len(year.split("-")) == 2:
                if 1800 <= int(year.split("-")[0]) <= 2024:
                    if 1800 <= int(year.split("-")[1]) <= 2024:
                        if int(year.split("-")[0]) < int(year.split("-")[1]):
                            return year
                        return None
                    return None
                return None
            return None
        return None
    except:
        return None
