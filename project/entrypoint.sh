#!/bin/sh

# Установка зависимостей из Pipfile

# Выполнить миграции (если это необходимо)
python manage.py migrate

# Запустить сервер
exec python manage.py runserver 0.0.0.0:8000
