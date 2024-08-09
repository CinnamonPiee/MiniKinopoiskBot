import re
import phonenumbers

from sqlalchemy import text
from datetime import datetime
from email_validator import EmailNotValidError, validate_email

from database.models import SearchSerial, HistorySerial, SearchFilm, User, HistoryFilm
from database.orm.serial import update_search_history, add_search_history
from database.databases import async_session_factory

from sqlalchemy.future import select
from urllib.parse import urlparse


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
            for i in password:
                if i.isdigit():
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
                await session.execute(text("TRUNCATE TABLE users_user RESTART IDENTITY CASCADE"))
                await session.execute(text("TRUNCATE TABLE films_serials_searchfilm RESTART IDENTITY CASCADE"))
                await session.execute(text("TRUNCATE TABLE films_serials_searchserial RESTART IDENTITY CASCADE"))
            await session.commit()

    async def valid_janr(janrs: str | list):
        genres = ['аниме', 'биография', 'боевик', 'вестерн', 'военный', 'детектив', 'детский', 
                  'для взрослых', 'документальный', 'драма', 'игра', 'история', 'комедия', 
                  'концерт', 'короткометражка', 'криминал', 'мелодрама', 'музыка', 'мультфильм', 
                  'мюзикл', 'новости', 'приключения', 'реальное ТВ', 'семейный', 'спорт', 
                  'ток-шоу', 'триллер', 'ужасы', 'фантастика', 'фильм-нуар', 'фэнтези', 'церемония']
        
        if type(janrs) == str:
            if janrs in genres:
                return janrs
            return None
        if type(janrs) == list:
            for i in janrs:
                if not i in genres:
                    return None
            return janrs

    async def valid_country(country: str | list):
        countries = ['Австралия', 'Австрия', 'Азербайджан', 'Албания', 'Алжир', 
                     'Американские Виргинские острова', 'Американское Самоа', 'Ангола', 'Андорра', 
                     'Антарктида', 'Антигуа и Барбуда', 'Антильские Острова', 'Аргентина', 
                     'Армения', 'Аруба', 'Афганистан', 'Багамы', 'Бангладеш', 'Барбадос', 
                     'Бахрейн', 'Беларусь', 'Белиз', 'Бельгия', 'Бенин', 'Берег Слоновой кости', 
                     'Бермуды', 'Бирма', 'Болгария', 'Боливия', 'Босния', 'Босния и Герцеговина', 
                     'Ботсвана', 'Бразилия', 'Бруней-Даруссалам', 'Буркина-Фасо', 'Бурунди', 
                     'Бутан', 'Вануату', 'Ватикан', 'Великобритания', 'Венгрия', 'Венесуэла', 
                     'Виргинские Острова', 'Внешние малые острова США', 'Вьетнам', 
                     'Вьетнам Северный', 'Габон', 'Гаити', 'Гайана', 'Гамбия', 'Гана', 
                     'Гваделупа', 'Гватемала', 'Гвинея', 'Гвинея-Бисау', 'Германия', 
                     'Германия (ГДР)', 'Германия (ФРГ)', 'Гибралтар', 'Гондурас', 'Гонконг', 
                     'Гренада', 'Гренландия', 'Греция', 'Грузия', 'Гуам', 'Дания', 'Джибути', 
                     'Доминика', 'Доминикана', 'Египет', 'Заир', 'Замбия', 'Западная Сахара', 
                     'Зимбабве', 'Израиль', 'Индия', 'Индонезия', 'Иордания', 'Ирак', 'Иран', 
                     'Ирландия', 'Исландия', 'Испания', 'Италия', 'Йемен', 'Кабо-Верде', 
                     'Казахстан', 'Каймановы острова', 'Камбоджа', 'Камерун', 'Канада', 'Катар', 
                     'Кения', 'Кипр', 'Кирибати', 'Китай', 'Колумбия', 'Коморы', 'Конго', 
                     'Конго (ДРК)', 'Корея', 'Корея Северная', 'Корея Южная', 'Косово', 
                     'Коста-Рика', 'Кот-д’Ивуар', 'Куба', 'Кувейт', 'Кыргызстан', 'Лаос', 
                     'Латвия', 'Лесото', 'Либерия', 'Ливан', 'Ливия', 'Литва', 'Лихтенштейн', 
                     'Люксембург', 'Маврикий', 'Мавритания', 'Мадагаскар', 'Макао',
                     'Македония', 'Малави', 'Малайзия', 'Мали', 'Мальдивы', 'Мальта', 'Марокко', 
                     'Мартиника', 'Маршалловы острова', 'Мексика', 'Мозамбик', 'Молдова', 'Монако', 
                     'Монголия', 'Монтсеррат', 'Мьянма', 'Намибия', 'Непал', 'Нигер', 'Нигерия', 
                     'Нидерланды', 'Никарагуа', 'Новая Зеландия', 'Новая Каледония', 'Норвегия', 
                     'ОАЭ', 'Оккупированная Палестинская территория', 'Оман', 'Остров Мэн', 
                     'Острова Кука', 'Пакистан', 'Палау', 'Палестина', 'Панама', 
                     'Папуа - Новая Гвинея', 'Парагвай', 'Перу', 'Польша', 'Португалия', 
                     'Пуэрто Рико', 'Реюньон', 'Российская империя', 'Россия', 'Руанда', 'Румыния', 
                     'СССР', 'США', 'Сальвадор', 'Самоа', 'Сан-Марино', 'Саудовская Аравия', 
                     'Свазиленд', 'Северная Македония', 'Сейшельские острова', 'Сенегал', 
                     'Сент-Винсент и Гренадины', 'Сент-Китс и Невис', 'Сент-Люсия ', 'Сербия', 
                     'Сербия и Черногория', 'Сиам', 'Сингапур', 'Сирия', 'Словакия', 'Словения', 
                     'Соломоновы Острова', 'Сомали', 'Судан', 'Суринам', 'Сьерра-Леоне', 
                     'Таджикистан', 'Таиланд', 'Тайвань', 'Танзания', 'Тимор-Лесте', 'Того', 
                     'Тонга', 'Тринидад и Тобаго', 'Тувалу', 'Тунис', 'Туркменистан', 'Турция', 
                     'Уганда', 'Узбекистан', 'Украина', 'Уругвай', 'Фарерские острова', 
                     'Федеративные Штаты Микронезии', 'Фиджи', 'Филиппины', 'Финляндия', 
                     'Фолклендские острова', 'Франция', 'Французская Гвиана', 
                     'Французская Полинезия', 'Хорватия', 'ЦАР', 'Чад', 'Черногория', 'Чехия', 
                     'Чехословакия', 'Чили', 'Швейцария', 'Швеция', 'Шри-Ланка', 'Эквадор', 
                     'Экваториальная Гвинея', 'Эритрея', 'Эстония', 'Эфиопия', 'ЮАР', 'Югославия', 
                     'Югославия (ФР)', 'Ямайка', 'Япония']
        
        if type(country) == str:
            if country in countries:
                return country
            return None
        if type(country) == list:
            for i in country:
                if not i in countries:
                    return None
            return country

    def get_valid_url(url):
        try:
            result = urlparse(url)
            if all([result.scheme, result.netloc]):
                return url
            else:
                return None
        except :
            return None
        
    
