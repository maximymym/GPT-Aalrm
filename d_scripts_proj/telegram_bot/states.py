from aiogram.fsm.state import State, StatesGroup

class AddScriptStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_type = State()
    waiting_for_price = State()
    waiting_for_video_url = State()
