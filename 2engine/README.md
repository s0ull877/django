# Тестовое задание backend 2engine
## Создание мини-системы управления задачами
[Тестовое задание](https://docs.google.com/document/d/17JJvq-tt2gzZUEeKepsw_OMBAVXfvaCyCqlNJr4x-UI/edit#heading=h.tqxy1xy2599w)  
</br>

## Оглавление:
- [Технологии](#технологии)
- [Установка и запуск](#starting)
- [Описание работы](#description)

## <a id="технологии">Технологии</a>
<details>
  <summary>Подробнее</summary>
    <p><strong>Языки программирования:</strong> python-10</p>
    <p><strong>Фреймворк и модули:</strong> Django-5.0.7, djangorestframework-3.15.2, django-elasticsearch-dsl-8.0</p>
    <p><strong>Базы данных и инструменты работы с ними:</strong> PostgreSQL, SQLite, ElasticSearch</p>
    <p><strong>Мониторинг и обработка задач:</strong> Celery-5.4.0, Flower-2, RabbitMQ</p>  
    <p><strong>CI/CD:</strong> Docker Hub, Docker Compose, Gunicorn, Nginx</p>  
</details>

## <a id="starting">Установка и запуск</a>

<details>
  <summary>Предварительные условия</summary>
  <p>Предполагается, что пользователь:</p>
  
  - Создал аккаунт [DockerHub](https://hub.docker.com/).
  - Установил [Docker](https://docs.docker.com/engine/install/) и [Dcoker Compose](https://docs.docker.com/compose/install/) на локальной машине или удаленном сервере, где проект будет запускаться в контейнерах. Проверить наличие можно выполнив команды:
    
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

Задачи представлены по адресу `http:container_ip/tasks/list`
