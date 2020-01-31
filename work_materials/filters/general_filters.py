"""
В этом модуле содержатся общие фильтры для бота
"""

from telegram.ext import BaseFilter
from telegram import Update

from work_materials.globals import CHAT_WARS_ID


class FilterIsChatWarsForward(BaseFilter):
    def filter(self, message):
        if isinstance(message, Update):
            message = message.message
        return message.forward_from is not None and message.forward_from.id == CHAT_WARS_ID


filter_is_chat_wars_forward = FilterIsChatWarsForward()
filter_is_chat_wars_forward.update_filter = True


class FilterIsPM(BaseFilter):
    def filter(self, message):
        if isinstance(message, Update):
            message = message.message
        if message.from_user is None:
            return False
        return message.chat_id == message.from_user.id


filter_is_pm = FilterIsPM()
filter_is_pm.update_filter = True

