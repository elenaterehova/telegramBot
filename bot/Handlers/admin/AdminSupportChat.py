from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.Chat.User import User
from bot.Chat.Formatter import Formatter
from bot.Handlers.admin.AdminsManagement import *
from bot.Handlers.General import states

router = Router()
main_admin_id = 1302324252
manager = AccountManager()


@router.message(F.text, StateFilter(states.get_help))
async def get_help(message: Message, bot: Bot, state: FSMContext):
    """Помощь от консультанта"""
    if message.text == strings.get_help_button:
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
        await message.answer(text=strings.message_has_send_to_admin, reply_markup=kb.users_start_keyboard())
        await state.set_state(states.choosing_act)


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
        await state.set_state(states.get_help)
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
