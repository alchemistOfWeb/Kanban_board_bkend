# kanban board backend
#### developed by Nikita Kuznetsov

## Описание задачи:
### Общие требования: 

* [x] реализовать REST API

* [x] Пользователь может создавать свои записи (в зависимости от задания), просматривать и удалять; просмотр доступен для списка записей и для каждой записи отдельно

* [x] Авторизация/аутентификация: 
    * [x] пользователь может регистрироваться в приложении (создание аккаунта)
    * [x] аутентификация (получение токена)
    * [x] выход из аккаунта (реализовано удаление токена из бд)

* [x] Ролевая модель(в данном случае встроенная в django): пользователи делятся на обычных и администраторов 
    * [x] зарегистрироваться в качестве администратора нельзя, можно только задать права вручную
    * [x] администратор может просматривать/редактировать/удалять любые записи любого пользователя
    * [x] администратор может создавать/удалять/блокировать пользователей.

* [x] кроме основной ветки main нужно создать ветку develop в которой будет вестись вся разработка

* Kanban-доска (Trello):
    * [x] записью являются проект, задача
    * [x] Доска - набор из Todo-списков, объединенных в проект
    * [x] У задач должны быть статусы (состояния), минимальный набор: “сделать”, “в работе”, “сделано” - задачи в соответствии со статусом попадают в разные списки внутри проекта
    * [x] Задачу можно перемещать по спискам

* Опционально:
    * [x] добавление тегов (напр. срочность)
    * [x] процент выполнения задачи
    * [ ] добавление связей между задачами: 
        * [x] “заблокирована задачей”
        * [x] “блокирует задачу”
        * [ ] “связана с” ???????
        * [x] “подзадача к”

* Дополнительно:
    * [x] Можно менять порядок задач и списков задач
    * [x] Для задач и тегов можно устанавливать цвет
    * [x] Сортировка задач и фильтрация

    * [ ] Пагинация
    * [ ] Seeders


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


### Auth 
```js
[POST] /auth/token/login
[POST] /auth/token/logout
```
В каждом следующем запросе нужно добавлять заголовок
`Authentication` со значение токена полученного при регистрации/входе

### Users
```js
[GET]    /auth/users/       // получение всех пользователей
[POST]   /auth/users/       // создание нового пользователя

[GET]    /auth/users/me/    // получение текущего пользователя
[PUT]    /auth/users/me/    // изменение данных текущего пользователя (можно изменить только email)
[DELETE] /auth/users/me/    // удаление текущего пользователя

[GET]    /auth/users/{id}/  // получение пользователя по id
[DELETE] /auth/users/{id}/  // удаление пользователя по id
```

### Boards
```js
[GET]    /api_v1/boards/        // get list
[POST]   /api_v1/boards/        // create new
[PUT]    /api_v1/boards/{id}/   // update
[PATCH]  /api_v1/boards/{id}/   // partial update
[DELETE] /api_v1/boards/{id}/   // delete
[GET]    /api_v1/boards/{id}/   // get one
```

### Tasks
```js
[GET]    /api_v1/tasks/         // get list
[POST]   /api_v1/tasks/         // create new
[PUT]    /api_v1/tasks/{id}/    // update
[PATCH]  /api_v1/tasks/{id}/    // partial update
[DELETE] /api_v1/tasks/{id}/    // delete
[GET]    /api_v1/tasks/{id}/    // get one
```

### TaskTags
```js
[GET]    /api_v1/tags/          // get list
[POST]   /api_v1/tags/          // create new
[PUT]    /api_v1/tags/{id}/     // update
[PATCH]  /api_v1/tags/{id}/     // partial update
[DELETE] /api_v1/tags/{id}/     // delete
[GET]    /api_v1/tags/{id}/     // get one
```

### TodoLists
```js
[GET]    /api_v1/todolists/         // get list
[POST]   /api_v1/todolists/         // create new
[PUT]    /api_v1/todolists/{id}/    // update

[DELETE] /api_v1/todolists/{id}/    // delete
[GET]    /api_v1/todolists/{id}/    // get one
```