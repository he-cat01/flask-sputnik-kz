FROM python:3.6-alpine

MAINTAINER kyarser "test@test.com"

COPY ./flask-sputnik-kz /srv/www/flask-sputnik-kz

WORKDIR /srv/www/flask-sputnik-kz

RUN pip install -r requirements.txt




ENTRYPOINT [ "python" ]

CMD [ "main.py"]