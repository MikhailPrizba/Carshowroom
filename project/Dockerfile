FROM python:3.10-alpine

WORKDIR /project

# Копируем все файлы из текущего каталога в контейнер
COPY . .

# Устанавливаем зависимости из Pipfile
RUN pip install -r Pipfile

# Копируем entrypoint.sh в контейнер
COPY entrypoint.sh /project/entrypoint.sh

# Устанавливаем исполняемые права для entrypoint.sh
RUN chmod +x /project/entrypoint.sh

# Устанавливаем entrypoint
ENTRYPOINT ["/project/entrypoint.sh"]
