import pytest
import requests


@pytest.mark.daily
def test_goombas_castles_consistency(basic_url, worldid):
    response = requests.get(f'{basic_url}/world/{worldid}/castle')
    castle_ids = [castle['id'] for castle in response.json()['castle']]
    response = requests.get(f'{basic_url}/world/{worldid}/goomba')
    goomba_castle_ids = [goomba['castleid'] for goomba in response.json()['goomba']]
    assert [x for x in goomba_castle_ids if x not in castle_ids] == []
