import pytest


@pytest.fixture
def db_path():
    """Возвращает путь к sqlite3 базе данных API"""
    return r'C:\Sources\BowserAPI-PostmanDemo\BowserAPI\bowser.db'