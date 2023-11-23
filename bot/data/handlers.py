import io
import re

import requests
from aiogram import types, F, Router, flags, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, message, KeyboardButton, ReplyKeyboardMarkup, FSInputFile, \
    InputMediaPhoto, URLInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter, state
from aiogram.fsm.context import FSMContext
from urllib.request import urlretrieve
from PIL import Image
import kb
import text as strings
import Storage
from bot.data import text
from bot.data.Storage import storage_class

router = Router()

from bot.Chat.AccountManager import AccountManager
from bot.Chat.User import User
from bot.Chat.Administrator import Administrator
from bot.Chat.Formatter import Formatter
from bot.data.Handlers.AdminsManagement import *

manager = AccountManager()

# Состояния пользователя
class GetProductInfo(StatesGroup):
    choosing_act = State()
    choosing_act_admin = State()
    choosing_category = State()
    choosing_product_name = State()
    get_help = State()
    add_or_delete_admin = State()
    add_admin = State()
    delete_admin = State()


# admin = Administrator(info=1302324252)
# add_main_admin = manager.add_admin(admin=admin)863813900

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    if not manager.is_user(info=message.from_user):
        manager.add_user(user=User(info=message.from_user))

    if message.from_user.id == 1302324252:
        manager.add_admin(admin=Administrator(info=message.from_user))

    # if not manager.is_admin(info=manager.get_user_by_id(int(1302324252)).info):
    #     manager.add_admin(admin=Administrator(info=manager.get_user_by_id(int(1302324252)).info))

    if manager.is_admin(info=message.from_user):
        await message.answer(text=text.greet.format(name=message.from_user.full_name),
                             reply_markup=kb.keyboard1_admin)
        await state.set_state(GetProductInfo.choosing_act_admin)
    else:
        await message.answer(
            text=text.greet.format(name=message.from_user.full_name),
            reply_markup=kb.keyboard1
        )
        await state.set_state(GetProductInfo.choosing_act)


@router.message(Command("help"))
async def help_command(message: Message, state: FSMContext):
    if manager.is_admin(info=message.from_user):
        await message.answer(text='Вы Администратор. Команда реализована только для пользователей.')
    else:
        await message.answer(text=text.get_help,
                             reply_markup=kb.help_keyboard)
        await state.set_state(GetProductInfo.get_help)


@router.message(GetProductInfo.choosing_act_admin)
async def admin_act_chosen(message: Message, state: FSMContext):
    if message.text == strings.get_instruction:
        await message.answer(text=text.get_category, reply_markup=kb.categories2_admin)
        await state.set_state(GetProductInfo.choosing_category)

    if message.text == strings.admins_list:
        admins_names = ''
        for admin in manager.admins:
            admins_names += admin.info.full_name + "\n"
        await message.answer(text=f'Список Администраторов:\n\n{admins_names}',
                             reply_markup=kb.keyboard2_admin)
        await state.set_state(GetProductInfo.add_or_delete_admin)

@router.message(GetProductInfo.add_or_delete_admin)
async def add_or_delete(message: Message, bot: Bot, state: FSMContext):
    if message.text == strings.add_admin:
        await message.answer(text='Введите ID или имя пользователя, которого хотите добавить в список Администраторов:',
                             reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(GetProductInfo.add_admin)
    if message.text == strings.delete_admin:
        await message.answer(text='.', reply_markup=types.ReplyKeyboardRemove())
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
        await message.answer(text='Список администраторов',
                             reply_markup=kb.delete_admin_keyboard(admins=manager.admins))
        await state.set_state(GetProductInfo.delete_admin)
#
# @router.message(GetProductInfo.add_admin)
# async def added_admin_id(message: Message, bot: Bot, state: FSMContext):
#     try:
#         if manager.is_admin(info=manager.get_user_by_id(id=int(message.text)).info):
#             await message.answer(text='Пользователь уже является Администратором.')
#             admins_names = ''
#             for admin in manager.admins:
#                 admins_names += admin.info.full_name
#             await message.answer(text=f'Список Администраторов:\n\n{admins_names}',
#                                  reply_markup=kb.keyboard1_admin)
#             await state.set_state(GetProductInfo.choosing_act_admin)
#         else:
#             manager.add_admin(admin=Administrator(info=manager.get_user_by_id(id=int(message.text)).info))
#             await message.answer(text='Пользователь добавлен в Администраторы.')
#             admins_names = ''
#             for admin in manager.admins:
#                 admins_names += admin.info.full_name
#             await message.answer(text=f'Список Администраторов:\n\n{admins_names}',
#                                  reply_markup=kb.keyboard1_admin)
#             await state.set_state(GetProductInfo.choosing_act_admin)
#     except Exception as e:
#         await message.answer(text='Пользователь не найден')
#         print(e)
#         print(message.text)
#     await state.clear()

#@router.message(GetProductInfo.delete_admin)
#async def added_admin_id_delete(message: Message, bot: Bot, state: FSMContext):
 #   id = int(message.text)
  #  manager.admins.remove(manager.get_admin_by_id(id=id))
   # await message.answer(text='Администратор удален.')
    #admins_names = ''
    #for admin in manager.admins:
     #   admins_names += admin.info.full_name
    #await message.answer(text=f'Список Администраторов:\n\n{admins_names}',
     #                    reply_markup=kb.keyboard1_admin)
    #await state.set_state(GetProductInfo.choosing_act_admin)

@router.message(GetProductInfo.get_help, F.text == '⏪ Выйти назад')
async def back(message: Message, state: FSMContext):
    if message.text == '⏪ Выйти назад':
        await message.answer(text=text.greet.format(name=message.from_user.full_name),
                             reply_markup=kb.keyboard1)
        await state.set_state(GetProductInfo.choosing_act)


# Пользователь выбирает действие (state: choosing_act)
@router.message(GetProductInfo.choosing_act)
async def act_chosen(message: Message, state: FSMContext):
    if message.text == strings.get_instruction:
        await message.answer(text=text.get_category, reply_markup=kb.categories2)
        await state.set_state(GetProductInfo.choosing_category)

    if message.text == strings.get_help1:
        # await message.answer(text.get_help, reply_markup=kb.help_keyboard)
        await message.answer(text.get_help, reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(GetProductInfo.get_help)

@router.message(GetProductInfo.choosing_category, F.text == strings.exit_button)
async def back_from_categories(message: Message, bot: Bot, state: FSMContext):
    if manager.is_admin(info=message.from_user):
        await message.answer(text=text.greet.format(name=message.from_user.full_name),
                             reply_markup=kb.keyboard1_admin)
        await state.set_state(GetProductInfo.choosing_act_admin)
    else:
        await message.answer(text=text.greet.format(name=message.from_user.full_name),
                             reply_markup=kb.keyboard1)
        await state.set_state(GetProductInfo.choosing_act)

@router.message(GetProductInfo.get_help, F.text == strings.exit_button)
async def back(message: Message, state: FSMContext):
    if message.text == strings.exit_button:
        await message.answer(text=text.greet.format(name=message.from_user.full_name),
                             reply_markup=kb.keyboard1)
        await state.set_state(GetProductInfo.choosing_act)


# Пользователь выбирает категорию (state: choosing_category)
@router.message(GetProductInfo.choosing_category, F.text.in_(kb.categories))
async def category_chosen(message: Message, state: FSMContext):
    names = Storage.storage_class.getNames(message.text)
    names2 = [[KeyboardButton(text=item)] for item in names]
    names2.append([KeyboardButton(text=strings.exit_button)])
    if manager.is_admin(info=manager.get_user_by_id(id=int(message.from_user.id)).info):
        await message.answer(text=strings.select_product_name1, reply_markup=ReplyKeyboardMarkup(keyboard=names2, resize_keyboard=True))
        await state.set_state(GetProductInfo.choosing_product_name)
    else:
        names2.append([KeyboardButton(text=strings.get_help1)])
        await message.answer(text=strings.select_product_name1, reply_markup=ReplyKeyboardMarkup(keyboard=names2, resize_keyboard=True))
        await state.set_state(GetProductInfo.choosing_product_name)


@router.message(GetProductInfo.choosing_category, F.text == strings.exit_button)
async def back(message: Message, state: FSMContext):
    if message.text == strings.exit_button:
        await message.answer(text=text.greet.format(name=message.from_user.full_name),
                             reply_markup=kb.keyboard1)
        await state.set_state(GetProductInfo.choosing_act)


@router.message(GetProductInfo.choosing_category, F.text == strings.get_help1)
async def help(message: Message, state: FSMContext):
    if message.text == strings.get_help1:
        await message.answer(text=text.get_help,
                             reply_markup=kb.help_keyboard)
        await state.set_state(GetProductInfo.get_help)


@router.message(StateFilter(GetProductInfo.choosing_category))
async def category_chosen_incorrectly(message: Message):
    await message.answer(
        text=strings.category_doesnot_find,
        reply_markup=kb.categories2
    )


# Пользователь выбирает название товара (state: choosing_product_name)
@router.message(GetProductInfo.choosing_product_name, F.text == strings.exit_button)
async def back(message: Message, state: FSMContext):
    if message.text == strings.exit_button:
        if manager.is_admin(info=message.from_user):
            await message.answer(text=text.get_category, reply_markup=kb.categories2_admin)
            await state.set_state(GetProductInfo.choosing_category)
        else:
            await message.answer(text=text.get_category, reply_markup=kb.categories2)
            await state.set_state(GetProductInfo.choosing_category)


@router.message(GetProductInfo.choosing_product_name, F.text == strings.get_help1)
async def help(message: Message, state: FSMContext):
    if message.text == strings.get_help1:
        await message.answer(text=text.get_help, reply_markup=kb.help_keyboard)
        await state.set_state(GetProductInfo.get_help)


@router.message(GetProductInfo.choosing_product_name)
async def product_name_chosen(message: Message, state: FSMContext, bot: Bot):
    try:
        await message.answer(text=strings.loading_instruction)
        photo = Storage.storage_class.getProductByName(message.text)
        if manager.is_admin(info=message.from_user):
            await bot.send_photo(message.chat.id, photo=photo, reply_markup=kb.keyboard1_admin)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
            await state.set_state(GetProductInfo.choosing_act_admin)
        else:
            await bot.send_photo(message.chat.id, photo=photo, reply_markup=kb.keyboard1)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
            await state.set_state(GetProductInfo.choosing_act)
    except Exception as e:
        await bot.send_message(chat_id=message.chat.id, text='Товар не найден. Попробуйте снова.')
        print(e)


@router.message(StateFilter(GetProductInfo.choosing_product_name))
async def product_name_chosen_incorrectly(message: Message, state: FSMContext):
    await message.answer(
        text=strings.product_doesnot_find
    )
    await state.set_state(GetProductInfo.choosing_category)
    await message.answer(text=strings.select_product_name2, reply_markup=kb.categories2)


@router.message(F.text, StateFilter(GetProductInfo.get_help))
async def get_help(message: Message, bot: Bot, state: FSMContext):
    """Помощь от консультанта"""
    if message.text == strings.get_help1:
        user = manager.get_user(info=message.from_user)
        if user is None:
            user = User(info=message.from_user)
            manager.add_user(user=user)

        # Почему-то выбивыет None
        manager.get_user_by_id(id=message.from_user.id).in_chat = True
        await message.answer(strings.get_help, reply_markup=types.ReplyKeyboardRemove())
        return


    if manager.is_admin_with_adding(info=message.from_user):
        # Сообщение от админа
        admin = manager.get_admin(info=message.from_user)
        if admin.selected_user is None:
            print('user is None')
            return

        if len(admin.new_messages) > 0:
            chatmates = admin.new_chatmates()
            switch_button = InlineKeyboardButton(text=strings.all_chats, callback_data="all_chatmates")
        else:
            chatmates = admin.all_chatmates()
            switch_button = InlineKeyboardButton(text=strings.new_messages, callback_data="new_messages")

        reply = kb.admin_users_list_keyboard(users=chatmates, admin=admin, switch_button=switch_button)
        await message.answer(text=strings.message_has_send_to_user, reply_markup=reply)
        user = admin.selected_user
        admin.send_message(message=message.text, to_user=user)
        user.new_message_from_admin(message=message.text, sender=admin)
        await bot.send_message(chat_id=user.info.id, text=Formatter.new_messages_count(len(user.new_messages)),
                               reply_markup=kb.user_show_message())
        await state.clear()
    else:
        # Сообщение от юзверя
        user = manager.get_user(info=message.from_user)
        if user is None or not user.in_chat:
            return

        for admin in manager.admins:
            user.send_message(message=message.text, to_admin=admin)
            admin.new_message_from_user(message=message.text, sender=user)
            button = [InlineKeyboardButton(text=strings.show_button, callback_data="new_messages")]
            await bot.send_message(chat_id=admin.info.id, text=Formatter.new_messages_count(len(admin.new_messages)),
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=[button]))
        await message.answer(text=strings.message_has_send_to_admin, reply_markup=kb.keyboard1)
        await state.set_state(GetProductInfo.choosing_act)


@router.callback_query(F.data == 'help')
async def get_help(callback_query: types.CallbackQuery, bot: Bot):
    user = manager.get_user(info=callback_query.from_user)
    if user is None:
        user = User(info=callback_query.from_user)
        manager.add_user(user=user)
    user.in_chat = True
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, strings.get_help)


@router.callback_query(F.data == "new_messages")
async def get_new_messages_list(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    admin = manager.get_admin_by_id(id=callback_query.from_user.id)
    if admin is None:
        return
    users = admin.new_chatmates()
    switch_button = InlineKeyboardButton(text=strings.all_chats, callback_data="all_chatmates")
    keyboard = kb.admin_users_list_keyboard(users=users, admin=admin, switch_button=switch_button)

    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id=admin.info.id, message_id=message_id)
    await bot.send_message(chat_id=admin.info.id, text=strings.new_messages, reply_markup=keyboard)

    if manager.is_admin(info=callback_query.from_user):
        await state.set_state(GetProductInfo.get_help)
    else:
        await state.clear()

@router.callback_query(F.data == "all_chatmates")
async def get_all_chatmates(callback_query: types.CallbackQuery, bot: Bot):
    admin = manager.get_admin_by_id(id=callback_query.from_user.id)
    if admin is None:
        return
    users = admin.all_chatmates()
    switch_button = InlineKeyboardButton(text=strings.only_new_messages, callback_data="new_messages")
    keyboard = kb.admin_users_list_keyboard(users=users, admin=admin, switch_button=switch_button)

    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id=admin.info.id, message_id=message_id)
    await bot.send_message(chat_id=admin.info.id, text=strings.all_chats, reply_markup=keyboard)


@router.callback_query(F.data.contains("chatmate"))
async def select_user(callback_query: types.CallbackQuery, bot: Bot):
    admin = manager.get_admin_by_id(id=callback_query.from_user.id)
    user = manager.get_user_by_id(id=int(callback_query.data.split(";")[0].split("=")[1]))
    if admin is None or user is None:
        print("no user or admin")
        return
    admin.select_user(user=user)
    new_messages = admin.show_new_messages()

    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id=admin.info.id, message_id=message_id)

    if len(new_messages) > 0:
        await bot.send_message(chat_id=admin.info.id, text=new_messages,
                               reply_markup=kb.admin_chat_with_user_keyboard())
        return
    chat_history = admin.chat_with_user()
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=strings.back_button, callback_data="unselect_user")]])
    await bot.send_message(chat_id=admin.info.id, text=chat_history, reply_markup=reply_markup)


@router.callback_query(F.data == "unselect_user")
async def unselect_user(callback_query: types.CallbackQuery, bot: Bot):
    admin = manager.get_admin_by_id(id=callback_query.from_user.id)
    if admin is None:
        return
    admin.unselect_user()
    if len(admin.new_messages) > 0:
        await get_new_messages_list(callback_query=callback_query, bot=bot)
    else:
        await get_all_chatmates(callback_query=callback_query, bot=bot)


@router.callback_query(F.data.contains("chat_history"))
async def get_new_messages_list(callback_query: types.CallbackQuery, bot: Bot):
    admin = manager.get_admin_by_id(id=callback_query.from_user.id)
    if admin is None:
        return

    chat_history = admin.chat_with_user()

    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id=admin.info.id, message_id=message_id)
    await bot.send_message(chat_id=admin.info.id, text=chat_history, reply_markup=kb.admin_chat_with_user_keyboard())


@router.callback_query(F.data == "user_show_new_message")
async def user_show_new_message(callback_query: types.CallbackQuery, bot: Bot):
    user = manager.get_user_by_id(id=callback_query.from_user.id)
    if user is None:
        return
    chat_history = user.chat_with_admin()

    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id=user.info.id, message_id=message_id)
    await bot.send_message(chat_id=user.info.id, text=chat_history)
