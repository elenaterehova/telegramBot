from bot.Chat.User import User
class Formatter:
    @classmethod
    def new_messages_count(cls, count):
        if count % 10 == 1 and count != 11:
            return f"У вас {count} новое сообщение"
        if count % 10 in range(2, 5) and count not in range(10, 20):
            return f"У вас {count} новых сообщения"
        return f"У вас {count} новых сообщений"

    @classmethod
    def user_full_name(cls, user: User) -> str:
        result = ""
        if user.info.first_name is not None:
            result += user.info.first_name + " "
        if user.info.last_name is not None:
            result += user.info.last_name

        if user.info.username is not None:
            result += f" ({user.info.username})"
        return result