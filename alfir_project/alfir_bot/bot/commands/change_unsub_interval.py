from aiogram.types import Message
from utils.redis import set_unsub_interval

async def change_interval_cmd(message: Message):

    min = message.text.split(' ')[-2].replace('-', '')
    max = message.text.split(' ')[-1]

    try:

        if int(min) < int(max):

            set_unsub_interval(min, max)
            await message.answer(f'Интервал отписки изменен на {min}-{max} часов')

        else:
            await message.answer('Неверно введенный интервал {min} не меньше {max}')

    except ValueError:

        await message.answer('Значения должны быть числами')

    