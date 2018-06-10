import contextlib
import peewee_async
import psycopg2
from peewee_async import Manager

import logging
import sys
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


@contextlib.contextmanager
def get_bare_cursor(database):
    """Gets the bare cursor which has no transaction context."""
    connection = database.get_conn()
    old_isolation_level = connection.isolation_level

    connection.set_isolation_level(
        psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    try:
        yield database.get_cursor()
    finally:
        connection.set_isolation_level(old_isolation_level)


class AsyncDatabase:
    """
    @type manager: Manager
    @type database: peewee_async.PostgresqlDatabase
    """
    DATABASE_NAME = 'test_db'
    manager = None
    database = peewee_async.PostgresqlDatabase(None)

    @classmethod
    async def setup_database(cls, app):
        app.database = cls.database
        cls.database.init(database=cls.DATABASE_NAME)
        app.database.set_allow_sync(False)
        app.objects = cls.manager = Manager(app.database)

    @classmethod
    def psycopg_exec(cls, query):
        with psycopg2.connect(host='localhost') as conn:
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            with conn.cursor() as cursor:
                cursor.execute(query)

    @classmethod
    def create(cls):
        cls.psycopg_exec('CREATE DATABASE {}'.format(cls.DATABASE_NAME))

    @classmethod
    def drop(cls):
        cls.psycopg_exec('DROP DATABASE IF EXISTS {}'.format(cls.DATABASE_NAME))
