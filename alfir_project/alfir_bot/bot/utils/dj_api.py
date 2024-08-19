import os
import json
import requests
from datetime import datetime

API_URL = os.getenv('DJ_API_URL')

HEADERS = {'Authorization': 'Token {}'.format(os.getenv('ROOT_TOKEN'))}


def create_worker(worker_tg_id: str, name: str, phone: str) -> None:

    r = requests.post(url=f'{API_URL}/workers/', headers=HEADERS, json={'worker_tg_id': worker_tg_id, 'name': name, 'phone':phone})

    return json.loads(r.content)


def delete_worker(worker_id: str) -> None:

    r = requests.delete(url=f'{API_URL}/workers/{worker_id}/', headers=HEADERS)


def get_workers():

    r = requests.get(url=f'{API_URL}/workers/', headers=HEADERS)

    return json.loads(r.content)


def create_link(name:str, telegram_link:str) -> dict:

    global API_URL, HEADERS

    r = requests.post(url=f'{API_URL}/link-create/', headers=HEADERS, data={'name': name, 'telegram_link': telegram_link})

    return json.loads(r.content)


def create_sub(link_id: int, worker_id: int, created: datetime):

    r = requests.post(url=f'{API_URL}/sub-create/', headers=HEADERS, data={'link_id': link_id, 'worker_id': worker_id, 'created': created})


