from telebot.handler_backends import State, StatesGroup  # States


class MyStates(StatesGroup):
    start = State()
    get_number_st = State()
    menu = State()
