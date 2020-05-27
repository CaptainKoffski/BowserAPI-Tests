import json

import requests
import pytest

def load_params(json_name):
    import os
    json_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), json_name)
    with open(json_path) as file:
        return json.load(file)

@pytest.mark.parametrize("id, castleid, expected_json", load_params('input.json'))
def test_get_world_castles_list_multiple(id, castleid, expected_json, basic_url):
    url = f'{basic_url}/world/{id}/castle/{castleid}'
    response = requests.get(url)
    assert response.ok
    assert response.json() == expected_json