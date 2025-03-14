import os
from flask import Flask, render_template, flash, redirect, request, url_for
from dotenv import load_dotenv
from validators import url
from urllib.parse import urlparse
import psycopg2
from page_analyzer.urls_repository import UrlsRepository

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require")


@app.route('/', methods=['POST', 'GET'])
def index():
    conn = get_db_connection()
    repo = UrlsRepository(conn)
    try:
        if request.method == 'POST':
            current_url = request.form.get('url')
            if url(current_url):
                url_parse = urlparse(current_url)
                full_url = f"{url_parse.scheme}://{url_parse.netloc}"
                if not is_check(full_url, repo):
                    id = repo.save(full_url)
                    flash('Страница успешно добавлена', 'success')
                    return redirect(url_for('url_id', id=id))
                else:
                    row = repo.find_name(full_url)
                    id = row['id']
                    flash('Страница уже существует', 'info')
                    return redirect(url_for('url_id', id=id))
            else:
                flash('Некорректный URL', 'danger')
                return render_template('index.html', url=current_url)
        return render_template('index.html')
    finally:
        conn.close()


@app.route('/urls')
def urls():
    conn = get_db_connection()
    repo = UrlsRepository(conn)
    try:
        content = repo.get_content()[::-1]
        return render_template('urls.html', content=content)
    finally:
        conn.close()


@app.route('/urls/<int:id>')
def url_id(id):
    conn = get_db_connection()
    repo = UrlsRepository(conn)
    try:
        url = repo.find_id(id)
        return render_template('url_id.html', url=url)
    finally:
        conn.close()


def is_check(name, repo):
    row = repo.find_name(name)
    return row is not None
