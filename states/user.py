from aiogram.fsm.state import State, StatesGroup

class CreateProject(StatesGroup):
    name = State()
    description = State()

class CreateTask(StatesGroup):
    name = State()
    description = State()
    due_date = State()
    
class UpdateTask(StatesGroup):
    due_date = State()

class SettingsNotif(StatesGroup):
    time = State()

class CreateReminder(StatesGroup):
    title = State()
    text = State()
    date = State()
    time = State()
    rules = State()

class PomodoroState(StatesGroup):
    waiting_for_description = State()
    working = State()
