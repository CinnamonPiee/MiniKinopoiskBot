def valid_years(year: str) -> str | None:
        try:
            if len(year) == 4:
                if year.isdigit() and 1800 < int(year) <= 2024:
                    return year
                return None

            elif 8 <= len(year) > 4:
                for i in year.split('-'):
                    if i.isdigit() and 1800 < int(i) <= 2024:
                        continue
                return year
            return None
        except:
            return None
