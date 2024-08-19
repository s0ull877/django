import random
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from utils.Fsm import ClientDataForm
from utils.client_actions import configurate_client, client_online
from utils.others import init_worker

from keyboards import change_ikb, cancel_ikb


async def cancel_callback(callback: CallbackQuery, state: FSMContext):
     
    await ClientDataForm.File.set()
    async with state.proxy() as data:

        info = 'Данные:'
        for k, v in data['settings'].items():
            v = 'Не указано' if v == None else v
            info += f'\n{k}: {v}'

    await callback.message.answer(info, reply_markup=change_ikb())
    await callback.message.delete()


async def change_callback(callback: CallbackQuery, state: FSMContext):

    arg = callback.data.split(':')[-1]
    await callback.message.delete()

    if arg == 'name':
        
        await callback.message.answer('Введите сообщение вида:\nfirst_name last_name - это поменяет имя и фамилию\nили же просто напишите имя если не хотите менять last_name', reply_markup=cancel_ikb())
        await ClientDataForm.FullName.set()

    elif arg == 'bio':

        await callback.message.answer('Введите bio для пользователя(максимум 128 символов, не используйте Enter)', reply_markup=cancel_ikb())
        await ClientDataForm.Bio.set()
    
    elif arg == 'photo':

        await callback.message.answer('Введите тему аватарки', reply_markup=cancel_ikb())
        await ClientDataForm.Query.set()
    
    elif arg == 'username':

        await callback.message.answer('Введите <a href="https://t.me/username_bot?start=start">доступный username</a>:', reply_markup=cancel_ikb(), parse_mode='HTML')
        await ClientDataForm.Username.set()

    else:

            async with state.proxy() as data:

                data['settings'][arg] = not data['settings'][arg]  

                info = 'Данные:'
                for k, v in data['settings'].items():
                    v = 'Не указано' if v == None else v
                    info += f'\n{k}: {v}'

                await callback.message.answer(info, reply_markup=change_ikb())


async def send_data_callback(callback: CallbackQuery, state: FSMContext):
     
    async with state.proxy() as data:

        settings = data['settings']
        settings['file_name'] = data['file_name']
        settings['chat_id'] = data['chat_id']
        send_request = settings['init']


    await callback.answer('Начинаем настройку...')
    await callback.message.delete()
    await configurate_client(settings)

    if send_request:
    
        worker_tg_id = settings['file_name'].split('.')[0]
        await init_worker(worker_tg_id, settings['first_name'], settings['phone'])

    
    await state.finish()

