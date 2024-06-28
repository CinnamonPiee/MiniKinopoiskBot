# MiniKinopoisk

## Описание

Телеграмм бот для поиска фильмов, мини аналог сайта Кинопоиск.\
Стек: aiogram, SQLAlchemy

## Установка

Следуйте инструкциям ниже для установки и запуска бота в телеграм.

### Шаги установки

1. Клонируйте репозиторий

    ```bash
    git clone https://github.com/KellTuz/MiniKinopoiskBot.git
    cd MiniKinopoiskBot
    ```

2. Создайте и активируйте виртуальное окружение

   - Windows
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

   - Linux and MacOS
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3. Установите зависимости

    ```bash
    pip install -r requirements.txt
    ```
   
4. Получите персональный токен в телеграм у BotFather и поместите его\
в файл .env (смотрите пример в .env.template)

5. Запустите бота командой

    - Windows
         ```python
         cd MiniKinopoiskBot
         python main.py
         ```
   
    - Linux and MacOS
        ```python
        cd MiniKinopoiskBot
        python3 main.py
        ```