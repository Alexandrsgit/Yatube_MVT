### Yatube_MVT ###
Yatube - соц. сеть для публикации дневников.
Разработан по классической MVT архитектуре. Используется пагинация постов и кэширование.
Регистрация реализована с верификацией данных, сменой и восстановлением пароля через почту.
Написаны тесты, проверяющие работу сервиса.


### Как запустить проект: ###
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Alexandrsgit/Yatube_MVT.git
```

Cоздать и активировать виртуальное окружение:
```
python -m venv venv
source venv/Script/activate
```

Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции и добавить данные в БД:
```
python manage.py makemigrations
python manage.py migrate
```

Создайте суперпользователя для доступа в admin-зону и запустить проект:
```
python manage.py createsuperuser
python manage.py runserver
```


### URL-адреса для работы с проектом: ###
```
Главная страница проекта - http://127.0.0.1:8080/
Админ зона проеката - http://127.0.0.1:8000/admin/
```
