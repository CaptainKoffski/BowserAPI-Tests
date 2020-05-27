import requests

def test_get_world_castles_list_json(basic_url):
    url = f'{basic_url}/world/1/castle/1'
    expected_json = {'castle': [{'id': 1, 'name': 'Castle #1'}]}
    response = requests.get(url)
    assert response.ok
    assert response.json() == expected_json