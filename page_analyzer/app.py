import os
import psycopg2
from validators import url
from page_analyzer.urls_repository import UrlsRepository
from urllib.parse import urlparse
from flask import Flask, render_template, flash, redirect, request, url_for
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
repo = UrlsRepository(conn)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        current_url = request.form.get('url')
        if url(current_url):
            try:
                url_parse = urlparse(current_url)
                full_url = f"{url_parse.scheme}://{url_parse.netloc}"
                if not is_check(full_url):
                    id = repo.save(full_url)
                    flash('Страница успешно добавлена', 'success')
                    return redirect(url_for('url_id', id=id))
                else:
                    row = repo.find_name(full_url)
                    id = row['id']
                    flash('Страница уже существует', 'info')
                    return redirect(url_for('url_id', id=id))
            except psycopg2.Error as e:
                app.logger.error(f"Database error: {e}")
                flash('Ошибка базы данных: ' + str(e), 'danger')
                return render_template('index.html', url=current_url)
            except Exception as e:
                app.logger.error(f"Unexpected error: {e}")
                flash('Неизвестная ошибка: ' + str(e), 'danger')
                return render_template('index.html', url=current_url)
        else:
            flash('Некорректный URL', 'danger')
            return render_template('index.html', url=current_url)
    return render_template('index.html')


@app.route('/urls')
def urls():
    try:
        content = repo.get_content()[::-1]
        return render_template('urls.html', content=content)
    except psycopg2.Error as e:
        app.logger.error(f"Database error: {e}")
        flash('Ошибка базы данных: ' + str(e), 'danger')
        return render_template('index.html')


@app.route('/urls/<int:id>')
def url_id(id):
    url = repo.find_id(id)
    return render_template('url_id.html', url=url)


def is_check(name):
    row = repo.find_name(name)
    return row is not None
