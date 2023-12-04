#!/bin/sh

# Установка зависимостей из Pipfile

# Выполнить миграции (если это необходимо)
python manage.py makemigrations
python manage.py migrate

# Запустить сервер
exec "$@"