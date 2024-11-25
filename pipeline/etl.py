import pandas as pd
import requests
from pandera import Column, Check
from sqlalchemy import create_engine, orm
from datetime import date
import pandera as pa


from .const import API_URL
from .models import VantaaOpenApplications


class SimpleValidator:
    def __init__(self):
        self.bounding_box = {  # ensuring the location in Vantaa city
            "min_lat": 60.20,
            "max_lat": 60.40,
            "min_lon": 24.80,
            "max_lon": 25.20,
        }
        self.schema = pa.DataFrameSchema(
            {
                "id": Column(int, checks=Check.gt(0), nullable=False),
                "organisaatio": Column(str, nullable=False),
                "ammattiala": Column(str, nullable=False),
                "tyotehtava": Column(str, nullable=False),
                "tyoavain": Column(str, nullable=False),
                "osoite": Column(str, nullable=False),
                "haku_paattyy_pvm": Column(str, nullable=True),
                "x": Column(float, checks=self._is_within_bounding_box_check("longitude"), nullable=True),
                "y": Column(float, checks=self._is_within_bounding_box_check("latitude"), nullable=True),
                "linkki": Column(str, checks=Check.str_contains("http"), nullable=False),
            }
        )

    def _is_within_bounding_box_check(self, coord_type):
        if coord_type == "longitude":
            return Check(
                lambda x: self.bounding_box["min_lon"] <= x <= self.bounding_box["max_lon"],
                element_wise=True
            )
        elif coord_type == "latitude":
            return Check(
                lambda x: self.bounding_box["min_lat"] <= x <= self.bounding_box["max_lat"],
                element_wise=True
            )
        else:
            raise ValueError("Invalid coordinate type")

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.schema.validate(df)

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.validate(df)


class SimpleExtractor:
    def __init__(self):
        self.api_url = API_URL

    def fetch_data(self):
        return requests.get(
            url=self.api_url,
            headers={"Content-Type": "application/json"},
        )

    def extract(self) -> pd.DataFrame:
        response = self.fetch_data()
        response.raise_for_status()
        return pd.DataFrame(response.json())

    def __call__(self) -> pd.DataFrame:
        return self.extract()


class SimpleTransformer:
    def __init__(self):
        self.rename_schema = {
            "id": "id",
            "ammattiala": "field",
            "tyotehtava": "job_title",
            "tyoavain": "job_key",
            "osoite": "address",
            "haku_paattyy_pvm": "application_end_date",
            "x": "longitude_wgs84",
            "y": "latitude_wgs84",
            "linkki": "link",
        }

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        # Rename based on the defined schema and drop irrelevant fields
        return df.rename(columns=self.rename_schema)[self.rename_schema.values()]

    def _transform_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        # Transfrom dates from strings to date objects
        df["application_end_date"] = df["application_end_date"].apply(
            lambda datestr: date.fromisoformat(datestr) if pd.notna(datestr) else None
        )
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.pipe(self._rename_columns).pipe(self._transform_dates)

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.transform(df=df)


class SimpleLoader:
    def __init__(self, conn_str: str):
        # Setup Engine
        self.engine = create_engine(conn_str)

    def load(self, df: pd.DataFrame) -> pd.DataFrame:
        # Load data into database inside session
        session = orm.sessionmaker(bind=self.engine)
        with session() as sess:
            sess.bulk_save_objects(
                [VantaaOpenApplications(**row) for row in df.to_dict(orient="records")]
            )
            sess.commit()

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        self.load(df=df)


def run_etl(conn_str: str):
    # Initialise ETL parts
    validator = SimpleValidator()
    extractor = SimpleExtractor()
    transformer = SimpleTransformer()
    loader = SimpleLoader(conn_str=conn_str)

    # Run parts
    df = extractor()
    df = validator(df=df)
    df = transformer(df=df)
    loader(df=df)

    print("Data loaded to database succesfully")
