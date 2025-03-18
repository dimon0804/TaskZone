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
        project = result.scalars().first()
        if project:
            return len(project.id)
        else:
            return 0
        
async def check_name_project(title: str):
    """ Проверка на существование проекта """
    async with async_session() as session:
        result = await session.execute(select(Project).where(Project.title == title))
        return result.scalars().first()
    