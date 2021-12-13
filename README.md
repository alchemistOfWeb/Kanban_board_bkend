# kanban board backend



### step 1
```bash
pip install -r requirements.txt
```

### step 2
Скопируйте файл .env.example и уберите строку `.exmaple` из названия копии (оставьте только `.env`)
```bash
...
```

### step
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key()) # скопируйте полученный командой ключ
>>> exit()
dotenv set SECRET_KEY 'getted_secret_key' # сюда нужно вставить полученный ключ
```
### step
настройте бд


### step
```bash
python manage.py makemigrations
python manage.py migrate
```

### step
```bash
python manage.py create superuser
name: *******
pas: **********
```
### step (seedering)
testuser: zUb88ABF
testuser2: LfqTAcG8
testuser3: 8yalLhfZ

### step

### step

### step