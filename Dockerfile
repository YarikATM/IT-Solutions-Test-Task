FROM python:3.11.4-alpine

WORKDIR /usr/src/app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY app /usr/src/app/


CMD python manage.py makemigrations --noinput\
    && python manage.py migrate --noinput\
    && python manage.py collectstatic --noinput\
    && python manage.py loaddata users.json\
    && python manage.py loaddata cars.json\
    && python manage.py loaddata comments.json\
    && python manage.py test\
    && gunicorn app.wsgi:application -c gunicorn_conf.py



EXPOSE 4000