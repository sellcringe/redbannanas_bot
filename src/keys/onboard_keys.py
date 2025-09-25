import json

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def cmd_start():
    kb = ReplyKeyboardBuilder()

    kb.button(text='☑️Поехали')

    return kb.as_markup(resize_keyboard=True)



def method_work():
    rows = []

    rows.append([InlineKeyboardButton(text="📄Трудовой договор", callback_data="employment contract")])
    rows.append([InlineKeyboardButton(text="📄Договор услуг с самозанятым/ГПХ/ИП", callback_data="agreement with an entrepreneur")])
    return InlineKeyboardMarkup(inline_keyboard=rows)



def work_form():
    rows = [[InlineKeyboardButton(text="☑️Анкета заполнена", callback_data="form complete")]]
    return InlineKeyboardMarkup(inline_keyboard=rows)



def story_complete_key():
    rows = [[InlineKeyboardButton(text="☑️Рассказ подготовил, что дальше?", callback_data="story complete")]]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def send_check_list():
    rows = [[InlineKeyboardButton(text="☑️«Что дальше?»", callback_data="send check list")]]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def send_access_complete():
    rows = [[InlineKeyboardButton(text="☑️Авторизовался в сервисах»»", callback_data="send access complete")]]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_meet():
    rows = [[InlineKeyboardButton(text="☑️Понял, пошёл на встречу", callback_data="go meet")]]
    return InlineKeyboardMarkup(inline_keyboard=rows)
