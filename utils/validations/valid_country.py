def valid_country(country: str) -> list | None:
    countries = ['Австралия', 'Австрия', 'Азербайджан', 'Албания', 'Алжир',
                  'Американское Самоа', 'Ангола', 'Андорра',
                 'Антарктида', 'Антигуа и Барбуда', 'Антильские Острова', 'Аргентина',
                 'Армения', 'Аруба', 'Афганистан', 'Багамы', 'Бангладеш', 'Барбадос',
                 'Бахрейн', 'Беларусь', 'Белиз', 'Бельгия', 'Бенин', 
                 'Бермуды', 'Бирма', 'Болгария', 'Боливия', 'Босния', 
                 'Ботсвана', 'Бразилия', 'Бруней-Даруссалам', 'Буркина-Фасо', 'Бурунди',
                 'Бутан', 'Вануату', 'Ватикан', 'Великобритания', 'Венгрия', 'Венесуэла',
                 'Виргинские Острова',  'Вьетнам',
                 'Вьетнам Северный', 'Габон', 'Гаити', 'Гайана', 'Гамбия', 'Гана',
                 'Гваделупа', 'Гватемала', 'Гвинея', 'Гвинея-Бисау', 'Германия',
                 'Гибралтар', 'Гондурас', 'Гонконг',
                 'Гренада', 'Гренландия', 'Греция', 'Грузия', 'Гуам', 'Дания', 'Джибути',
                 'Доминика', 'Доминикана', 'Египет', 'Заир', 'Замбия', 'Западная Сахара',
                 'Зимбабве', 'Израиль', 'Индия', 'Индонезия', 'Иордания', 'Ирак', 'Иран',
                 'Ирландия', 'Исландия', 'Испания', 'Италия', 'Йемен', 'Кабо-Верде',
                 'Казахстан', 'Каймановы острова', 'Камбоджа', 'Камерун', 'Канада', 'Катар',
                 'Кения', 'Кипр', 'Кирибати', 'Китай', 'Колумбия', 'Коморы', 'Конго',
                 'Корея', 'Корея Северная', 'Корея Южная', 'Косово',
                 'Коста-Рика',  'Куба', 'Кувейт', 'Кыргызстан', 'Лаос',
                 'Латвия', 'Лесото', 'Либерия', 'Ливан', 'Ливия', 'Литва', 'Лихтенштейн',
                 'Люксембург', 'Маврикий', 'Мавритания', 'Мадагаскар', 'Макао',
                 'Македония', 'Малави', 'Малайзия', 'Мали', 'Мальдивы', 'Мальта', 'Марокко',
                 'Мартиника', 'Маршалловы острова', 'Мексика', 'Мозамбик', 'Молдова', 'Монако',
                 'Монголия', 'Монтсеррат', 'Мьянма', 'Намибия', 'Непал', 'Нигер', 'Нигерия',
                 'Нидерланды', 'Никарагуа', 'Новая Зеландия', 'Новая Каледония', 'Норвегия',
                 'ОАЭ',  'Оман', 'Остров Мэн',
                 'Острова Кука', 'Пакистан', 'Палау', 'Палестина', 'Панама',
                 'Парагвай', 'Перу', 'Польша', 'Португалия',
                 'Пуэрто Рико', 'Реюньон', 'Российская империя', 'Россия', 'Руанда', 'Румыния',
                 'СССР', 'США', 'Сальвадор', 'Самоа', 'Сан-Марино', 'Саудовская Аравия',
                 'Свазиленд', 'Северная Македония', 'Сейшельские острова', 'Сенегал',
                 'Сент-Люсия ', 'Сербия',
                 'Сиам', 'Сингапур', 'Сирия', 'Словакия', 'Словения',
                 'Соломоновы Острова', 'Сомали', 'Судан', 'Суринам', 'Сьерра-Леоне',
                 'Таджикистан', 'Таиланд', 'Тайвань', 'Танзания', 'Тимор-Лесте', 'Того',
                 'Тонга',  'Тувалу', 'Тунис', 'Туркменистан', 'Турция',
                 'Уганда', 'Узбекистан', 'Украина', 'Уругвай', 'Фарерские острова',
                 'Фиджи', 'Филиппины', 'Финляндия',
                 'Фолклендские острова', 'Франция', 'Французская Гвиана',
                 'Французская Полинезия', 'Хорватия', 'ЦАР', 'Чад', 'Черногория', 'Чехия',
                 'Чехословакия', 'Чили', 'Швейцария', 'Швеция', 'Шри-Ланка', 'Эквадор',
                 'Экваториальная Гвинея', 'Эритрея', 'Эстония', 'Эфиопия', 'ЮАР', 'Югославия',
                 'Ямайка', 'Япония']
    hight_countries = ['Югославия (ФР)', 'Федеративные Штаты Микронезии', 'Тринидад и Тобаго',
                       'Сербия и Черногория', 'Сент-Винсент и Гренадины', 'Сент-Китс и Невис',
                       'Папуа - Новая Гвинея', 'Оккупированная Палестинская территория',
                       'Кот-д’Ивуар', 'Конго (ДРК)', 'Германия (ГДР)', 'Германия (ФРГ)',
                       'Внешние малые острова США', 'Босния и Герцеговина', 'Берег Слоновой кости',
                       'Американские Виргинские острова']

    if len(country.split(" ")) == 1:
        if country.isupper():
            if country[0] in countries:
                return [country]
            return None
        
        elif country.title() in countries:
            return [country.title()]
        return None
    
    if len(country.split(" ")) == 2 or len(country.split("-")) == 2:
        if " ".join(country.split(" ")[0].title() and country.split(" ")[1].title()) in countries:
            return " ".join([country.split(" ")[0].title(), country.split(" ")[1].title()])
        
        if " ".join(country.split(" ")[0].title() and country.split(" ")[1].lower()) in countries:
            return " ".join([country.split(" ")[0].title(), country.split(" ")[1].lower()])

    if len(country.split("-")) == 2:
        if " ".join(country.split("-")[0].title() and country.split("-")[1].title()) in countries:
            return " ".join([country.split("-")[0].title(), country.split("-")[1].title()])
        
    if country in hight_countries:
        return [country]

    return None
