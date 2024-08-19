from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def change_ikb() -> InlineKeyboardMarkup:
    
    ikeyboard = InlineKeyboardMarkup(row_width=1)

    ikeyboard.add(InlineKeyboardButton(text='Изменить имя', callback_data='change:name'))
    ikeyboard.add(InlineKeyboardButton(text='Изменить bio', callback_data='change:bio'))
    ikeyboard.add(InlineKeyboardButton(text='Изменить фото профиля', callback_data='change:photo'))
    ikeyboard.add(InlineKeyboardButton(text='Изменить юзернейм', callback_data='change:username'))
    ikeyboard.add(InlineKeyboardButton(text='Изменить отображение статуса', callback_data='change:hidden_status'))
    ikeyboard.add(InlineKeyboardButton(text='Отправить', callback_data='send'))

    return ikeyboard


def cancel_ikb() -> InlineKeyboardMarkup:
    
    ikeyboard = InlineKeyboardMarkup(row_width=1)

    ikeyboard.add(InlineKeyboardButton(text='Отмена', callback_data='cancel'))

    return ikeyboard



def type_code(digits: str='', digit: str='' ) -> InlineKeyboardMarkup:
    
    ikeyboard = InlineKeyboardMarkup(row_width=3)
    ikeyboard.add(InlineKeyboardButton(text=f'Код: {digits}', callback_data='temp'))

    for i in range(1,10,3):
        buttons_row = []

        for n in range(i, i+3):
            
            button = InlineKeyboardButton(text=n, callback_data=f'code:{digits}{n}')
            buttons_row.append(button)

        ikeyboard.add(*buttons_row)

    last_row = [
        InlineKeyboardButton(text='🔙', callback_data=f'clear:{digits}'),
        InlineKeyboardButton(text='0', callback_data=f'code:{digits}0'),
        InlineKeyboardButton(text='🔙', callback_data=f'clear:{digits}')
    ]

    ikeyboard.add(*last_row)
    return ikeyboard


def type_finish(digits: str):
    
    ikeyboard = InlineKeyboardMarkup()

    ikeyboard.add(
        InlineKeyboardButton(text=f'Код: {digits}', callback_data='temp')
    )
    
    last_row = [
        InlineKeyboardButton(text='🔙', callback_data=f'clear:{digits}'),
        InlineKeyboardButton(text='✅', callback_data=f'send:{digits}')
    ]
    ikeyboard.add(*last_row)


    return ikeyboard