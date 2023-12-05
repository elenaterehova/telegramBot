# Класс AccountManager
# Назначение: хранит информацию о всех пользователях бота
# Поля:
#   – users: массив пользователей User
#   – admins: массив администраторов Administrator
# Методы:
#   – add_user(self, user: User):
#       Добавление пользователя в систему
#
#   – admins_contains_id(self, user_id) -> bool:
#       Есть ли среди администраторов передаваемый id
#
#   – add_admin(self, admin: Administrator):
#       Добавление администратора
#
#   – is_admin(self, info) -> bool:
#   – is_user(self, info) -> bool:
#
#   – is_admin_with_adding(self, info) -> bool:
#       Проверка на администратора. Если это администратор, возвращается True.
#       Иначе добавится новый пользователь и вернётся False
#
#   – get_admin(self, info) -> Administrator:
#       Получить администратора по заданной информации
#   – get_user(self, info) -> Optional[User]:
#       Получить администратора по заданной информации

#   – get_admin_by_id(self, id) -> Optional[Administrator]:
#   – get_user_by_id(self, id) -> Optional[User]:

from typing import Optional
from aiogram.types import user
from bot.chat.User import User
from bot.chat.Administrator import Administrator

import difflib


def similarity(s1, s2):
    if s1 is None or type(s1) != str:
        return 0.0

    if s2 is None or type(s2) != str:
        return 0.0

    normalized1 = s1.lower()
    normalized2 = s2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()


class AccountManager:
    def __init__(self):
        self.users = []
        self.admins = []

    def add_user(self, user: User):
        # Если пользователь уже есть
        if len(list(filter(lambda x: x.info.id == user.info.id, self.users))) > 0:
            return

        # Если это админ
        if len(list(filter(lambda x: x.info.id == user.info.id, self.admins))) > 0:
            return
        self.users.append(user)

    def add_admin(self, admin: Administrator):
        # Если админ уже есть
        if len(list(filter(lambda x: x.info.id == admin.info.id, self.admins))) > 0:
            return
        self.admins.append(admin)
        self.users = list(filter(lambda x: x.info.id != admin.info.id, self.users))

    def admins_contains_id(self, user_id) -> bool:
        return len(list(filter(lambda x: user_id == x.info.id, self.admins))) > 0

    def is_admin(self, info) -> bool:
        return len(list(filter(lambda x: info.id == x.info.id, self.admins))) > 0

    def is_user(self, info) -> bool:
        return len(list(filter(lambda x: info.id == x.info.id, self.users))) > 0

    def is_admin_with_adding(self, info) -> bool:
        if self.is_admin(info=info):
            return True
        if not self.is_user(info=info):
            self.users.append(User(info=info))
        return False

    def get_admin(self, info) -> Administrator:
        return list(filter(lambda x: info.id == x.info.id, self.admins))[0]

    def get_user(self, info) -> Optional[User]:
        users = list(filter(lambda x: info.id == x.info.id, self.users))
        if len(users) > 0:
            return users[0]
        return None

    def get_admin_by_id(self, id) -> Optional[Administrator]:
        admins = list(filter(lambda x: id == x.info.id, self.admins))
        if len(admins) > 0:
            return admins[0]
        return None

    def get_user_by_id(self, id) -> Optional[User]:
        users = list(filter(lambda x: id == x.info.id, self.users))
        if len(users) > 0:
            return users[0]
        return None

    def find_users(self, query: str) -> [User]:
        by_username = list(filter(lambda x: similarity(str(x.info.username), query) > 0.85, self.users))

        if len(by_username) > 0:
            return by_username

        by_first_name = list(filter(lambda x: similarity(x.info.first_name, query) > 0.85, self.users))
        if len(by_first_name) > 0:
            return by_first_name

        by_last_name = list(filter(lambda x: similarity(x.info.last_name, query) > 0.85, self.users))
        if len(by_last_name) > 0:
            return by_last_name

        def full_name(user: User) -> str:
            result = ""
            if user.info.first_name is not None:
                result += user.info.first_name + " "
            if user.info.last_name is not None:
                result += user.info.last_name
            return result

        by_full_name = list(filter(lambda x: similarity(full_name(x), query) > 0.85, self.users))
        return by_full_name