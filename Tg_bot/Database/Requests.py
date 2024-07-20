from Tg_bot.Database.Models import async_session
from Tg_bot.Database.Models import User, Admins, Note, Category, Appeal, Online
from sqlalchemy import select, update, delete, func

async def set_user (tg_id,name,username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        admin = await session.scalar(select(Admins).where(Admins.tg_id == tg_id))
        status = 101
        if not user:
            if username is None:
                username = 'username_false'
                session.add(User(tg_id=tg_id, name=name, username=username))
                await session.commit()
            else:
                session.add(User(tg_id=tg_id, name=name, username=username)) # , status=status
                await session.commit()
        else:
            if username is None:
                username = 'username_false'
                user_new = (update(User).where(User.name == name).values(username=username))
                await session.execute(user_new)
                await session.commit()
            else:
                user_new = (update(User).where(User.name == name).values(username=username))
                await session.execute(user_new)
                await session.commit()

async def set_admins(tg_id,name,username):
    async with async_session() as session:
        admin = await session.scalar(select(Admins).where(Admins.tg_id == tg_id))
        first_admin = await session.scalar(select(func.count()).select_from(Admins))
        if not admin:
            status = '1' if first_admin == 0 else '0'
            if username is None:
                username = 'username_false'
                session.add(Admins(tg_id=tg_id, name=name, username=username, status=status))           
                await session.commit()
            else:
                session.add(Admins(tg_id=tg_id, name=name, username=username, status=status))           
                await session.commit()
        else:
            if username is None:
                username = 'username_false'
                admin.username = username
                await session.commit()
            else:
                admin.username = username
                await session.commit()

async def get_all_admins():
    async with async_session() as session:
        return await session.scalars(select(Admins))

async def get_id_admin():
    async with async_session() as session:
        return await session.scalars(select(Admins.tg_id))
    
async def update_role(username, txt):
    async with async_session() as session:
        admin = await session.scalar(select(Admins).where(Admins.username == username))
        if admin:
            admin.status = txt
            await session.commit()
        
async def add_question(topic, question, explanation):
    async with async_session() as session:
        category = await session.scalar(select(Category).where(Category.topic == topic))
        if not category:
            new_category = (Category(topic = topic))
            session.add(new_category)
            await session.commit()
            await session.refresh(new_category)
            category_id = new_category.id
        else:
            category_id = category.id
        session.add(Note(topic=category_id, question=question,explanation=explanation))
        await session.commit()

async def get_topic():
    async with async_session() as session:
        return await session.scalars(select(Category))
    
async def get_question(topic_id):
    async with async_session() as session:
        return await session.scalars(select(Note).where(Note.topic == topic_id))

async def get_explanation(question_id):
    async with async_session() as session:
        return await session.scalar(select(Note).where(Note.id == question_id))

async def update_edit_topic(id_topic, topic):
    async with async_session() as session:
        add_edit = await session.scalar(select(Category).where(Category.id == id_topic))
        add_edit.topic = topic
        await session.commit()

async def update_edit_question(id_question, question):
    async with async_session() as session:
        edit_new = await session.scalar(select(Note).where(Note.id == id_question))
        edit_new.question = question
        await session.commit()

async def update_edit_answer(id_answer, answer):
    async with async_session() as session:
        edit_new = await session.scalar(select(Note).where(Note.id == id_answer))
        edit_new.explanation = answer
        await session.commit()

async def delete_tabl(id_question):
    async with async_session() as session:
        result = await session.scalars(select(Note).where(Note.id == id_question))
        db_data = result.first()
        if db_data:
            await session.delete(db_data)
            await session.commit()

async def add_appeal(id, txt, act):
    async with async_session() as session:
        session.add(Appeal(id_user = id, question = txt, active = act))
        await session.commit()

async def reboot_appeal(user, act):
    async with async_session() as session:
        data = await session.scalar(select(Appeal).where(Appeal.id_user == user))
        data.active = act
        await session.commit()

async def all_appeal():
    async with async_session() as session:
        result = await session.scalars(select(Appeal))
        return result.all()
    
async def appeal_user(user):
    async with async_session() as session:
        return await session.scalar(select(Appeal).where(Appeal.id_user == user))
    
async def appeal_to_admin(user_id, admin_id, active):
    async with async_session() as session:
        session.add(Online(id_user=user_id, id_admin=admin_id, active=active))    
        await session.commit()

async def get_active():
    async with async_session() as session:
        return await session.scalars(select(Online))
    
async def delete_active(user):
    async with async_session() as session:
        result = await session.scalars(select(Online).where(Online.id_user==user))
        active_del = result.first()
        if active_del:
            await session.delete(active_del)
            await session.commit()

async def delet_user_request(user):
    async with async_session() as session:
        result_appeal = await session.scalars(select(Appeal).where(Appeal.id_user == user))
        appeal_del = result_appeal.first()
        if appeal_del:
            await session.delete(appeal_del)
            await session.commit()
    