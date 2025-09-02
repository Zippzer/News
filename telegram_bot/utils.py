from aiogram.fsm.state import StatesGroup,State


class Post(StatesGroup):
    topic = State()
    dashboard_url = State()
    indicators = State()
    date = State()