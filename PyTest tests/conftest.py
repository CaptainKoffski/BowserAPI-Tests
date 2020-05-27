import pytest
import requests


def pytest_addoption(parser):
    parser.addoption("--env", default="localhost", action="store", help="environment to handle")

envs = {'localhost': 'http://127.0.0.1:5000',
        'dev': 'https://postman-echo.com/'}

@pytest.fixture
def basic_url(request):
    return envs[request.config.option.env]

def pytest_generate_tests(metafunc):
    url = envs[metafunc.config.getoption("env")]
    if 'worldid' in metafunc.fixturenames:
        response = requests.get(f'{url}/world')
        worldids = [world['id'] for world in response.json()['world']]
        metafunc.parametrize("worldid", worldids)