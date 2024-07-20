from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import Tg_bot.Keyboard as Keyboard
import Tg_bot.Info as Info
import Tg_bot.Question as Question
import Tg_bot.Func as Func
import Tg_bot.Help as Help
import Tg_bot.Database.Requests as Req
import Tg_bot.Support as Support


async def call_menu(callback: CallbackQuery, state: FSMContext ):
    user = callback.from_user.first_name
    id = callback.from_user.id
    print(id, user)
    if callback.data == 'edit_quests':    # Меню для вписування або редактора
        await callback.answer('')
        await callback.message.edit_text('Яке питання ви б хотіли записати або відредагувати?', reply_markup=Keyboard.edit_quest_menu)

    elif callback.data == 'edit':           # Редагування повідомлення 
        await callback.answer('Ви обрали редагування Популярних питань')
        await Question.edit_menu(callback.message)

    elif callback.data == 'edit_topic':
        await callback.answer('')
        await Question.edit_topic(callback.message)

    elif callback.data == 'edit_quest':
        await callback.answer('')
        await Question.choice_topic(callback.message)

    elif callback.data == 'edit_answer':
        await callback.answer('')
        await Question.choice_topic_two(callback.message)

    elif callback.data == 'back_edit':
        await callback.answer('')
        await Func.popular_que(callback.message)

    elif callback.data == 'edit_menu_back':
        await callback.answer('')
        await Question.edit_menu(callback.message)

    elif callback.data == 'edit_true':
        await callback.answer('Записуємо ще одне питання')
        await Question.note_topic(callback.message)

    elif callback.data == 'edit_false':
        await callback.answer('Ви повернулись в голловне меню')
        await Question.Choose_edit_false(callback.message)

    elif callback.data =='delete':
        await callback.answer('')
        await Question.delete_question(callback.message)

    elif callback.data == 'notes':          # Запис питання в бд
        await callback.answer('')
        await Question.note_topic(callback.message)

    elif callback.data == 'back_quest':     # Повернення на одне меню назад
        await callback.answer('')
        await callback.message.edit_text('Ви в меню для популярних завдань, що ви б хотіли зробити?', reply_markup= Keyboard.quest_menu)

    elif callback.data == 'topic_new':      # Запис нового блоку питань 
        await callback.answer("Ви обобрали записати новий блок")
        await Question.set_new_topic(callback.message, state)

    elif callback.data == 'topic_old':      # Запис старого блоку питаннь 
        await callback.answer("Ви обобрали (обрати старий блок)")
        await Question.set_old_topic(callback.message, state)

    elif callback.data == 'out_popular':    # Назад в популярні питання
        await callback.answer('Ви повернулись в Популярні питання')
        await Func.poopular_question_edit(callback.message)

    elif callback.data == 'bd_admin_tabl':  # Таблиці адміністраторів 
        await callback.answer("Ви обрали таблиці адмінісраторів")
        await Func.get_all_admin_tabl(callback.message)

    elif callback.data == 'bd_admin_role':  # Зміна ролі дл адмінів
        await callback.answer("Ви обрали зміну ролі")
        await Func.new_role(callback.message, state)

    elif callback.data == "back_to_menu":   # Назад в меню 
        await callback.answer("Ви повернулись в меню адмінів")
        await Func.admin_menu_bd_edit(callback.message)

    elif callback.data == 'chanel_func':    # Назад в меню
        await callback.answer('Ви повернулись в меню адмінів')
        await state.clear()
        await Func.admin_menu_bd_edit(callback.message)

    elif callback.data == 'to_menu':        # Назад в головне меню
        await callback.answer("Ви обрали головне меню")
        await callback.message.edit_text('Ви повернулись в головне меню')
        await callback.message.answer("Знання чекають тебе!", reply_markup=Keyboard.menu)

    elif callback.data == '2':              # Допомога в адмінів
        await callback.answer('')
        await Help.get_help_popular_question(callback.message)

    elif callback.data == '1':              # Допомога в адмінів 
        await callback.answer('')
        await Help.get_help_admin(callback.message)

    elif callback.data == 'back_all_help':  # Назад в меню допомоги
        await callback.answer('')
        await Help.help_inf_two(callback.message) 

    elif callback.data == 'return_topic':
        await callback.answer('Ви повернулись до вибору теми')
        await Question.abitur_topic_two(callback.message)
# Абітурієнти

    elif callback.data == 'online_support':
        await callback.answer('Ви обрали онлайн підтримку')
        await Support.support_start(callback.message, state)
    
    elif callback.data == 'to_menu_help':
        await callback.answer('Ви повернулись в меню допомоги')
        await Help.abitur_help_two(callback.message)

    elif callback.data == '1.1':
        await callback.answer('')
        await Help.help_11(callback.message)

    elif callback.data == '2.2':
        await callback.answer('')
        await Help.help_22(callback.message)

    elif callback.data == '3.3':
        await callback.answer('')
        await Help.help_33(callback.message)

    # elif callback.data == '4.4':
    #     await callback.answer('')
    #     await Help.help_44(callback.message)
        
    elif callback.data == '5.5':
        await callback.answer('')
        await Help.help_55(callback.message)

    elif callback.data == 'q_true':
        await callback.answer('')
        await Support.support_off(callback)

    elif callback.data == 'q_false':
        await callback.answer('')
        await Support.support_not_off(callback)

# Інформація
    elif callback.data == 'univ': 
        await Info.inf_univ(callback.message)

    elif callback.data == 'fac': 
        await Info.inf_fac(callback.message)



async def text_check(message: Message, state: FSMContext):
    user = message.from_user.first_name
    id = message.from_user.id
    print(id, user)


    # Бот клавіатура для абітури
    if message.text == 'ℹ️ Інформація':
        await Req.set_user(message.from_user.id, message.from_user.first_name, message.from_user.username) 
        await Info.info(message)
    
    elif message.text == '⚙️ Налаштування': 
        await Req.set_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
        pass
    
    elif message.text == '❓ Поширені запитання':
        await Req.set_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
        await Question.abitur_topic(message)
        

    elif message.text == '👤 Аккаунт':
        await Req.set_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
        await Support.account_users(message)
        

    elif message.text == '📖 Допомога':
        await Req.set_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
        await Help.abitur_help(message)
        

    elif message.text == '🌐 Онлайн підтримка':
        await Req.set_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
        await Support.support_start(message, state)
        

    # Адмін панель в группі
    elif message.text == 'Адміністратори':
        await Req.set_admins(message.from_user.id, message.from_user.first_name, '@' + message.from_user.username)
        await Func.admin_menu_bd(message)
            
    elif message.text == 'Популярні питання':
        await Req.set_admins(message.from_user.id, message.from_user.first_name, '@' + message.from_user.username)
        await message.answer('Ви в меню для популярних питань, що ви б хотіли зробити?', reply_markup= Keyboard.edit_quest_menu)    
    
    elif message.text == 'Допомога':
        await Req.set_admins(message.from_user.id, message.from_user.first_name, '@' + message.from_user.username)
        await Help.help_inf(message)

    elif message.text == 'Перегляд питань':
        await Req.set_admins(message.from_user.id, message.from_user.first_name, '@' + message.from_user.username)
        await Support.show_records(message, state)
    
    
        # await Support.send_message(message, state)