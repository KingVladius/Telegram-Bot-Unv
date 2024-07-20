from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import F
from aiogram.fsm.context import FSMContext
from config import bot
import Tg_bot.Question as Question
import Tg_bot.Database.Requests as Req
import Tg_bot.Keyboard as Keyboard
import Tg_bot.Func as Func
import Tg_bot.Callbacks as Callbacks
import Tg_bot.Support as Support
import Tg_bot.FSM as FSM


router = Router()

# # # # # # # # # # # # #  ПРИ РЕЛІЗІ УДАЛИТЬ !!!!!!!!!!!
@router.message(Command('chat_inf'))
async def message_chat_inf(message: Message):
    message_data = str(message)
    await message.answer(message_data)
# # # # # # # # # # # # #  


@router.message(CommandStart())             # Start in bot
async def WELCOME (message: Message):
    Chat = message.chat.id
    id = message.from_user.id
    user = message.from_user.first_name
    print(id, user)

    admin = await Req.get_id_admin()
    if Chat == -1002115443993:   # check admin group
        await Req.set_admins(message.from_user.id, message.from_user.first_name, '@' + message.from_user.username)
        await message.answer('Вітаю, вельмишановний адміністраторе', reply_markup=Keyboard.admin_menu)
    elif id in admin:
        await Req.set_admins(message.from_user.id, message.from_user.first_name, '@' + message.from_user.username)
        await message.answer ("Вітаю вельми шановний вдмністраторе", reply_markup= Keyboard.menu_adm)
    else:
        await Req.set_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
        await Func.welcome(message)

@router.message(FSM.db_text.txt)        # FSM add new role
async def get_text(message: Message, state: FSMContext):
    await state.update_data(txt = message.text)
    await Func.state_role(message, state)

@router.message(FSM.question_db.topic)
async def get_topic_quest(message: Message, state: FSMContext):
    if message.text =='❌ Відміна':
        await state.clear()
        await message.answer("Ви повернулись в меню", reply_markup=Keyboard.admin_menu)
    else:
        await state.update_data(topic = message.text)
        await Question.set_question(message, state)

@router.message(FSM.question_db.que)
async def get_que_quest(message: Message, state: FSMContext):
    if message.text =='❌ Відміна':
        await state.clear()
        await message.answer("Ви повернулись в меню", reply_markup=Keyboard.admin_menu)
    else:
        await state.update_data(que=message.text)
        await Question.set_explanation(message, state)

@router.message(FSM.question_db.explanation)
async def get_explanation_quest(message: Message, state:FSMContext):
    if message.text =='❌ Відміна':
        await state.clear()
        await message.answer("Ви повернулись в меню", reply_markup=Keyboard.admin_menu)
    else:
        await state.update_data(explanation=message.text)
        await Question.add_question_db(message, state)

@router.message(FSM.appeal.user_text)
async def set_appeal(message: Message, state: FSMContext):
    exclude = ['ℹ️ Інформація', '❓ Поширені запитання', '👤 Аккаунт', '📖 Допомога', '🌐 Онлайн підримка']
    if message.text in exclude:
        await state.clear()
        await Callbacks.text_check(message, state)
    else:
        await Support.support_add_db(message, state)

@router.callback_query(F.data.startswith('category_'))
async def category_topic(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Оберіть питання з блоку яке вас цікавить:", 
                                  reply_markup= await Keyboard.question_for_abiture(callback.data.split('_')[1]))   

@router.callback_query(F.data.startswith('question_')) 
async def keyboard_callback(callback: CallbackQuery):
    question_data = await Req.get_explanation(callback.data.split('_')[1])
    await callback.message.edit_text(f"Відповідь на питання: {question_data.question}\n\n{question_data.explanation}", 
                                     reply_markup=Keyboard.return_topic)

@router.callback_query(F.data.startswith('edittopic_'))
async def byboard_topic_edit(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    edit_top = callback.data.split('_')[1]
    await state.set_state(FSM.edit_question.id_text)
    await state.update_data(id_text=edit_top)
    await state.set_state(FSM.edit_question.edit_topic)
    await callback.message.edit_text('Введіть новий текст для зміни блоку:')

@router.message(FSM.edit_question.edit_topic)
async def edit_topic_add(message: Message, state: FSMContext):
    await state.update_data(edit_topic=message.text)
    await Question.add_edit_topic(message, state)

@router.callback_query(F.data.startswith('choicetopic_'))
async def handle_choice_topic(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Оберіть питання з блоку яке вас цікавить:", 
                                  reply_markup= await Keyboard.edit_question_kb(callback.data.split('_')[1]))   

@router.callback_query(F.data.startswith('editque_')) 
async def handle_edit_question(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    edit_quest = callback.data.split('_')[1]
    await state.set_state(FSM.edit_question.id_que)
    await state.update_data(id_que=edit_quest)
    await state.set_state(FSM.edit_question.edit_que)
    await callback.message.edit_text('Введіть новий текст для зміни питання:')
    
@router.message(FSM.edit_question.edit_que)
async def add_edit_que(message: Message, state: FSMContext):
    await state.update_data(edit_que=message.text)
    await Question.add_new_question(message, state)

@router.callback_query(F.data.startswith('twicetopic_'))
async def handle_choice_topic_two(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Оберіть питання з блоку яке вас цікавить:", 
                                  reply_markup= await Keyboard.choice_question_kb(callback.data.split('_')[1]))   

@router.callback_query(F.data.startswith('choiceque_')) 
async def handle_edit_question_two(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    edit_answer = callback.data.split('_')[1]
    await state.set_state(FSM.edit_question.id_answer)
    await state.update_data(id_answer=edit_answer)
    await state.set_state(FSM.edit_question.edit_explanation)
    await callback.message.edit_text('Введіть новий текст для зміни відповіді:')
    
@router.message(FSM.edit_question.edit_explanation)
async def add_edit_que(message: Message, state: FSMContext):
    await state.update_data(edit_answer=message.text)
    await Question.add_new_answer(message, state)

@router.callback_query(F.data.startswith('deletetop_'))
async def handle_choice_topic_del(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Оберіть питання з блоку яке вас цікавить:", 
                                  reply_markup= await Keyboard.delete_question(callback.data.split('_')[1]))   

@router.callback_query(F.data.startswith('deleteque_')) 
async def handle_edit_question_two(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    id_delete = callback.data.split('_')[1]
    await state.set_state(FSM.delete_db.id_question)
    await state.update_data(id_question=id_delete)
    await Question.tabl_clear(callback.message, state)

@router.callback_query(F.data.startswith('prev_record_') | F.data.startswith('next_record_') | F.data.startswith('take_appeal_')) 
async def navigate_records(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    action = data[0]
    record_id =int(data[-1])
    state_data = await state.get_data()
    Appeals = state_data.get('record')
    if Appeals is None:
        await callback.message.answer('Не має запису для показу.')
        callback.answer('')
        return
    total = len(Appeals)
    if action == 'take':
        admin_id = callback.from_user.id
        active = True
        Records = Appeals[record_id - 1]
        active_data = await Req.get_active()
        if active_data:
            for act in active_data:
                if act.id_user == Records.id_user and act.active:
                    await callback.message.edit_text("Користувача взяв інишй адміністратор. Виберіть інше питання, якщо воно є")
                    await callback.answer('')
                    return
        active_true = 'Вирішується'
        await Req.reboot_appeal(Records.id_user, active_true)
        await Req.appeal_to_admin(Records.id_user, admin_id, active)
        await callback.message.edit_text(f'Ви взяли запит: \n{Records.question}')
        await callback.message.answer('Напишіть користувачу він чекає вашого повідомлення:',reply_markup=Keyboard.chat_stop)
        await state.clear()
        await state.update_data(admin=admin_id, user=Records.id_user, active=active)
        await state.set_state(FSM.Chat.chatting)
        await bot.send_message(Records.id_user, 'Ваше питання взяте адміністратором, можете спілкуватись.')
    else:
        await Support.show_record_two(callback.message, state, appeal_id=record_id, total=total)
    await callback.answer('')

@router.message(FSM.Chat.chatting)
async def set_message(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'Завершити діалог':
        await state.clear()
        await message.answer("Чат завершено", reply_markup=Keyboard.menu_adm)
        await bot.send_message(data['user'], "Адміністратор завершив чат.\n\nВаше питання було вирішене?", 
                               reply_markup=Keyboard.what_question)
        await Req.delete_active(data['user'])
    else:
        await Support.send_message(message, state)

@router.callback_query(F.data)
async def callback_menu(callback: CallbackQuery, state: FSMContext):
    await Callbacks.call_menu(callback, state)

@router.message(F.text)
async def button_call(message: Message, state: FSMContext):
    chat_data = await Req.all_appeal()
    active_data = await Req.get_active()
    user = None
    active = None
    if chat_data:
        for chat in chat_data:
                user = chat.id_user
    if active_data:
        for act in active_data:
                active = act.active
    if active == True and user == message.from_user.id:
        await Support.send_message(message, state)
    else:
        await Callbacks.text_check(message, state)

