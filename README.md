# kanban board backend



### step
```bash
pip install -r requirements.txt
```

### step
Скопируйте файл .env.example и уберите строку `.exmaple` из названия копии (оставьте только `.env`)
```bash
pip install -r requirements.txt
```

### step
скопируйте полученный командой ключ
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key()) # скопируйте полученный командой ключ
>>> exit()
dotenv set SECRET_KEY 'getted_secret_key' # сюда нужно вставить полученный ключ
```

### step
```bash
create superuser
name: *******
pas: **********
```

testuser: zUb88ABF
testuser2: LfqTAcG8
testuser3: 8yalLhfZ

