import pandas as pd
import pytest
import requests
from pipeline.etl import SimpleExtractor


def test_extract_success(mock_success_response, mock_data):
    """
    Test successful data extraction via SimpleExtractor.
    Validates that the data is converted into a DataFrame and contains expected columns.
    """
    extractor_result = SimpleExtractor().extract()

    # Expected columns that should be present in the data
    expected_columns = [
        "id",
        "organisaatio",
        "ammattiala",
        "tyoavain",
        "osoite",
        "haku_paattyy_pvm",
        "tyotehtava",
        "x",
        "y",
        "linkki",
    ]

    # Assert that the expected columns exist in the dataframe
    for col in expected_columns:
        assert (
            col in extractor_result.columns
        ), f"Column '{col}' is missing in the DataFrame."

    # Assert the data is of correct type and structure
    assert isinstance(extractor_result, pd.DataFrame), "The result is not a DataFrame."
    assert len(extractor_result) == 2, "Expected 2 rows of data."
    assert (
        extractor_result.loc[0, "organisaatio"]
        == "Kasvatus ja oppiminen, Varhaiskasvatus"
    )
    assert extractor_result.loc[1, "haku_paattyy_pvm"] == "2024-12-09"


def test_extract_no_data(mock_empty_response):
    """
    Test the scenario where the API returns an empty response.
    Validates that an empty DataFrame is returned.
    """
    extractor = SimpleExtractor()
    result = extractor.extract()

    assert isinstance(result, pd.DataFrame), "Result is not a DataFrame."
    assert result.empty, "Expected an empty DataFrame."


@pytest.mark.parametrize(
    "status_code, error_message",
    [(500, "500 Server Error"), (404, "404 Not Found"), (403, "403 Forbidden")],
)
def test_extract_api_error(mock_api_error, status_code, error_message):
    """
    Test different API errors (500, 404, 403).
    Validates that the extractor raises the appropriate HTTP error.
    """
    mock_api_error(status_code, error_message)

    extractor = SimpleExtractor()

    with pytest.raises(requests.exceptions.HTTPError):
        extractor.extract()


def test_extract_timeout(mock_requests):
    """
    Test the timeout scenario where the API request times out.
    """
    mock_response = mock_requests.return_value
    mock_response.status_code = 200
    mock_response.json.side_effect = requests.exceptions.Timeout("Request timed out")

    extractor = SimpleExtractor()

    with pytest.raises(requests.exceptions.Timeout):
        extractor.extract()
