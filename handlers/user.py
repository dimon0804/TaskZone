from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext

import database.requests as db
import text
from states import user as states
from keyboards import user as kb
from config import TASK_STATUSES, TASK_PRIORITIES
from utils.calendar import CalendarKeyboard


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
    await message.answer(text.create_project_finaly.format(title=title, 
                                                           description=description), 
                                                           reply_markup=kb.menu)
    await db.add_project(message.from_user.id, title, description)
    await state.clear()

@router.message(states.CreateTask.name)
async def create_task_name(message: Message, state: FSMContext):
    if message.text.lower() in ['отмена', '/cancel']:
        await state.clear()
        await message.answer(text.cancel, reply_markup=kb.menu)
        return
    await state.update_data(name=message.text)
    await message.answer(text.create_task_description)
    await state.set_state(states.CreateTask.description)

selected_date = None
@router.message(states.CreateTask.description)
async def create_task_description(message: Message, state: FSMContext):
    if message.text.lower() in ['отмена', '/cancel']:
        await state.clear()
        await message.answer(text.cancel, reply_markup=kb.menu)
        return
    await state.update_data(description=message.text)

    calendar_keyboard = CalendarKeyboard()
    calendar_markup = calendar_keyboard.get_keyboard()
   
    await state.update_data(month=calendar_keyboard.current_month, year=calendar_keyboard.current_year)

    await message.answer(text.create_task_due, reply_markup=calendar_markup)
    await state.set_state(states.CreateTask.due_date)

@router.message(F.content_type==ContentType.TEXT)
async def text_message(message: Message, state: FSMContext):
    if message.text.lower() in ['проекты', '/project']:
        await message.answer(text.project_message, reply_markup=kb.project)
    elif message.text.lower() in ['задачи', '/tasks']:
        await message.answer(text.tasks_message, reply_markup=kb.task)
    elif message.text.lower() in ['отмена', '/cancel']:
        await state.clear()
        await message.answer(text.cancel, reply_markup=kb.menu)

@router.callback_query(F.data.startswith("project_"))
async def callback_project(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.delete_message(chat_id=callback.message.chat.id, 
                             message_id=callback.message.message_id)
    action_data = callback.data[len("project_"):]
    await state.update_data(level="see_project")
    project = await db.get_project(int(action_data))
    sum_tasks = await db.get_sum_tasks(int(action_data))
    await callback.message.answer(text.project.format(title=project.title, 
                                                      description=project.description, 
                                                      date_creat=project.created_at, 
                                                      sum_tasks=sum_tasks), 
                                                      reply_markup=await kb.project_num(action_data))

@router.callback_query(F.data.startswith("tasks_"))
async def callback_tasks(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.delete_message(chat_id=callback.message.chat.id, 
                             message_id=callback.message.message_id)
    action_data = callback.data[len("tasks_"):]
    await state.update_data(level="see_tasks")
    task = await db.get_task(int(action_data))
    project = await db.get_project(int(task.project_id))
    await callback.message.answer(text.task.format(title=task.title, 
                                                      description=task.description, 
                                                      project=project.title,
                                                      due_date=task.due_date,
                                                      date_creat=task.created_at, 
                                                      status=TASK_STATUSES.get(task.status, "Неизвестный статус"),
                                                      priority=TASK_PRIORITIES.get(task.priority, "Неизвестный приоритет"), 
                                                      updated_at=task.updated_at
                                                      ), 
                                                      reply_markup=await kb.task_num(action_data))

@router.callback_query(F.data.startswith("cr_project_"))
async def callback_cr_project(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.delete_message(chat_id=callback.message.chat.id, 
                             message_id=callback.message.message_id)
    action_data = callback.data[len("cr_project_"):]
    await state.update_data(id_project=action_data)
    await callback.message.answer(text.create_task_name)
    await state.set_state(states.CreateTask.name)

@router.callback_query(F.data.startswith("change_status_"))
async def callback_change_status(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.delete_message(chat_id=callback.message.chat.id, 
                             message_id=callback.message.message_id)

    data_parts = callback.data.split("_")

    if len(data_parts) < 3 or not data_parts[2].isdigit():
        await callback.message.answer("Invalid task ID. Please try again.")
        return

    action_data = int(data_parts[2])
    
    # Если в callback нет статуса, значит, нужно показать клавиатуру выбора статусов
    if len(data_parts) == 3:
        await state.update_data(level='change_status')
        await callback.message.answer(text.change_status_message,
                                      reply_markup=await kb.change_status(action_data))
        return

    new_status = "_".join(data_parts[3:])

    valid_statuses = {
        "not_started", "in_progress", "pending_review",
        "needs_revision", "completed", "canceled", "paused"
    }

    if new_status in valid_statuses:
        await callback.message.answer(text.change_status_finaly)
        await db.update_task_status(action_data, new_status)

@router.callback_query(F.data.startswith("change_priority_"))
async def callback_change_priority(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.delete_message(chat_id=callback.message.chat.id, 
                             message_id=callback.message.message_id)

    data_parts = callback.data.split("_")

    if len(data_parts) < 3 or not data_parts[2].isdigit():
        await callback.message.answer("Invalid task ID. Please try again.")
        return

    action_data = int(data_parts[2])
    
    # Если в callback нет приоритета, значит, нужно показать клавиатуру выбора приоритетов
    if len(data_parts) == 3:
        await state.update_data(level='change_priority')
        await callback.message.answer(text.change_priority_message,
                                      reply_markup=await kb.change_priority(action_data))
        return

    new_priority = "_".join(data_parts[3:])

    valid_priorities = {"none", "low", "medium", "high", "urgent"}

    if new_priority in valid_priorities:
        await callback.message.answer(text.change_priority_finaly)
        await db.update_task_priority(action_data, new_priority)

@router.callback_query(F.data.startswith("change_due_date_"))
async def callback_change_due_date(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)

    action_data = callback.data[len("change_due_date_"):]
    await state.update_data(level='change_due_date', id_task=action_data)
    calendar_keyboard = CalendarKeyboard()
    calendar_markup = calendar_keyboard.get_keyboard()
   
    await state.update_data(month=calendar_keyboard.current_month, year=calendar_keyboard.current_year)

    await callback.message.answer(text.change_task_due, reply_markup=calendar_markup)
    await state.set_state(states.UpdateTask.due_date)

@router.callback_query(F.data.startswith("delete_task_"))
async def callback_delete_task(callback: CallbackQuery, bot: Bot):
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    action_data = callback.data[len("delete_task_"):]
    await callback.message.answer(text.delete_task_finaly)
    await db.delete_task(int(action_data))

@router.callback_query(lambda query: query.data == "next_month")
async def next_month(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    calendar_keyboard = CalendarKeyboard(data['month'], data['year']).next_month()
    calendar_markup = calendar_keyboard.get_keyboard()

    await state.update_data(month=calendar_keyboard.current_month, year=calendar_keyboard.current_year)

    await callback_query.message.edit_text("Выберите день:", reply_markup=calendar_markup)

@router.callback_query(lambda query: query.data == "prev_month")
async def prev_month(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    calendar_keyboard = CalendarKeyboard(data['month'], data['year']).prev_month()
    calendar_markup = calendar_keyboard.get_keyboard()

    await state.update_data(month=calendar_keyboard.current_month, year=calendar_keyboard.current_year)
    await callback_query.message.edit_text("Выберите день:", reply_markup=calendar_markup)

@router.callback_query(lambda query: query.data.startswith("day_"), states.CreateTask.due_date)
async def select_day(callback_query: CallbackQuery, state: FSMContext):
    day = int(callback_query.data.split("_")[1])
    data = await state.get_data()
    calendar_keyboard = CalendarKeyboard(data['month'], data['year'])

    if 1 <= day <= calendar_keyboard.days_in_month:
        selected_date = calendar_keyboard.get_date(day)
        await callback_query.message.edit_text(f"Вы выбрали {selected_date}")

        await state.update_data(due_date=selected_date)
        id_project = data['id_project']
        name = data['name']
        description = data['description']
        user_id = callback_query.from_user.id

        await callback_query.message.answer(
            text.create_task_finaly.format(name=name, description=description, due_date=selected_date),
            reply_markup=kb.menu
        )

        await db.add_task(id_project, name, description, selected_date, user_id)
        await state.clear()
    else:
        await callback_query.message.answer("Пожалуйста, выберите корректный день из календаря.")

@router.callback_query(lambda query: query.data.startswith("day_"), states.UpdateTask.due_date)
async def select_day_update(callback_query: CallbackQuery, state: FSMContext):
    day = int(callback_query.data.split("_")[1])
    data = await state.get_data()
    calendar_keyboard = CalendarKeyboard(data['month'], data['year'])

    if 1 <= day <= calendar_keyboard.days_in_month:
        selected_date = calendar_keyboard.get_date(day)
        await callback_query.message.edit_text(f"Вы выбрали {selected_date}")

        await state.update_data(due_date=selected_date)
        id_task = data['id_task']
        user_id = callback_query.from_user.id

        await callback_query.message.answer(
            text.change_task_due_finaly,
            reply_markup=kb.menu
        )

        await db.update_due(int(id_task), selected_date)
        await state.clear()
    else:
        await callback_query.message.answer("Пожалуйста, выберите корректный день из календаря.")

@router.callback_query()
async def callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    if callback.data == "create_project":
        await bot.delete_message(chat_id=callback.message.chat.id, 
                                 message_id=callback.message.message_id)
        await callback.message.answer(text.create_project, reply_markup=kb.cancel)
        await state.set_state(states.CreateProject.name)
    elif callback.data == "my_projects":
        await bot.delete_message(chat_id=callback.message.chat.id, 
                                 message_id=callback.message.message_id)
        projects = await db.get_projects(callback.from_user.id)
        await callback.message.answer(text.projects_message, 
                                      reply_markup=await kb.my_projects(projects=projects))
        await state.update_data(level="list_project")
    elif callback.data == "tasks":
        await callback.message.answer(text.tasks_message)
    elif callback.data == "create_task":
        projects = await db.get_projects(callback.from_user.id)
        await callback.message.answer(text.choice_project, 
                                      reply_markup=await kb.choice_projects(projects=projects))
        await state.update_data(level="choice_project")
    elif callback.data == "my_tasks":
        await bot.delete_message(chat_id=callback.message.chat.id, 
                                 message_id=callback.message.message_id)
        tasks = await db.get_tasks(callback.from_user.id)
        await callback.message.answer(text.tasks_message_l, 
                                      reply_markup=await kb.my_tasks(tasks=tasks))
        await state.update_data(level="list_task")
    elif callback.data == "back":
        await bot.delete_message(chat_id=callback.message.chat.id, 
                                 message_id=callback.message.message_id)
        data = await state.get_data()
        level = data['level']
        await state.clear()
        if level == "list_project":
            await callback.message.answer(text.project_message, reply_markup=kb.project)
        elif level == "see_project":
            projects = await db.get_projects(callback.from_user.id)
            await callback.message.answer(text.projects_message,
                                          reply_markup=await kb.my_projects(projects=projects))
        elif level == "list_task":
            await callback.message.answer(text.tasks_message, reply_markup=kb.task)
        elif level == "see_tasks":
            tasks = await db.get_tasks(callback.from_user.id)
            await callback.message.answer(text.tasks_message_l,
                                          reply_markup=await kb.my_tasks(tasks=tasks))
        elif level == "choice_project":
            projects = await db.get_projects(callback.from_user.id)
            await callback.message.answer(text.choice_project,
                                          reply_markup=await kb.choice_projects(projects=projects))
        elif level == "change_status":
            tasks = await db.get_tasks(callback.from_user.id)
            await callback.message.answer(text.tasks_message_l,
                                          reply_markup=await kb.my_tasks(tasks=tasks))
