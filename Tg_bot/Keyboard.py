from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from Tg_bot.Database.Requests import get_topic, get_question

# Меню при вході в сам бот для абітури
menu = ReplyKeyboardMarkup(
    keyboard= [
        [KeyboardButton(text='🌐 Онлайн підтримка'), KeyboardButton(text='ℹ️ Інформація')],
        [KeyboardButton(text='❓ Поширені запитання'),KeyboardButton(text='👤 Аккаунт')], # KeyboardButton(text='⚙️ Налаштування')
        [ KeyboardButton(text='📖 Допомога')]
    ],
    resize_keyboard=True, 
    input_field_pleceholder="Оберіть пункт меню"
)

journal = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Перейти на Journal', url='https://example.com')]
])

menu_adm = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Перегляд питань')]
    ],
    resize_keyboard=True, 
    input_field_pleceholder="Оберіть пункт меню"
)

bot_call = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Перейти в бот', url='https://t.me/N_T_U_bot')]
])

return_topic = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='return_topic')]])

# # # # # # # #
# Кнопки з бд #
# # # # # # # #

admin_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Адміністратори'), KeyboardButton(text='Популярні питання')],
    [KeyboardButton(text='Допомога')]
],
resize_keyboard=True,
input_field_placeholder='Вітаю, оберіть дію з клавіатури'
)

chanel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='❌ Відміна')]], resize_keyboard=True)

out_role = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='chanel_func')]])

back_on_menu_bd = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data='back_to_menu')]])

bd_admin_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Таблиці адміністраторів', callback_data='bd_admin_tabl'), 
    InlineKeyboardButton(text='Встановлення/Зміна ролі', callback_data='bd_admin_role')]
])

edit_quest_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Редагувати питання', callback_data='edit'),
    InlineKeyboardButton(text='Записати нове питання', callback_data='notes')],
    [InlineKeyboardButton(text='Видалити питання', callback_data='delete')]
])

edit_block = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Блок питань', callback_data='edit_topic'),
    InlineKeyboardButton(text='Питання', callback_data='edit_quest')],
    [InlineKeyboardButton(text='Відповідь', callback_data='edit_answer'),
    InlineKeyboardButton(text='Назад', callback_data='back_edit') ]
])

topic = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Новий блок', callback_data='topic_new'), 
    InlineKeyboardButton(text='Обрати блок', callback_data='topic_old')],
    [InlineKeyboardButton(text='Назад',callback_data='out_popular')]
])

return_set = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Так', callback_data='edit_true'),
    InlineKeyboardButton(text='Ні', callback_data='edit_false')]
])

async def get_all_topic():
    all_topic = await get_topic()
    keyboard = ReplyKeyboardBuilder()
    for txt in all_topic:
        keyboard.add(KeyboardButton(text=txt.topic))
    keyboard.add(KeyboardButton(text='❌ Відміна'))
    return keyboard.adjust(2).as_markup(resize_keyboard=True)

async def topic_for_abiture():
    all_topic = await get_topic()
    keyboard = InlineKeyboardBuilder()
    for txt in all_topic:
        keyboard.add(InlineKeyboardButton(text=txt.topic, callback_data = f'category_{txt.id}'))
    return keyboard.adjust(1).as_markup()

async def question_for_abiture(question_data):
    all_quest = await get_question(question_data)
    keyboard = InlineKeyboardBuilder()
    for txt in all_quest:
        keyboard.add(InlineKeyboardButton(text=txt.question, callback_data = f'question_{txt.id}'))
    keyboard.add(InlineKeyboardButton(text='🌐 Онлайн підримка', callback_data='online_support'))
    keyboard.add(InlineKeyboardButton(text='❌ В меню', callback_data='to_menu'))
    return keyboard.adjust(1).as_markup()

async def edit_topic_kb():
    edit_topic = await get_topic()
    keyboard = InlineKeyboardBuilder()
    for txt in edit_topic:
        keyboard.add(InlineKeyboardButton(text=txt.topic, callback_data = f'edittopic_{txt.id}'))    
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='edit_menu_back'))
    return keyboard.adjust(1).as_markup()

async def choice_topic_kb():
    edit_topic = await get_topic()
    keyboard = InlineKeyboardBuilder()
    for txt in edit_topic:
        keyboard.add(InlineKeyboardButton(text=txt.topic, callback_data = f'choicetopic_{txt.id}'))    
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='edit_menu_back'))
    return keyboard.adjust(1).as_markup()

async def edit_question_kb(id_topic):
    edit_quest = await get_question(id_topic)
    keyboard = InlineKeyboardBuilder()
    for txt in edit_quest:
        keyboard.add(InlineKeyboardButton(text=txt.question, callback_data = f'editque_{txt.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='edit_menu_back'))
    return keyboard.adjust(1).as_markup()

async def choice_topic_kb_two():
    edit_topic = await get_topic()
    keyboard = InlineKeyboardBuilder()
    for txt in edit_topic:
        keyboard.add(InlineKeyboardButton(text=txt.topic, callback_data = f'twicetopic_{txt.id}'))    
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='edit_menu_back'))
    return keyboard.adjust(1).as_markup()

async def choice_question_kb(id_topic):
    edit_quest = await get_question(id_topic)
    keyboard = InlineKeyboardBuilder()
    for txt in edit_quest:
        keyboard.add(InlineKeyboardButton(text=txt.question, callback_data = f'choiceque_{txt.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='edit_menu_back'))
    return keyboard.adjust(1).as_markup()

async def choice_topic_delete():
    choice_topic = await get_topic()
    keyboard = InlineKeyboardBuilder()
    for txt in choice_topic:
        keyboard.add(InlineKeyboardButton(text=txt.topic, callback_data = f'deletetop_{txt.id}'))    
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back_edit'))
    return keyboard.adjust(1).as_markup()

async def delete_question(id_question):
    edit_quest = await get_question(id_question)
    keyboard = InlineKeyboardBuilder()
    for txt in edit_quest:
        keyboard.add(InlineKeyboardButton(text=txt.question, callback_data = f'deleteque_{txt.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back_edit'))
    return keyboard.adjust(1).as_markup()

# # # # # # # #
# Кнопки з inf#
# # # # # # # #

inf = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Інформація про університет', callback_data='univ'),
    InlineKeyboardButton(text='Інформація про факультет', callback_data='fac')]
])

inf_university = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Інформація про факультет', callback_data='fac')]])

inf_facultet = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Інформація про університет', callback_data='univ')]])

# # # # # # # # #
# Кнопки з help #
# # # # # # # # #

All_help = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Адміністратори', callback_data='1'), 
    InlineKeyboardButton(text='Популярні питання', callback_data='2') ]
])

One_table = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад',callback_data='back_all_help'),
    InlineKeyboardButton(text='1/2', callback_data='0'),
    InlineKeyboardButton(text='➡️', callback_data='2')]
])

Two_table = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️', callback_data='1'),
    InlineKeyboardButton(text='2/2', callback_data='0'),
    InlineKeyboardButton(text='Назад',callback_data='back_all_help') ]
])

All_abiture_help = InlineKeyboardMarkup(inline_keyboard=[       # Abitura
    [InlineKeyboardButton(text='🌐 Онлайн підримка',  callback_data='1.1'), 
    InlineKeyboardButton(text='ℹ️ Інформація', callback_data='2.2')],
    [InlineKeyboardButton(text='❓ Поширені запитання', callback_data='3.3'), #InlineKeyboardButton(text='⚙️ Налаштування', callback_data='4.4')
    InlineKeyboardButton(text='👤 Аккаунт', callback_data='5.5')]
])

help_11 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='to_menu_help'),
    InlineKeyboardButton(text='➡️', callback_data='2.2') ]
])

help_22 =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️', callback_data='1.1'),
    InlineKeyboardButton(text='Назад', callback_data='to_menu_help'), 
    InlineKeyboardButton(text='➡️', callback_data='3.3') ]
])

help_33 =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️', callback_data='2.2'),
    InlineKeyboardButton(text='Назад', callback_data='to_menu_help'), 
    InlineKeyboardButton(text='➡️', callback_data='5.5') ]
])

# help_44 =InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='⬅️', callback_data='3.3'),
#     InlineKeyboardButton(text='Назад', callback_data='to_menu_help'), 
#     InlineKeyboardButton(text='➡️', callback_data='5.5') ]
# ])

help_55 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️', callback_data='3.3'),
    InlineKeyboardButton(text='Назад', callback_data='to_menu_help') ]
])

# # # # # # # # #
# Кнопки online #
# # # # # # # # #

async def recor_keyboard(record_id, total):
    
    buttons = []
    if record_id > 1:
        buttons.append(InlineKeyboardButton(text='⬅️', callback_data=f'prev_record_{record_id - 1}'))
    buttons.append(InlineKeyboardButton(text='Взятись', callback_data=f'take_appeal_{record_id}'))
    if  record_id < total:
        buttons.append(InlineKeyboardButton(text='➡️', callback_data=f'next_record_{record_id + 1}'))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return keyboard

chat_stop = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Завершити діалог')]
],
resize_keyboard=True,
input_field_placeholder='Напишіть відповідь користувачу'
)

what_question = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Так', callback_data='q_true'),
    InlineKeyboardButton(text='Ні', callback_data='q_false')]
])