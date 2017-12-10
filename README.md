# Peewee Async Test Project

This is a test project to demonstrate testing Peewee Async with Pytest
where every test function is wrapped in a transaction and the changes
to the database rolled back once the test is completed.

The issue I am having is that the code works fine with one test, but the
second test always fails with the following exception:

    RuntimeError: The transaction must run within a task

## To run the tests

The tests require a local Postgres server to be running which allows
passwordless logins. The Pytest will create a `test_db` database.

Create a virtual environment for the project and install the
project with its dependencies with:

    $ pip install -e .

To run the tests:

    $ pytest

