import atexit
from app import app, db
from models import Base
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent
from apscheduler.schedulers.background import BackgroundScheduler

def parse() -> None:
    url = 'https://m.ru.sputniknews.kz/archive/'
    page = get(url, headers={'User-Agent': UserAgent(verify_ssl=False).random})
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find_all('div', class_='b-plainlist__info')
    count = 0
    for item in table:
        data = item.find('span', class_='b-plainlist__date').get_text(strip=True)
        data_mod = datetime.strptime(data, "%H:%M %d.%m.%Y")
        title = item.find('h2', class_='b-plainlist__title').get_text(strip=True)
        link = 'https://m.ru.sputniknews.kz' + item.find('h2', class_='b-plainlist__title').find('a').get('href')

        query_double_file = db.session.query(Base).filter_by(title=title).first()
        if not query_double_file:
            save_db = Base(date=f"{data_mod.year}.{data_mod.month}.{data_mod.day}", title=title, link=link)
            db.session.add(save_db)
            count += 1
    db.session.commit()
    save_logs(count)

def save_logs(count: int) -> None:
    with open("logs.txt", mode="a", encoding="utf-8") as file:
        if count != 0:
            file.write(
                f"{datetime.now().date()} {datetime.now().hour}:{datetime.now().minute}    add rows:    {count}\n"
            )

def main_program(time: int) -> None:
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=parse, trigger="interval", seconds=time)
    scheduler.start()


if __name__ == '__main__':
    db.create_all()
    db.session.commit()