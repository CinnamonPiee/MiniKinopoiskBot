def valid_movie_length(movie_length: str) -> str | None:
    try:
        if 2 <= len(movie_length) <= 3:
            if int(movie_length):
                if 15 <= int(movie_length) <= 350:
                    return movie_length
                return None
            return None
        
        elif 5 <= len(movie_length) <= 7:
            if len(movie_length.split("-")) == 2:
                if (15 <= int(movie_length.split("-")[0]) <= 350):
                    if (15 <= int(movie_length.split("-")[1]) <= 350):
                        if (int(movie_length.split("-")[0]) < int(movie_length.split("-")[1])):
                            return movie_length
                        return None
                    return None
                return None
            return None
        return None
    except:
        return None
