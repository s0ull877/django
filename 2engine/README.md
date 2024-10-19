# Тестовое задание backend 2engine
## Создание мини-системы управления задачами
[Тестовое задание](https://docs.google.com/document/d/17JJvq-tt2gzZUEeKepsw_OMBAVXfvaCyCqlNJr4x-UI/edit#heading=h.tqxy1xy2599w)  
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
    <p><strong>Фреймворк и модули:</strong> Django-5.0.7, djangorestframework-3.15.2, django-elasticsearch-dsl-8.0</p>
    <p><strong>Базы данных и инструменты работы с ними:</strong> PostgreSQL, SQLite, ElasticSearch</p>
    <p><strong>Мониторинг и обработка задач:</strong> Celery-5.4.0, Flower-2, RabbitMQ</p>  
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
    cd django/2engine && \
    cp .env_example .env && \
    nano .env

  2. Из корневой директории проекта выполните команду:

    docker compose -f infra/docker-compose.yml up -d --build

  Проект будет развернут в шести docker-контейнерах (db, elasticsearch, rabbitmq, web, nginx, celery) по адресу `http:/container_ip`
  
  3. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:

    docker compose -f infra/docker-compose.yml down
  
  Если также необходимо удалить тома базы данных, статики и медиа:

    docker compose -f infra/docker-compose.yml down -v

</details>

---

При первом запуске будут автоматически произведены следующие действия:

  - выполнены миграции

  - Бд заполнена начальными данными

  - собрана статика

  - создан суперюзер с учетными данными:
    - username = 'root', password = 'root'
      
    - собственными данными, если внесете в .env переменные `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_USERNAME`
      
Задачи представлены по адресу (в зависимости от способа запуска):

  - http://127.0.0.1:8000/tasks/list/`
  - http://localhost/tasks/list/
  - `http://<IP-адрес удаленного сервера>/tasks/list/`
   
Вход в админ-зону осуществляется по адресу (в зависимости от способа запуска):

  - http://127.0.0.1:8000/admin/
  - http://localhost/admin/
  - `http://<IP-адрес удаленного сервера>/admin/`

Запросы к api осуществляются через endpoint`ы (в зависимости от способа запуска):

  - http://127.0.0.1:8000/api/list-tasks/ | http://127.0.0.1:8000/api/task/
  - http://localhost/api/list-tasks/ | http://localhost/api/task/
  - `http://<IP-адрес удаленного сервера>/api/list-tasks/` | http://<IP-адрес удаленного сервера>/api/task/

GUI flower представлен по адресу (в зависимости от способа запуска):

  - http://127.0.0.1:555/`
  - http://localhost:555/
  - `http://<IP-адрес удаленного сервера>:5555/`

## Описание работы

На странице http://<hostname>/task/list/ представлена таблица Task обьектов, имеющая поля ID, NAME, DESCRIPTION, STATUS. На данной странице реализован поиск по NAME и DESCRIPTION, используя elasticsearch и пагинация для уменьшения количества обьектов на странице. После создании обьекта Task с помощью админки сервиса или же специального запроса к апи, выполняется shared_task, который имитирует работу задачи (слип 10 секунд) и обновляет статусы задачи. Просмотреть информацию о shared_task можно в веб интерфейсе flower на 5555 порту.

P.S. Диапазон между написанием кода и README очень велик, поэтому описание такое скудное.

## Удаление
Для удаления проекта выполните следующие действия:

  `cd .. && rm -fr django && deactivate`

[Оглавление](#оглавление)

## <a id="#автор">Автор</a>
[Radmir Galiullin](https://github.com/s0ull877)
