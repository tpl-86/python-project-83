from urllib.parse import urlparse

import requests
from flask import Flask, flash, redirect, render_template, request, url_for
from validators import url

from page_analyzer.config import Config
from page_analyzer.parser import parse_seo
from page_analyzer.urls_repository import UrlsRepository

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET'])
def urls_get():
    repo = UrlsRepository()
    url_checks = repo.get_urls_with_check()
    return render_template('urls.html', url_checks=url_checks)


@app.route('/urls', methods=['POST'])
def urls_post():
    repo = UrlsRepository()
    new_url = request.form.get('url')
    if not url(new_url):
        flash('Некорректный URL', 'danger')
        return render_template('index.html', url=new_url), 422
    url_parse = urlparse(new_url)
    full_url = f"{url_parse.scheme}://{url_parse.netloc}"
    url_id = repo.add_url(full_url)
    if url_id is not None:
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('url_id', id=url_id))
    row = repo.find_url_by_name(full_url)
    url_id = row['id']
    flash('Страница уже существует', 'info')
    return redirect(url_for('url_id', id=url_id))


@app.route('/urls/<int:id>', methods=['GET'])
def url_id(id):
    repo = UrlsRepository()
    url_data = repo.find_url_by_id(id)
    checks = repo.get_url_checks_by_id(id)
    return render_template('url_id.html', url=url_data, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def url_checks(id):
    repo = UrlsRepository()
    url_by_id = repo.find_url_by_id(id)
    try:
        response = requests.get(url_by_id['name'], timeout=30)
        response.raise_for_status()
        code = str(response.status_code)
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url_id', id=id))
    html_content = response.text
    h1, title, description = parse_seo(html_content)
    repo.save_check(id, code, h1, title, description)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url_id', id=id))
