import sys

from pyspark.sql import SparkSession

SPARK_CONFIGURE_OUTPUT = "spark.mongodb.output.uri"

# Database setting
DB_HOST = "localhost:27017"
DB_NAME = "taxi"
DB_TABLE = "taxi_info"


def transform_data(df):
    """
        Structures data to store in Dynamo db
    :param df: Spark dataframe to be structured
    :return:
    """
    return df


def write_df_to_mongodb(df):
    """
        Write pyspark dataframe to dynamo db table
    :param df: pyspark df
    """
    df.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()


def read_csv(spark, csv_file):
    """
        Reads sanitized csv into spark dataframe
    :return: spark dataframe
    """

    df = spark.read.csv(str(csv_file), header=True)

    return df


def configure_spark():
    """
        Configure dynamo db
    :return:
    """
    spark = SparkSession \
        .builder \
        .appName("taxiApp") \
        .config(SPARK_CONFIGURE_OUTPUT,
                "mongodb://{}/{}.{}".format(DB_HOST, DB_NAME, DB_TABLE)) \
        .getOrCreate()

    return spark


if __name__ == '__main__':
    # Configure Spark with mongodb configurations
    spark = configure_spark()
    # take first argument as filename
    input_file = sys.argv[1]
    # Create a spark dataframe from the csv
    df = read_csv(spark, input_file)
    # Write dataframe to mongodb table
    write_df_to_mongodb(df)
