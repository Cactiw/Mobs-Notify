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
                          "<em>Обратите внимание, на текущий момент бот работает для 🖤Скалы, 🐢Тортуги, 🦇Ночи и "
                          "(частично) ☘️Оплота.</em>",
                     parse_mode='HTML',
                     reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))


def selected_castle(bot, update, user_data):
    mes = update.message
    user_data.update({"castle": mes.text, "status": "selecting_lvls"})
    bot.send_message(chat_id=mes.chat_id,
                     text="Замок сохранён.\n\nВведите диапазон уровней получаемых мобов. От Вашего уровня примерно "
                          "+/-5 включительно. Так, например, если Ваш уровень 🏅<code>20</code>, "
                          "то <code>15</code>-<code>30</code>.\n\n"
                          "(синтаксис: MIN-MAX):",
                     reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')


def selected_lvls(bot, update, user_data):
    mes = update.message
    castle = user_data.get("castle")
    parse = re.search("(\\d+)[-: /\\\\](\\d+)", mes.text)
    if parse is None:
        bot.send_message(chat_id=mes.chat_id, text="Неверный синтаксис.\nПример: 15-25")
        return
    lvl_min = int(parse.group(1))
    lvl_max = int(parse.group(2))
    if lvl_min < 0 or lvl_max < lvl_min:
        bot.send_message(chat_id=mes.chat_id, text="Неверный синтаксис. Уровни должны быть положительными, "
                                                   "второе число не меньше первого ")
        return
    reply_markup = get_general_buttons(user_data)
    request = "insert into players(id, username, castle, lvl_min, lvl_max) values (%s, %s, %s, %s, %s)"
    try:
        cursor.execute(request, (mes.from_user.id, mes.from_user.username, castle, lvl_min, lvl_max))
        bot.send_message(chat_id=mes.chat_id,
                         text="Успешно сохранено! Вы подписались на рассылку.\n"
                              "Теперь вам будут приходить уведомления о мобах из {} со среднем уровнем в диапазоне "
                              "{} - {}".format(castle, lvl_min, lvl_max),
                         reply_markup=reply_markup)
    except psycopg2.IntegrityError:
        request = "update players set username = %s, castle = %s, lvl_min = %s, lvl_max = %s where id = %s"
        cursor.execute(request, (mes.from_user.username, castle, lvl_min, lvl_max, mes.from_user.id))
        bot.send_message(chat_id=mes.chat_id, text="Данные обновлены.", reply_markup=reply_markup)
    user_data.pop("status")


def info(bot, update):
    mes = update.message
    response = "ℹ️ Инфо:\n"
    request = "select castle, lvl_min, lvl_max, active from players where id = %s limit 1"
    cursor.execute(request, (mes.from_user.id,))
    row = cursor.fetchone()
    if row is None:
        bot.send_message(chat_id=mes.chat_id, text="Произошла ошибка. Попробуйте начать снова (/start)")
        return
    castle, lvl_min, lvl_max, active = row
    response += "💬Статус: <b>{}</b>\n".format("✅ Активно" if active else "❌ Отключено")
    response += "🏰Замок: {}\n".format(castle)
    response += "🏅Диапазон уровней: <b>{}</b> - <b>{}</b>\n".format(lvl_min, lvl_max)
    response += "\n↔️Изменить данные: /start\n"
    response += "🔺Включить: /on\n" if not active else "🔻Отключить: /off"
    bot.send_message(chat_id=mes.chat_id, text=response, parse_mode='HTML')


def change_status(bot, update):
    mes = update.message
    set_active = 'on' in mes.text
    request = "update players set active = %s where id = %s"
    cursor.execute(request, (set_active, mes.from_user.id))
    if set_active:
        response = "Готово! Вы снова будете получать уведомления."
    else:
        response = "Готово. Вы не будете больше получать уведомления.\n" \
                   "Снова включить: /on"
    bot.send_message(chat_id=mes.chat_id, text=response)
