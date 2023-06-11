import os
import psycopg2
from datetime import date
from flask import Flask, render_template, request, url_for, redirect, flash, get_flashed_messages
from dotenv import load_dotenv
from urllib.parse import urlparse
from page_analyzer.validation import validate

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
    conn = get_db_connection()
    url = request.form['url']
    current_date = date.today()
    errors = validate(url)
    if errors:
        return render_template('index.html', url=url, errors=errors)
    pure_url = urlparse(url).scheme + "://" + urlparse(url).netloc
    cur = conn.cursor()
    cur.execute('INSERT INTO urls(name,created_at)'
                'VALUES(%s,%s)',
                (pure_url, current_date)
                )
    conn.commit()
    cur.close()
    conn.close()
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_urls'))


@app.route('/urls')
def show_urls():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM urls;')
    urls = cur.fetchall()
    cur.close()
    conn.close()
    messages = get_flashed_messages(with_categories=True)
    return render_template('show_all.html', urls=urls, messages=messages)


@app.route('/urls/<int:id>')
def show_one(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM urls WHERE id={id}')
    url = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('show_one.html', url=url)
