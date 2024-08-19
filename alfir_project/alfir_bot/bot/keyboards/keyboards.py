from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def share_contact() -> ReplyKeyboardMarkup:
    
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Share contact', request_contact=True)
    keyboard.add(button)

    return keyboard


def cancel_kb() -> ReplyKeyboardMarkup:

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)    
    button = KeyboardButton('/stop')
    keyboard.add(button)

    return keyboard


def without_password() -> ReplyKeyboardMarkup:

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)    
    button = KeyboardButton('Без пароля')
    keyboard.add(button)

    return keyboard