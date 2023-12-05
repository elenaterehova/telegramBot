from bot.handlers.admin.AdminsManagement import *
from bot.handlers.General import states, manager
from aiogram import Router

router = Router()


@router.message(states.choosing_act_admin)
async def admin_act_chosen(message: Message, state: FSMContext):
    if message.text == strings.get_instruction_button:
        await message.answer(text=strings.get_category, reply_markup=kb.admins_categories_keyboard())
        await state.set_state(states.choosing_category)

    if message.text == strings.admins_list:
        admins_names = ''
        for admin in manager.admins:
            admins_names += admin.info.full_name + "\n"
        await message.answer(text=f'Список Администраторов:\n\n{admins_names}',
                             reply_markup=kb.admins_management_keyboard())
        await state.set_state(states.add_or_delete_admin)


@router.message(states.add_or_delete_admin)
async def add_or_delete(message: Message, bot: Bot, state: FSMContext):
    if message.text == strings.add_admin:
        await message.answer(text='Введите ID или имя пользователя, которого хотите добавить в список Администраторов:',
                             reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(states.add_admin)
    if message.text == strings.delete_admin:
        await message.answer(text='.', reply_markup=types.ReplyKeyboardRemove())
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
        await message.answer(text='Список администраторов',
                             reply_markup=kb.delete_admin_keyboard(admins=manager.admins))
        await state.set_state(states.delete_admin)


# @router.message(StateFilter(states.choosing_category))
# async def category_chosen_incorrectly(message: Message):
#     await message.answer(
#         text=strings.category_doesnot_find,
#         reply_markup=kb.admins_categories_keyboard()
#     )
