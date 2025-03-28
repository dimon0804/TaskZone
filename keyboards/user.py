from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

menu = ReplyKeyboardMarkup(resize_keyboard=True, 
                                keyboard=[
                                    [KeyboardButton(text='Быстрая задача')],
                                    [KeyboardButton(text='Проекты'), KeyboardButton(text='Задачи')], 
                                    [KeyboardButton(text='Профиль')]])

cancel = ReplyKeyboardMarkup(resize_keyboard=True, 
                                keyboard=[
                                    [KeyboardButton(text='Отмена')]])

project = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать проект', callback_data='create_project'), 
     InlineKeyboardButton(text='Мои проекты', callback_data='my_projects')],
])

task = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать задачу', callback_data='create_task'), 
     InlineKeyboardButton(text='Мои задачи', callback_data='my_tasks')],
])

async def my_projects(projects):
    if not projects:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='У вас нет проектов', callback_data='back')]])

    keyboard = [
        [InlineKeyboardButton(text=project.title, callback_data=f'project_{project.id}')]
        for project in projects
    ]
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data='back')])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def project_num(project_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Посмотреть задачи", callback_data=f'see_tasks_{project_id}'), 
         InlineKeyboardButton(text='Добавить задачу', callback_data=f'add_task_{project_id}')],
        [InlineKeyboardButton(text='Удалить проект', callback_data=f'delete_project_{project_id}')],
        [InlineKeyboardButton(text='Назад', callback_data='back')]
    ])

async def task_num(task_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить статус", callback_data=f'change_status_{task_id}'),
        InlineKeyboardButton(text="Изменить приоритет", callback_data=f'change_priority_{task_id}'),
        InlineKeyboardButton(text="Изменить дедлайн", callback_data=f'change_due_date_{task_id}')],

        [InlineKeyboardButton(text="Удалить задачу", callback_data=f'delete_task_{task_id}')],
        [InlineKeyboardButton(text='Назад', callback_data='back')]
    ])

async def choice_projects(projects):
    if not projects:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='У вас нет проектов', callback_data='back')]])

    keyboard = [
        [InlineKeyboardButton(text=project.title, callback_data=f'cr_project_{project.id}')]
        for project in projects
    ]
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data='back')])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def my_tasks(tasks):
    if not tasks:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='У вас нет задач', callback_data='back')]])

    keyboard = [
        [InlineKeyboardButton(text=task.title, callback_data=f'tasks_{task.id}')]
        for task in tasks
    ]
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data='back')])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def change_status(action_data):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Не начато", callback_data=f'change_status_{action_data}_not_started')],
        [InlineKeyboardButton(text="В процессе", callback_data=f'change_status_{action_data}_in_progress')],
        [InlineKeyboardButton(text="Ожидание проверки", callback_data=f'change_status_{action_data}_pending_review')],
        [InlineKeyboardButton(text="Требует доработки", callback_data=f'change_status_{action_data}_needs_revision')],
        [InlineKeyboardButton(text="Завершено", callback_data=f'change_status_{action_data}_completed')],
        [InlineKeyboardButton(text="Отменено", callback_data=f'change_status_{action_data}_canceled')],
        [InlineKeyboardButton(text="Приостановлено", callback_data=f'change_status_{action_data}_paused')],
        [InlineKeyboardButton(text="Назад", callback_data='back')]
    ])

async def change_priority(action_data):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Без приоритета", callback_data=f'change_priority_{action_data}_none')],
        [InlineKeyboardButton(text="Низкий", callback_data=f'change_priority_{action_data}_low')],
        [InlineKeyboardButton(text="Средний", callback_data=f'change_priority_{action_data}_medium')],
        [InlineKeyboardButton(text="Высокий", callback_data=f'change_priority_{action_data}_high')],
        [InlineKeyboardButton(text="Срочный", callback_data=f'change_priority_{action_data}_urgent')],
        [InlineKeyboardButton(text="Назад", callback_data='back')]
    ])

miss = ReplyKeyboardMarkup(resize_keyboard=True, 
                                keyboard=[
                                    [KeyboardButton(text='Пропуск')]])

async def task_notif(task_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Посмотреть задачу", callback_data=f'tasks_{task_id}')],
        [InlineKeyboardButton(text="Изменить статус", callback_data=f'change_status_{task_id}')],
    ])
