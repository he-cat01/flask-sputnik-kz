# flask-sputnik-kz

Веб приложение свежих новостей новостного портала Sputnik. 

Новости выводятся в табличном представлении с использованием DataTables JQuery.

### Особенность:
1) Приложение развертывается с помощью docker-a.
2) Использованные технологии Flask, SQLAlchemy, BackgroundScheduler, bs4

### Запуск сервера
```
cd flask-sputnik-kz
docker build -t flask-sputnik:latest .
docker run -d - p 5000:5000 flask-sputnik:latest
https://127.0.0.0:5000/
