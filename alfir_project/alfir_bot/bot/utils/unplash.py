import os
import json
import requests

async def download_photo(query: str, path: str) -> None:

    query = query.replace(' ', '+')
    url = 'https://api.unsplash.com/photos/random/?client_id={}&query={}&orientation=squarish'.format(os.getenv('UNPLASH_ACCESS'), query)

    r = requests.get(url=url).content
    data = json.loads(r)
    
    if data.get('urls'):

        end_point = data['urls']['full'] + '&client_id={}'.format(os.getenv('UNPLASH_ACCESS'))
        
        res = requests.get(end_point)

        with open(path, 'wb') as avatar:
            avatar.write(res.content)
        ...
        return True
    
    return False
    