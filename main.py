import telebot
from telebot import custom_filters
from telebot.storage import StateMemoryStorage

from tgbot.files.config import token
from tgbot.handlers.user import *

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(token, state_storage=state_storage, parse_mode='HTML')


def register_handlers():
    register_m_handler(start, None, None, ['start'])
    bot.register_message_handler(handle_contacts, content_types=['contact'], state=MyStates.get_number_st,
                                 pass_bot=True)
    register_m_handler(handle_text_message, None, MyStates.get_number_st, None)



# To shorten the "register_message_handler" code
def register_m_handler(func, text, state, commands):
    return bot.register_message_handler(func, text=text, state=state, commands=commands, pass_bot=True)


# function that returns all sentences with the same meaning
def lang_texts(list, text_index):
    texts = []
    # if text_index is -1, it returns all sentences in the list
    if text_index == -1:
        return [elem for sublist in list for elem in sublist]

    for k in list:
        texts.append(k[text_index])
    return texts


def run():
    bot.infinity_polling(skip_pending=True)


register_handlers()

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.IsDigitFilter())
run()
