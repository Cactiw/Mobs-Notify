"""
Здесь находится большинство фильтров к callback функциям
"""

from telegram.ext import BaseFilter

from work_materials.globals import dispatcher, castles
from work_materials.filters.general_filters import filter_is_pm


class FilterSelectCastle(BaseFilter):
    def filter(self, message):
        user_data = dispatcher.user_data.get(message.from_user.id)
        if user_data is None:
            return False
        return filter_is_pm(message) and message.text in castles and \
            user_data.get("status") == 'selecting_castle'


filter_select_castle = FilterSelectCastle()


class FilterSelectLvls(BaseFilter):
    def filter(self, message):
        user_data = dispatcher.user_data.get(message.from_user.id)
        if user_data is None:
            return False
        return filter_is_pm(message) and user_data.get("status") == 'selecting_lvls'


filter_select_lvls = FilterSelectLvls()
