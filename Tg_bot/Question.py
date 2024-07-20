import Tg_bot.Database.Requests as Req
import Tg_bot.Keyboard as Keyboard
from Tg_bot.FSM import question_db
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def note_topic(message: Message):
    await message.edit_text('Ви можете записати новий блок питань або обрати з того, що вже є. Оберіть, що будемо робити', reply_markup=Keyboard.topic)

async def set_new_topic(message: Message, state: FSMContext):
    await state.set_state(question_db.topic)
    await message.answer('Введіть блок питань (Кількість символів - 30):',reply_markup=Keyboard.chanel)

async def set_old_topic(message: Message, state: FSMContext):
    await state.set_state(question_db.topic)
    data_topic = await Req.get_topic()
    if not data_topic:
        await message.answer('Блоків питань нема, оберіть іншу функція для того, щоб їх записати.')
    await message.answer("Виберіть болк питань з переліку👇", reply_markup= await Keyboard.get_all_topic())

async def set_question(message:Message, state:FSMContext):
    await state.set_state(question_db.que)
    await message.reply("Напишіть питання (Кількість символів - 50):")

async def set_explanation(message: Message, state: FSMContext):
    await state.set_state(question_db.explanation)
    await message.reply("Напишіть відповідь до свого питання (Кількість символів - 2к):")

async def add_question_db(message: Message, state: FSMContext):
    question_data = await state.get_data()
    await message.reply("Ваш текст записаний в базу данних", reply_markup=Keyboard.return_set)
    await Req.add_question(question_data['topic'], question_data['que'], question_data['explanation'])
    await state.clear()

async def Choose_edit_false(message: Message):
    await message.edit_text('Запис завершено і все додано до бази данних')
    await message.answer('Що ви оберете?', reply_markup=Keyboard.admin_menu)

async def abitur_topic(message: Message):
    await message.answer('Виберіть блок питань які вас цікавлять:', reply_markup=await Keyboard.topic_for_abiture())

async def abitur_topic_two(message: Message):
    await message.edit_text('Виберіть блок питань які вас цікавлять:', reply_markup=await Keyboard.topic_for_abiture())

async def edit_menu(message: Message):
    await message.edit_text('Оберіть, що ви хочете редагувати:', reply_markup=Keyboard.edit_block)

async def edit_topic(message:Message):
    await message.edit_text('Оберіть блок питань які ви хочете змінити:', reply_markup= await Keyboard.edit_topic_kb())

async def add_edit_topic(message: Message, state: FSMContext):
    await message.reply("Оновлення прошло успішно")
    edit_data = await state.get_data()
    await Req.update_edit_topic(edit_data['id_text'], edit_data['edit_topic'])
    await state.clear()

async def choice_topic(message: Message):
    await message.edit_text("Оберіть блок питань в якому ви хочете змінити запитання:", 
                            reply_markup= await Keyboard.choice_topic_kb())
    
async def add_new_question(message: Message, state: FSMContext):
    await message.reply("Оновлення прошло успішно")
    edit_data = await state.get_data()
    await Req.update_edit_question(edit_data['id_que'], edit_data['edit_que'])
    await state.clear()

async def choice_topic_two(message: Message):
    await message.edit_text("Для того щоб змінити відповідь, вам потрібно вибрати блок в якому вона знаходиться:", 
                            reply_markup= await Keyboard.choice_topic_kb_two())
    
async def add_new_answer(message: Message, state: FSMContext):
    await message.reply("Оновлення прошло успішно")
    edit_data = await state.get_data()
    await Req.update_edit_answer(edit_data['id_answer'], edit_data['edit_answer'])
    await state.clear()

async def delete_question(message: Message):
    txt = ['''Вітаю! Щоб видалити питання, потрібно обрати блок і обрати питання яке ви хочете видалити\n
🛑 ! УВАГА ! 🛑
ПИтання яке ви видалите не можливо буде повернути назад, тільки якщо заново його написати
''']
    await message.edit_text(txt[0], reply_markup= await Keyboard.choice_topic_delete())

async def tabl_clear(message: Message, state: FSMContext):
    await message.reply("Все пройшло добре")
    delete_data = await state.get_data()
    await Req.delete_tabl(delete_data['id_question'])
    await state.clear()