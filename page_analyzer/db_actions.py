from psycopg2.extras import NamedTupleCursor


def get_id(f, valid_url):
    with f() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE name=%s;', [valid_url])
            result = cur.fetchone()

    return result.id


def insert_into(f, valid_url, current_date):
    with f() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute('INSERT INTO urls(name,created_at)'
                        'VALUES(%s,%s)',
                        (valid_url, current_date))


def take_all(f):
    with f() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute('SELECT * FROM urls;')
            urls = cur.fetchall()

    return urls


def take_one(f, id):
    with f() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE id=%s', [id])
            url = cur.fetchone()

    return url


def get_name(f, valid_url):
    with f() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE name=%s', [valid_url])
            url = cur.fetchone()

    return url
