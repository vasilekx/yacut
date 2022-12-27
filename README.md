# Проект YaCut на Flask

## Описание

Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис. API сервиса доступен всем желающим.

## Применяемые технологи

[![Python](https://img.shields.io/badge/Python-3.8-blue?style=flat-square&logo=Python&logoColor=3776AB&labelColor=d0d0d0)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0.2-blue?style=flat-square&logo=Flask&logoColor=3776AB&labelColor=d0d0d0)](https://flask.palletsprojects.com/en/latest/)

Расширения для Flask:

[![flask-sqlalchemy](https://img.shields.io/badge/Flask_SQLAlchemy-2.5.1-blue?style=flat-square&logoColor=3776AB&labelColor=d0d0d0)](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
[![Flask-wtf](https://img.shields.io/badge/Flask_WTF-1.0.0-blue?style=flat-square&logoColor=3776AB&labelColor=d0d0d0)](https://flask-wtf.readthedocs.io/en/latest/)
[![Flask-Migrate](https://img.shields.io/badge/Flask_Migrate-3.1.0-blue?style=flat-square&logoColor=3776AB&labelColor=d0d0d0)](https://flask-migrate.readthedocs.io/en/latest/index.html)

## Запуск сервиса

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:vasilekx/yacut.git
```

```bash
cd yacut
```

Создать файл .env

* Если у вас Linux/MacOS
    ```bash
    touch .env
    ```

* Если у вас Windows

    ```bash
    type nul > .env
    ```

Заполнить файл .env:

```
FLASK_APP=opinions_app
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=YOUR_SECRET_KEY
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv venv
```

* Если у вас Linux/MacOS

    ```bash
    source venv/bin/activate
    ```

* Если у вас windows

    ```bash
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

Создать базу данных:
```bash
flask shell
```

```bash
from yacut import db; db.create_all(); exit()
```

Выполнить запус сервиса:

```bash
flask run
```

## Доступ к сервису
```http
http://127.0.0.1:5000/
```
<img width="1243" alt="Снимок экрана 2022-12-27 в 14 16 30" src="https://user-images.githubusercontent.com/11489198/209658961-01755882-52f7-4681-a6e6-d1c9dc280f17.png">


### Доступ к API сервиса
```http
http://127.0.0.1:5000/api/id/
```

### [Спецификация на API](openapi.yml)

### Примеры запросов к API

#### Создание новой короткой ссылки:

**POST**-запрос:

```http
http://127.0.0.1:5000/api/id/
```

Тело запроса:

```json
{
  "url": "https://flask.palletsprojects.com/en/latest/",
  "custom_id": "myshorturl"
}
```

Ответ:

```json
{
    "short_link": "http://127.0.0.1:5000/myshorturl",
    "url": "https://flask.palletsprojects.com/en/latest/"
}
```

#### Получение оригинальной ссылки по указанному короткому идентификатору:

**GET**-запрос:

```http
http://127.0.0.1:5000/api/id/myshorturl
```

Ответ:

```json
{
    "url": "https://flask.palletsprojects.com/en/latest/"
}
```

## Автор
[Владислав Василенко](https://github.com/vasilekx)
