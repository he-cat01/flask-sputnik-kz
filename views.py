from flask import render_template, send_from_directory
from models import Base
from scraping import *

main_program(60)

@app.route('/')
def index():
    news_list = Base.query.order_by(Base.date).all()
    return render_template('index.html', news_list=news_list)

@app.route('/logs')
def download():
    return send_from_directory('', 'logs.txt', as_attachment=True)