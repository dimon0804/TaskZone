from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext

import database.requests as db
import text
from states import user as states
from keyboards import user as kb

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id
    if await db.get_user(user_id) is None:
        await db.add_user(user_id, message.from_user.first_name)
    await message.answer(text.start_message.format(name=message.from_user.first_name), 
                         reply_markup=kb.menu)

@router.message(states.CreateProject.name)
async def create_project_name(message: Message, state: FSMContext):
    if message.text.lower() in ['отмена', '/cancel']:
        await state.clear()
        await message.answer(text.cancel, reply_markup=kb.menu)
        return
    
    if await db.check_name_project(message.text):
        await message.answer(text.create_project_name_error)
        return
    await state.update_data(title=message.text)
    await message.answer(text.create_project_description)
    await state.set_state(states.CreateProject.description)

@router.message(states.CreateProject.description)
async def create_project_description(message: Message, state: FSMContext):
    if message.text.lower() in ['отмена', '/cancel']:
        await state.clear()
        await message.answer(text.cancel, reply_markup=kb.menu)
        return
    await state.update_data(description=message.text)
    data = await state.get_data()
    title = data['title']
    description = data['description']
    await message.answer(text.create_project_finaly.format(title=title, description=description), 
                         reply_markup=kb.menu)
    await db.add_project(message.from_user.id, title, description)
    await state.clear()

@router.message(F.content_type==ContentType.TEXT)
async def text_message(message: Message, state: FSMContext):
    if message.text.lower() in ['проекты', '/project']:
        await message.answer(text.project_message, reply_markup=kb.project)
    elif message.text.lower() in ['задачи', '/tasks']:
        await message.answer(text.tasks_message)
    elif message.text.lower() in ['отмена', '/cancel']:
        await state.clear()
        await message.answer(text.cancel, reply_markup=kb.menu)


@router.callback_query(F.data.startswith("project_"))
async def callback_project(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    action_data = callback.data[len("project_"):]
    await state.update_data(level="see_project")
    project = await db.get_project(int(action_data))
    sum_tasks = await db.get_sum_tasks(int(action_data))
    await callback.message.answer(text.project.format(title=project.title, 
                                                      description=project.description, 
                                                      date_creat=project.created_at, 
                                                      sum_tasks=sum_tasks), 
                                                      reply_markup=await kb.project_num(action_data))


@router.callback_query()
async def callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    if callback.data == "create_project":
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        await callback.message.answer(text.create_project, reply_markup=kb.cancel)
        await state.set_state(states.CreateProject.name)
    elif callback.data == "my_projects":
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        projects = await db.get_projects(callback.from_user.id)
        await callback.message.answer(text.projects_message, 
                                      reply_markup=await kb.my_projects(projects=projects))
        await state.update_data(level="list_project")
    elif callback.data == "tasks":
        await callback.message.answer(text.tasks_message)
    elif callback.data == "back":
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        data = await state.get_data()
        level = data['level']
        await state.clear()
        if level == "list_project":
            await callback.message.answer(text.project_message, reply_markup=kb.project)
        elif level == "see_project":
            projects = await db.get_projects(callback.from_user.id)
            await callback.message.answer(text.projects_message,
                                          reply_markup=await kb.my_projects(projects=projects))
