import string
from bot.Chat.ChatHistory import ChatHistory

class User:
    def __init__(self, info):
        self.info = info
        self.is_admin = False
        self.chat_history = []
        self.new_messages = []
        self.in_chat = False

    def new_message_from_admin(self, message: string, sender):
        chat_message = ChatHistory(message=message, sender=sender, receiver=self)
        self.new_messages.append(chat_message)

    def send_message(self, message: string, to_admin):
        chat_message = ChatHistory(message=message, sender=self, receiver=to_admin)
        for m in self.new_messages:
            self.chat_history.append(m)
        self.new_messages = []
        self.chat_history.append(chat_message)

    def chat_with_admin(self) -> string:
        # old_messages = list(filter(lambda x: x.sender.info.id == user_id or x.sender == self, self.chat_history))
        # new_messages = list(filter(lambda x: x.sender.info.id == user_id or x.sender == self, self.new_messages))
        old_messages = self.chat_history
        new_messages = self.new_messages
        result = ""
        for message in old_messages + new_messages:
            result += message.formatted(sender_is_me=message.sender == self)
            result += "\n\n"

        return result

    def show_new_messages(self, admin_id) -> string:
        new_messages = list(filter(lambda x: x.sender.info.id == admin_id or x.sender == self, self.new_messages))
        result = ""
        for message in new_messages:
            self.chat_history.append(message)
            result += message.formatted(sender_is_me=message.sender == self)
            result += "\n\n"
        self.new_messages = []

        return result