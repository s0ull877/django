from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from utils.client_actions import sign_request, delete_session
from keyboards import share_contact, without_password, type_code
from utils.Fsm import RelateForm
from config import bot, BASE_DIR
import os

async def relate_cmd(message: Message):

    await message.answer('Вы перешли в режим привязки вашего аккаунта.\nДля выхода воспользуйтесь командой /stop', parse_mode='HTML')
    await message.answer('Отправьте мне контакт, нажав на кнопку "Share contact".', reply_markup=share_contact())
    await RelateForm.Contact.set()


async def on_contact(message: Message, state: FSMContext): #current state - Contact

    async with state.proxy() as data:
        
        data['user_id'] = message.contact.user_id
        data['name'] = message.contact.full_name
        data['phone'] = message.contact.phone_number

    await RelateForm.Password.set()
    await message.answer('Отправьте пароль от аккаунта, если он имеется.\nВ противном случае нажмите кнопку ниже/', reply_markup=without_password())


# Получаем пароль
async def on_password(message: Message, state: FSMContext):

    await message.answer('Пробуем запросить код', reply_markup=ReplyKeyboardRemove())
    
    password = message.text if message.text != 'Без пароля' else None

    async with state.proxy() as data:
        
        data['password'] = password

        try:

            already_auth = await sign_request(session_id=str(data['user_id']), phone=data['phone'])

            if already_auth:

                await message.answer('Этот аккаунт уже привязан к боту!')
                await state.finish()
                return

            await message.answer('Telegram отправил вам код, пожалуйста введите его клавиатурой ниже.')
            await message.answer('_____________________', reply_markup=type_code())
            await RelateForm.Code.set()


        except Exception as e:
            
            await message.answer('Произошла ошибка.')
            path = str(BASE_DIR) + '/sessions/' + str(data['user_id']) + '.session'
            os.remove(path=path)
            await bot.send_message(os.getenv('LOG_CHAT_ID'), str(e) + '\nin commands\\relate.py on_password func')

