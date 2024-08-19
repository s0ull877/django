import asyncio
import os
from aiogram import Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils.Fsm import AddAdminForm, ClientDataForm, CreateLinkForm, SetProxyForm, \
    RelateForm
from utils.filters import IsAdmin, HaveArgs, ProxyValidator
from utils.others import workers_online

from commands import admin, change_sub_interval, proxy, simple, account, change_account,  \
    create_link, change_unsub_interval, relate
from callbacks.change_client import change_callback, cancel_callback, send_data_callback
from callbacks.type_code import get_number_for_code, clear_number_in_code, send_code

from config import bot

dp = Dispatcher(bot, storage=MemoryStorage())


dp.register_message_handler(simple.help_cmd, commands=['help', 'start'])

dp.register_message_handler(simple.stop_cmd, state=['*'], commands=['stop'])

dp.register_message_handler(proxy.show_proxies_cmd, IsAdmin(), commands=['proxies'])
dp.register_message_handler(proxy.set_proxy_cmd, IsAdmin(), commands=['set_proxy'])
dp.register_message_handler(proxy.proxy_setter, ProxyValidator(), state=SetProxyForm.Proxy)


dp.register_message_handler(admin.show_admins, IsAdmin(), commands=['admins'])
dp.register_message_handler(admin.add_admin, IsAdmin(), commands=['add_admin'])
dp.register_message_handler(admin.add_admin_on_contact, content_types=[types.ContentType.CONTACT], state=AddAdminForm.Contact)
dp.register_message_handler(admin.del_admin, HaveArgs(1), IsAdmin(), commands=['del_admin'])


dp.register_message_handler(account.add_account_cmd, IsAdmin(), commands=['add_account'])
dp.register_message_handler(account.add_account_file, content_types=[types.ContentType.DOCUMENT], state=ClientDataForm.File)
dp.register_message_handler(account.add_account_name, lambda message: len(message.text.split(' ')) < 3, state=ClientDataForm.FullName)
dp.register_message_handler(account.add_account_bio, lambda message: len(message.text) < 128, state=ClientDataForm.Bio)
dp.register_message_handler(account.add_account_query, state=ClientDataForm.Query)
dp.register_message_handler(account.add_account_username, state=ClientDataForm.Username)

dp.register_message_handler(change_account.change_account_cmd, IsAdmin(), commands=['change_account'])
dp.register_message_handler(change_account.change_account_filename, content_types=[types.ContentType.TEXT], state=ClientDataForm.File)

dp.register_message_handler(create_link.create_link_cmd, IsAdmin(), commands=['create_link'])
dp.register_message_handler(create_link.on_link, lambda message: message.text.startswith('https://t.me/+'), state=CreateLinkForm.Link)
dp.register_message_handler(create_link.on_name, state=CreateLinkForm.Name)
dp.register_message_handler(create_link.start_working, lambda message: message.text.isdigit() ,state=CreateLinkForm.WorkersQ)

dp.register_message_handler(change_sub_interval.change_interval_cmd, IsAdmin(), HaveArgs(1), commands=['sub_interval'])
dp.register_message_handler(change_unsub_interval.change_interval_cmd, IsAdmin(), HaveArgs(2), commands=['unsub_interval'])

dp.register_message_handler(relate.relate_cmd, commands=['relate'])
dp.register_message_handler(relate.on_contact, content_types=[types.ContentType.CONTACT], state=RelateForm.Contact)
dp.register_message_handler(relate.on_password, content_types=[types.ContentType.TEXT], state=RelateForm.Password)


dp.register_callback_query_handler(change_callback, lambda callback: callback.data.startswith('change:'), state=ClientDataForm.File)
dp.register_callback_query_handler(send_data_callback, lambda callback: callback.data == 'send', state=ClientDataForm.File)

dp.register_callback_query_handler(cancel_callback, lambda callback: callback.data == 'cancel', state=['*'])

dp.register_callback_query_handler(get_number_for_code, lambda callback: callback.data.startswith('code:'), state=RelateForm.Code)
dp.register_callback_query_handler(clear_number_in_code, lambda callback: callback.data.startswith('clear:'), state=RelateForm.Code)
dp.register_callback_query_handler(send_code, lambda callback: callback.data.startswith('send:'), state=RelateForm.Code)

async def on_startup(_):

    await workers_online()
    


if __name__ == "__main__":

    import logging
    logging.basicConfig(
        format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
        level=logging.INFO,
    )

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    # executor.start_polling(dp, skip_updates=True)
