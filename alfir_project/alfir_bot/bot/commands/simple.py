from aiogram.types import ReplyKeyboardRemove, Message
from aiogram.dispatcher import FSMContext

async def stop_cmd(message: Message, state: FSMContext) -> None:

    await state.finish()
    await message.answer('Действие остановлено.', reply_markup=ReplyKeyboardRemove())


async def help_cmd(message: Message):

    text = '''
<b>Настройка админов:</b>
/admins - выводит список всех админов

/add_admin - напиши команду для инициализации и после отправьте контакт пользователя, которого хотите назначить админом.

<code>/del_admin id</code> - при помощи /admins получите id пользователя и введите команду вместе с id


<b>Настройка прокси:</b>
/proxies - выводит список всех прокси
*невалидные прокси удаляются автоматически*

/set_proxy - для добавления прокси в базу


<b>Настройка интервала:</b>
<code>/sub_interval minutes</code> - настраивает интервал подписки, в промежутке от 0 до minutes минут аккаунт подпишется

<code>/unsub_interval min max</code> - настраивает интервал отписки, после подписки на ссылку аккаунт в промежутке от min до max часов отпишется


<b>Настройка аккаунтов:</b>
/relate - для привязки активного аккаунта в базу, не используя файлы сессии

/add_account - добавление нового аккунта, для добавления используется *.session файл, после происходит настройка конфигурации аккаунта

/change_account - настройка конфигурации существующего аккаунта, для изменения нужно id файла из прошлой команды

<b>Конфигурация:</b>
<b>first_name: Lily</b> - имя
<b>last_name: Не указано</b> - фамилия
<b>username: B3auty_pr1nc3ss</b> - юзернейм
<b>phone: 14066087275</b> - номер телефона без +
<b>bio: Подо мной M5...</b> - бар "обо мне"
<b>photo: True</b> - Если True, значит у аккаунта установлен публичный аватар, вы можете назначить тему аватара, в последующем будет надпись "Не указано"
<b>hidden_status: False</b> - скрыт ли статус онлайна "True" - Да / "False" - Нет
<b>init: False</b> - Первичная ли инициализация


<b>Создание ссылок:</b>
/create_link - создание ссылки, следуйте шагам

<b>! Не используйте create_link c одинаковыми ссылками</b>
'''

    await message.answer(text=text, parse_mode='HTML')