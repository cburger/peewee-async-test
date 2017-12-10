from factory import Factory
from peewee_async_test import models


class ModelFactory(Factory):
    class Meta:
        abstract = True

    @classmethod
    def _build(cls, model_class, **kwargs):
        return model_class(**kwargs)

    @classmethod
    def _create(cls, model_class, **kwargs):
        return cls._build(model_class, **kwargs)


class PersonFactory(ModelFactory):
    first_name = 'John'
    last_name = 'Doe'

    class Meta:
        model = models.Person
