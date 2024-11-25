
from sqlalchemy.orm import sessionmaker

from pipeline.etl import SimpleLoader
from pipeline.models import Base, VantaaOpenApplications


def test_data_loading_into_table(sample_data):
    """
    Test the successful loading of data into the vantaa_open_applications table.
    Verifies that the number of rows matches the sample data and each column value is correct.
    """
    loader = SimpleLoader("sqlite:///:memory:")

    Base.metadata.create_all(loader.engine)

    loader.load(sample_data)

    Session = sessionmaker(bind=loader.engine)

    with Session() as session:
        rows = session.query(VantaaOpenApplications).all()
        assert len(rows) == len(sample_data), f"Expected {len(sample_data)} rows, but got {len(rows)}."

        for idx, obj in enumerate(rows):
            for col in sample_data.columns:
                expected = sample_data.iloc[idx][col]  # idx - choosing by id, col - field name (column)
                actual = getattr(obj, col)
                assert actual == expected, f"Mismatch in column '{col}' for row {idx}: expected {expected}, got {actual}."
