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
from bot.data.handlers import router
from bot.data.handlers import manager
from bot.data.handlers import GetProductInfo
from bot.Chat.User import User
from bot.Chat.Administrator import Administrator

@router.message(StateFilter(GetProductInfo.add_admin))
async def find_user(message: Message, bot: Bot, state: FSMContext):
    matches = manager.find_users(query=message.text)
    if len(matches) > 0:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Найденные пользователи",
                               reply_markup=kb.add_admin_keyboard(users=matches))
        await state.clear()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Пользователи не найдены. Попробуйте изменить запрос")
        # await state.clear()
@router.callback_query(F.data.contains("add_administrator"))
async def add_administrator(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    id = int(callback_query.data.split(":")[1])
    admin = manager.get_user_by_id(id=id)
    if admin is not None:
        manager.add_admin(admin = admin)
        await bot.send_message(chat_id=callback_query.from_user.id, text=strings.admin_added)
        await state.clear()
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text=strings.general_error)

@router.callback_query(F.data.contains("remove_administrator"))
async def add_administrator(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    id = int(callback_query.data.split(":")[1])
    admin = manager.get_user_by_id(id=id)
    if admin is not None:
        manager.admins.remove(admin)
        await bot.send_message(chat_id=callback_query.from_user.id, text=strings.admin_removed)
        await state.clear()
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text=strings.general_error)

