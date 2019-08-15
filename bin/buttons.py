"""
Здесь находится большинство функций по работе с кнопками
"""

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


def get_general_buttons(user_data):
    buttons = [
        [
            KeyboardButton("ℹ️ Инфо")
        ]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


