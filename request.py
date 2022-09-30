from cgitb import text
from email import header
from aiogram.dispatcher.filters.state import StatesGroup, State

class Request_reg(StatesGroup):
    
    header = State()
    text = State()
    comfer = State()