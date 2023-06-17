import os
import psycopg2
from datetime import date
from flask import Flask, render_template, request, url_for, redirect, flash, get_flashed_messages
from dotenv import load_dotenv
from urllib.parse import urlparse
from page_analyzer.validation import validate
from page_analyzer.db_actions import get_id, insert_into, take_all, take_one, get_name

app = Flask(__name__)
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn



@app.route('/')
def index():
    url = ''
    return render_template('index.html', url=url)


@app.post('/urls')
def post_urls():
    url = request.form['url']
    current_date = date.today()
    errors = validate(url)
    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('index.html', url=url, errors=errors)
    valid_url = urlparse(url).scheme + "://" + urlparse(url).netloc
    result = get_name(get_db_connection, valid_url)
    if result:
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_one', id=result.id))
    insert_into(get_db_connection, valid_url, current_date)
    url_id = get_id(get_db_connection, valid_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_one', id=url_id))


@app.route('/urls')
def show_all():
    urls = take_all(get_db_connection)
    return render_template('show_all.html', urls=urls)


@app.route('/urls/<int:id>')
def show_one(id):
    url = take_one(get_db_connection, id)
    name = url.name
    date_of_insert = url.created_at
    return render_template('show_one.html', id=id, name=name, date_of_insert=date_of_insert.date())
