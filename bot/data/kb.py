from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from Storage import storage_class
import text as strings
from bot.Chat.User import User
from bot.Chat.Administrator import Administrator

keyboard1 = [
    [KeyboardButton(text=strings.get_instruction)],
    [KeyboardButton(text=strings.get_help1)],
]

categories = storage_class.getCategories()
categories2 = [[KeyboardButton(text=item)]for item in categories]
categories2.append([KeyboardButton(text='⏪ Выйти назад')])
categories2.append([KeyboardButton(text=strings.get_help1)])


keyboard1 = ReplyKeyboardMarkup(keyboard=keyboard1, resize_keyboard=True)
categories2 = ReplyKeyboardMarkup(keyboard=categories2, resize_keyboard=True)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='◀️ Выйти в меню')]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='◀️ Выйти в меню', callback_data='menu')]])

def admin_users_list_keyboard(users: [User], admin: Administrator, switch_button: InlineKeyboardButton) -> InlineKeyboardMarkup:
    keyboard_buttons = []
    for user in users:
        button = [InlineKeyboardButton(text=user.info.first_name + ' ' + user.info.last_name, callback_data=f"chatmate chat_id={user.info.id};admin_id={admin.info.id}")]
        keyboard_buttons.append(button)
    keyboard_buttons.append([switch_button])
    exit_button = [InlineKeyboardButton(text="Назад", callback_data="unselect_user")]
    keyboard_buttons.append(exit_button)
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

def admin_chat_with_user_keyboard() -> InlineKeyboardMarkup:
    keyboard_buttons = []
    chat_history_button = [InlineKeyboardButton(text="Показать всю переписку", callback_data="chat_history")]
    back_button = [InlineKeyboardButton(text="Назад", callback_data="unselect_user")]
    return InlineKeyboardMarkup(inline_keyboard=[chat_history_button, back_button])

def user_show_message() -> InlineKeyboardMarkup:
    show_button = [InlineKeyboardButton(text="Показать", callback_data="user_show_new_message")]
    return InlineKeyboardMarkup(inline_keyboard=[show_button])