import asyncio
from orm import (
    get_films,
    get_users,
    get_history,
    add_user,
    update_user,
    get_user_by_id
)


async def main():
    # Получение данных
    users = await get_users()
    films = await get_films()
    history = await get_history()

    print("Users:", users)
    print("Films:", films)
    print("History:", history)

    # Добавление нового пользователя
    # await add_user("Jone Doe", "jyne.dae@example.com", "987355321", 9876544230)

    # Обновление данных о пользователе
    # await update_user(1, name="Jahn Smith", email="jahn.smiith@example.com")


# Запуск основного цикла
asyncio.run(main())
