from psycopg2.extras import DictCursor


class UrlsRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls")
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
