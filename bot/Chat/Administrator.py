import string

from bot.Chat.ChatHistory import ChatHistory
class Administrator:
    def __init__(self, info):
        self.info = info
        self.is_admin = True
        self.chat_history = []
        self.new_messages = []
        self.selected_user = None

    def new_message_from_user(self, message: string, sender):
        chat_message = ChatHistory(message=message, sender=sender, receiver=self)
        self.new_messages.append(chat_message)

    def send_message(self, message: string, to_user):
        chat_message = ChatHistory(message=message, sender=self, receiver=to_user)
        for m in self.new_messages:
            self.chat_history.append(m)
        self.new_messages = []
        self.chat_history.append(chat_message)

    def chat_with_user(self) -> string:
        old_messages = list(filter(lambda x: x.sender.info.id == self.selected_user.info.id or x.sender == self, self.chat_history))
        new_messages = list(filter(lambda x: x.sender.info.id == self.selected_user.info.id or x.sender == self, self.new_messages))
        result = ""
        for message in old_messages + new_messages:
            result += message.formatted(sender_is_me=message.sender == self, respond="Сообщение от")
            result += "\n\n"

        return result

    def show_new_messages(self) -> string:
        new_messages = list(filter(lambda x: x.sender.info.id == self.selected_user.info.id or x.sender == self, self.new_messages))
        result = ""
        for message in new_messages:
            self.chat_history.append(message)
            result += message.formatted(sender_is_me=message.sender == self, respond="Сообщение от")
            result += "\n\n"
        self.new_messages = []

        return result

    def all_chatmates(self):
        old_messages = list(map(lambda x: x.sender.info.first_name, self.chat_history))
        new_messages = list(map(lambda x: x.sender.info.first_name, self.new_messages))
        return list(set(old_messages + new_messages))

    def new_chatmates(self):
        new_messages = list(map(lambda x: x.sender, self.new_messages))
        return list(set(new_messages))
    def all_chatmates(self):
        new_messages = list(map(lambda x: x.sender, self.new_messages + self.chat_history))
        return list(set(new_messages))
    def select_user(self, user):
        self.selected_user = user

    def unselect_user(self):
        self.selected_user = None