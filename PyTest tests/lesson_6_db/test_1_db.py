import sqlite3

import pytest
import requests


@pytest.fixture()
def db_worlds(db_path):
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    connection = sqlite3.connect(db_path)
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM world')
    worlds = cursor.fetchall()
    yield worlds
    connection.close()

def test_db_vs_response(db_worlds, basic_url):
    response = requests.get(f'{basic_url}/world')
    assert response.ok
    assert {'world': db_worlds} == response.json()