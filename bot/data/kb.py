from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from Storage import storage_class
import strings as strings
from bot.Chat.User import User
from bot.Chat.Administrator import Administrator
from bot.Chat.Formatter import Formatter

categories = storage_class.getCategories()


# -----USER KEYBOARDS-------------------------------------------------------------
def users_start_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=strings.get_instruction_button)],
        [KeyboardButton(text=strings.get_help_button)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def users_categories_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=item)] for item in categories]
    keyboard.append([KeyboardButton(text=strings.exit_button)])
    keyboard.append([KeyboardButton(text=strings.get_help_button)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def user_show_message() -> InlineKeyboardMarkup:
    show_button = [InlineKeyboardButton(text=strings.show_button, callback_data="user_show_new_message")]
    return InlineKeyboardMarkup(inline_keyboard=[show_button])


# -----ADMIN KEYBOARDS-------------------------------------------------------------
def admins_start_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=strings.get_instruction_button)],
        [KeyboardButton(text=strings.admins_list)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def admins_management_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=strings.add_admin)],
        [KeyboardButton(text=strings.delete_admin)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def admins_categories_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=item)] for item in categories]
    keyboard.append([KeyboardButton(text=strings.exit_button)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def admin_users_list_keyboard(users: [User], admin: Administrator,
                              switch_button: InlineKeyboardButton) -> InlineKeyboardMarkup:
    keyboard_buttons = []
    for user in users:
        if user is not admin:
            first_name = user.info.first_name
            last_name = user.info.last_name
            row = ""
            if first_name is not None:
                row += first_name
            if last_name is not None:
                row += " " + last_name
            if first_name is None and last_name is None:
                row = "Unknown"
            button = [InlineKeyboardButton(text=row,
                                           callback_data=f"chatmate chat_id={user.info.id};admin_id={admin.info.id}")]
            keyboard_buttons.append(button)
    keyboard_buttons.append([switch_button])
    exit_button = [InlineKeyboardButton(text=strings.back_button, callback_data="unselect_user")]
    keyboard_buttons.append(exit_button)
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def admin_chat_with_user_keyboard() -> InlineKeyboardMarkup:
    keyboard_buttons = []
    chat_history_button = [InlineKeyboardButton(text=strings.full_chat, callback_data="chat_history")]
    back_button = [InlineKeyboardButton(text=strings.back_button, callback_data="unselect_user")]
    return InlineKeyboardMarkup(inline_keyboard=[chat_history_button, back_button])


def add_admin_keyboard(users: [User]) -> InlineKeyboardMarkup:
    buttons = []
    for user in users:
        buttons.append([InlineKeyboardButton(text=Formatter.user_full_name(user),
                                             callback_data=f"add_administrator:{user.info.id}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def delete_admin_keyboard(admins: [Administrator]) -> InlineKeyboardMarkup:
    buttons = []
    for admin in admins:
        buttons.append([InlineKeyboardButton(text=Formatter.user_full_name(admin),
                                             callback_data=f"remove_administrator:{admin.info.id}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# -----GENERAL KEYBOARDS-------------------------------------------------------------
def back_button_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=strings.exit_button)]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
