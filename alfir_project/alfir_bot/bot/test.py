import os
import asyncio
from utils.client_actions import get_proxy
from utils.redis import set_proxy, get_proxies

async def main():

    set_proxy('172358:wuey')
    print(get_proxy())
    print(get_proxies())

def main():
    from utils.dj_api import create_link
    print(create_link('test', 'dskagdsa'))

if __name__ == '__main__':
    # asyncio.run(main())
    main()