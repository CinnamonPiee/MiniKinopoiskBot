def get_film_data(item):
    if item["poster"]["previewUrl"] is not None and valid_url(item["poster"]["previewUrl"]):
        url = item["poster"]["previewUrl"]
    else:
        url = FSInputFile(
            "/media/simon/MY FILES/Python/Bots/MiniKinopoiskBot/img/not-found-image-15383864787lu.jpg"
        )
    if item["name"] == None:
        name = ""
    else:
        name = item["name"]
    if item["genres"] == None:
        genres = ""
    else:
        genres = ', '.join([i["name"] for i in item["genres"]])
    if item["rating"]["imdb"] == None:
        rating = ""
    else:
        rating = item["rating"]["imdb"]
    if item["year"] == None:
        year = 0
    else:
        year = item["year"]
    if item["movieLength"] == None:
        movie_length = 0
    else:
        movie_length = str(int(item["movieLength"]) // 60) + ":" + str(
            int(item["movieLength"]) % 60)
    if item["countries"] == None:
        countries = ""
    else:
        countries = ', '.join([i["name"] for i in item["countries"]])
    if item["ageRating"] == None:
        age_rating = 0
    else:
        age_rating = item["ageRating"]
    if item["shortDescription"] == None or item["shortDescription"] == "":
        if item["description"] == None:
            description = ""
        else:
            description = item["description"]
    else:
        description = item["shortDescription"]