from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqllite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String)
    title = db.Column(db.String)
    link = db.Column(db.String)

def parse():
    url = 'https://m.ru.sputniknews.kz/archive/'
    host = 'https://m.ru.sputniknews.kz'

    page = get(url, headers={'User-Agent': UserAgent().random})
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find_all('div', class_='b-plainlist__info')

    for item in table:
        data = item.find('span', class_='b-plainlist__date').get_text(strip=True)
        data_mod = datetime.strptime(data, "%H:%M %d.%m.%Y")
        title = item.find('h2', class_='b-plainlist__title').get_text(strip=True)
        link = host + item.find('h2', class_='b-plainlist__title').find('a').get('href')

        query_double_file = db.session.query(Base).filter_by(title=title).first()
        if not query_double_file:
            save_db = Base(date=f"{data_mod.year}.{data_mod.month}.{data_mod.day}", title=title, link=link)
            db.session.add(save_db)

        db.session.commit()

@app.route('/')
def index():
    news_list = Base.query.order_by(Base.date).all()
    return render_template('index.html', news_list=news_list)

scheduler = BackgroundScheduler()
scheduler.add_job(func=parse, trigger="interval", seconds=20)
scheduler.start()

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(debug=True, threaded=True)