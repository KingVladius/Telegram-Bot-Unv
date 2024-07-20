import Tg_bot.Keyboard as Keyboard
from aiogram.fsm.context import FSMContext


from aiogram.types import Message
from aiogram import F
from Tg_bot.Database.Requests import get_all_admins, update_role
from Tg_bot.FSM import db_text


async def welcome (message: Message):
    await message.answer(f"Привіт, {message.from_user.first_name} !\nЦе офіційний телеграм-бот Національного транспортного університету.\nЩо б ви хотіли дізнатись?", reply_markup = Keyboard.menu)

async def group_welcome(message: Message):
    await message.answer("Вітаю, якими будуть ваші дії? ",reply_markup=Keyboard.menu_bd)

async def popular_que(message: Message):
    await message.edit_text('Ви в меню для популярних завдань, що ви б хотіли зробити?', reply_markup= Keyboard.edit_quest_menu)

async def admin_menu_bd(message: Message):
    await message.answer('Ви хочете подивитись всіх адміністраторів чи змінити їм роль?',reply_markup=Keyboard.bd_admin_menu)

async def admin_menu_bd_edit(message: Message):
    await message.edit_text('Ви хочете подивитись всіх адміністраторів чи змінити їм роль?',reply_markup=Keyboard.bd_admin_menu)

async def poopular_question_edit(message: Message):
    await message.edit_text('Ви в меню для популярних завдань, що ви б хотіли зробити?', reply_markup= Keyboard.edit_quest_menu)    

async def get_all_admin_tabl(message: Message):
    all_tabl = await get_all_admins()
    inf =''
    for el in all_tabl:
        if el.status == '1':
            role = 'Адмін 👤'
        elif el.status == '2':
            role = 'Методист 👨‍🎓'
        elif el.status == '3':
            role = 'Хелпер 👨‍💻'
        else:
            role = 'Роль не встановлена'
        inf+=f"{el.username}  ->  {role} \n\n"
    await message.edit_text(text=inf, reply_markup=Keyboard.back_on_menu_bd)

async def new_role (message: Message, state:FSMContext ):
    await state.set_state(db_text.txt)
    await message.edit_text("Введіть данні про користувача таким чином:\n\nХелпер - 3\nМетодист - 2\nТех - 1\n\n@username role(1-3)", reply_markup=Keyboard.out_role)

async def new_role_second (message: Message, state:FSMContext ):
    await state.set_state(db_text.txt)
    await message.answer("Введіть данні про користувача таким чином:\n\nХелпер - 3\nМетодист - 2\nТех - 1\n\n@username role(1-3)", reply_markup=Keyboard.out_role)


async def state_role(message: Message, state: FSMContext):   
    admins = await get_all_admins()
    current_admin = None
    data = await state.get_data()
    role_text = data.get('txt', '')
    role = role_text.split()
    await state.clear()
    for admin in admins:
        if admin.tg_id == message.from_user.id:
            current_admin = admin
            break
        else:
            await message.answer("Ви не є адміністратором")
    if current_admin and current_admin.status == '1':
        if len(role) == 2:
            UserName = role[0]
            Role = role[1]
            await update_role(UserName, Role)
            await message.answer(f"Роль для {UserName} успішно оновлена на {Role}")
        else:
            await message.answer("Неправильно введені данні, спробуйте ще раз")
            await new_role_second(message, state)
    else:
        await message.answer("У вас не достатньо прав для зміни ролі, зверніться до головного адміністратора")
