FROM python:3.10-alpine

WORKDIR /project

COPY . .

RUN pip install -r Pipfile

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
