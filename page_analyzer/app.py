import os
import psycopg2
from datetime import date
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def post_urls():
    conn = get_db_connection()
    url = request.form['url']
    current_date = date.today()
    validation = ''
    if not validation:
        return render_template('index.html')
    cur = conn.cursor()
    cur.execute('INSERT INTO urls(name,created_at)'
                'VALUES(%s,%s)',
                (url, current_date)
                )
    conn.commit()
    cur.close()
    conn.close()
    return url_for('show_urls')


@app.route('/urls')
def show_urls():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM urls;')
    urls = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('show_all.html', urls=urls)


@app.route('/urls/<int:id>')
def show_one(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM urls WHERE id={id}')
    url = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('show_one.html', url=url)


