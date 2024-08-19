from config import REDIS as r


def get_admins() -> dict:

    return r.hgetall('admins')


def set_admin(user_id: str, name: str) -> str:

    ids = get_admins().keys()

    if user_id in ids:

        return 'Данный пользователь уже состоит в группе admins'
    
    else:

        r.hset('admins', user_id, name)
        return f'Пользователь {name} добавлен в группу admins'


def del_admin(user_id: str) -> str:

    ids = get_admins().keys()

    if user_id not in ids:

        return f'Данный пользователь не состоит в группе admins'
    
    else:

        r.hdel('admins', user_id)
        return f'Пользователь удален из группы admins'
    


def set_interval(interval: str) -> None:

    r.set('interval', interval)

def get_interval() -> int:

    minutes = int(r.get('interval'))

    return minutes * 60


def set_unsub_interval(min: str, max:str) -> None:

    r.hset('unsub_interval', 'min', min)
    r.hset('unsub_interval', 'max', max)

def get_unsub_interval() -> tuple[int, int]:

    min = r.hget('unsub_interval', 'min')
    max = r.hget('unsub_interval', 'max')

    return int(min) * 60, int(max) * 60


def get_proxies() -> list:

    proxies = r.hgetall('proxies')
    return list(proxies.keys())

def set_proxy(proxy:str) -> None:

    proxies = get_proxies()
    if not proxy in proxies:
        r.hset('proxies', proxy, len(proxies))


def del_proxy(proxy: str) -> None:

    r.hdel('proxies', proxy)