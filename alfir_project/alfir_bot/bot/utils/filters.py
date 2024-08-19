from aiogram import types
from aiogram.dispatcher.filters import Filter
from utils import redis
import os


class IsAdmin(Filter):
    key = "is_admin"

    async def check(self, message: types.Message):

        try:        
            user_id = str(message.from_user.id) 
            admins_ids = redis.get_admins().keys()
            return user_id in admins_ids or user_id == os.getenv('MAIN_ID')
        except Exception as ex:
            print(ex)
        finally:
            print('pass')

class HaveArgs(Filter):
    key = "args_count"

    def __init__(self, args_count: str) -> None:
        self.args_count = args_count


    async def check(self, message: types.Message):
        
        msg_list = message.text.split(' ')

        if len(msg_list) == self.args_count + 1:
            return True
        
        else:

            await message.answer(f'Данная команда принимает {self.args_count} аргумент(a)')


class ProxyValidator(Filter):
    key = "None"

    async def check(self, message: types.Message):
        
        msg_list = message.text.split(':')
        l = len(msg_list)

        if l in [2, 4]:
            return True
        
        else:

            await message.answer(f'Неверный формат ввода, {l} аргументов принято, хотя ожидалось 2 или 4')
