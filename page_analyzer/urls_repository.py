from psycopg2.extras import DictCursor


class UrlsRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                "SELECT DISTINCT ON (urls.id) "
                "urls.id, "
                "urls.name, "
                "url_checks.status_code, "
                "url_checks.created_at "
                "FROM urls "
                "LEFT JOIN url_checks ON url_checks.url_id = urls.id "
                "ORDER BY urls.id, url_checks.created_at DESC;"
                )
            return [dict(row) for row in cur]

    def get_content_checks(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM url_checks")
            return [dict(row) for row in cur]

    def find_name(self, name):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE name=%s', (name,))
            row = cur.fetchone()
            return row

    def find_id(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id=%s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def save(self, name):
        if self.find_name(name):
            return None
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                "INSERT INTO urls (name) VALUES (%s) RETURNING id", (name,))
            new_id = cur.fetchone()[0]
            self.conn.commit()
            return new_id

    def save_checks(
            self, id,
            status_code='',
            h1='',
            title='',
            description='',
            ):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            data = self.find_id(id)
            sql = (
                "INSERT INTO url_checks"
                "(url_id, status_code, h1, title, description) "
                "VALUES (%s, %s, %s, %s, %s);"
            )
            cur.execute(
                sql,
                (data['id'], status_code, h1, title, description)
                )
            self.conn.commit()

    def url_check(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            sql = (
                'SELECT * FROM url_checks '
                'WHERE url_id = (%s);'
            )
            cur.execute(sql, (id,))
            row = cur.fetchall()
            return row
