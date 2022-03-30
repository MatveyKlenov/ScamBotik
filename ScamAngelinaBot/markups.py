from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

MainPanel = ReplyKeyboardMarkup(row_width=1)
btnFAQ = KeyboardButton("FAQ(ЧАСТЫЕ ВОПРОСЫ)")
btnHotLine = KeyboardButton("СВЯЗЬ С ОПЕРАТОРОМ")
btnFlag1 = KeyboardButton("[❌]ВЫ НЕ В ОЧЕРЕДИ")
MainPanel.add(btnFAQ, btnHotLine, btnFlag1)

QuePanel = ReplyKeyboardMarkup(row_width=1)
btnExit = KeyboardButton("ВЫЙТИ ИЗ ОЧЕРЕДИ")
btnFlag2 = KeyboardButton("[✅]ВЫ В ОЧЕРЕДИ")
QuePanel.add(btnExit, btnFlag2)

HotLinePanel = ReplyKeyboardMarkup(row_width=1)
btnExitHotLine = KeyboardButton("ВЫЙТИ ИЗ ЧАТА")
btnFlag3 = KeyboardButton("[✅]ВЫ В ЧАТЕ")
HotLinePanel.add(btnExitHotLine, btnFlag3)

keyboard_arg = InlineKeyboardMarkup()
btnArgument = InlineKeyboardButton(text="ЗАКОН", url="https://telegra.ph/PODTVERZHDENIE-BEZOPASNOSTI-PERSONALNYH-DANNYH-03-29")
keyboard_arg.add(btnArgument)

"""
        if db1.set_que(message.from_user.id, "inchat"):
            if db2.get_active_chat(message.chat.id):
                chat_info = db2.get_active_chat(message.chat.id)
                await bot.send_message(chat_info[1], message.text)
"""