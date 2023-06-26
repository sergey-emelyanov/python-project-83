from psycopg2.extras import NamedTupleCursor


def get_id(get_db_connection, valid_url):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE name=%s;', [valid_url])
            result = cur.fetchone()

    return result.id


def insert_into(get_db_connection, valid_url, current_date):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute('INSERT INTO urls(name,created_at)'
                        'VALUES(%s,%s)',
                        (valid_url, current_date))


def take_all(get_db_connection):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("""
            SELECT urls.id, urls.name, url_checks.created_at,
                url_checks.status_code FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                WHERE url_checks.url_id IS NULL OR
                url_checks.id = (SELECT MAX(url_checks.id) FROM url_checks
                WHERE url_checks.url_id = urls.id)
                ORDER BY urls.id DESC
            """)
            urls = cur.fetchall()

    return urls


def take_one(get_db_connection, id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE id=%s', [id])
            url = cur.fetchone()
    return url


def get_name(get_db_connection, valid_url):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE name=%s', [valid_url])
            url = cur.fetchone()

    return url


def insert_into_checks(get_db_connection, url_id, current_date,
                       status_code, h1, title, content):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO url_checks
            (url_id,created_at,status_code,h1,title,description)
            VALUES(%s, %s, %s, %s, %s, %s)""",
                        (url_id, current_date, status_code, h1, title, content))


def take_from_checks(get_db_connection, url_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                """SELECT * FROM url_checks
                WHERE url_id=%s ORDER BY id DESC;""",
                [url_id]
            )
            checks = cur.fetchall()

    return checks
