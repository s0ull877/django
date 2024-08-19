import asyncio
import os
import pytz
import random

from aiogram import types
from telethon import errors, TelegramClient
from datetime import datetime, timedelta
from sqlite3 import OperationalError
from json.decoder import JSONDecodeError

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

from .client_actions import client_sub, client_unsub, client_online, get_data
from .dj_api import create_sub, get_workers, create_worker
from .redis import get_interval, get_unsub_interval
from config import bot, BASE_DIR


async def download_document(message: types.Message):

    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    downloaded_file = await bot.download_file(file_path)


    file_name = str(BASE_DIR / 'sessions' / message.document.file_name)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file.read())


async def process(worker: dict, target:str, link_id: int):

    hash = target.replace('https://t.me/+', '')
    error = True

    if not worker.get('try'):
        worker['try'] = 1
    else:
        worker['try'] += 1

    try:

        created = datetime.now(tz=pytz.timezone('Europe/Moscow'))

        entity = await client_sub(worker['worker_tg_id'], hash, worker['id'])


    except (OperationalError, TypeError):

        if worker['try'] < 4:

            text = 'ОШИБКА | нет подключения к сессии {}, попытка {}/3'.format(worker['worker_tg_id'], worker['try'])

            run_date = created + timedelta(seconds=600)
            trigger = DateTrigger(run_date=run_date)

            scheduler_sub = AsyncIOScheduler()
            scheduler_sub.add_job(process, args=[worker, target, link_id], trigger=trigger)
            scheduler_sub.start()
        
        else:
            text = 'ОШИБКА | нет подключения к сессии {}'.format(worker['worker_tg_id'])

    except (errors.InviteHashInvalidError, errors.InviteHashExpiredError):
        text = 'ОШИБКА | Ссылка {} устарела или не существует.'.format(target)

    except errors.InviteRequestSentError:

        error = False
        run_date = created + timedelta(seconds=120)
        trigger = DateTrigger(run_date=run_date)

        scheduler_sub = AsyncIOScheduler()
        scheduler_sub.add_job(process, args=[worker, target, link_id], trigger=trigger)
        scheduler_sub.start()

    except Exception as ex:
        text = 'ОШИБКА | Пользователь {} - {}'.format(worker['worker_tg_id'], str(ex))

    else:

        error = False

        create_sub(link_id=link_id, worker_id=worker['id'], created=created)

        date = created + timedelta(minutes=random.randint(*get_unsub_interval()))
        trigger = DateTrigger(run_date=date)

        scheduler_unsub = AsyncIOScheduler()
        scheduler_unsub.add_job(client_unsub, args=[worker['worker_tg_id'], entity, worker['id']], trigger=trigger)
        scheduler_unsub.start()

    finally:

        if error:
            await bot.send_message(os.getenv('LOG_CHAT_ID'), text)



async def start_sub(link_id: int, workers: list, target: str):

    scheduler = AsyncIOScheduler()
    start = 0 
    interval = get_interval() 
    for worker in workers:

        max_time = start + interval
        seconds = random.randint(start, max_time)

        date = datetime.now(tz=pytz.timezone('Europe/Moscow')) + timedelta(seconds=seconds)
        trigger = DateTrigger(run_date=date)
        
        scheduler.add_job(process, args=[worker, target, link_id], trigger=trigger) 
        start = seconds

    scheduler.start()

    
async def workers_online():

    workers = get_workers()

    if workers:
    
        scheduler = AsyncIOScheduler()

        for worker in workers:

            trigger = IntervalTrigger(minutes=random.randint(60, 240))
            
            job = scheduler.add_job(client_online, args=[worker['worker_tg_id'], worker['id'], scheduler], trigger=trigger)

            job.args = [worker['worker_tg_id'], worker['id'], scheduler, job.id]
            
        
        scheduler.start()
    else:
        print('pass')

async def init_worker(worker_tg_id, name, phone):
        
        try:
            await get_data(worker_tg_id)
        
        except Exception as ex:
            await bot.send_message(os.getenv('LOG_CHAT_ID'), f'Не удалось зарегистрировать аккаунт {name}|{worker_tg_id}\nПричина: {ex}')
        
        else:
            scheduler = AsyncIOScheduler()
            trigger = IntervalTrigger(minutes=random.randint(15,60))

            try:
                response = create_worker(
                    worker_tg_id=worker_tg_id,
                    name=name,
                    phone=phone
                )

                job = scheduler.add_job(client_online, args=[worker_tg_id, response['id'], scheduler], trigger=trigger)

            except (KeyError, JSONDecodeError):

                pass

            else:

                job.args = [worker_tg_id, response['id'], scheduler, job.id]
                scheduler.start()



    


