# Инструкция по запуску приложения #

Первичная настройка приложения возможна в 2 форматах:
1. Стандартный формат (подойдет тем, кто не хочет вручную вбивать команды по установке зависимостей, применения миграций, заполнения базы данных и тд)
2. Пользовательский формат (для тех, кому стандартный формат не подходит)

## Первичная настройка в стандартном формате ##

Запуск в стандартном формате крайне прост. Все что вам нужно будет сделать после установки исходного кода приложения - это перейти в корневую папку проекта и ввести следующую команду в консоль:

    python3 start.py


## Первичная настройка в пользовательском формате ##

Запуск в пользовательском формате чуть сложнее. Вам необходимо после установки исходного кода программы сделать следующее:

1. Установка зависимостей:
    

    pip install --upgrade
    pip3 install -r requirements.txt


2. Применение миграций:


    python3 manage.py migrate


3. Заполнение базы данных из фикстур:


    python3 manage.py loaddata api/fixtures/users.json
    python3 manage.py loaddata api/fixtures/authors.json
    python3 manage.py loaddata api/fixtures/tokens.json
    python3 manage.py loaddata api/fixtures/books.json


## Запуск приложения ##

Для запуска приложения необходимо ввести следующую команду в терминале:

    python3 manage.py runserver

По умолчанию приложение запустится по адресу "127.0.0.1:8000" или по адресу "localhost:8000"


## Примечания ##

Получить доступ к API через браузер не получится, так как включена авторизация по токену. Для того, чтобы протестировать API вручную, необходимо запустить приложение и использовать один из следующих инструментов:
curl, requests, postman, insomnia или аналогичные им. Вы можете использовать API Token уже существующих аккаунтов, либо создать новый (зарегистрироваться через внутреннюю форму регистрации в приложении). При регистрации в приложении вам будет присвоен уникальный API Token. В приложении также есть подробная документация API, которая наглядно показывает, как использовать API приложения