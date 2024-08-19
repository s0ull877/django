from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from keyboards import cancel_kb
from utils.dj_api import get_workers, create_link
from utils.others import start_sub
from json.decoder import JSONDecodeError
from random import sample
from utils.Fsm import CreateLinkForm


async def create_link_cmd(message: Message):

    await message.answer('Отправьте мне вступительную ссылку', reply_markup=cancel_kb())

    await CreateLinkForm.Link.set()


async def on_link(message: Message, state: FSMContext):

    async with state.proxy() as data:

        data['link'] = message.text

    await message.answer('Придумайте имя для данной ссылки (под таким именем она будет отображаться в базе)')
    await CreateLinkForm.Name.set()


async def on_name(message: Message, state: FSMContext):

    workers = get_workers()
    async with state.proxy() as data:

        data['workers'] = workers
        data['name'] = message.text

    await message.answer('На данный момент в базе {} аккаунтов.\nКакое количество аккаунтов должно подписаться?'.format(len(workers)))
    await CreateLinkForm.WorkersQ.set()


async def start_working(message: Message, state: FSMContext):

    count = int(message.text)
    async with state.proxy() as data:

        if count > len(data['workers']):

            await message.answer('Некорректный ввод')
            return
        
        try:   
            response = create_link(data['name'], data['link'])
            link_id = response['id']

        except (JSONDecodeError, KeyError):
            text = 'Ответ от сервера:'
            for k,v in response.items():
                text += '\n{} : {}'.format(k, *v)
            await message.answer(text, reply_markup=ReplyKeyboardRemove())

        else:
            workers = sample(data['workers'], k=count)
            await message.answer('Начинаю подписываться.', reply_markup=ReplyKeyboardRemove())
            await start_sub(link_id=link_id, workers=workers , target=data['link'])

        finally:
            await state.finish()