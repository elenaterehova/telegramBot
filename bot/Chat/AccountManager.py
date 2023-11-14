from typing import Optional

from bot.Chat.User import User
from bot.Chat.Administrator import Administrator

class AccountManager:
    def __init__(self):
        self.users = []
        self.admins = []

    def add_user(self, user: User):
        # Если пользователь уже есть
        if len(list(filter(lambda x: x.info.id != user.info.id, self.users))) > 0:
            return

        # # Если это админ
        # if len(list(filter(lambda x: x.info.id != user.info.id, self.admins))) > 0:
        #     return
        self.users.append(user)

    def admins_contains_id(self, user_id) -> bool:
        return len(list(filter(lambda x: user_id == x.info.id, self.admins))) > 0
    def add_admin(self, admin: Administrator):
        # Если админ уже есть
        if len(list(filter(lambda x: x.info.id != user.info.id, self.admins))) > 0:
            return

        self.admins.append(admin)

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

    def get_user(self, info) -> Optional[User]:
        users = list(filter(lambda x: info.id == x.info.id, self.users))
        if len(users) > 0:
            return users[0]
        return None