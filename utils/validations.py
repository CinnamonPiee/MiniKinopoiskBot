import re
import phonenumbers

from sqlalchemy import text
from datetime import datetime
from email_validator import EmailNotValidError, validate_email

from database.models import SearchSerial, HistorySerial, SearchFilm, User, HistoryFilm
from database.orm.serial import update_search_history, add_search_history
from database.databases import async_session_factory

from sqlalchemy.future import select




class Validations():
    def valid_years(year: str):
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


    async def valid_user_and_serial_id_in_history(name, telegram_id):
        async with async_session_factory() as session:
            result = await session.execute(select(SearchSerial).where(SearchSerial.name == name))
            existing_serial = result.scalars().first()

            if existing_serial:
                user_result = await session.execute(select(User).where(User.telegram_id == telegram_id))
                user = user_result.scalars().first()

                if user:
                    data = await session.execute(select(HistorySerial).where(
                        HistorySerial.user_id == user.id, HistorySerial.serial_id == existing_serial.id))
                    data = data.scalars().first()

                    if data:
                        await update_search_history(user.id, existing_serial.id)
                    else:
                        await add_search_history(user.id, existing_serial.id)


    async def valid_user_and_film_id_in_history(name, telegram_id):
        async with async_session_factory() as session:
            result = await session.execute(select(SearchFilm).where(SearchFilm.name == name))
            existing_film = result.scalars().first()

            if existing_film:
                user_result = await session.execute(select(User).where(User.telegram_id == telegram_id))
                user = user_result.scalars().first()

                if user:
                    data = await session.execute(select(HistoryFilm).where(
                        HistoryFilm.user_id == user.id, HistoryFilm.film_id == existing_film.id))
                    data = data.scalars().first()

                    if data:
                        await update_search_history(user.id, existing_film.id)
                    else:
                        await add_search_history(user.id, existing_film.id)


    def valid_series_length(series_length: str):
        if 2 <= len(series_length) <= 3:
            if 10 <= int(series_length) <= 150:
                return series_length
            return None
        elif 5 <= len(series_length) <= 7 and len(series_length.split("-")) == 2:
            if (10 <= int(series_length.split("-")[0]) <= 150) and (10 <= int(series_length.split("-")[1]) <= 150) and (int(series_length.split("-")[0]) < int(series_length.split("-")[1])):
                return series_length
            return None
    

    def valid_rating(rating: str):
        if 1 <= len(rating) <= 3:
            if 1 <= float(rating) <= 10:
                return rating
            return None
        elif 3 <= len(rating) <= 7 and len(rating.split("-")) == 2:
            if (1 <= float(rating.split("-")[0]) <= 10) and (1 <= float(rating.split("-")[1]) <= 10) and (float(rating.split("-")[0]) < float(rating.split("-")[1])):
                return rating
            return None
    

    def phonenumber_validation(phonenumber) -> str | bool:
        p = phonenumbers.parse(phonenumber, None)
        if phonenumbers.is_valid_number(p):
            return phonenumber
        return phonenumbers.is_valid_number(p)


    def valid_password(password: str):
        if len(password) >= 8:
            if password.isalnum():
                second_str = password
                if not second_str.lower() == password:
                    return password
                return None
            return None
        return None


    def valid_num(num: str):
        if num.isdigit():
            return int(num)
        return None


    def name_validation(name):
        if name.isalpha() and len(name) > 1:
            return name
        return None


    def valid_movie_length(movie_length: str):
        if 2 <= len(movie_length) <= 3:
            if 50 <= int(movie_length) <= 300:
                return movie_length
            return None
        elif 5 <= len(movie_length) <= 7 and len(movie_length.split("-")) == 2:
            if (50 <= int(movie_length.split("-")[0]) <= 300) and (50 <= int(movie_length.split("-")[1]) <= 300) and (int(movie_length.split("-")[0]) < int(movie_length.split("-")[1])):
                return movie_length
            return None


    def email_validation(email):
        try:
            v = validate_email(email)
            email = v["email"]
            return email

        except EmailNotValidError as e:
            print(str(e))
            return None


    def date_valid(date_string):
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

        if not date_pattern.match(date_string):
            return False

        try:
            datetime.strptime(date_string, '%Y-%m-%d')
        except ValueError:
            return False

        return date_string


    def valid_choose_in_history(choose: str):
        if choose in ["Фильмы и сериалы", "Сериалы", "Фильмы"]:
            return choose
        return None


    def valid_age_rating(age_rating: str):
        if len(age_rating) == 1:
            if 0 <= int(age_rating) <= 18:
                return age_rating
            return None
        elif 3 <= len(age_rating) <= 5 and len(age_rating.split("-")) == 2:
            if (0 <= int(age_rating.split("-")[0]) <= 18) and (0 <= int(age_rating.split("-")[1]) <= 18) and (int(age_rating.split("-")[0]) < int(age_rating.split("-")[1])):
                return age_rating
            return None


    async def truncate_tables():
        async with async_session_factory() as session:
            async with session.begin():
                await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
                await session.execute(text("TRUNCATE TABLE search_film RESTART IDENTITY CASCADE"))
                await session.execute(text("TRUNCATE TABLE search_serial RESTART IDENTITY CASCADE"))
                await session.execute(text("TRUNCATE TABLE history_search_film RESTART IDENTITY CASCADE"))
                await session.execute(text("TRUNCATE TABLE history_search_serial RESTART IDENTITY CASCADE"))
            await session.commit()

    async def valid_janr(janrs):
        pass
