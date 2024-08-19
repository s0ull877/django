from aiogram.types import Message, ReplyKeyboardRemove
from utils.others import download_document
from aiogram.dispatcher import FSMContext
from keyboards import cancel_kb, change_ikb
from utils.client_actions import get_data
from utils.Fsm import ClientDataForm
from config import bot, BASE_DIR
import os

async def add_account_cmd(message: Message):

    await message.answer('Вы перешли в режим привязки аккаунта.\nДля выхода воспользуйтесь командой /stop', parse_mode='HTML')
    await message.answer('Отправьте мне файл с разрешением *.session', reply_markup=cancel_kb())
    await ClientDataForm.File.set()


async def add_account_file(message: Message, state: FSMContext):

    ext = message.document.file_name.split('.')[-1]

    if ext != 'session':

        await message.reply('Неверный формат файла')
        return
    
    path = str(BASE_DIR / 'sessions' / message.document.file_name)
    if os.path.exists(path):

        await message.reply(f'В базе уже есть такая сессия - {message.document.file_name}')
        await state.finish()
        return
    

    temp = await message.answer('Скачиваю файл...')

    await download_document(message=message)
    
    await temp.delete()
    temp = await message.answer("Получаем информацию с аккаунта...")

    try:

        client_data = await get_data(message.document.file_name)
        client_data['init'] = True
    
    except Exception as ex:
        
        await state.finish()
        await message.answer(f'Ошибка\n{ex}', reply_markup=ReplyKeyboardRemove())
        return

    else:

        async with state.proxy() as data:

            data['chat_id'] = message.chat.id
            data['settings'] = client_data
            data['file_name'] = message.document.file_name

        info = 'Данные:'
        await temp.delete()
        for k, v in client_data.items():
            v = 'Не указано' if v == None else v
            info += f'\n{k}: {v}'

        await message.answer(info, reply_markup=change_ikb())


async def add_account_name(message: Message, state: FSMContext):
    
    message_list = message.text.split(' ')
    
    async with state.proxy() as data:

        data['settings']['first_name'] = message_list[0]

        try:
            data['settings']['last_name'] = message_list[1]
        except IndexError:
            pass

        info = 'Данные:'
        for k, v in data['settings'].items():
            v = 'Не указано' if not v else v
            info += f'\n{k}: {v}'

    await ClientDataForm.File.set()
    await message.answer(info, reply_markup=change_ikb())


async def add_account_bio(message: Message, state: FSMContext):
    
    
    async with state.proxy() as data:

        data['settings']['bio'] = message.text

        info = 'Данные:'
        for k, v in data['settings'].items():
            v = 'Не указано' if not v else v
            info += f'\n{k}: {v}'

    await ClientDataForm.File.set()
    await message.answer(info, reply_markup=change_ikb())


async def add_account_query(message: Message, state: FSMContext):
    
    
    async with state.proxy() as data:

        data['settings']['photo'] = message.text

        info = 'Данные:'
        for k, v in data['settings'].items():
            v = 'Не указано' if not v else v
            info += f'\n{k}: {v}'

    await ClientDataForm.File.set()
    await message.answer(info, reply_markup=change_ikb())



async def add_account_username(message: Message, state: FSMContext):
    
    
    async with state.proxy() as data:

        data['settings']['username'] = message.text

        info = 'Данные:'
        for k, v in data['settings'].items():
            v = 'Не указано' if v == None else v
            info += f'\n{k}: {v}'

    await ClientDataForm.File.set()
    await message.answer(info, reply_markup=change_ikb())