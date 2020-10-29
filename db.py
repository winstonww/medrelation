import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        # g is unique to each request
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="wwww")

        g.conn = conn
        g.cur = conn.cursor()
        # g.db = sqlite3.connect(
        #     current_app.config['DATABASE'],
        #     detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.row_factory = sqlite3.Row

    return g.conn, g.cur


def close_db(e=None):
    # db = g.pop('db', None)

    # if db is not None:
    #     db.close()
    conn = g.pop('conn', None)

    if conn is not None:
        conn.close()



def init_db():
    conn, db = get_db()

    print("yessss")
   #  with current_app.open_resource('schema.sql') as f:
   #      db.executescript(f.read().decode('utf8'))

   #  with current_app.open_resource('tests/data.sql') as f:
   #      db.executescript(f.read().decode('utf8'))

    with current_app.open_resource('schema/schema.sql') as f:
        db.execute(f.read())

    with current_app.open_resource('schema/data.sql') as f:
        db.execute(f.read().decode('utf8'))
    conn.commit()



@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
