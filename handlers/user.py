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
import re
import asyncio
from utils import ai_manager 

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
    await message.answer(text.create_task_description, reply_markup=kb.miss)
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

@router.message(states.SettingsNotif.time)
async def settings_notif_time(message: Message, state: FSMContext):
    if message.text.lower() in ['отмена', '/cancel']:
        await state.clear()
        await message.answer(text.cancel, reply_markup=kb.menu)
        return
    
    # Check if the input matches the HH:MM format
    if not message.text or not re.match(r"^(?:[01]?\d|2[0-3]):[0-5]\d$", message.text):
        await message.answer("Пожалуйста, введите время в формате HH:MM (например, 00:30 или 14:30).")
        return
    
    await state.update_data(time=message.text)
    data = await state.get_data()
    time = data['time']
    await message.answer(text.settings_notif_finaly.format(time=time),
                         reply_markup=kb.menu)
    await db.update_time(message.from_user.id, time)
    await state.clear()

@router.message(states.CreateReminder.title)
async def create_reminder_title(message: Message, state: FSMContext):
    if message.text.lower() in ['отмена', '/cancel']:
        await state.clear()
        await message.answer(text.cancel, reply_markup=kb.menu)
        return
    await state.update_data(title=message.text)
    await message.answer(text.create_reminder_text)
    await state.set_state(states.CreateReminder.text)

@router.message(states.CreateReminder.text)
async def create_reminder_text(message: Message, state: FSMContext):
    if message.text.lower() in ['отмена', '/cancel']:
        await state.clear()
        await message.answer(text.cancel, reply_markup=kb.menu)
        return
    await state.update_data(text=message.text)
    calendar_keyboard = CalendarKeyboard()
    calendar_markup = calendar_keyboard.get_keyboard()
   
    await state.update_data(month=calendar_keyboard.current_month, year=calendar_keyboard.current_year)
    await message.answer(text.create_reminder_date, reply_markup=calendar_markup)
    await state.set_state(states.CreateReminder.date)

# @router.message(states.CreateReminder.date)
# async def create_reminder_date(message: Message, state: FSMContext):
#     if message.text.lower() in ['отмена', '/cancel']:
#         await state.clear()
#         await message.answer(text.cancel, reply_markup=kb.menu)
#         return
#     await state.update_data(date=message.text)
#     calendar_keyboard = CalendarKeyboard()
#     calendar_markup = calendar_keyboard.get_keyboard()
   
#     await state.update_data(month=calendar_keyboard.current_month, year=calendar_keyboard.current_year)
#     await message.answer(text.create_reminder_time, reply_markup=calendar_markup)
#     await state.set_state(states.CreateReminder.time)

@router.message(states.CreateReminder.time)
async def create_reminder_time(message: Message, state: FSMContext):
    if message.text.lower() in ['отмена', '/cancel']:
        await state.clear()
        await message.answer(text.cancel, reply_markup=kb.menu)
        return
    
    if not message.text or not re.match(r"^(?:[01]?\d|2[0-3]):[0-5]\d$", message.text):
        await message.answer("Пожалуйста, введите время в формате HH:MM (например, 00:30 или 14:30).")
        return
    
    await state.update_data(time=message.text)
    await message.answer(text.create_reminder_rules, reply_markup=kb.rules)
    await state.set_state(states.CreateReminder.rules)

@router.message(states.CreateReminder.rules)
async def create_reminder_rules(message: Message, state: FSMContext):
    if message.text.lower() in ['отмена', '/cancel']:
        await state.clear()
        await message.answer(text.cancel, reply_markup=kb.menu)
        return
    await state.update_data(rules=message.text)
    data = await state.get_data()
    title = data['title']
    text_c = data['text']
    date = data['date']
    time = data['time']
    rules = data['rules']
    await message.answer(text.create_reminder_finaly.format(title=title,
                                                           text=text_c,
                                                           date=date,
                                                           time=time,
                                                           rules=rules,
                                                           created_at=message.date),
                                                           reply_markup=kb.menu)
    await db.add_reminder(message.from_user.id, title, text_c, date, time, rules)
    await state.clear()

@router.message(states.PomodoroState.working, F.text.lower() == "завершить задачу")
async def finish_task(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("✅ Задача завершена! Вы отлично поработали.", reply_markup=kb.menu)

async def pomodoro_cycle(message: Message, state: FSMContext):
    work_time = 25 * 60  # 25 минут работы
    rest_time = 5 * 60   # 5 минут отдыха

    while True:
        user_state = await state.get_state()
        if user_state != states.PomodoroState.working:
            break
        
        await message.answer("⏰ Время работать! Сосредоточьтесь на задаче.")
        await asyncio.sleep(work_time)

        user_state = await state.get_state()
        if user_state != states.PomodoroState.working:
            break
        
        await message.answer("🎉 Отличная работа! Теперь 5 минут отдыха.")
        await asyncio.sleep(rest_time)

@router.message(states.PomodoroState.waiting_for_description)
async def process_task_description(message: Message, state: FSMContext):
    await state.update_data(task_description=message.text)

    await message.answer(
        "Описание задачи сохранено! ⏳ Начинаем работать по методу Помидоро! "
        "Но для начала искусственный интеллект даст рекомендации... Пожалуйста, подождите немного.", 
        reply_markup=kb.pomodoro_kb
    )

    sent_message = await message.answer("⌛ Генерация...")

    full_text = ""

    # Потоковая обработка данных
    async for chunk in ai_manager.ai_manager_stream(message.text):
        full_text = chunk
        if full_text.strip():
            try:
                await sent_message.edit_text(
                    f"Ответ от нейросети:\n\n<blockquote>{full_text}</blockquote>",
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Ошибка редактирования: {e}")

            # Задержка, чтобы не перегрузить Telegram
            await asyncio.sleep(1)
    await state.set_state(states.PomodoroState.working)
    asyncio.create_task(pomodoro_cycle(message, state)) 

# Обработчик текстовых сообщений
@router.message(F.content_type == ContentType.TEXT)
async def text_message(message: Message, state: FSMContext):
    if message.text.lower() in ['проекты', '/project']:
        await message.answer(text.project_message, reply_markup=kb.project)
    
    elif message.text.lower() in ['задачи', '/tasks']:
        await message.answer(text.tasks_message, reply_markup=kb.task)
    
    elif message.text.lower() in ['профиль', '/profile']:
        user = await db.get_user(message.from_user.id)
        date_reg = user.created_at
        count_project = len(await db.get_projects(message.from_user.id))
        count_task = len(await db.get_tasks(message.from_user.id))
        await message.answer(
            text.profile_message.format(
                date_reg=date_reg,
                count_project=count_project,
                count_task=count_task,
                fullname=message.from_user.full_name
            ),
            reply_markup=kb.menu
        )
    
    elif message.text.lower() in ['напоминания', "/notifications"]:
        await message.answer(text.settings_notif_message, reply_markup=kb.notif)
    
    elif message.text.lower() in ['отмена', '/cancel']:
        await state.clear()
        await message.answer(text.cancel, reply_markup=kb.menu)
    
    elif message.text.lower() == "быстрая задача":
        await message.answer("Отлично! Опишите задачу, которую хотите выполнить:")
        await state.set_state(states.PomodoroState.waiting_for_description)

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
 
@router.callback_query(lambda query: query.data.startswith("see_tasks_"))
async def see_tasks(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(level='see_tasks')
    action_data = int(callback_query.data[len("see_tasks_"):])
    await callback_query.message.answer(text.tasks_message_l,
                                        reply_markup=await kb.my_tasks(await db.get_tasks_by_project(action_data)))

@router.callback_query(lambda query: query.data.startswith("add_task_"))
async def add_task(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(level='add_task')
    action_data = int(callback_query.data[len("add_task_"):])
    await state.update_data(id_project=action_data)
    await callback_query.message.answer(text.create_task_name)
    await state.set_state(states.CreateTask.name)

@router.callback_query(lambda query: query.data.startswith("delete_project_"))
async def delete_project(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(level='delete_project')
    action_data = int(callback_query.data[len("delete_project_"):])
    await callback_query.message.answer(text.delete_project_finaly)
    await db.delete_project(action_data)

@router.callback_query(lambda query: query.data.startswith("reminder_"))
async def reminder(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                                 message_id=callback_query.message.message_id)
    await state.update_data(level='reminder')
    action_data = int(callback_query.data[len("reminder_"):])
    reminder_data = await db.get_reminder(action_data)
    await callback_query.message.answer(text.reminder_message.format(title=reminder_data.title, 
                                                                     text=reminder_data.text, 
                                                                     date=reminder_data.date, 
                                                                     time=reminder_data.time, 
                                                                     rules=reminder_data.rules, 
                                                                     created_at=reminder_data.created_at),
                                        reply_markup=await kb.reminder_num(action_data))
    
@router.callback_query(lambda query: query.data.startswith("delete_reminder_"))
async def delete_reminder(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                                 message_id=callback_query.message.message_id)
    await state.update_data(level='delete_reminder')
    action_data = int(callback_query.data[len("delete_reminder_"):])
    await callback_query.message.answer(text.delete_reminder_finaly)
    await db.delete_reminder(action_data)

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
        await callback_query.message.answer("Пожалуйста, выберите корректный день из календаря.", reply_markup=kb.menu)

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

@router.callback_query(lambda query: query.data.startswith("day_"), states.CreateReminder.date)
async def select_day_reminder(callback_query: CallbackQuery, state: FSMContext):
    day = int(callback_query.data.split("_")[1])
    data = await state.get_data()
    calendar_keyboard = CalendarKeyboard(data['month'], data['year'])

    if 1 <= day <= calendar_keyboard.days_in_month:
        selected_date = calendar_keyboard.get_date(day)
        await callback_query.message.edit_text(f"Вы выбрали {selected_date}")

        await state.update_data(date=selected_date)

        await callback_query.message.answer(
            text.create_reminder_time,
            reply_markup=kb.settings_notif
        )
        await state.set_state(states.CreateReminder.time)
    else:
        await callback_query.message.answer("Пожалуйста, выберите корректный день из календаря.", reply_markup=kb.menu)

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
    elif callback.data == "settings_notif":
        await bot.delete_message(chat_id=callback.message.chat.id, 
                                 message_id=callback.message.message_id)
        await callback.message.answer(text.settings_notif_message, reply_markup=kb.settings_notif)
        await state.set_state(states.SettingsNotif.time)
    elif callback.data == "reminders":
        await bot.delete_message(chat_id=callback.message.chat.id, 
                                 message_id=callback.message.message_id)
        await callback.message.answer(text.reminders_message, reply_markup=kb.reminders)
        await state.update_data(level="reminders")
    elif callback.data == "my_reminders":
        await bot.delete_message(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id)
        reminders = await db.get_reminders(callback.from_user.id)
        await callback.message.answer(text.reminders_message, reply_markup=await kb.my_reminders(reminders))
        await state.update_data(level="my_reminders")
    elif callback.data == "create_reminder":
        await bot.delete_message(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id)
        await callback.message.answer(text.create_reminder, reply_markup=kb.cancel)
        await state.set_state(states.CreateReminder.title)
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
        elif level == "change_priority":
            tasks = await db.get_tasks(callback.from_user.id)
            await callback.message.answer(text.tasks_message_l,
                                          reply_markup=await kb.my_tasks(tasks=tasks))
        elif level == "reminders":
            await callback.message.answer(text.reminders_message, reply_markup=kb.reminders)
        elif level == "my_reminders":
            reminders = await db.get_reminders(callback.from_user.id)
            await callback.message.answer(text.reminders_message, reply_markup=await kb.my_reminders(reminders))
