from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from keyboards import change_ikb
from utils.client_actions import get_data
from utils.Fsm import ClientDataForm
from config import BASE_DIR
import os

async def change_account_cmd(message: Message):

    await message.answer('Введите имя сессионного файла юзера, которого вы хотите настроить.')
    await ClientDataForm.File.set()


async def change_account_filename(message: Message, state: FSMContext):

    file_name = message.text + '.session'

    path = str(BASE_DIR / 'sessions' / file_name)
    if not os.path.exists(path):

        await message.reply(f'В базе нет такой сессии - {file_name}')
        await state.finish()
        return
    
    else:

        try:

            client_data = await get_data(file_name)
            client_data['init'] = False
        
        except Exception as ex:
            
            await state.finish()
            await message.answer(f'Ошибка\n{ex}', reply_markup=ReplyKeyboardRemove())
            return

        else:

            async with state.proxy() as data:

                data['chat_id'] = message.chat.id
                data['settings'] = client_data
                data['file_name'] = file_name

            info = 'Данные:'
            for k, v in client_data.items():
                v = 'Не указано' if v == None else v
                info += f'\n{k}: {v}'

            await message.answer(info, reply_markup=change_ikb())
