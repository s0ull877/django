from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from utils.Fsm import SetProxyForm
from utils.redis import set_proxy, get_proxies
from keyboards import cancel_kb

async def set_proxy_cmd(message: Message) -> None:

    await message.answer('Отправляйте прокси SOCKS5 формата addr:port:username:password или addr:port\n По окончанию напишите /stop', reply_markup=cancel_kb())
    await SetProxyForm.Proxy.set()

async def proxy_setter(message: Message, state: FSMContext) -> None:

    set_proxy(message.text)
    await message.answer(f'Прокси {message.text}  добавлен, он пройдет валидацию при первом же использовании.')

async def show_proxies_cmd(message: Message) -> None:

    proxies = get_proxies()

    text = 'Proxy:'
    i = 0

    for proxy in proxies:
        
        i += 1
        text += f'\n{i}: {proxy}'

    await message.answer(text=text)