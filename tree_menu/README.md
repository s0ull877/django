# Проект tree-menu: 
[![Tree-menu CI/CD](https://github.com/alexpro2022/Django-tree_menu/actions/workflows/main.yml/badge.svg)](https://github.com/alexpro2022/Django-tree_menu/actions/workflows/main.yml)

### Древовидное меню на Django, испоьзуя custom template tag.

[Тестовое задание](https://docs.google.com/document/d/1XTnbcXhejyGB-I2cHRiiSZqI3ElHzqDJeetwHkJbTa8/edit?usp=sharing)

<br>

## Оглавление:
- [Технологии](#технологии)
- [Установка и запуск](#установка-и-запуск)
- [Описание работы](#описание-работы)
- [Удаление](#удаление)
- [Автор](#автор)

<br>

## Технологии:

<details><summary>Подробнее</summary>

**Языки программирования, библиотеки и модули:**

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue?logo=python)](https://www.python.org/)

**Фреймворк, расширения и библиотеки:**

[![Django](https://img.shields.io/badge/Django-v4.2.1-blue?logo=Django)](https://www.djangoproject.com/)


**Базы данных и инструменты работы с БД:**

[![SQLite3](https://img.shields.io/badge/-SQLite3-464646?logo=SQLite)](https://www.sqlite.com/version3.html)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)



**CI/CD:**

[![docker_hub](https://img.shields.io/badge/-Docker_Hub-464646?logo=docker)](https://hub.docker.com/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?logo=gunicorn)](https://gunicorn.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?logo=NGINX)](https://nginx.org/ru/)


[⬆️Оглавление](#оглавление)
</details>

<br>

## Установка и запуск:
Удобно использовать принцип copy-paste - копировать команды из GitHub Readme и вставлять в командную строку Git Bash или IDE (например VSCode).

<details><summary>Предварительные условия</summary>

Предполагается, что пользователь:
 - создал аккаунт [DockerHub](https://hub.docker.com/), если запуск будет производиться на удаленном сервере.
 - установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине или на удаленном сервере, где проект будет запускаться в контейнерах. Проверить наличие можно выполнив команды:
    ```bash
    docker --version && docker-compose --version
    ```
<h1></h1>
</details>

<details><summary>Локальный запуск</summary> 

**!!! Для пользователей Windows обязательно выполнить команду:** 
```bash
git config --global core.autocrlf false
```
иначе файл start.sh при клонировании будет бракован.

1. Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, некоторые можно оставить по типу postgres):
```bash
git clone https://github.com/s0ull877/django.git && \
cd django/tree_menu && \
cp infra/local/env_example infra/local/.env && \
nano ./infra/local/.env
```

2. Из корневой директории проекта выполните команду:
```bash
docker compose -f infra/local/docker-compose.yml up -d --build
```
Проект будет развернут в трех docker-контейнерах (db, web, nginx) по адресу `http://host`.

3. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:
```bash
docker compose -f infra/local/docker-compose.yml down
```
Если также необходимо удалить тома базы данных, статики и медиа:
```bash
docker compose -f infra/local/docker-compose.yml down -v
```
</details><h1></h1></details>

При первом запуске будут автоматически произведены следующие действия:

  - выполнены миграции

  - Бд заполнена начальными данными

  - собрана статика

  - создан суперюзер с учетными данными:
    - username = 'root', password = 'root'
      
    - собственными данными, если внесете в .env переменные `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_USERNAME`
      
 
Меню представлены по адресу (в зависимости от способа запуска):
  - http://127.0.0.1:8000/menu/
  - http://localhost/menu/
  - `http://<IP-адрес удаленного сервера>/menu/`

Вход в админ-зону осуществляется по адресу (в зависимости от способа запуска):
  - http://127.0.0.1:8000/admin/
  - http://localhost/admin/
  - `http://<IP-адрес удаленного сервера>/admin/`

[⬆️Оглавление](#оглавление)

<br>

## Описание работы:

На странице `http://<hostname>/menu/` представлена категория DNS, при клике на которую происходит переход на страницу данной категории. Возврат в главное меню происходит при клике `В главное меню`.
Принцип работы приложения основан на выборке из БД всех пунктов категорий, которые имеют в поле `categoty` название выбранной категории. Название выбранной категории извлекается из url. Далее происходит отображение этого категории и ее сабкатегорий. При клике на сабкатегорию происходит рекурсивный поиск по извлеченным данным, чтобы построить список сабкатегорий которые должны быть открыты на пути к этому сабкатегории. 
Далее данный список передается в шаблон который выводит сабкатегории, рекурсивно вызывая себя при выводе развернутых сабкатегорий. Такой алгоритм позволяет обратиться к любой сабкатегории указав в url только категорию и ее сабкатегорию. 
Например, при вводе url (в зависимости от типа локального запуска)

[⬆️Оглавление](#оглавление)

<br>

## Удаление:
Для удаления проекта выполните следующие действия:
```bash
cd .. && rm -fr django && deactivate
```
  
[⬆️Оглавление](#оглавление)

<br>

## Автор:
[Radmir Galiullin](https://github.com/s0ull877)

[⬆️В начало](#Проект)
