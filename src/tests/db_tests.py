import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.constants import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker()


# https://medium.com/@vittorio.camisa/agile-database-integration-tests-with-python-sqlalchemy-and-factory-boy-6824e8fe33a1

@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def session(connection):
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()

def test_case(session):
    assert session.is_active is True
