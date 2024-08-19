import os
import datetime
import random

from sqlite3 import OperationalError
from aiogram.types import ReplyKeyboardRemove

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from telethon import TelegramClient
from telethon import functions, types, errors
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, DeleteChatUserRequest

from .unplash import download_photo
from .dj_api import delete_worker
from .redis import get_proxies, del_proxy

from config import BASE_DIR, bot, AVAILABLE_PHONE


def get_proxy() -> dict:

    proxies = get_proxies()
    random.shuffle(proxies)
    path = str(BASE_DIR / 'sessions' / 'test.session')


    if proxies:
        for proxy in proxies:

            attrs = proxy.split(':')

            try:

                proxy_dict = {
                    'proxy_type': 'socks5',
                    'addr': attrs[0],     
                    'port': int(attrs[1]),          
                }

                if len(attrs) == 4:

                    proxy_dict['username'] = attrs[2]
                    proxy_dict['password'] = attrs[3]

                client = TelegramClient(path, api_hash=os.getenv('API_HASH'), api_id=os.getenv('API_ID'), proxy=proxy, connection_retries=0)
            
            except (ConnectionError, ValueError):
                del_proxy(proxy)

            except OperationalError:
                return None

            else:
                return proxy_dict
            
    else:
        return None


def delete_session(path: str, worker_id: str) -> None:

    try:
        delete_worker(worker_id)
        os.remove(path=path)
    except Exception as ex:
        pass

# ! add/change account cmd utils
async def get_data(file_name: str) -> dict:

    path = str(BASE_DIR / 'sessions' / file_name)
    proxy = get_proxy()
    print(proxy)
    client = TelegramClient(path, api_hash=os.getenv('API_HASH'), api_id=os.getenv('API_ID'), proxy=proxy)

    await client.connect()
    if not await client.is_user_authorized():
        await client.disconnect()
        os.remove(path)
        raise Exception('Невалидный файл сессии!')

    else:

        await client.start()
        me = await client.get_me()
        full = await client(GetFullUserRequest(me))
        update = await client(functions.account.GetPrivacyRequest(
            key=types.InputPrivacyKeyStatusTimestamp()
        ))
        rule = update.to_dict()['rules'][0]['_']

        data = {
            'first_name': me.first_name,
            'last_name': me.last_name,
            'username': me.username,
            'phone': me.phone,
            'username': me.username,
            'bio': full.full_user.about,
            'photo': True if full.full_user.profile_photo else None,
            'hidden_status': rule == 'PrivacyValueDisallowAll'
        }
        await client.disconnect()

        return data


async def configurate_client(settings: dict) -> None:

    errors_count = 0
    proxy = get_proxy()
    session_path = str(BASE_DIR / 'sessions' / settings['file_name'])
    client = TelegramClient(session_path, api_hash=os.getenv('API_HASH'), api_id=os.getenv('API_ID'), proxy=proxy)

    # номер приходит в строке юез +
    await client.connect()
    
    if not await client.is_user_authorized():
        await client.disconnect()
        os.remove(session_path)
        raise Exception('Невалидный файл сессии!')
    
    await client.start()
    if isinstance(settings['photo'], str):
        avatar_path = str(BASE_DIR / 'media' / '{}_avatar.jpg'.format(settings['chat_id']))
        avatar = await download_photo(settings['photo'], path=avatar_path)

    await client(functions.account.UpdateStatusRequest(offline=False))

    # ! Имя и Описание
    temp = await bot.send_message(settings['chat_id'], 'Обновление профиля...')
    try:
        update_profile = await client(functions.account.UpdateProfileRequest(
        first_name=settings['first_name'],
        last_name=settings['last_name'],
        about=settings['bio']
        ))
    except errors.FirstNameInvalidError:
        errors_count += 1
        await temp.edit_text('Некоректное имя пользователя для сессии {}'. format(settings['file_name']))
    else:
        await temp.edit_text('Обновление профиля. -> Успешно!')

    # ! Юзернейм
    if settings['username']:

        temp = await bot.send_message(settings['chat_id'], 'Обрабатываем юзернейм...')
        try:

            update_username = await client(functions.account.UpdateUsernameRequest(
                username=settings['username']
            ))
        
        except (errors.UsernameInvalidError, errors.UsernameOccupiedError):
            await temp.edit_text('Юзернейм {} занят или невалиден для сессии {}'. format(settings['username'], settings['file_name']))
            errors_count += 1
        except errors.UsernameNotModifiedError:
            await temp.edit_text('Обработка юзернейма. -> @{}'.format(settings['username']))
        else:
            await temp.edit_text('Обработка юзернейма. -> Изменен на @{}!'.format(settings['username']))

    else:
        temp = await bot.send_message(settings['chat_id'], 'Юзернейм отсутствует.')

    # ! Телефон
    if settings['init']:

        temp = await bot.send_message(settings['chat_id'], 'Обновление отображения номера...')

        rule = types.InputPrivacyValueAllowAll if settings['phone'][0:2] in AVAILABLE_PHONE else types.InputPrivacyValueDisallowAll
        print(settings['phone'][0:2])
        rule_string = 'доступен' if settings['phone'][0:2] in AVAILABLE_PHONE  else 'скрыт'

        try:
            await client(functions.account.SetPrivacyRequest(
                        key=types.InputPrivacyKeyPhoneNumber(),
                        rules=[rule()]
                    ))
        
        except Exception as ex:
            await temp.edit_text('Отображение номера  -> ОШИБКА: {}\n для сессии {}'.format(str(ex), settings['file_name']))
            errors_count += 1
        else:
            await temp.edit_text(f'Номер {rule_string}. -> Успешно!')
            


        # temp = await bot.send_message(settings['chat_id'], 'Ставим пароль...')
        # try:
        #     await client.edit_2fa(new_password=os.getenv('PASSWORD'))
        
        # except Exception as ex:
        #     await temp.edit_text('Обновление пароля  -> ОШИБКА: {}\n для сессии {}'.format(str(ex), settings['file_name']))
        #     errors_count += 1
        # else:
        #     await temp.edit_text('Обновление пароля. -> Успешно!')

    # ! Статус онлайна
    try:

        rule = types.InputPrivacyValueDisallowAll if settings['hidden_status'] else types.InputPrivacyValueAllowAll

        temp = await bot.send_message(settings['chat_id'], 'Обрабатываем политику статуса онлайна...')
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyStatusTimestamp(),
            rules=[rule()]
        ))

    except Exception as ex:
        await temp.edit_text('Статус онлайна  -> ОШИБКА: {}\n для сессии {}'.format(str(ex), settings['file_name']))
        errors_count += 1
    else:
        text = 'Статус онлайн -> Cкрыт' if settings['hidden_status'] else 'Статус онлайн -> Доступен'
        await temp.edit_text(text)

    # ! Фото профиля
    if isinstance(settings['photo'], str):

        temp = await bot.send_message(settings['chat_id'], 'Обновление фото профиля...')
        try:

            await temp.edit_text('Обновление фото профиля. -> Настройка приватности.')
            await client(functions.account.SetPrivacyRequest(
                    key=types.InputPrivacyKeyProfilePhoto(),
                    rules=[types.InputPrivacyValueDisallowAll()]
                ))

            if avatar:
                await temp.edit_text('Обновление фото профиля. -> Отправляем фото на сервер Telegram.\n(Это занимает достаточно времени)')
                await client(functions.photos.UploadProfilePhotoRequest(
                    file=await client.upload_file(avatar_path),          
                    fallback=True
                ))
            else:
                raise Exception('К сожалению, нам не удалось найти фото по запросу "{}"'.format(settings['photo']))
        
        except Exception as ex:
            await temp.edit_text('Фото профиля  -> ОШИБКА: {}\n для сессии {}'.format(str(ex), settings['file_name']))
            errors_count += 1
        else:
            await temp.edit_text('Обновление фото профиля. -> Успешно!')
            os.remove(avatar_path)

    await client.disconnect()
    await bot.send_message(settings['chat_id'], 'Настройка конфигурации для сессии {} завершена!\n\nОшибок: {}'.format(settings['file_name'], errors_count), reply_markup=ReplyKeyboardRemove())


# ! create_link cmd utils
async def client_sub(session_id: str, hash: str, worker_id: int) -> types:

    proxy = get_proxy()
    path = str(BASE_DIR / 'sessions' / session_id)
    client = TelegramClient(path, api_hash=os.getenv('API_HASH'), api_id=os.getenv('API_ID'), proxy=proxy)
    
    await client.connect()
    
    if not await client.is_user_authorized():
        await client.disconnect()
        delete_session(path=f'{path}.session', worker_id=worker_id)
        raise Exception('Невалидный файл сессии {} при подписке!'. format(session_id))

    else:    
        await client.start()

        try:
            await client(functions.account.UpdateStatusRequest(
                offline=False
            ))
            update = await client(ImportChatInviteRequest(hash=hash))  

        except errors.UserAlreadyParticipantError:

            link = 'https://t.me/+' + hash
            entity = await client.get_entity(link)
            return entity

        except errors.PeerIdInvalidError:

            return update.chats[0]

        else:

            return update.chats[0]

        finally:
            await client.disconnect()

async def client_unsub(session_id: str, entity, worker_id: int) -> None:

    proxy = get_proxy()
    path = str(BASE_DIR / 'sessions' / session_id)
    client = TelegramClient(path, api_hash=os.getenv('API_HASH'), api_id=os.getenv('API_ID'), proxy=proxy)
    
    try:
        await client.connect()
        
        if not await client.is_user_authorized():
            await client.disconnect()
            delete_session(path=f'{path}.session', worker_id=worker_id)
            raise Exception('ОШИБКА | Невалидный файл сессии {} при отписке!'. format(session_id))

        await client.start()
        
        await client(functions.account.UpdateStatusRequest(
            offline=False
        ))
        
        if isinstance(entity, types.Channel):

            await client(functions.channels.LeaveChannelRequest(
                channel=entity
            ))

        else:

            await client(functions.messages.DeleteChatUserRequest(
                chat_id=entity.id,
                user_id='me'
            ))

    except (OperationalError, TypeError):

        date = datetime.datetime.now() + datetime.timedelta(minutes=5)
        trigger = DateTrigger(run_date=date)

        scheduler_unsub = AsyncIOScheduler()
        scheduler_unsub.add_job(client_unsub, args=[session_id, entity, worker_id], trigger=trigger)
        scheduler_unsub.start()


    except Exception as ex:
        await bot.send_message(os.getenv('LOG_CHAT_ID'), str(ex))
    
    finally:
        await client.disconnect()


async def client_online(session: str, worker_id: int, scheduler: AsyncIOScheduler, job_id=None) -> None:

    proxy = get_proxy()
    session_id = session.replace('.session', '')
    path = str(BASE_DIR / 'sessions' / session_id)
    client = TelegramClient(path, api_hash=os.getenv('API_HASH'), api_id=os.getenv('API_ID'), proxy=proxy)

    try:
        await client.connect()
        
        if not await client.is_user_authorized():

            if job_id:
                scheduler.remove_job(job_id)

            await client.disconnect()
            delete_session(path=f'{path}.session', worker_id=worker_id)
            raise Exception('ОШИБКА | Невалидный файл сессии {} при попытке войти в онлайн!'. format(session_id))
        
        await client(functions.account.UpdateStatusRequest(
            offline=False
        ))

    except (OperationalError, TypeError):
        pass

    except Exception as ex:
        await bot.send_message(os.getenv('LOG_CHAT_ID'), str(ex))

    finally:

        await client.disconnect()


# ! relate cmd utils

client = None

async def sign_request(session_id: str, phone: str) -> bool:
        
    global client

    proxy = get_proxy()

    path = str(BASE_DIR / 'sessions' / session_id)
    client = TelegramClient(path, api_hash=os.getenv('API_HASH'), api_id=os.getenv('API_ID'), proxy=proxy)
    await client.connect()

    if not await client.is_user_authorized():

        await client.send_code_request(phone)
        
        return False
    
    else:
        
        await client.disconnect()
        return True


async def sign_in_client(phone: str, code: str, password=None):
    
    global client


    try:
        await client.sign_in(phone=phone, code=code, password=password)
    
    except errors.SessionPasswordNeededError:
        await client.sign_in(password=password)
    
    finally:
        await client.disconnect()
