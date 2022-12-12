import json
from pprint import pprint

import pytest
from pytest_mock import mocker
import src.allegro_api


class TestAllegroApi:
    def test_get_code(self, mocker):
        mocker.patch(
            'src.allegro_api.requests.post',
            return_value='{"device_code":"8bxwX9zPx26C29n9yWXMHDWESrVbgaZZ","expires_in":3600,"user_code":"kvntgmijf","interval":5,"verification_uri":"https://allegro.pl/skojarz-aplikacje","verification_uri_complete":"https://allegro.pl/skojarz-aplikacje?code=kvntgmijf"}'
        )
        response = src.allegro_api.get_code()
        assert response is not None

    def test_allegro_connection_get_code(self):
        response = src.allegro_api.get_code()
        assert response.status_code == 200

    def test_allegro_connection_auth(self):
        json_with_link = src.allegro_api.auth()
        assert json_with_link['verification_uri_complete'] is not None