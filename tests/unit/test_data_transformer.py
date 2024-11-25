import pandas as pd
from datetime import date
from pipeline.etl import SimpleTransformer


def test_data_rename_columns(sample_data_with_original_fields):
    """
    Test the renaming of columns in the data.
    Verifies that the columns are renamed correctly.
    """
    transformer = SimpleTransformer()

    data_with_renamed_columns = transformer._rename_columns(
        sample_data_with_original_fields
    )

    expected_columns = [
        "id",
        "field",
        "job_title",
        "job_key",
        "address",
        "application_end_date",
        "longitude_wgs84",
        "latitude_wgs84",
        "link",
    ]

    assert list(data_with_renamed_columns.columns) == expected_columns


def test_data_transform_dates(sample_data_with_original_fields):
    """
    Test the transformation of date columns.
    Verifies that the 'application_end_date' column is correctly transformed to 'date' type.
    """
    transformer = SimpleTransformer()
    data_with_renamed_columns = transformer._rename_columns(
        sample_data_with_original_fields
    )
    data_with_transformed_dates = transformer._transform_dates(
        data_with_renamed_columns
    )

    assert isinstance(data_with_transformed_dates.loc[0, "application_end_date"], date)
    assert data_with_transformed_dates.loc[0, "application_end_date"] == date(
        2024, 12, 9
    )
    assert isinstance(data_with_transformed_dates.loc[1, "application_end_date"], date)
    assert data_with_transformed_dates.loc[1, "application_end_date"] == date(
        2024, 12, 5
    )


def test_missing_date(sample_data_with_original_fields):
    """
    Test handling of missing date values.
    Verifies that None values are handled correctly when transforming date columns.
    """
    sample_data_with_original_fields.loc[0, "haku_paattyy_pvm"] = None
    transformer = SimpleTransformer()

    data_with_renamed_columns = transformer._rename_columns(
        sample_data_with_original_fields
    )
    data_with_transformed_dates = transformer._transform_dates(
        data_with_renamed_columns
    )

    assert data_with_transformed_dates.loc[0, "application_end_date"] is None


def test_empty_dataframe():
    """
    Test the transformer behavior with an empty dataframe.
    Verifies that transforming an empty dataframe results in an empty dataframe.
    """
    transformer = SimpleTransformer()

    empty_df = pd.DataFrame(
        columns=[
            "id",
            "ammattiala",
            "tyotehtava",
            "tyoavain",
            "osoite",
            "haku_paattyy_pvm",
            "x",
            "y",
            "linkki",
        ]
    )
    transformed_empty_data = transformer.transform(empty_df)
    assert transformed_empty_data.empty


def test_transformer_integration(sample_data_with_original_fields):
    """
    Integration test for the complete transformation process.
    Verifies that the data is transformed correctly with all columns renamed and dates processed.
    """
    transformer = SimpleTransformer()

    transformed_data = transformer.transform(sample_data_with_original_fields)

    assert list(transformed_data.columns) == [
        "id",
        "field",
        "job_title",
        "job_key",
        "address",
        "application_end_date",
        "longitude_wgs84",
        "latitude_wgs84",
        "link",
    ]

    assert isinstance(transformed_data.loc[0, "application_end_date"], date)
    assert transformed_data.loc[0, "application_end_date"] == date(2024, 12, 9)
    assert transformed_data.loc[1, "application_end_date"] == date(2024, 12, 5)
