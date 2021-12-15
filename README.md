# kanban board backend
#### developed by Nikita Kuznetsov

## Описание задачи:


## 1. Getting started
### step 1
```bash
> cd нужный каталог
> git clone https://github.com/alchemistOfWeb/kanban_board_bkend.git
> cd kanban_board_bkend
> python -m venv venv
> pip install -r requirements.txt
```

### step 2
Скопируйте файл .env.example и уберите строку `.exmaple` из названия копии (оставьте только `.env`)

### step 3
Создайте секретный ключ и добавьте в настройки соответствующими командами:
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key()) # скопируйте полученный командой ключ
>>> exit()
dotenv set SECRET_KEY 'getted_secret_key' # сюда нужно вставить полученный ключ
```

### step 4
настройте бд в `kanban_board_project\settings.py`

### step 5
Сделайте миг-ции в вашу бд
```bash
python manage.py makemigrations
python manage.py migrate
```

### step 6
Создайте суперюзера для доступа к админке
```bash
python manage.py create superuser
name: *******
pas: **********
```

### step 7 (autoseedering in development)
После можно будет создать пользователей со следующими данными
testuser: zUb88ABF
testuser2: LfqTAcG8
testuser3: 8yalLhfZ

### step 8
теперь можно запустить тестовый сервер
```bash
python manage.py runserver
```

### step 9 (swagger)
перейдя по данному адресу можно посмотреть и опробовать все возможные запросы к серверу
```
http:\\{your_host}\swagger
```
где `your_host` вставьте домен на котором запущен сервер(по умолчанию тестовый сервер запускается на ``)

## 2. Описание API и функционала приложения
...