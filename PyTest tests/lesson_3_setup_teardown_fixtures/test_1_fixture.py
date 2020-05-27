import names

import pytest
import requests

@pytest.fixture
def new_world_id(basic_url):
    """Добавляет новый мир, возвращает его ID и удаляет по окончании тестирования"""
    response = requests.post(f'{basic_url}/addworld', json={'name': 'whatever'})
    worldid = response.json()['world'][0]['id']
    yield worldid
    requests.delete(f'{basic_url}/world/{worldid}')

def test_add_castle(basic_url, new_world_id):
    url = f'{basic_url}/world/{new_world_id}/castle'
    name = names.get_first_name()
    response = requests.post(url, json={'name': name})
    assert response.ok
    assert name == response.json()['castle'][0]['name']