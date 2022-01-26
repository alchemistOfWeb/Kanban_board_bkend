# kanban board backend
#### developed by Nikita Kuznetsov


* [1. Формулировка тз](#task_description)
* [2. Установка и настройка](#setup)
    * [1. Установка зависимостей](#dependences)
    * [2. Секретный ключ](#create_secret_key)
    * [3. Настройка базы данных](#setup_db)
    * [4. Миграции](#migrations)
    * [5. Для доступа к админке ](#admin_panel)
    * [6. Запуск тестового сервера](#test_server)
    * [7. swagger и документация к АПИ](#swagger)
* [3. Описание API и функционала приложения](#api_description)
    * [Регистрация и вход](#auth)
    * [Пользователи](#users)
    * [Доски](#boards)
    * [Задачи](#tasks)
    * [Теги для задач](#tasktags)
    * [Списки задач](#todolists)


## 1. Формулировка тз:
<a name="task_description"></a> 
За основу были взяты принципы работы kanban доски Trello

### Общие требования: 

* [x] REST API
* [x] Django, drf

* [x] Пользователь может создавать свои записи (в зависимости от задания), просматривать и удалять; просмотр доступен для списка записей и для каждой записи отдельно
* [x] Авторизация/аутентификация: 
    * [x] пользователь может регистрироваться в приложении (создание аккаунта)
    * [x] аутентификация (получение токена)
    * [x] выход из аккаунта (реализовано удаление токена из бд)
* [x] Ролевая модель(в данном случае встроенная в django): пользователи делятся на обычных и администраторов 
    * [x] зарегистрироваться в качестве администратора нельзя, можно только задать права вручную
    * [x] администратор может просматривать/редактировать/удалять любые записи любого пользователя
    * [x] администратор может создавать/удалять/блокировать пользователей.

### Основные задачи:
* Kanban-доска (Trello):
    * [x] записью являются проект, задача
    * [x] Доска - набор из Todo-списков, объединенных в проект
    * [x] У задач должны быть статусы (состояния), минимальный набор: “сделать”, “в работе”, “сделано” - задачи в соответствии со статусом попадают в разные списки внутри проекта.
    * [x] Задачу можно перемещать по спискам.

* Опционально:
    * [x] добавление тегов (напр. срочность)
    * [x] процент выполнения задачи
    * [ ] добавление связей между задачами: 
        * [x] “заблокирована задачей”
        * [x] “блокирует задачу”
        * [ ] “связана с” ??????
        * [x] “подзадача к”

### Ещё идеи:

* [x] Можно менять порядок задач и списков задач
* [x] Для задач и тегов можно устанавливать цвет
* [x] Сортировка выборки задач
* [x] фильтрация выборки задач
* [ ] Назначение задач пользователям

* [x] Пагинация
* [ ] архивирование задач, списков задач и досок
* [ ] Tests
* [ ] docker image

<br><br>

---
---
---
---

<br>  

## 2. Установка и настройка
<a name="setup"></a> 

### 1 Установка зависимостей
<a name="dependences"></a> 

Для начала установите python.
Допустимы версии от 3.6 до 3.9

```bash
cd нужный каталог
git clone https://github.com/alchemistOfWeb/kanban_board_bkend.git
cd kanban_board_bkend
python -m venv venv
source <venv>/bin/activate # if u use linux
venv\Scripts\activate # if u use windows platform
pip install -r requirements.txt
```

### 2 Секретный ключ
<a name="create_secret_key"></a> 

Для начала скопируйте файл .env.example и уберите строку `.exmaple` из названия копии (оставьте только `.env`)

Создайте секретный ключ и добавьте в настройки соответствующими командами:
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key()) # скопируйте полученный командой ключ
>>> exit()
dotenv set SECRET_KEY 'getted_secret_key' # сюда нужно вставить полученный ключ
```

### 3 Настройка базы данных
<a name="setup_db"></a> 

Установите настройки для вашей бд в `kanban_board_project\settings.py`.
По умолчание для бд стоят след. настройки. Их можно не изменять, тогда в дирекотории с manage.py будет создан файл db.sqlite3 в качестве базы данных.
```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
для подключения к др. базам данных смотрите https://docs.djangoproject.com/en/3.1/ref/databases/

Затем вы можете заимпортировать базу данных созданную мной с помощью средств джанго.
Для этого исполните следующую команду в терминале из директории `kanban_board_project/`:
```bash
python manage.py loaddata db.json
```

Также в таком случае вам не придётся создавать суперюзера, те. вы можете пропустить шаги 4 и 5.
Вот имя и пароль для доступа к админке
```txt
username: nikita
password: nikita
```

### 4 Миграции
<a name="migrations"></a> 

> Пропустите этот шаг, если вы выполнили django-миграцию бд (см. шаг 3)

Сделайте миграции в вашу бд
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5 Для доступа к админке 
<a name="admin_panel"></a> 

> Пропустите этот шаг, если вы выполнили django-миграцию бд (см. шаг 3)

Создайте суперюзера для доступа к админке
```bash
python manage.py create superuser
name: ******* # придумайте, например admin
pas: ********** # придумайте, например admin
```

### 6 Запуск тестового сервера
<a name="test_server"></a> 

теперь можно запустить тестовый сервер
```bash
python manage.py runserver
```

### 7 swagger и документация к АПИ
<a name="swagger"></a> 

перейдя по данному адресу можно посмотреть и опробовать все возможные запросы к серверу
```s
http:\\{your_host}\swagger
```
где `your_host` вставьте домен на котором запущен сервер.


<br><br>

---
---
---
---

<br>

## 3. Описание API и функционала приложения
<a name="api_description"></a> 

> Подробнее про api можно посмотреть запустив проект и перейдя адресу c uri /swagger/

### Регистрация и вход 
<a name="auth"></a> 


```js
[POST] /auth/token/login
[POST] /auth/token/logout
```
В каждом следующем запросе нужно добавлять заголовок
`Authentication` со значение токена полученного при регистрации/входе в формате `Token {your_token}`
        

### Пользователи
<a name="Users"></a> 


```js
[GET]    /auth/users/       // получение всех пользователей
[POST]   /auth/users/       // создание нового пользователя

[GET]    /auth/users/me/    // получение текущего пользователя
[PUT]    /auth/users/me/    // изменение данных текущего пользователя (можно изменить только email)
[DELETE] /auth/users/me/    // удаление текущего пользователя

[GET]    /auth/users/{id}/  // получение пользователя по id
[DELETE] /auth/users/{id}/  // удаление пользователя по id
```

### Доски
<a name="boards"></a> 


Доска - она же и проект.
```js
[GET]    /api_v1/boards/        // get list
[POST]   /api_v1/boards/        // create new
[PUT]    /api_v1/boards/{id}/   // update
[PATCH]  /api_v1/boards/{id}/   // partial update
[DELETE] /api_v1/boards/{id}/   // delete
[GET]    /api_v1/boards/{id}/   // get one
```
При создании нового проекта для него будут созданы 3 стандартных списка для задач, 
среди которых:
* "todo"(сделать) 
* "doing"(в работе), 
* "done"(сделано)


### Задачи
<a name="tasks"></a> 


```js
/* Все запросы к задачам */
[GET]    /api_v1/tasks/         // get list
[POST]   /api_v1/tasks/         // create new
[PUT]    /api_v1/tasks/{id}/    // update
[PATCH]  /api_v1/tasks/{id}/    // partial update
[DELETE] /api_v1/tasks/{id}/    // delete
[GET]    /api_v1/tasks/{id}/    // get one
```
Задачу можно перемещать по спискам(тем самым устанавливая и статус) с помощью следующего запроса
[PATCH]  /api_v1/tasks/{id}/ 
```json
    {
        "todolist": todolist_id
    }
```

задаче можно установить тег(и) из существующих(либо можно создать новые отдельным запросом) следующим запросом:
[PATCH]  /api_v1/tasks/{id}/ 
```json
    {
        "tags": [1,2,3] // перезапись тегов для задачи
    }
```

у каждой задачи есть процент выполнения, который можно изменять от 0 до 100 следующим запросом:
[PATCH]  /api_v1/tasks/{id}/
```json
    {
        "completion": 30.5
    }
```

Также можно добавлять следующие связи между задачами:
* “заблокирована задачей”
[PATCH]  /api_v1/tasks/{id}/
```json
    {
        "blocked_by": [task_ids]
    }
```

* “блокирует задачу”
[PATCH]  /api_v1/tasks/{id}/
```json
    {
        "blocks_tasks": [task_ids]
    }
```

* “подзадача к”
для одной задачи можно установить только одну надзадачу
[PATCH]  /api_v1/tasks/{id}/
```json
    {
        "subtask_for": task_id 
    }
```

```js
todo:
1. запрещать создание связей с задачами других досок
```
### Теги для задач
<a name="tasktags"></a> 


```js
[GET]    /api_v1/tags/          // get list
[POST]   /api_v1/tags/          // create new
[PUT]    /api_v1/tags/{id}/     // update
[PATCH]  /api_v1/tags/{id}/     // partial update
[DELETE] /api_v1/tags/{id}/     // delete
[GET]    /api_v1/tags/{id}/     // get one
```

### Списки задач
<a name="todolists"></a> 


Списки которые соответствуют статусам для задач

```js
[GET]    /api_v1/todolists/         // get list
[POST]   /api_v1/todolists/         // create new
[PUT]    /api_v1/todolists/{id}/    // update

[DELETE] /api_v1/todolists/{id}/    // delete
[GET]    /api_v1/todolists/{id}/    // get one
```