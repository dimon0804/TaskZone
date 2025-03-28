from sqlalchemy.future import select
from .models import User, Project, Task, async_session


async def add_user(tg_id: int, name: str) -> User:
    """ Создать пользователя """
    async with async_session() as session:
        async with session.begin():
            user = User(tg_id=tg_id, name=name)
            session.add(user)
            await session.commit()
            return user

async def get_user(tg_id: int):
    """ Получить пользователя по Telegram ID """
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        return result.scalars().first()
    
async def add_project(tg_id: int, title: str, description: str):
    """ Создание проекта """
    async with async_session() as session:
        async with session.begin():
            user = await get_user(tg_id)
            if user:
                project = Project(user_id=user.id, title=title, description=description)
                session.add(project)
                await session.commit()
                return project
            else:
                return None
            
async def get_projects(tg_id: int):
    """ Получение проектов пользователя """
    async with async_session() as session:
        user = await get_user(tg_id)
        if user:
            result = await session.execute(select(Project).where(Project.user_id == user.id))
            return result.scalars().all()
        else:
            return None
        
async def get_project(id: int):
    """ Получение проекта по ID """
    async with async_session() as session:
        result = await session.execute(select(Project).where(Project.id == id))
        return result.scalars().first()
    
async def get_sum_tasks(id: int):
    """ Получение количества задач в проекте """
    async with async_session() as session:
        result = await session.execute(select(Task).where(Task.project_id == id))
        tasks = result.scalars().all()
        return len(tasks)
        
async def check_name_project(title: str):
    """ Проверка на существование проекта """
    async with async_session() as session:
        result = await session.execute(select(Project).where(Project.title == title))
        return result.scalars().first()
    
async def add_task(id_project: int, title: str, description: str, due_date: str, user_id: int):
    """ Создание задачи """
    async with async_session() as session:
        async with session.begin():
            project = await get_project(int(id_project))
            user = await get_user(user_id)
            if project:
                task = Task(user_id=user.id, assigned_to=user.id, project_id=project.id, title=title, description=description, due_date=due_date)
                session.add(task)
                await session.commit()
                return task
            else:
                return None

async def get_tasks(tg_id: int):
    """ Получение задач пользователя """
    async with async_session() as session:
        user = await get_user(tg_id)
        if user:
            result = await session.execute(select(Task).where(Task.user_id == user.id))
            return result.scalars().all()
        else:
            return None

async def get_task(id: int):
    """ Получение задачи по ID """
    async with async_session() as session:
        result = await session.execute(select(Task).where(Task.id == id))
        return result.scalars().first()
    
async def update_task_status(id: int, status: str):
    """ Обновление статуса задачи """
    async with async_session() as session:
        async with session.begin():
            task = await get_task(id)
            if task:
                task.status = status
                session.add(task)
                await session.commit()
                return task
            else:
                return None
            
async def update_task_priority(id: int, priority: str):
    """ Обновление приоритета задачи """
    async with async_session() as session:
        async with session.begin():
            task = await get_task(id)
            if task:
                task.priority = priority
                session.add(task)
                await session.commit()
                return task
            else:
                return None

async def update_due(task_id: int, due_date: str):
    """ Обновление срока задачи """
    async with async_session() as session:
        async with session.begin():
            task = await get_task(task_id)
            if task:
                task.due_date = due_date
                session.add(task)
                await session.commit()
                return task
            else:
                return None

async def delete_task(id: int):
    """ Удаление задачи """
    async with async_session() as session:
        async with session.begin():
            task = await get_task(id)
            if task:
                await session.delete(task)
                await session.commit()
                return True
            else:
                return False
            
async def get_tasks_by_project(project_id: int):
    """ Получение задач по ID проекта """
    async with async_session() as session:
        result = await session.execute(select(Task).where(Task.project_id == project_id))
        return result.scalars().all()
    
async def delete_project(id: int):
    """ Удаление проекта """
    async with async_session() as session:
        async with session.begin():
            project = await get_project(id)
            if project:
                await session.execute(Task.__table__.delete().where(Task.project_id == id))
                await session.delete(project)
                await session.commit()
                return True
            else:
                return False