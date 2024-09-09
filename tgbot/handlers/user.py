from telebot import TeleBot
import requests
from io import BytesIO

from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

# for state
from tgbot.states.state import MyStates

# messages
from tgbot.texts.messages import *

# for use keyboards
from tgbot.helpers.keyboards import reply_markup  # , inline_markup
from tgbot.texts.text_reply import *

# for use database
from tgbot.helpers.database import SQLite
from tgbot.files.config import db_path

API_URL = 'https://back.geolink.uz/api/v1/telegram/get/data'


def start(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, msg_start)
    bot.set_state(message.from_user.id, MyStates.start, message.chat.id)
    get_phone_number(message, bot)


def get_phone_number(message: Message, bot: TeleBot):
    message.text.isdigit()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button = KeyboardButton(text=get_contact_btn, request_contact=True)
    markup.add(contact_button)
    bot.send_message(message.chat.id, ask_phone_number, reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.get_number_st, message.chat.id)


def handle_contacts(message: Message, bot: TeleBot):
    user_id = message.from_user.id
    phone_number = message.contact.phone_number

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['phone'] = message.contact.phone_number

    response(message, bot)


def handle_text_message(message: Message, bot: TeleBot):
    phone_number = message.text.strip()
    try:
        n = int(message.text)
    except Exception as e:
        bot.send_message(message.chat.id, contact_int)
        bot.set_state(message.from_user.id, MyStates.get_number_st, message.chat.id)
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone'] = message.text.strip()
        response(message, bot)


def response(message: Message, bot: TeleBot):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        phone_number = data.get('phone')

    api_response = requests.post(API_URL, json={'phone': phone_number})

    if api_response.status_code == 200:
        response_data = api_response.json()

        if response_data.get('status'):
            pdf_url = response_data.get('data')
            if pdf_url:
                bot.send_document(message.chat.id, pdf_url)
                bot.send_message(message.chat.id, 'Sizning Malumotingiz')
            else:
                bot.send_message(message.chat.id, "PDF fayl topilmadi")
        else:
            bot.send_message(message.chat.id, "Telefon raqami ma'lumotlar bazasida topilmadi.")
    else:
        bot.send_message(message.chat.id, "Telefon raqamini tekshirishda xatolik yuz berdi.")
