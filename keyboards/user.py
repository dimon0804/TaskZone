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