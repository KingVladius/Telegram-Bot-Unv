from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class db_text(StatesGroup):
    txt = State()

class question_db(StatesGroup):
    topic = State()
    que = State()
    explanation = State()

class edit_question(StatesGroup):
    id_text = State()
    edit_topic = State()
    edit_que = State()
    edit_explanation = State()
    id_que = State()
    id_answer = State()

class delete_db(StatesGroup):
    id_question = State()

class appeal(StatesGroup):
    user_text = State()
    set_appeal = State()

class Chat(StatesGroup):
    chatting = State()
    