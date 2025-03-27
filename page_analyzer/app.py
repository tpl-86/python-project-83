import os
from flask import Flask, render_template, flash, redirect, request, url_for
from dotenv import load_dotenv
from validators import url
from urllib.parse import urlparse
import psycopg2
import requests
from page_analyzer.urls_repository import UrlsRepository
from bs4 import BeautifulSoup


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="disable")


@app.route('/', methods=['POST', 'GET'])
def index():
    with get_db_connection() as conn:
        repo = UrlsRepository(conn)
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


@app.route('/urls')
def urls():
    with get_db_connection() as conn:
        repo = UrlsRepository(conn)
        content = repo.get_content()[::-1]
        return render_template('urls.html', content=content)


@app.route('/urls/<int:id>', methods=['GET'])
def url_id(id):
    with get_db_connection() as conn:
        repo = UrlsRepository(conn)
        url = repo.find_id(id)
        checks = repo.url_check(id)[::-1]
        return render_template('url_id.html', url=url, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def url_checks(id):
    with get_db_connection() as conn:
        repo = UrlsRepository(conn)
        data = repo.find_id(id)
        try:
            response = requests.get(data['name'])
            response.raise_for_status()  # Поднимает исключение при HTTP-ошибке
            code = str(response.status_code)
        except requests.exceptions.RequestException:
            flash("Произошла ошибка при проверке", 'danger')
            return redirect(url_for('url_id', id=id))
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        h1 = soup.h1.get_text() if soup.h1 else ''
        title = soup.title.get_text() if soup.title else ''
        meta_tag = soup.find("meta", attrs={"name": "description"})
        description = meta_tag.get('content') if meta_tag else ''
        repo.save_checks(id, code, h1, title, description)
        return redirect(url_for('url_id', id=id))


def is_check(name, repo):
    row = repo.find_name(name)
    return row is not None
