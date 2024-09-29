
# можно было бы через мету брать все поля, но мешают служебные поля
USER_FIELDS = {'email', 'fam', 'name', 'otc', 'phone'}
LEVEL_FILEDS = {'winter', 'summer', 'autumn', 'spring'}
COORDS_FIELDS = {'latitude', 'longitude', 'height'}
IMAGE_FIELDS = {'data', 'title'}
PEREVAL_FIELDS = {'beauty_title', 'title', 'other_titles', 'connect', 'add_time' , 'user', 'coords', 'level', 'images'}

INCLUDED={'user':USER_FIELDS, 'coords':COORDS_FIELDS, 'level':LEVEL_FILEDS}

def check_fields(data: dict) -> None:

    pereval_fields = PEREVAL_FIELDS - set(data.keys())

    if pereval_fields:
        raise KeyError(f'Пропущены обязательные поля: {pereval_fields}')
    
    for field_name, fields_set in INCLUDED.items():

        try:
            remain_fields = fields_set - set(data[field_name].keys())
        except AttributeError:
            raise KeyError(f'Неверный формат поля {field_name}!')
    
        if remain_fields:
            raise KeyError(f'Пропущены обязательные поля user: {remain_fields}')
    
    for image in data['images']:

        try:    
            image_fields = IMAGE_FIELDS - set(image.keys())
        except AttributeError:
            raise KeyError('Неверный формат обьекта поля images!')
        
        if image_fields:
            raise KeyError(f'Пропущены обязательные поля обьекта images: {image_fields}')
