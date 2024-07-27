
def valid_movie_length(movie_length: str):
    if 2 <= len(movie_length) <= 3:
        if 50 <= int(movie_length) <= 300:
            return movie_length
        return None
    elif 5 <= len(movie_length) <= 7 and len(movie_length.split("-")) == 2:
        if (50 <= int(movie_length.split("-")[0]) <= 300) and (50 <= int(movie_length.split("-")[1]) <= 300) and (int(movie_length.split("-")[0]) < int(movie_length.split("-")[1])):
            return movie_length
        return None

