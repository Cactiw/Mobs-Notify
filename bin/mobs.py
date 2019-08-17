"""
Здесь происходит обработка мобов
"""

from work_materials.globals import dispatcher, conn, mobs_queue, local_tz, moscow_tz

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import logging
import traceback
import re
import psycopg2
import datetime


def mobs_monitor():
    cursor = conn.cursor()
    data = mobs_queue.get()
    while data is not None:
        try:
            castle, text, player_id, forward_message_date = data.get("castle"), data.get("text"), data.get("telegram_id"), \
                                                            data.get("forward_date")
            forward_message_date = datetime.datetime.fromtimestamp(forward_message_date,
                                                                   tz=moscow_tz).replace(tzinfo=None)
            link = re.search("/fight_(.*)$", text)
            if link is None:
                logging.error("No link found: {}".format(data))
                return
            link = link.group(1)
            names, lvls, buffs = [], [], []
            for string in text.splitlines():
                parse = re.search("(.+) lvl\\.(\\d+)", string)
                if parse is not None:
                    name = parse.group(1)
                    lvl = int(parse.group(2))
                    names.append(name)
                    lvls.append(lvl)
                    buffs.append("")
                else:
                    parse = re.search("  ╰ (.+)", string)
                    if parse is not None:
                        buff = parse.group(1)
                        buffs.pop()
                        buffs.append(buff)
            request = "insert into mobs(link, castle, mob_names, mob_lvls, date_created, created_player, buffs) " \
                      "values (%s, %s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(request, (link, castle, names, lvls, forward_message_date, player_id, buffs))
            except psycopg2.IntegrityError:
                logging.error("Repeating notification for data: {}".format(data))
                return
            response, buttons, avg_lvl = get_mobs_text_and_buttons(link, castle, names, lvls, forward_message_date,
                                                                   buffs)
            request = "select id from players where active = true and castle = %s and %s between lvl_min and lvl_max"
            cursor.execute(request, (castle, avg_lvl))
            rows = cursor.fetchall()
            count = 0
            for row in rows:
                dispatcher.bot.send_message(chat_id=row[0], text=response, parse_mode='HTML', reply_markup=buttons)
                count += 1
            logging.info("Sent {} notifications".format(count))
        except Exception:
            logging.error(traceback.format_exc())

        data = mobs_queue.get()


def get_mobs_text_and_buttons(link, castle, mobs, lvls, forward_message_date, buffs):
    response = "{} Обнаруженные мобы:\n".format(castle)
    avg_lvl = 0
    for i, name in enumerate(mobs):
        lvl = lvls[i]
        avg_lvl += lvl
        response += "<b>{}</b> 🏅: <code>{}</code>\n{}".format(name, lvl, "  ╰ {}\n".format(buffs[i]) if buffs[i] != ""
                                                              else "")
    avg_lvl /= len(lvls)

    now = datetime.datetime.now(tz=moscow_tz).replace(tzinfo=None)
    remaining_time = datetime.timedelta(minutes=3) - (now - forward_message_date)
    response += "\nСредний уровень: {}\n".format(avg_lvl)
    if remaining_time < datetime.timedelta(0):
        response += "\nВремени не осталось!"
    else:
        response += "\nОсталось: <b>{}</b>".format("{:02d}:{:02d}".format(int(remaining_time.total_seconds() // 60),
                                                                          int(remaining_time.total_seconds() % 60)))
    buttons = [[InlineKeyboardButton(text="⚔ {}-{}🏅".format(int(avg_lvl - 5), int(avg_lvl + 5)),
                                     url=u"https://t.me/share/url?url=/fight_{}".format(link)),
                ]]
    return [response, InlineKeyboardMarkup(buttons), avg_lvl]
