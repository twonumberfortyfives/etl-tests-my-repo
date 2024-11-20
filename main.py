import argparse
from pipeline import initialize_database, run_etl, reset_enviroment
from typing import Literal
import os

DB_PATH = f"db/reagle_test.db"

class PipelineArguments(argparse.Namespace):
    method: Literal["init", "reset", "etl"]

def main():
    # Check Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", type=str , default="etl", help="Method argument")
    args:PipelineArguments = parser.parse_args()
    
    # Run method
    match args.method:
        case "init":
            initialize_database(conn_str = f"sqlite:///{DB_PATH}")
        case "reset":
            reset_enviroment(path=DB_PATH)
        case "etl":
            run_etl(conn_str=f"sqlite:///{DB_PATH}")
        case _other:
            raise Exception(f"Method {_other} not recognized.")


if __name__ == '__main__':
    main()

