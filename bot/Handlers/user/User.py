from aiogram import Router
from bot.Handlers.General import *

router = Router()


@router.message(states.get_help, F.text == strings.exit_button)
async def back(message: Message, state: FSMContext):
    if message.text == strings.exit_button:
        await message.answer(text=strings.greet.format(name=message.from_user.full_name),
                             reply_markup=kb.users_start_keyboard())
        await state.set_state(states.choosing_act)


@router.message(states.choosing_act, F.text == strings.get_help_button)
async def help(message: Message, state: FSMContext):
    if message.text == strings.get_help_button:
        await message.answer(text=strings.get_help,
                             reply_markup=kb.back_button_keyboard())
        await state.set_state(states.get_help)


# Пользователь выбирает действие (state: choosing_act)
@router.message(states.choosing_act)
async def act_chosen(message: Message, state: FSMContext):
    if message.text == strings.get_instruction_button:
        await message.answer(text=strings.get_category, reply_markup=kb.users_categories_keyboard())
        await state.set_state(states.choosing_category)

    if message.text == strings.get_help_button:
        # await message.answer(text.get_help, reply_markup=kb.back_button_keyboard())
        await message.answer(strings.get_help, reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(states.get_help)


@router.message(states.choosing_category, F.text == strings.get_help_button)
async def help(message: Message, state: FSMContext):
    if message.text == strings.get_help_button:
        await message.answer(text=strings.get_help,
                             reply_markup=kb.back_button_keyboard())
        await state.set_state(states.get_help)


@router.message(StateFilter(states.choosing_category))
async def category_chosen_incorrectly(message: Message):
    await message.answer(
        text=strings.category_doesnot_find,
        reply_markup=kb.users_categories_keyboard()
    )
