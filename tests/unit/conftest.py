from datetime import date

import pandas as pd
import pytest
from unittest.mock import patch
import requests


@pytest.fixture
def mock_data():
    return [
        {
            "id": 15839,
            "organisaatio": "Kasvatus ja oppiminen, Varhaiskasvatus",
            "ammattiala": "Hallinto-, esimies- ja asiantuntijatyö",
            "tyotehtava": "Varhaiskasvatuspäällikkö",
            "tyoavain": "https://vantaa.rekrytointi.com/paikat/?o=A_RJ&jgid=1&jid=15839",
            "osoite": "Silkkitehtaantie 5C, 01300 Vantaa",
            "haku_paattyy_pvm": "2024-12-05",
            "x": 25.036196681892456,
            "y": 60.28870816893006,
            "linkki": "https://vantaa.rekrytointi.com/paikat/?o=A_RJ&jgid=1&jid=15839"
        },
        {
            "id": 15840,
            "organisaatio": "Kaupunkiympäristö, Kadut ja puistot",
            "ammattiala": "Hallinto-, esimies- ja asiantuntijatyö",
            "tyotehtava": "Rakennuttajapäällikkö, Kadut ja puistot",
            "tyoavain": "https://vantaa.rekrytointi.com/paikat/?o=A_RJ&jgid=1&jid=15840",
            "osoite": "Asematie 6, 01300 Vantaa",
            "haku_paattyy_pvm": "2024-12-09",
            "x": 25.041968610843043,
            "y": 60.29238682868207,
            "linkki": "https://vantaa.rekrytointi.com/paikat/?o=A_RJ&jgid=1&jid=15840"
        },
    ]


@pytest.fixture
def mock_requests():
    with patch.object(requests, "get") as mock_get:
        yield mock_get


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "id": [1, 2],
        "field": [
            "Hallinto-, esimies- ja asiantuntijatyö",
            "Varhaiskasvatuksen opettaja ja sosionomi"
        ],
        "job_title": [
            "Varhaiskasvatuspäällikkö",
            "Varhaiskasvatuksen kehittäjäsosionomi, Seljapolun päiväkoti"
        ],
        "job_key": [
            "https://vantaa.rekrytointi.com/paikat/?o=A_RJ&jgid=1&jid=15839",
            "https://vantaa.rekrytointi.com/paikat/?o=A_RJ&jgid=1&jid=15825"
        ],
        "address": [
            "Silkkitehtaantie 5C, 01300 Vantaa",
            "Seljapolku 11 01360 Vantaa"
        ],
        "application_end_date": [
            date(2024, 12, 9),
            date(2024, 12, 5)
        ],
        "longitude_wgs84": [25.036196681892456, 25.056850631880877],
        "latitude_wgs84": [60.28870816893006, 60.32318383805195],
        "link": [
            "https://vantaa.rekrytointi.com/paikat/?o=A_RJ&jgid=1&jid=15839",
            "https://vantaa.rekrytointi.com/paikat/?o=A_RJ&jgid=1&jid=15825"
        ]
    })


@pytest.fixture
def sample_data_with_original_fields():
    return pd.DataFrame({
        "id": [1, 2],
        "ammattiala": [
            "Hallinto-, esimies- ja asiantuntijatyö",
            "Varhaiskasvatuksen opettaja ja sosionomi"
        ],
        "tyotehtava": [
            "Varhaiskasvatuspäällikkö",
            "Varhaiskasvatuksen kehittäjäsosionomi, Seljapolun päiväkoti"
        ],
        "tyoavain": [
            "https://vantaa.rekrytointi.com/paikat/?o=A_RJ&jgid=1&jid=15839",
            "https://vantaa.rekrytointi.com/paikat/?o=A_RJ&jgid=1&jid=15825"
        ],
        "osoite": [
            "Silkkitehtaantie 5C, 01300 Vantaa",
            "Seljapolku 11 01360 Vantaa"
        ],
        "haku_paattyy_pvm": [
            "2024-12-09",
            "2024-12-05"
        ],
        "x": [25.036196681892456, 25.056850631880877],
        "y": [60.28870816893006, 60.32318383805195],
        "linkki": [
            "https://vantaa.rekrytointi.com/paikat/?o=A_RJ&jgid=1&jid=15839",
            "https://vantaa.rekrytointi.com/paikat/?o=A_RJ&jgid=1&jid=15825"
        ]
    })


@pytest.fixture
def mock_success_response(mock_requests, mock_data):
    """
    Fixture to mock a successful API response.
    """
    mock_response = mock_requests.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    return mock_response


@pytest.fixture
def mock_empty_response(mock_requests):
    """
    Fixture to mock an empty response.
    """
    mock_response = mock_requests.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = []
    return mock_response


@pytest.fixture
def mock_api_error(mock_requests, status_code, error_message):
    """
    Fixture to mock API errors (e.g., 404, 500).
    """
    mock_response = mock_requests.return_value
    mock_response.status_code = status_code
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(error_message)
    return mock_response
