"""
Здесь находятся все основные callback-функции
"""

from bin.buttons import get_general_buttons

from work_materials.globals import cursor

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

import re
import psycopg2


def start(bot, update, user_data):
    buttons = [
        [
            KeyboardButton(text='🖤'),
            KeyboardButton(text='🐢'),
        ],
        [
            KeyboardButton(text='🦇'),
            KeyboardButton(text='☘'),
        ],
        [
            KeyboardButton(text='🍆'),
            KeyboardButton(text='🌹'),
            KeyboardButton(text='🍁'),
        ],
    ]
    user_data.update({"status": "selecting_castle"})
    bot.send_message(chat_id=update.message.chat_id,
                     text="Здравствуйте!\nВыберите замок, мобов из которого необходимо присылать.\n\n"
                          "<em>Обратите внимание, на текущий момент бот работает только для Скалы и Тортуги.</em>",
                     parse_mode='HTML',
                     reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))


def selected_castle(bot, update, user_data):
    mes = update.message
    user_data.update({"castle": mes.text, "status": "selecting_lvls"})
    bot.send_message(chat_id=mes.chat_id, text="Замок сохранён.\n"
                                               "Введите диапазон уровней получаемых мобов\n(синтаксис: MIN-MAX):",
                     reply_markup=ReplyKeyboardRemove())


def selected_lvls(bot, update, user_data):
    mes = update.message
    castle = user_data.get("castle")
    parse = re.search("(\\d+)[-: /\\\\](\\d+)", mes.text)
    if parse is None:
        bot.send_message(chat_id=mes.chat_id, text="Неверный синтаксис.\nПример: 15-25")
        return
    lvl_min = int(parse.group(1))
    lvl_max = int(parse.group(2))
    reply_markup = get_general_buttons(user_data)
    request = "insert into players(id, username, castle, lvl_min, lvl_max) values (%s, %s, %s, %s, %s)"
    try:
        cursor.execute(request, (mes.from_user.id, mes.from_user.username, castle, lvl_min, lvl_max))
        bot.send_message(chat_id=mes.chat_id, text="Успешно сохранено! Вы подписались на рассылку.",
                         reply_markup=reply_markup)
    except psycopg2.IntegrityError:
        request = "update players set username = %s, castle = %s, lvl_min = %s, lvl_max = %s where id = %s"
        cursor.execute(request, (mes.from_user.username, castle, lvl_min, lvl_max, mes.from_user.id))
        bot.send_message(chat_id=mes.chat_id, text="Данные обновлены.", reply_markup=reply_markup)
    user_data.pop("status")


def info(bot, update):
    mes = update.message
    pass




