start_message = """📌 Привет, {name}!
Добро пожаловать в умного помощника по управлению задачами! Теперь твое время – в надежных руках. Планируй, организовывай и достигай целей легко. 🚀

Начнем?"""
project_message = """🌟 Проекты - это место, где каждая задача становится важной частью нашего плана. Они могут быть простыми, но они могут быть такими сложными, что их выполнение может быть непростым. Но не бойтесь, у нас есть способ помочь вам сделать каждую задачу легким и эффективным.

Наша цель – помочь вам стать более эффективным и умным, чтобы достигать своих целей. Начните с простых задач и постепенно переходите к сложным. Наша помощь – это ваша задача!"""
tasks_message = """📝 Задачи - это ключ к успеху. Они могут быть простыми, но они могут быть такими сложными, что их выполнение может быть непростым. Но не бойтесь, у нас есть способ помочь вам сделать каждую задачу легким и эффективным.

Наша цель – помочь вам стать более эффективным и умным, чтобы достигать своих целей. Начните с простых задач и постепенно переходите к сложным. Наша помощь – это ваша задача!"""
create_project = """📝 Создание проекта - это просто! Просто напишите название вашего проекта и начните планировать свои задачи. Наша помощь – это ваша задача!"""
create_project_description = """📝 Пожалуйста, введите описание вашего проекта. Это поможет нам лучше понять ваши цели и задачи, чтобы предоставить вам наилучшую помощь."""
create_project_finaly = """📝 Поздравляем! Вы успешно создали проект. Теперь вы можете начать планировать свои задачи и достигать своих целей. Наша помощь – это ваша задача!

Ваш проект: 
Название: {title}
Описание: {description}"""
projects_message = """📝 Вот список ваших проектов:"""
project = """Проект: {title}

Был создан: {date_creat}
Количество задач в проекте: {sum_tasks}

Описание проекта: {description}"""
create_project_name_error = """Данное название проекта уже существует... 

Введите <b>уникальное</b> название"""
delete_project_finaly = "Вы удалили этот проект."

create_task = """📝 Создание задачи - это просто! Просто напишите название вашей задачи и начните планировать свои задачи. Наша помощь – это ваша задача!"""
choice_project = """Выберите проект в котором хотите создать задачу"""
create_task_name = """Название задачи"""
create_task_description = """📝 Пожалуйста, введите описание вашей задачи. Это поможет нам лучше понять ваши цели и задачи, чтобы предоставить вам наилучшую помощь."""
create_task_due = """📝 Пожалуйста, введите срок выполнения задачи. Это поможет нам лучше понять ваши цели и задачи, чтобы предоставить вам наилучшую помощь."""
create_task_finaly = """📝 Поздравляем! Вы успешно создали задачу. Теперь вы можете начать планировать свои задачи и достигать своих целей. Наша помощь – это ваша задача!

Задача: {name}
описание: {description}
дедлайн: {due_date}"""
create_task_name_error = """Данное название задачи уже существует...

Введите <b>уникальное</b> название"""
tasks_message_l = """📝 Вот список ваших задач:"""
task = """Задача: {title}

Была создана: {date_creat}
Обновлена: {updated_at}
Дедлайн: {due_date}
Статус: {status}
Приоритет: {priority}
Проект: {project}
Описание задачи: {description}"""

cancel = 'Действие отменено...'

change_status_message = """Выберите статус задачи"""
change_status_finaly = """Статус задачи успешно изменен!"""
change_priority_message = """Выберите приоритет задачи"""
change_priority_finaly = """Приоритет задачи успешно изменен!"""
change_task_due = "Выберите дату"
change_task_due_finaly = "Срок выполнения задачи успешно изменен!"
delete_task_finaly = "Вы успешно удалили задачу"

profile_message = """Профиль: {fullname}

Зарегистрирован с: {date_reg}
Всего проектов: {count_project}
Всего задач: {count_task}"""

settings_notif_message = "Выберете нужное вам время для оповещения о дедлайнах"
settings_notif_finaly = "Вы изменили время отправки оповещений о дедлайнах на {time}"

reminders_message = """🔔 Напоминания помогут не забыть о важных делах! Выберите удобный день и время, чтобы бот напомнил вам о нужном событии."""
reminder_message = """Напоминание: {title}

Текст напоминания: {text}
Дата напоминания: {date}
Время напоминания: {time}
Правило напоминания: {rules}

Дата создания напоминания: {created_at}"""
delete_reminder_finaly = "Ваше напоминание удалено"
create_reminder = "Отлично! Напишите название нового напоминания"
create_reminder_text = "Введите текст напоминания"
create_reminder_date = "Выберите дату напоминания"
create_reminder_time = "Выберите время напоминания"
create_reminder_rules = "Выберите правило напоминания"
create_reminder_finaly = """🔔 Новое напоминание успешно создано!

Напоминание: {title}
Текст напоминания: {text}
Дата напоминания: {date}
Время напоминания: {time}
Правило напоминания: {rules}
Дата создания напоминания: {created_at}"""