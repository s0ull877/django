from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards import cancel_kb
from utils.Fsm import AddAdminForm
from utils import redis


async def show_admins(message:Message):

    admins_dict = redis.get_admins()

    text = 'Группа <b>admins</b>:'
    for admin_id, admin_name in admins_dict.items():

        text += '\nname: {} | id: <code>{}</code>'.format(admin_name, admin_id)

    await message.answer(text=text, parse_mode='HTML')


async def add_admin(message: Message):

    await message.answer('Отправьте контакт пользователя, которого хотите назначить админом', reply_markup=cancel_kb())
    await AddAdminForm.Contact.set()

async def add_admin_on_contact(message: Message, state: FSMContext):

    await state.finish()
    answer = redis.set_admin(message.contact.user_id, message.contact.full_name)
    await message.answer(answer, reply_markup=ReplyKeyboardRemove())


# /del_admin user_id
async def del_admin(message: Message):

    message_list = message.text.split(' ')
    answer = redis.del_admin(message_list[-1])
    await message.answer(answer)