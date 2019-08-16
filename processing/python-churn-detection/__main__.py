import json
import os
import logging
from sqlalchemy import create_engine
import urllib.parse
import pandas as pd
import random

REDSHIFT_SCHEMA = "customer360"
REDSHIFT_DB = "customer360"
REDSHIFT_HOST = os.environ['REDSHIFT_HOST']
REDSHIFT_PORT = "5439"
REDSHIFT_USER = os.environ['REDSHIFT_USER']
REDSHIFT_PWD = os.environ['REDSHIFT_PWD']


def churn_detection():
    connection_string = """postgresql://{}:{}@{}:5439/{}""".format(REDSHIFT_USER,
                                                                   urllib.parse.quote_plus(REDSHIFT_PWD),
                                                                   REDSHIFT_HOST,
                                                                   REDSHIFT_DB)
    engine = create_engine(connection_string)
    data_frame = pd.read_sql_query('select distinct id from customer360.tblaccount;', engine)
    data_frame["churn_probability"] = data_frame.apply(lambda row: predict_churn(), axis=1)
    data_frame.columns = ['id_account', 'churn_probability']
    data_frame.to_sql('tblchurn', engine, schema=REDSHIFT_SCHEMA, index=False, if_exists='replace')


def predict_churn():
    return random.random()


if __name__ == "__main__":
    logger = logging.getLogger("customer-360-churn")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %H:%M:%S")
    churn_detection()
