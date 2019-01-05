"""
    Lambda function which does the following
    1. initial pre-processing of data
    2. push data to s3 bucket
"""
import pandas as pd
from settings import DATA_FOLDER

DATA_FILE_PATH = DATA_FOLDER / "2014_Green_Taxi_Trip_Data.csv"
SANITIZED_DATA_FILE_PATH = DATA_FOLDER / "sanitized_2014_Green_Taxi_Trip_Data.csv"

columns_to_drop = ["Store_and_fwd_flag", "Extra", "MTA_tax", "Tolls_amount", "Ehail_fee", "Trip_type"]


def preprocess_handler():
    """
        Preprocess data:
        1. remove unnecessary columns
        2. some calculations (maybe later)
    :return:
    """
    # TODO: Have this as part of S3 after discussion

    # Create dataframe from csv file
    df = pd.read_csv(DATA_FILE_PATH)

    # Remove unnecessary columns
    df = df.drop(columns=columns_to_drop)

    # save as csv
    df.to_csv(SANITIZED_DATA_FILE_PATH)


if __name__ == '__main__':
    preprocess_handler()
