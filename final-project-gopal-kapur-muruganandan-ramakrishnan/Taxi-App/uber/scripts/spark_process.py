import argparse
import sys
from datetime import timedelta, datetime

from pyspark.sql import SparkSession

# For read
SPARK_CONFIGURE_OUTPUT = "spark.mongodb.input.uri"

# Database setting
DB_HOST = "localhost:27017"
DB_NAME = "greentaxi"
DB_TABLE = "uber_ride"

MAXIMUM_RIDES = 10
DECIMAL_LIMIT_FORMAT = "{0:.3f}"


def run_query(spark, params):
    # create dataframe
    df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()

    df.createOrReplaceTempView("temp")
    query = "SELECT pickup_latitude, pickup_longitude, pickup_datetime FROM temp WHERE (pickup_latitude between {} " \
            "and {}) and (pickup_longitude between {} and {}) and (CAST(pickup_datetime as INT) >= unix_timestamp('{" \
            "}', 'yyyy-MM-dd HH:mm:ss') and CAST(pickup_datetime as INT) <= unix_timestamp('{}', 'yyyy-MM-dd " \
            "HH:mm:ss'))"\
        .format(params["latitude_lb"], params["latitude_ub"],
                params["longitude_lb"], params["longitude_ub"],
                datetime.strftime(params["time_lb"], "%Y-%m-%d %H:%M:%S"),
                datetime.strftime(params["time_ub"], "%Y-%m-%d %H:%M:%S"))

    rides = spark.sql(query)

    rides.show()


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


def get_params(latitude, longitude, latitude_threshold, longitude_threshold, now_time, time_threshold):
    now_time = datetime.strptime(now_time, "%Y/%m/%dT%H:%M:%S")
    params = {}
    params["latitude_lb"] = float(DECIMAL_LIMIT_FORMAT.format(latitude - latitude_threshold))
    params["latitude_ub"] = float(DECIMAL_LIMIT_FORMAT.format(latitude + latitude_threshold))
    params["longitude_lb"] = float(DECIMAL_LIMIT_FORMAT.format(longitude - longitude_threshold))
    params["longitude_ub"] = float(DECIMAL_LIMIT_FORMAT.format(longitude + longitude_threshold))
    params["time_lb"] = now_time
    params["time_ub"] = now_time + timedelta(minutes=time_threshold)

    return params


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Enter Query parameters to find nearby rides')
    parser.add_argument('latitude', type=float,
                        help='Required float latitude value')
    parser.add_argument('longitude', type=float,
                        help='Required float longitude value')
    parser.add_argument('latitude_threshold', type=float,
                        help='Required float latitude threshold')
    parser.add_argument('longitude_threshold', type=float,
                        help='Required float longitude threshold')
    parser.add_argument('now_time', type=str,
                        help='string time in datetime format')
    parser.add_argument('time_threshold', type=int,
                        help='Required integer time threshold')

    args = parser.parse_args()

    # Configure Spark with mongodb configurations
    spark = configure_spark()
    params = get_params(args.latitude, args.longitude, args.latitude_threshold,
                        args.longitude_threshold, args.now_time, args.time_threshold)
    # take first argument as filename
    run_query(spark, params)
