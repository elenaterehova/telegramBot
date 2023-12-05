# Класс ChatHistory
# Назначение: хранит информацию о сообщении
# Поля:
#   – message: сообщения
#   – sender: отправитель
#   – reveiver: получатель

import string


class ChatHistory:
    def __init__(self, message, sender, receiver):
        self.message = message
        self.sender = sender
        self.receiver = receiver

    def formatted(self, sender_is_me: bool, respond="Отвечает") -> string:
        result = ""

        if sender_is_me:
            result += "Вы:\n"
        else:
            result += f"{respond} {self.sender.info.first_name}:\n"

        result += self.message
        return result
