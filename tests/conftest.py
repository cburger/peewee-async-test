import pytest
from aiohttp import web
from aiohttp.test_utils import setup_test_loop
from peewee_async_test.db import AsyncDatabase
from peewee_async_test.models import Person


async def get_application():
    return web.Application()


@pytest.fixture(scope="session", autouse=True)
def setup_database(request):
    loop = setup_test_loop()
    app = loop.run_until_complete(get_application())

    # Drop any existing database with same name, and then recreate it.
    print('Dropping database {}'.format(AsyncDatabase.DATABASE_NAME))
    AsyncDatabase.drop()
    print('Creating database {}'.format(AsyncDatabase.DATABASE_NAME))
    AsyncDatabase.create()

    # Setup the database so models etc can use it.
    loop.run_until_complete(AsyncDatabase.setup_database(app))

    # Apply database tables
    with AsyncDatabase.manager.allow_sync():
        Person.create_table(True)

    def destroy_db():
        print('Dropping database {}'.format(AsyncDatabase.DATABASE_NAME))
        if AsyncDatabase.manager.is_connected:
            loop.run_until_complete(AsyncDatabase.manager.close())
        AsyncDatabase.drop()

    # Tear down the database once one with tests.
    request.addfinalizer(destroy_db)
