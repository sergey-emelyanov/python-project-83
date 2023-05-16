import os

import psycopg2
from flask import Flask, render_template
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    return render_template('index.html')
