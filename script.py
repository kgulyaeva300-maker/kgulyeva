from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio

from dotenv import load_dotenv  # Добавляем в начало файла
import os                   # Добавляем в начало файла

load_dotenv()  # Читаем .env

TOKEN = os.getenv("BOT_TOKEN")  # Берём токен из .env
if not TOKEN:
    raise ValueError("Токен не найден! Проверьте .env.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню
film_button = KeyboardButton(text="Фильм")
series_button = KeyboardButton(text="Сериал")
keyboard = ReplyKeyboardMarkup(
    keyboard=[[film_button, series_button]],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Данные с фото (примеры URL)
films = [
    {
        "title": "Аритмия (2017)",
        "description": "История врача скорой помощи, который сталкивается с кризисом в профессиональной и личной жизни. Фильм затрагивает темы системы здравоохранения, семейных отношений и профессионального выгорания.",
        "photo": "http://mtsby.server-img.lfstrm.tv/images/archive-images/media/68/3e/683ef860bceeb97a4df981d4d68b5379.jpg"  # замените на реальный URL
    },
    {
        "title": "Левиафан (2014)",
        "description": "История рыбака из северного городка, который сталкивается с коррумпированными чиновниками, пытающимися отобрать его дом и землю. Фильм поднимает темы власти, морали и человеческой трагедии.",
        "photo": "https://static.okko.tv/images/v4/931ac3fe-0554-4d76-b807-3f9fb63683fd?presetId=4000&width=1200&height=630&scale=1&quality=80"
    },
    {
        "title": "Сталинград (2013)",
        "description": "Масштабная историческая драма о битве за Сталинград. Фильм показывает события через призму личных историй солдат и мирных жителей.",
        "photo": "https://static.okko.tv/images/v4/7c184d3e-64d4-44ff-9452-708b51cf1274?presetId=4000&amp;width=1200&amp;height=630&amp;scale=1&amp;quality=80"
    },
    {
        "title": "Горько!(2013)",
        "description": "Сатира на российские свадебные традиции. Фильм рассказывает о свадьбе, которая превращается в череду абсурдных и комичных ситуаций.",
        "photo": "https://mtr.server-img.lfstrm.tv/image/aHR0cDovL210ci5zZXJ2ZXItY21zLmxmc3RybS50di9hcmNoaXZlLWltZy9zdGF0aWMvbWVkaWEvNTcvNTcvNTc1N2MzYzAxMTU5ZTA5N2FlYTdjNjcxZmQwMTg4Nzk="
    },
    {
        "title": "9 рота (2005)",
        "description": "История группы солдат, попавших в афганскую кампанию. Фильм показывает их превращение из «мальчиков» в «мужей» через призму боевых действий.",
        "photo": "https://static.okko.tv/images/v4/228292f3-49fb-4ac3-af36-a73ef08aeaa2?presetId=4000&amp;width=1200&amp;height=630&amp;scale=1&amp;quality=80"
    },
    {
        "title": "Мы из будущего (2008)",
        "description": "Четверо «чёрных следопытов» случайно попадают в 1942 год и оказываются в центре боевых действий.",
        "photo": "https://static.okko.tv/images/v4/eef0be80-97a0-405e-b967-7137d1727610?presetId=4000&amp;width=1200&amp;height=630&amp;scale=1&amp;quality=80"
    },
    {
        "title": "Салют-7 (2017)",
        "description": "Основанный на реальных событиях фильм о миссии по спасению космической станции «Салют-7».",
        "photo": "https://avatars.mds.yandex.net/get-vh/5103318/2a0000017f88995b0a83c15f21bc70561b57/1920x1080q15"
    },
    {
        "title": "Мастер и Маргарита(2024)",
        "description": "Экранизация романа Михаила Булгакова с акцентом на мистические и философские аспекты произведения.",
        "photo": "https://avatars.mds.yandex.net/get-vh/5103318/2a0000017f88995b0a83c15f21bc70561b57/1920x1080q15"
    },
    {
        "title": "Бумер (2003)",
        "description": "История двух друзей, которые после случайной кражи оказываются втянуты в криминальный мир.",
        "photo": "https://images.iptv.rt.ru/images/cfl3u6bir4ssk120b2u0.jpg"
    },
    {
        "title": "О чём говорят мужчины (2010)",
        "description": "Роуд‑муви о четырёх друзьях, которые едут на концерт и по пути обсуждают жизнь, отношения и всё на свете.",
        "photo": "https://avatars.mds.yandex.net/i?id=59949f2dd88ed40d2e82382ef47e4984_l-8710170-images-thumbs&n=13"
    }
]

# Подборка сериалов (10 шт.)
series = [
    {
        "title": "Метод (3 сезона)",
        "description": "История следователя Родиона Меглина, который использует нестандартные методы для раскрытия преступлений. В третьем сезоне к нему присоединяется новая напарница.",
        "photo": "https://avatars.mds.yandex.net/i?id=3d589a105b4a3777f7cb8931d03a7971_l-4628413-images-thumbs&n=13"
    },
    {
        "title": "Кухня (6 сезонов)",
        "description": "История повара Максима Лаврова, который работает в московском ресторане «Claude Monet». Сериал рассказывает о его профессиональном росте и личных отношениях.",
        "photo": "https://pics.ru/wp-content/uploads/2020/10/kuhnya_1200.jpg"
    },
    {
        "title": "Папины дочки (20 сезонов)",
        "description": "История отца‑одиночки Сергея Васнецова и его пяти дочерей. Сериал стал культовым благодаря юмору и семейным ценностям.",
        "photo": "http://images-s.kinorium.com/movie/poster/735093/w1500_51966034.jpg"
    },
    {
        "title": "След (35 сезонов)",
        "description": "Сериал о работе Федеральной экспертной службы (ФЭС), которая расследует сложные преступления с использованием современных технологий.",
        "photo": "https://static.okko.tv/images/v4/1d48f9ec-dc90-46a8-be1f-713e26ef0a10?presetId=4000&amp;width=1200&amp;height=630&amp;scale=1&amp;quality=80"
    },
    {
        "title": "Молодёжка (6 сезонов)",
        "description": "История хоккейной команды «Медведи» и её игроков. Сериал показывает их тренировки, матчи и личные проблемы.",
        "photo": "https://avatars.mds.yandex.net/i?id=e04a2fc0888f84455314ef07d58c4bbb_l-10966259-images-thumbs&n=13"
    },
    {
        "title": "Невский (7 сезонов)",
        "description": "История полицейского Павла Семёнова, который работает в центре Санкт‑Петербурга и сталкивается с опасными преступниками.",
        "photo": "https://media.myshows.me/shows/normal/1/f3/1f3bf163361e2ff2009e34cd1fdf9d88.jpg"
    },
    {
        "title": "Скорая помощь (8 сезонов)",
        "description": "Сериал о работе бригады скорой помощи. В центре сюжета — профессиональные и личные истории врачей и фельдшеров.",
        "photo": "http://images-s.kinorium.com/movie/poster/1627224/w1500_52041442.jpg"
    },
    {
        "title": "Ищейка (2 сезона)",
        "description": "История следователя Александры Кушнир, которая переводится в небольшой город и начинает распутывать сложные дела.",
        "photo": "https://avatars.mds.yandex.net/i?id=f947f852ea3213d9fecca89723b50c04e0f19737-5888889-images-thumbs&n=13"
    },
    {
        "title": "Фишер (2 сезона)",
        "description": "Сериал о расследовании дел серийного убийцы Сергея Головкина (Фишера) в 1980‑х годах.",
        "photo": "http://mtsby.server-img.lfstrm.tv/images/archive-images/media/b8/13/b81361a7b14fccbcc14d697be04dcaac"
    },
    {
        "title": "Кибердеревня (2 сезона)",
        "description": "История фермера Николая, который живёт в «Кибердеревне» и сталкивается с космическими приключениями и технологиями.",
        "photo": "https://cs14.pikabu.ru/post_img/2024/03/26/3/og_og_1711423883223348297.jpg"
    }
]


class ShowState(StatesGroup):
    showing = State()


def make_nav_keyboard(page: int, total: int, category: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    nav_buttons = []

    if page > 1:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=f"nav_{category}_{page - 1}"
        ))

    nav_buttons.append(InlineKeyboardButton(
        text=f"{page}/{total}",
        callback_data="ignore"
    ))

    if page < total:
        nav_buttons.append(InlineKeyboardButton(
            text="➡️ Вперёд",
            callback_data=f"nav_{category}_{page + 1}"
        ))

    kb.inline_keyboard.append(nav_buttons)
    kb.inline_keyboard.append([
        InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="back_to_menu"
        )
    ])
    return kb


@dp.message(Command('start'))
async def send_welcome(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Что хотите посмотреть? Выберите один из вариантов:",
        reply_markup=keyboard
    )


@dp.message(F.text.in_({"Фильм", "Сериал"}))
async def process_choice(message: types.Message, state: FSMContext):
    choice = message.text
    if choice == "Фильм":
        await state.update_data(category="film", page=1)
        item = films[0]
        text = f"🎬 {item['title']}\n{item['description']}"
        kb = make_nav_keyboard(page=1, total=len(films), category="film")
        await message.answer_photo(
            photo=item["photo"],
            caption=text,
            reply_markup=kb
        )
    elif choice == "Сериал":
        await state.update_data(category="series", page=1)
        item = series[0]
        text = f"📺 {item['title']}\n{item['description']}"
        kb = make_nav_keyboard(page=1, total=len(series), category="series")
        await message.answer_photo(
            photo=item["photo"],
            caption=text,
            reply_markup=kb
        )
    await state.set_state(ShowState.showing)


@dp.callback_query(F.data.startswith("nav_"))
async def navigate(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split("_")
    if len(data) != 3:
        await callback.answer("Ошибка навигации.")
        return

    category, page_str = data[1], data[2]
    page = int(page_str)

    user_data = await state.get_data()
    if user_data.get("category") != category:
        await callback.answer("Вы переключились на другой раздел.")
        return

    items = films if category == "film" else series

    if 1 <= page <= len(items):
        item = items[page - 1]
        text = (f"🎬 {item['title']}\n{item['description']}"
                if category == "film"
                else f"📺 {item['title']}\n{item['description']}")
        kb = make_nav_keyboard(page=page, total=len(items), category=category)

        # Редактируем сообщение: меняем фото и подпись
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=item["photo"],
                caption=text
            ),
            reply_markup=kb
        )
        await state.update_data(page=page)
    else:
        await callback.answer("Такой страницы нет.")
    await callback.answer()


@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Выберите, что хотите посмотреть:",
        reply_markup=keyboard
    )
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
