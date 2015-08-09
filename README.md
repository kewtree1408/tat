API расписания TAT
========================

Установка:
----------
Устанавливаем виртуальное окружение, если не установленно ранее [Virtualenv Burrito](https://github.com/brainsik/virtualenv-burrito):

    curl -s https://raw.github.com/brainsik/virtualenv-burrito/master/virtualenv-burrito.sh | $SHELL

Создаём окружение:

    mkvirtualenv newname

Устанавливам зависимости:

    pip install -r requirements.txt

Инициализируем базу и запускаем:

    ./manage.py syncdb
    ./manage.py runserver

Стащить расписание с [Мосгортранс](http://www.mosgortrans.org/pass3/) можно командой:

    ./manage.py fetch_mostrans  # это займёт довольно приличное время
