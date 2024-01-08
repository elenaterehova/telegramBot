import asyncio
import logging

from aiogram import F, Bot, Router
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message
from aiogram.filters import Command, StateFilter
from bot.storage.Storage import storage_class
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.chat.User import User
from bot.chat.Administrator import Administrator
from bot.chat.AccountManager import AccountManager
from bot.strings import strings
from bot.keyboards import kb


router = Router()
main_admin_id = 1302324252
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


states = GetProductInfo()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    global main_admin_id
    if not manager.is_user(info=message.from_user):
        manager.add_user(user=User(info=message.from_user))

    # if message.from_user.id == 1302324252:
    if main_admin_id is not None and message.from_user.id == main_admin_id:
        manager.add_admin(admin=Administrator(info=message.from_user))

    # if not manager.is_admin(info=manager.get_user_by_id(int(1302324252)).info):
    #     manager.add_admin(admin=Administrator(info=manager.get_user_by_id(int(1302324252)).info))

    if manager.is_admin(info=message.from_user):
        await message.answer(text=strings.greet.format(name=message.from_user.full_name),
                             reply_markup=kb.admins_start_keyboard())
        await state.set_state(states.choosing_act_admin)
    else:
        await message.answer(
            text=strings.greet.format(name=message.from_user.full_name),
            reply_markup=kb.users_start_keyboard()
        )
        await state.set_state(states.choosing_act)


@router.message(Command("help"))
async def help_command(message: Message, state: FSMContext):
    if manager.is_admin(info=message.from_user):
        await message.answer(text='Вы Администратор. Команда реализована только для пользователей.')
    else:
        await message.answer(text=strings.get_help,
                             reply_markup=kb.back_button_keyboard())
        await state.set_state(states.get_help)


# Выйти из списка категорий
@router.message(states.choosing_category, F.text == strings.exit_button)
async def back_from_categories(message: Message, state: FSMContext):
    if manager.is_admin(info=message.from_user):
        await message.answer(text=strings.greet.format(name=message.from_user.full_name),
                             reply_markup=kb.admins_start_keyboard())
        await state.set_state(states.choosing_act_admin)
    else:
        await message.answer(text=strings.greet.format(name=message.from_user.full_name),
                             reply_markup=kb.users_start_keyboard())
        await state.set_state(states.choosing_act)


# Пользователь или Администратор выбирает категорию (state: choosing_category)
@router.message(states.choosing_category, F.text.in_(storage_class.getCategories()))
async def category_chosen(message: Message, state: FSMContext):
    names = storage_class.getNames(message.text)
    names2 = [[KeyboardButton(text=item)] for item in names]
    names2.append([KeyboardButton(text=strings.exit_button)])

    # if manager.is_admin(info=manager.get_user_by_id(id=int(message.from_user.id)).info):
    if manager.is_admin(info=message.from_user):
        await message.answer(text=strings.select_product_name1,
                             reply_markup=ReplyKeyboardMarkup(keyboard=names2, resize_keyboard=True))
        await state.set_state(states.choosing_product_name)
    else:
        names2.append([KeyboardButton(text=strings.get_help_button)])
        await message.answer(text=strings.select_product_name1,
                             reply_markup=ReplyKeyboardMarkup(keyboard=names2, resize_keyboard=True))
        await state.set_state(states.choosing_product_name)


# Пользователь или Администратор выбирает название товара (state: choosing_product_name)
@router.message(states.choosing_product_name, F.text == strings.exit_button)
async def back(message: Message, state: FSMContext):
    if message.text == strings.exit_button:
        if manager.is_admin(info=message.from_user):
            await message.answer(text=strings.get_category, reply_markup=kb.admins_categories_keyboard())
            await state.set_state(states.choosing_category)
        else:
            await message.answer(text=strings.get_category, reply_markup=kb.users_categories_keyboard())
            await state.set_state(states.choosing_category)


@router.message(states.choosing_product_name, F.text == strings.get_help_button)
async def help(message: Message, state: FSMContext):
    if message.text == strings.get_help_button:
        await message.answer(text=strings.get_help, reply_markup=kb.back_button_keyboard())
        await state.set_state(states.get_help)


# Отправка инструкции
@router.message(states.choosing_product_name)
async def product_name_chosen(message: Message, state: FSMContext, bot: Bot):
    try:
        await message.answer(text=strings.loading_instruction)
        photo = storage_class.getProductByName(message.text)
        await asyncio.sleep(1)
        if manager.is_admin(info=message.from_user):
            await bot.send_photo(message.chat.id, photo, reply_markup=kb.admins_start_keyboard())
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
            await state.set_state(states.choosing_act_admin)
        else:
            await bot.send_photo(message.chat.id, photo=photo, reply_markup=kb.users_start_keyboard())
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
            await state.set_state(states.choosing_act)
        print(photo)
    except Exception as e:
        logging.exception(f"Error: {e}.")
        await bot.send_message(chat_id=message.chat.id, text='Товар не найден. Попробуйте снова.')
        print(e)


@router.message(StateFilter(states.choosing_product_name))
async def product_name_chosen_incorrectly(message: Message, state: FSMContext):
    await message.answer(
        text=strings.product_doesnot_find
    )
    await state.set_state(states.choosing_category)
    await message.answer(text=strings.select_product_name2, reply_markup=kb.users_categories_keyboard())
