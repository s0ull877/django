from aiogram.types import Message
from utils.redis import set_interval

async def change_interval_cmd(message: Message):

    interval = message.text.split(' ')[-1]

    if not interval.isdigit():

        await message.answer('Некорректный ввод интервала!')
        return
    
    set_interval(interval)
    await message.answer(f'Интеврал в 0-{interval} минут установлен.')


    