# Первый проект на Django. Интернет магазин одежды.
[Курс Stepik](https://stepik.org/course/125859/syllabus)  
</br>

## Оглавление:
- [Технологии](#технологии)
- [Установка и запуск](#установка-и-запуск)
- [Описание работы](#описание-работы)
- [Удаление](#удаление)

## Технологии
<details>
  <summary>Подробнее</summary>
    <p><strong>Языки программирования:</strong> python-10</p>
    <p><strong>Фреймворк и модули:</strong> Django-5.0.7, djangorestframework-3.15.2</p>
    <p><strong>Базы данных и инструменты работы с ними:</strong> PostgreSQL, SQLite, Redis</p>
    <p><strong>Мониторинг и обработка задач:</strong> Celery-5.4.0, Redis</p>  
    <p><strong>CI/CD:</strong> Docker Hub, Docker Compose, Gunicorn, Nginx</p>  
</details>

## Установка и запуск

<details>
  <summary>Предварительные условия</summary>
  <p>Предполагается, что пользователь:</p>
  
  - Создал аккаунт [DockerHub](https://hub.docker.com/).
  - Установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине или удаленном сервере, где проект будет запускаться в контейнерах. Проверить наличие можно выполнив команды:
    
  `docker --version && docker-compose --version`
  
</details>
<details>
  <summary>Локальный запуск</summary>
  
  <p><strong>!!! Для пользователей Windows обязательно выполнить команду:</strong></p>
  
    `git config --global core.autocrlf false`
    
  <p>иначе файл start.sh при клонировании будет бракован</p>
  
  1. Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, некоторые можно оставить по типу DB*):
    
    git clone https://github.com/s0ull877/django.git && \
    cd django/strore-server && \
    cp infra/local/.env_example infra/local/.env && \
    nano ./infra/local/.env

  <strong>Если вы хотите использовать регистрацию через github, то нужно через админку подключить github, либо же закоменьтить блок socialapp, чтобы не возникала ошибка!</strong>

  2. Из корневой директории проекта выполните команду:

    docker compose -f infra/local/docker-compose.yml up -d --build

  Проект будет развернут в четырех docker-контейнерах (db, redis, web, nginx) по адресу `http:/container_ip`
  
  3. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:

    docker compose -f infra/local/docker-compose.yml down
  
  Если также необходимо удалить тома базы данных, статики и медиа:

    docker compose -f infra/local/docker-compose.yml down -v

</details>

---

При первом запуске будут автоматически произведены следующие действия:

  - выполнены миграции

  - Бд заполнена начальными данными

  - собрана статика

  - создан суперюзер с учетными данными:
    - username = 'root', password = 'root'
      
    - собственными данными, если внесете в .env переменные `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_USERNAME`
      
Вход на сайт представлен по адресу (в зависимости от способа запуска):

  - http://127.0.0.1:8000/`
  - http://localhost/
  - `http://<IP-адрес удаленного сервера>/`
   
Вход в админ-зону осуществляется по адресу (в зависимости от способа запуска):

  - http://127.0.0.1:8000/admin/
  - http://localhost/admin/
  - `http://<IP-адрес удаленного сервера>/admin/`

Запросы к api осуществляются через endpoint`ы (в зависимости от способа запуска):

  - http://127.0.0.1:8000/api/ 
  - http://localhost/api/
  - `http://<IP-адрес удаленного сервера>/api/`

## Описание работы


На странице http://HOSTNAME/ представлена главня страница входа. 
На сервере реализована регистрация и авторизация пользователя. 
Подтверждение аккаунта через почту с использованием celery или вход через socialapp.
Изменение профиля пользователя и его пользовательской корзины.
Страница товаров и отдельного товара, их фильтрация и поиск с помощью postgresql
Подключение вебхука для оплаты через Юкассу.
Реализовано простейшее api crud запросов над моделями проекта.

Код практически полностью скопирован с исходного, но реализация docker-compose полностью моя инициатива.

P.S. Диапазон между написанием кода и README очень велик, поэтому описание такое скудное.

## Удаление
Для удаления проекта выполните следующие действия:

  `cd .. && rm -fr django && deactivate`

[Оглавление](#оглавление)

## <a id="#автор">Автор</a>
[Radmir Galiullin](https://github.com/s0ull877)
