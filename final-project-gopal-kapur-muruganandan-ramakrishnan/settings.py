"""
    Add all project related settings here!
"""

import os
from pathlib import Path

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FOLDER = Path("{}/data/".format(PROJECT_DIR))

SPARK_CONFIGURE_OUTPUT = "spark.mongodb.output.uri"

# Database setting
DB_HOST = "localhost"
DB_PORT = "27017"
DB_NAME = "taxi"
