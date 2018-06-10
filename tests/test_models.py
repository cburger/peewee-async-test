import functools
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase
from peewee_async_test.db import AsyncDatabase

from tests.factories import PersonFactory


class BaseTestCase(AioHTTPTestCase):
    def setUp(self):
        super().setUp()
        self.loop.run_until_complete(AsyncDatabase.setup_database(self.app))

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        return web.Application()

    def tearDown(self):
        self.loop.run_until_complete(AsyncDatabase.manager.close())
        super().tearDown()


def db_unittest_run_loop(func, *args, **kwargs):
    """A decorator dedicated to use with asynchronous methods of an
    AioHTTPTestCase which wraps the test in a transaction and will
    roll back any database changes.
    """
    async def do_transaction(func, self, *inner_args, **inner_kwargs):
        # Run in transaction and roll back.
        async with AsyncDatabase.manager.atomic() as txn:
            await func(self, *inner_args, **inner_kwargs)
        txn.rollback()

    @functools.wraps(func, *args, **kwargs)
    def new_func(self, *inner_args, **inner_kwargs):
        task = do_transaction(func, self, *inner_args, **inner_kwargs)
        return self.loop.run_until_complete(task)

    return new_func


class ModelTestCase(BaseTestCase):
    @db_unittest_run_loop
    async def test_peewee_model_1(self):
        async with AsyncDatabase.manager.atomic():
            person = PersonFactory()
            await person.async_save()
            assert person.id is not None

    @db_unittest_run_loop
    async def test_peewee_model_2(self):
        async with AsyncDatabase.manager.atomic():
            person = PersonFactory()
            await person.async_save()
            assert person.id is not None


class ModelTestCase2(BaseTestCase):
    @db_unittest_run_loop
    async def test_peewee_model_2(self):
        async with AsyncDatabase.manager.atomic():
            person = PersonFactory(first_name='Jack', last_name='Black')
            await person.async_save()
            assert person.id is not None
