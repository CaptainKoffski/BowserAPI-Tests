import requests
import pytest

test_data = [
    (1, 1, {'castle': [{'id': 1, 'name': 'Castle #1'}]}),
    (1, 5, {'castle':[{'id': 5, 'name': 'Castle #5'}]}),
    (2, 7, {'castle':[{'id': 7, 'name': 'Castle #7'}]})
]

@pytest.mark.parametrize("id, castleid, expected_json", test_data)
def test_get_world_castles_list_multiple(id, castleid, expected_json, basic_url):
    url = f'{basic_url}/world/{id}/castle/{castleid}'
    response = requests.get(url)
    assert response.ok
    assert response.json() == expected_json