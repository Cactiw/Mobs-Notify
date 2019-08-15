from telegram.ext import CommandHandler, MessageHandler, Filters

from bin.save_load_user_data import save_data, load_data
from bin.bot_callback import start, selected_castle, selected_lvls

from work_materials.filters.general_filters import filter_is_pm
from work_materials.filters.callback_filters import filter_select_castle, filter_select_lvls

from work_materials.globals import conn, updater, dispatcher, cursor

import work_materials.globals as file_globals

import threading


def bot_processing():

    dispatcher.add_handler(CommandHandler('start', start, filters=filter_is_pm, pass_user_data=True))
    dispatcher.add_handler(MessageHandler(Filters.text & filter_select_castle, selected_castle, pass_user_data=True))
    dispatcher.add_handler(MessageHandler(Filters.text & filter_select_lvls, selected_lvls, pass_user_data=True))

    load_data()

    processes = []

    save_user_data = threading.Thread(target=save_data, name="Save User Data", args=())
    save_user_data.start()
    processes.append(save_user_data)

    updater.start_polling(clean=False)
    updater.idle()
    conn.close()
    file_globals.processing = False

