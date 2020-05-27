import names

import pytest
import requests

@pytest.fixture(scope='class')
def requests_data():
    """Менеджер миров: сохраняет имя и ID мира"""
    class RequestsData:
        def __init__(self):
            self.world_name = None
            self.worldid = None
    return RequestsData()

@pytest.mark.daily
class TestWorldCRUD:

    def test_post(self, basic_url, requests_data):
        requests_data.world_name = names.get_first_name()
        response = requests.post(f'{basic_url}/addworld', json={'name': requests_data.world_name})
        assert response.ok
        assert requests_data.world_name == response.json()['world'][0]['name']
        requests_data.worldid = response.json()['world'][0]['id']

    def test_get_posted(self, basic_url, requests_data):
        response = requests.get(f'{basic_url}/world/{requests_data.worldid}')
        assert response.ok
        assert requests_data.world_name == response.json()['world'][0]['name']

    def test_put(self, basic_url, requests_data):
        requests_data.world_name = names.get_first_name()
        response = requests.put(f'{basic_url}/world/{requests_data.worldid}', json={'name': requests_data.world_name})
        assert response.ok
        assert requests_data.world_name == response.json()['world']['name']

    def test_get_put(self, basic_url, requests_data):
        response = requests.get(f'{basic_url}/world/{requests_data.worldid}')
        assert response.ok
        assert requests_data.world_name == response.json()['world'][0]['name']

    def test_delete(self, basic_url, requests_data):
        response = requests.delete(f'{basic_url}/world/{requests_data.worldid}')
        assert 204 == response.status_code

    def test_get_deleted(self, basic_url, requests_data):
        response = requests.get(f'{basic_url}/world/{requests_data.worldid}')
        assert response.ok
        assert [] == response.json()['world']