from aiogram.fsm.state import State, StatesGroup

class CreateProject(StatesGroup):
    name = State()
    description = State()
    