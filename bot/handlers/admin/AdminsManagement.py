from aiogram import types

from bot.handlers.General import *

router = Router()


@router.message(StateFilter(states.add_admin))
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
        manager.add_admin(admin=admin)
        await bot.send_message(chat_id=callback_query.from_user.id, text=strings.admin_added)
        await state.clear()
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text=strings.general_error)


@router.callback_query(F.data.contains("remove_administrator"))
async def remove_administrator(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    global main_admin_id
    id = int(callback_query.data.split(":")[1])
    admin = manager.get_admin_by_id(id=id)
    if admin is not None:
        manager.admins.remove(admin)
        await bot.send_message(chat_id=callback_query.from_user.id, text=strings.admin_removed)
        if main_admin_id is not None and main_admin_id == id:
            main_admin_id = None
        await state.clear()
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text=strings.general_error)

# code review
