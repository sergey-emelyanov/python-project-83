import os
import psycopg2
import requests
from requests import ConnectionError, HTTPError
from datetime import date
from flask import Flask, render_template, request, url_for, redirect, flash
from dotenv import load_dotenv
from urllib.parse import urlparse
from page_analyzer.validation import validate
from page_analyzer.page_parser import parse_data
from page_analyzer.database_handler import (get_id, insert_into,
                                            get_all_records,
                                            get_one_record,
                                            get_name,
                                            insert_into_checks,
                                            take_from_checks)

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
        return render_template('index.html', url=url, errors=errors), 422
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
    urls = get_all_records(get_db_connection)
    return render_template('show_all.html', urls=urls)


@app.route('/urls/<int:id>')
def show_one(id):
    url = get_one_record(get_db_connection, id)
    checks = take_from_checks(get_db_connection, id)
    return render_template('show_one.html', url=url, checks=checks)


@app.post('/urls/<int:id>/checks')
def check_url(id):
    url = get_one_record(get_db_connection, id)
    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except (ConnectionError, HTTPError):
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_one', id=id))
    h1, title, content = parse_data(url.name)
    status_code = requests.get(url.name).status_code
    current_date = date.today()
    insert_into_checks(get_db_connection, id, current_date,
                       status_code, h1, title, content)
    flash("Страница успешно проверена", "success")
    return redirect(url_for('show_one', id=id))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
