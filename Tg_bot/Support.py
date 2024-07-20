import Tg_bot.Keyboard as Keyboard
import Tg_bot.Database.Requests as Req
import Tg_bot.FSM as FSM
from aiogram.types import Message, CallbackQuery
from config import bot
from aiogram.fsm.context import FSMContext
from aiogram import F


async def account_users(message: Message):
    id_chat = message.chat.id
    user_name = message.from_user.first_name
    await message.answer(f"Привіт, {user_name}. Це ваш персональний аккаунт в телеграм-боті.\n\nВаш індетифікатор - {id_chat}\n\nВаш статус - абітурієнт", 
                         reply_markup=Keyboard.journal)
    
async def support_start(message: Message, state: FSMContext):
    await state.set_state(FSM.appeal.user_text)
    await message.answer('Вітаємо! Ви звернулися до онлайн підтримки Національного транспортного університету. Як ми можемо вам допомогти? Напишіть своє питання або проблему, і наші фахівці з радістю вам допоможуть.')

async def support_add_db(message: Message, state: FSMContext):
    await state.update_data(appeal_txt = message.text)
    id_user = message.from_user.id
    appeal_data = await state.get_data()
    await state.clear()
    active = 'Вільний'
    await Req.add_appeal(id_user, appeal_data['appeal_txt'], active)
    await bot.send_message(-1002115443993, f'Вам прийшло повідомлення від користувача!\n\n{appeal_data["appeal_txt"]}',
                           reply_markup= Keyboard.bot_call)
    await message.answer('Ваше питання відправлено в підтримку. Очікуйте відповіді')
    

async def show_records(message: Message, state: FSMContext):
    records = await Req.all_appeal()
    await state.set_state(FSM.appeal.set_appeal)
    if not records:
        await message.answer("Немає записів")
        return
    total = len(records)
    await state.update_data(record=records)
    await show_record(message, state, appeal_id=1, total=total )

async def show_record(message: Message, state: FSMContext, appeal_id, total):
    data = await state.get_data()
    appeals = data.get('record')
    record = appeals[appeal_id - 1]
    txt = f'Запит {appeal_id} з {total}:\n\n{record.active}\n\n{record.question}'
    await message.answer(text=txt, reply_markup= await Keyboard.recor_keyboard(appeal_id, total))
    
async def show_record_two(message: Message, state: FSMContext, appeal_id, total):
    data = await state.get_data()
    appeals = data.get('record')
    record = appeals[appeal_id - 1]
    txt = f'Запит {appeal_id} з {total}:\n\n{record.active}\n\n{record.question}'
    await message.edit_text(text=txt, reply_markup= await Keyboard.recor_keyboard(appeal_id, total))

async def send_message(message: Message, state: FSMContext):
    user = None
    admin = None
    active = False
    chat_data = await Req.get_active()
    if chat_data:
        for chat in chat_data:
            user = chat.id_user
            admin = chat.id_admin
            active = chat.active
    if message.from_user.id == admin:
        await bot.send_message(user, message.text)
    elif active == True and message.from_user.id == user:
        await bot.send_message(admin, message.text)
    
async def support_off(callback: CallbackQuery):
        user_id = callback.from_user.id
        await Req.delet_user_request(user_id)
        await callback.message.edit_text('Я радий це чути.')

async def support_not_off(callback: CallbackQuery):
        user = callback.from_user.id
        data = await Req.appeal_user(user)
        if data:
            await callback.message.edit_text('Дуже прикро це чути. Зачекайте поки ваш запит візьме інший адміністратор.')
            await bot.send_message(-1002115443993, f'Питання не було вирішено, будь ласка дайте відповідь знову на це питання.\n\n{data.question}',
                                   reply_markup=Keyboard.bot_call)
            active = 'Вільно'
            await Req.reboot_appeal(user, active)
        else:
             await callback.message.edit_text('Вашого запитання не знайдено, будь ласка напишіть знову своє запитання в онлайн підтримку.')