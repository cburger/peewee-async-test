import peewee
from peewee_async_test.db import AsyncDatabase


class Person(peewee.Model):
    first_name = peewee.CharField()
    last_name = peewee.CharField()

    async def async_save(self):
        """
        Create a new object saved to database.
        """
        query = self.insert(**dict(self._data))
        pk = await AsyncDatabase.manager.execute(query)
        if pk is None:
            pk = self._get_pk_value()
        self._set_pk_value(pk)
        self._prepare_instance()

    class Meta:
        database = AsyncDatabase.database
