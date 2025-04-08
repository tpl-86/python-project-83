import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

load_dotenv()


def get_db_connection():
    """
    The function returns a connection object
    to the PostgreSQL database taking
    into account the SSL mode
    """
    ssl_mode = os.getenv('DATABASE_SSL_MODE', 'disable')
    return psycopg2.connect(os.getenv('DATABASE_URL'), sslmode=ssl_mode)


class UrlsRepository:
    def __init__(self, conn=None):
        self.conn = conn or get_db_connection()

    def get_urls_with_check(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                "SELECT DISTINCT ON (urls.id) "
                "urls.id, "
                "urls.name, "
                "url_checks.status_code, "
                "url_checks.created_at "
                "FROM urls "
                "LEFT JOIN url_checks ON url_checks.url_id = urls.id "
                "ORDER BY urls.id DESC, url_checks.created_at DESC;"
                )
            return [dict(row) for row in cur]

    def find_url_by_name(self, name):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE name=%s', (name,))
            row = cur.fetchone()
            return row

    def find_url_by_id(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id=%s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def add_url(self, name):
        if self.find_url_by_name(name):
            return None
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                "INSERT INTO urls (name) VALUES (%s) RETURNING id", (name,))
            new_id = cur.fetchone()[0]
            self.conn.commit()
            return new_id

    def save_check(
            self, id,
            status_code='',
            h1='',
            title='',
            description='',
            ):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            url_record = self.find_url_by_id(id)
            sql = (
                "INSERT INTO url_checks"
                "(url_id, status_code, h1, title, description) "
                "VALUES (%s, %s, %s, %s, %s);"
            )
            cur.execute(
                sql,
                (url_record['id'], status_code, h1, title, description)
                )
            self.conn.commit()

    def get_url_checks_by_id(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            sql = (
                'SELECT * FROM url_checks '
                'WHERE url_id = (%s) '
                'ORDER BY id DESC;'
            )
            cur.execute(sql, (id,))
            row = cur.fetchall()
            return row
